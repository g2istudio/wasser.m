"""One-command, fail-closed WasserMarket pipeline without AI."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
import subprocess
import sys

from crawler.candidate_worker import preflight_url
from crawler.discovery import is_likely_system_url
from crawler.worker import run_batch
from database.repository import ProductRepository
from sources.brave_search import load_local_env


ROOT = Path(__file__).resolve().parent
DEFAULT_SITE = Path(os.getenv("WASSER_SITE_ROOT", str(Path.cwd())))


def queued_candidates(repository: ProductRepository, limit: int) -> list[str]:
    return [url for url in repository.queued_urls(limit=max(limit * 10, limit)) if is_likely_system_url(url)][:limit]


async def run(args) -> dict:
    load_local_env(ROOT / ".env")
    os.environ.setdefault("WASSER_ALLOW_AI", "true")
    os.environ.setdefault("WASSER_AI_PROVIDER", "gemini")
    os.environ.setdefault("WASSER_AI_FALLBACK_LOCAL", "false")
    repository = ProductRepository(args.db)
    report = {"mode": "publish" if args.publish else "dry-run", "discovery": None}

    if args.discover:
        command = [sys.executable, str(ROOT / "run_discovery.py"), "--db", str(args.db), "--query", args.query,
                   "--search-limit", str(args.search_limit), "--domain-limit", str(args.domain_limit),
                   "--country", args.country, "--language", args.language, "--location", args.location]
        completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        report["discovery"] = {"returncode": completed.returncode, "output": completed.stdout[-4000:], "error": completed.stderr[-2000:]}
        if completed.returncode:
            raise RuntimeError("Discovery failed; no extraction or publication attempted")

    preflight = []
    for url in queued_candidates(repository, args.preflight_limit):
        result = preflight_url(repository, url)
        preflight.append(result.__dict__)
    report["preflight"] = preflight

    extracted = await run_batch(repository, limit=args.extract_limit)
    report["extraction"] = [item.__dict__ for item in extracted]
    report["queue"] = repository.queue_summary()

    publisher = args.site / "scripts" / "agent-auto-publish.ps1"
    command = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(publisher),
               "-Database", str(args.db), "-Limit", str(args.publish_limit)]
    if not args.publish:
        command.append("-DryRun")
    completed = subprocess.run(command, cwd=args.site, text=True, capture_output=True)
    report["publication"] = {"returncode": completed.returncode, "output": completed.stdout[-5000:], "error": completed.stderr[-3000:]}
    if completed.returncode:
        raise RuntimeError("Publication stage failed")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=str(ROOT / "data" / "wasser_market.db"))
    parser.add_argument("--site", type=Path, default=DEFAULT_SITE)
    parser.add_argument("--discover", action="store_true")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--query", default="umkehrosmose system germany")
    parser.add_argument("--country", default="DE")
    parser.add_argument("--language", default="de")
    parser.add_argument("--location", default="Germany")
    parser.add_argument("--search-limit", type=int, default=10)
    parser.add_argument("--domain-limit", type=int, default=3)
    parser.add_argument("--preflight-limit", type=int, default=20)
    parser.add_argument("--extract-limit", type=int, default=5)
    parser.add_argument("--publish-limit", type=int, default=10)
    args = parser.parse_args()
    try:
        result = asyncio.run(run(args))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as error:
        print(json.dumps({"status": "ERROR", "error": f"{type(error).__name__}: {error}"}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
