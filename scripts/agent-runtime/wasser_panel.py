"""Local, model-free control panel for WasserMarket Agent."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import secrets
import sqlite3
import subprocess
import sys
import threading
import time
from urllib.parse import urlsplit
import webbrowser

from database.repository import ProductRepository, canonical_product_id


ROOT = Path(__file__).resolve().parent
DEFAULT_DB = ROOT / "data" / "wasser_market.db"
DEFAULT_PANEL_DB = ROOT / "data" / "panel.db"
DEFAULT_SITE = ROOT.parents[1] if ROOT.name == "agent-runtime" else Path.cwd()
PANEL_HTML = ROOT / "panel" / "index.html"
TERMINAL = {"COMPLETED", "FAILED"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def valid_product_url(value: str) -> bool:
    parts = urlsplit(value.strip())
    return parts.scheme == "https" and bool(parts.hostname) and not parts.username and not parts.password


class PanelStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS panel_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kind TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'QUEUED',
                    result_json TEXT,
                    error TEXT,
                    created_at TEXT NOT NULL,
                    started_at TEXT,
                    finished_at TEXT
                )
            """)
            connection.execute(
                "UPDATE panel_tasks SET status='QUEUED', started_at=NULL WHERE status='RUNNING'"
            )

    @contextmanager
    def connect(self):
        connection = sqlite3.connect(self.path, timeout=30)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def enqueue(self, kind: str, payload: dict) -> int:
        if kind not in {"process_url", "publish"}:
            raise ValueError("Unsupported panel task")
        with self.connect() as connection:
            cursor = connection.execute(
                "INSERT INTO panel_tasks (kind, payload_json, created_at) VALUES (?, ?, ?)",
                (kind, json.dumps(payload, ensure_ascii=False), utc_now()),
            )
            return int(cursor.lastrowid)

    def next_task(self) -> dict | None:
        with self.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT * FROM panel_tasks WHERE status='QUEUED' ORDER BY id LIMIT 1"
            ).fetchone()
            if not row:
                return None
            connection.execute(
                "UPDATE panel_tasks SET status='RUNNING', started_at=? WHERE id=?",
                (utc_now(), row["id"]),
            )
            result = dict(row)
            result["status"] = "RUNNING"
            result["payload"] = json.loads(result.pop("payload_json"))
            return result

    def finish(self, task_id: int, result: dict | None = None, error: str | None = None) -> None:
        status = "FAILED" if error else "COMPLETED"
        with self.connect() as connection:
            connection.execute(
                "UPDATE panel_tasks SET status=?, result_json=?, error=?, finished_at=? WHERE id=?",
                (status, json.dumps(result or {}, ensure_ascii=False), error, utc_now(), task_id),
            )

    def retry(self, task_id: int) -> bool:
        with self.connect() as connection:
            cursor = connection.execute(
                "UPDATE panel_tasks SET status='QUEUED', result_json=NULL, error=NULL, started_at=NULL, finished_at=NULL "
                "WHERE id=? AND status='FAILED'",
                (task_id,),
            )
            return bool(cursor.rowcount)

    def list(self, limit: int = 100) -> list[dict]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT * FROM panel_tasks ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        result = []
        for row in rows:
            item = dict(row)
            item["payload"] = json.loads(item.pop("payload_json"))
            item["result"] = json.loads(item.pop("result_json")) if item.get("result_json") else None
            item.pop("result_json", None)
            outcome = (item.get("result") or {}).get("result") or {}
            item["outcome_status"] = str(outcome.get("status") or item["status"])
            item["outcome_detail"] = str(outcome.get("detail") or "")
            result.append(item)
        return result


class TaskRunner:
    def __init__(self, store: PanelStore, db: Path, site: Path):
        self.store, self.db, self.site = store, db, site
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.loop, name="wasser-panel-worker", daemon=True)

    def start(self) -> None:
        self.thread.start()

    def command(self, task: dict) -> tuple[list[str], int]:
        payload = task["payload"]
        command = [
            sys.executable, str(ROOT / "wasser_agent.py"),
            "--db", str(self.db), "--site", str(self.site),
            "--allow-gemini" if payload.get("allow_gemini", True) else "--no-allow-gemini",
        ]
        if task["kind"] == "process_url":
            command.extend(["process-url", "--url", payload["url"]])
            for field in ("brand", "model"):
                if payload.get(field):
                    command.extend([f"--{field}", str(payload[field])])
            if payload.get("force"):
                command.append("--force")
            budget_flags = {
                "max_brave_queries": "--max-brave-queries",
                "max_http_requests": "--max-http-requests",
                "max_firecrawl_credits": "--max-firecrawl-credits",
                "max_gemini_tokens": "--max-gemini-tokens",
                "max_runtime": "--max-runtime",
            }
            for key, flag in budget_flags.items():
                command.extend([flag, str(int(payload["budgets"][key]))])
            command.extend(["--max-products", "1"])
            return command, int(payload["budgets"]["max_runtime"]) + 90
        command.extend([
            "publish", "--status", "PUBLISH_READY", "--limit", "1",
            "--brand", payload["brand"], "--model", payload["model"],
            "--transport", payload.get("transport", "auto"), "--apply",
        ])
        return command, 900

    def execute(self, task: dict) -> dict:
        command, timeout = self.command(task)
        completed = subprocess.run(
            command, cwd=ROOT, text=True, capture_output=True, timeout=timeout,
            encoding="utf-8", errors="replace",
        )
        output = completed.stdout.strip()
        try:
            result = json.loads(output) if output else {}
        except json.JSONDecodeError:
            result = {"output": output[-4000:]}
        if completed.returncode:
            message = result.get("error") or completed.stderr.strip() or output or "Agent command failed"
            raise RuntimeError(str(message)[-4000:])
        return result

    def loop(self) -> None:
        while not self.stop_event.is_set():
            task = self.store.next_task()
            if not task:
                self.stop_event.wait(0.75)
                continue
            try:
                self.store.finish(task["id"], result=self.execute(task))
            except Exception as error:
                self.store.finish(task["id"], error=f"{type(error).__name__}: {error}")


def published_products(site: Path | None) -> dict[str, str]:
    """Return canonical identities already present in the public site catalog."""
    catalog = site / "data" / "products.json" if site else None
    if not catalog or not catalog.is_file():
        return {}
    try:
        products = json.loads(catalog.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    result = {}
    for item in products if isinstance(products, list) else []:
        identity = (item.get("agent_import") or {}).get("identity") or {}
        brand = str(identity.get("brand") or item.get("brand") or "").strip()
        model = str(identity.get("model") or item.get("name") or "").strip()
        if brand and model:
            result[canonical_product_id(brand, model)] = str(item.get("slug") or item.get("id") or "")
    return result


def product_summaries(db_path: Path, site: Path | None = None) -> list[dict]:
    repository = ProductRepository(db_path)
    rows = repository.product_rows()
    published = published_products(site)
    summaries = []
    for row in rows:
        try:
            product = json.loads(row["product_json"])
        except (TypeError, json.JSONDecodeError):
            product = {}
        product_id = canonical_product_id(row["brand"], row["model"])
        summaries.append({
            "id": row["id"], "brand": row["brand"], "model": row["model"],
            "status": row["quality_status"] if row["status"] == row["quality_status"] else "NEEDS_REVIEW",
            "record_status": row["status"], "taxonomy": product.get("taxonomy"),
            "source_url": row["source_url"], "updated_at": row["updated_at"],
            "needs_review": bool(row.get("needs_review")),
            "source_conflict": bool(row.get("source_conflict")),
            "published": product_id in published,
            "published_slug": published.get(product_id),
        })
    return summaries


class PanelHandler(BaseHTTPRequestHandler):
    server_version = "WasserPanel/1.0"

    @property
    def app(self):
        return self.server.app

    def log_message(self, format, *args):
        return

    def send_json(self, value: object, status: int = 200) -> None:
        body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length > 100_000:
            raise ValueError("Request is too large")
        return json.loads(self.rfile.read(length).decode("utf-8")) if length else {}

    def authorized(self) -> bool:
        return secrets.compare_digest(self.headers.get("X-Wasser-Panel-Token", ""), self.app.token)

    def do_GET(self):
        if self.path == "/":
            body = PANEL_HTML.read_text(encoding="utf-8").replace("__PANEL_TOKEN__", self.app.token).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src 'self' data:")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/api/state":
            self.send_json({
                "tasks": self.app.store.list(),
                "products": product_summaries(self.app.db, self.app.site),
                "queue": ProductRepository(self.app.db).queue_summary(),
            })
            return
        self.send_error(404)

    def do_POST(self):
        if not self.authorized():
            self.send_json({"error": "Invalid panel token"}, HTTPStatus.FORBIDDEN)
            return
        try:
            data = self.read_json()
            if self.path == "/api/jobs":
                urls = [line.strip() for line in str(data.get("urls") or "").splitlines() if line.strip()]
                if not urls or len(urls) > 100 or any(not valid_product_url(url) for url in urls):
                    raise ValueError("Enter 1–100 valid HTTPS product URLs, one per line")
                budgets = data.get("budgets") or {}
                defaults = {
                    "max_brave_queries": 3, "max_http_requests": 30,
                    "max_firecrawl_credits": 3, "max_gemini_tokens": 12000,
                    "max_runtime": 600,
                }
                normalized = {key: max(0, int(budgets.get(key, value))) for key, value in defaults.items()}
                ids = [self.app.store.enqueue("process_url", {
                    "url": url, "brand": str(data.get("brand") or "").strip(),
                    "model": str(data.get("model") or "").strip(),
                    "allow_gemini": bool(data.get("allow_gemini", True)),
                    "force": bool(data.get("force", False)), "budgets": normalized,
                }) for url in urls]
                self.send_json({"task_ids": ids}, 201)
                return
            if self.path == "/api/publish":
                brand, model = str(data.get("brand") or "").strip(), str(data.get("model") or "").strip()
                summaries = product_summaries(self.app.db, self.app.site)
                selected = next((item for item in summaries if item["brand"] == brand and item["model"] == model), None)
                if selected and selected["published"]:
                    raise ValueError("This product is already published on the site")
                ready = {(item["brand"], item["model"]) for item in summaries if item["status"] == "PUBLISH_READY"}
                if (brand, model) not in ready:
                    raise ValueError("This exact product is not PUBLISH_READY")
                task_id = self.app.store.enqueue("publish", {
                    "brand": brand, "model": model, "transport": data.get("transport", "auto"),
                    "allow_gemini": False,
                })
                self.send_json({"task_id": task_id}, 201)
                return
            if self.path == "/api/retry":
                if not self.app.store.retry(int(data.get("task_id", 0))):
                    raise ValueError("Only failed tasks can be retried")
                self.send_json({"retried": True})
                return
            self.send_error(404)
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            self.send_json({"error": str(error)}, HTTPStatus.BAD_REQUEST)


class PanelApplication:
    def __init__(self, db: Path, site: Path, panel_db: Path):
        self.db, self.site = db, site
        self.token = secrets.token_urlsafe(32)
        self.store = PanelStore(panel_db)
        self.runner = TaskRunner(self.store, db, site)


def main() -> int:
    parser = argparse.ArgumentParser(prog="wasser-panel")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--panel-db", type=Path, default=DEFAULT_PANEL_DB)
    parser.add_argument("--site", type=Path, default=DEFAULT_SITE)
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    app = PanelApplication(args.db, args.site.resolve(), args.panel_db)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), PanelHandler)
    server.app = app
    app.runner.start()
    address = f"http://127.0.0.1:{args.port}/"
    print(f"WasserMarket Agent panel: {address}")
    if not args.no_browser:
        threading.Timer(0.5, lambda: webbrowser.open(address)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        app.runner.stop_event.set()
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
