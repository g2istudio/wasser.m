import json
import hashlib
import re
import sqlite3
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from models.product import ProductRecord, WaterFilterProduct


class ClosingConnection(sqlite3.Connection):
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            return super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()


SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    status TEXT NOT NULL,
    source_url TEXT NOT NULL,
    product_json TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(brand, model)
)
"""

QUEUE_SCHEMA = """
CREATE TABLE IF NOT EXISTS url_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,
    source_url TEXT,
    status TEXT NOT NULL DEFAULT 'QUEUED',
    classification TEXT,
    reason TEXT,
    discovered_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""

DISCOVERY_SCHEMA = """
CREATE TABLE IF NOT EXISTS discovery_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    query TEXT NOT NULL,
    country TEXT,
    language TEXT,
    status TEXT NOT NULL DEFAULT 'RUNNING',
    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TEXT
);
CREATE TABLE IF NOT EXISTS discovery_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    provider TEXT NOT NULL,
    query TEXT NOT NULL,
    rank INTEGER NOT NULL,
    title TEXT,
    result_url TEXT NOT NULL,
    canonical_domain TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(run_id, result_url),
    FOREIGN KEY(run_id) REFERENCES discovery_runs(id)
)
;
CREATE TABLE IF NOT EXISTS discovered_sites (
    provider TEXT NOT NULL,
    canonical_domain TEXT NOT NULL,
    home_url TEXT NOT NULL,
    discovered_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(provider, canonical_domain)
);
CREATE TABLE IF NOT EXISTS url_discovery_sources (
    url TEXT NOT NULL,
    provider TEXT NOT NULL,
    source_url TEXT NOT NULL,
    discovered_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(url, provider),
    FOREIGN KEY(url) REFERENCES url_queue(url)
)
"""

TRIAL_SCHEMA = """
CREATE TABLE IF NOT EXISTS extraction_trials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT,
    model TEXT,
    source_url TEXT NOT NULL,
    provider TEXT NOT NULL,
    model_chain TEXT,
    status TEXT NOT NULL,
    product_json TEXT,
    metrics_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""

RUNTIME_SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    kind TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'RUNNING',
    parameters_json TEXT NOT NULL,
    budgets_json TEXT NOT NULL,
    checkpoint TEXT,
    started_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    completed_at TEXT
);
CREATE TABLE IF NOT EXISTS source_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    canonical_url TEXT NOT NULL,
    source_type TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    raw_content TEXT NOT NULL,
    normalized_content TEXT NOT NULL,
    http_metadata_json TEXT NOT NULL DEFAULT '{}',
    fetched_at TEXT NOT NULL,
    UNIQUE(canonical_url, content_hash)
);
CREATE INDEX IF NOT EXISTS idx_source_snapshots_url
    ON source_snapshots(canonical_url, fetched_at DESC);
CREATE TABLE IF NOT EXISTS canonical_products (
    id TEXT PRIMARY KEY,
    brand TEXT NOT NULL,
    normalized_model TEXT NOT NULL,
    variant_key TEXT NOT NULL DEFAULT '',
    taxonomy TEXT NOT NULL DEFAULT 'UNKNOWN/NEW_TYPE',
    status TEXT NOT NULL DEFAULT 'NEEDS_REVIEW',
    schema_version TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(brand, normalized_model, variant_key)
);
CREATE TABLE IF NOT EXISTS product_sources (
    product_id TEXT NOT NULL,
    snapshot_id INTEGER NOT NULL,
    applicability_json TEXT NOT NULL DEFAULT '{}',
    priority INTEGER NOT NULL DEFAULT 100,
    created_at TEXT NOT NULL,
    PRIMARY KEY(product_id, snapshot_id)
);
CREATE TABLE IF NOT EXISTS facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL,
    field_path TEXT NOT NULL,
    original_name TEXT,
    value_json TEXT NOT NULL,
    normalized_value_json TEXT,
    unit TEXT,
    source_url TEXT NOT NULL,
    source_type TEXT NOT NULL,
    evidence TEXT NOT NULL,
    extraction_method TEXT NOT NULL,
    confidence REAL NOT NULL,
    fetched_at TEXT,
    parser_version TEXT NOT NULL,
    schema_version TEXT NOT NULL,
    resolution_status TEXT NOT NULL DEFAULT 'CANDIDATE',
    created_at TEXT NOT NULL,
    UNIQUE(product_id, field_path, source_url, evidence, parser_version, schema_version)
);
CREATE INDEX IF NOT EXISTS idx_facts_product_field ON facts(product_id, field_path);
CREATE TABLE IF NOT EXISTS unmapped_attributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL,
    original_name TEXT NOT NULL,
    value_json TEXT NOT NULL,
    unit TEXT,
    source_url TEXT NOT NULL,
    evidence TEXT NOT NULL,
    proposed_field TEXT,
    extraction_method TEXT NOT NULL DEFAULT 'html',
    confidence REAL NOT NULL DEFAULT 0.0,
    fetched_at TEXT,
    status TEXT NOT NULL DEFAULT 'NEEDS_REVIEW',
    parser_version TEXT NOT NULL,
    schema_version TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(product_id, original_name, value_json, source_url, evidence)
);
CREATE TABLE IF NOT EXISTS audit_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT,
    product_id TEXT,
    event_type TEXT NOT NULL,
    stage TEXT NOT NULL,
    detail_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_audit_product ON audit_events(product_id, id);
CREATE TABLE IF NOT EXISTS usage_ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT NOT NULL,
    product_id TEXT,
    provider TEXT NOT NULL,
    metric TEXT NOT NULL,
    amount REAL NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_usage_job ON usage_ledger(job_id, provider, metric);
CREATE TABLE IF NOT EXISTS stage_cache (
    cache_key TEXT PRIMARY KEY,
    stage TEXT NOT NULL,
    input_hash TEXT NOT NULL,
    version TEXT NOT NULL,
    output_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS brand_candidates (
    canonical_domain TEXT PRIMARY KEY,
    brand_name TEXT NOT NULL,
    source_url TEXT NOT NULL,
    region TEXT,
    status TEXT NOT NULL DEFAULT 'CANDIDATE',
    evidence TEXT,
    discovered_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS discovery_frontier (
    url TEXT PRIMARY KEY,
    parent_url TEXT,
    kind TEXT NOT NULL,
    depth INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'QUEUED',
    canonical_domain TEXT NOT NULL,
    discovered_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonicalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    host = (parts.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    port = f":{parts.port}" if parts.port and parts.port not in {80, 443} else ""
    query = urlencode(sorted(
        (key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in {"gclid", "fbclid"}
    ))
    path = re.sub(r"/{2,}", "/", parts.path or "/").rstrip("/") or "/"
    return urlunsplit(((parts.scheme or "https").lower(), host + port, path, query, ""))


def canonical_product_id(brand: str, model: str, variant: str = "") -> str:
    def token(value: str) -> str:
        folded = value.casefold().replace("ß", "ss")
        ascii_value = unicodedata.normalize("NFKD", folded).encode("ascii", "ignore").decode()
        return re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")
    normalized_model = re.sub(r"[^A-Z0-9]", "", model.upper())
    base = f"{token(brand)}:{normalized_model.casefold()}"
    return f"{base}:{token(variant)}" if variant.strip() else base


class ProductRepository:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(SCHEMA)
            connection.execute(QUEUE_SCHEMA)
            connection.executescript(DISCOVERY_SCHEMA)
            connection.execute(TRIAL_SCHEMA)
            connection.executescript(RUNTIME_SCHEMA)
            unmapped_columns = {row[1] for row in connection.execute("PRAGMA table_info(unmapped_attributes)")}
            if "extraction_method" not in unmapped_columns:
                connection.execute("ALTER TABLE unmapped_attributes ADD COLUMN extraction_method TEXT NOT NULL DEFAULT 'html'")
            if "confidence" not in unmapped_columns:
                connection.execute("ALTER TABLE unmapped_attributes ADD COLUMN confidence REAL NOT NULL DEFAULT 0.0")
            if "fetched_at" not in unmapped_columns:
                connection.execute("ALTER TABLE unmapped_attributes ADD COLUMN fetched_at TEXT")
            columns = {row[1] for row in connection.execute("PRAGMA table_info(products)")}
            if "quality_status" not in columns:
                connection.execute(
                    "ALTER TABLE products ADD COLUMN quality_status TEXT NOT NULL DEFAULT 'DATA_VERIFIED'"
                )
            connection.execute(
                "UPDATE products SET quality_status='DATA_VERIFIED' WHERE quality_status='VERIFIED'"
            )

    def start_job(self, kind: str, parameters: dict, budgets: dict) -> str:
        job_id = str(uuid.uuid4())
        now = utc_now()
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO jobs (id, kind, parameters_json, budgets_json, started_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (job_id, kind, json.dumps(parameters, ensure_ascii=False), json.dumps(budgets), now, now),
            )
        self.audit(job_id, None, "JOB_STARTED", kind, {"parameters": parameters, "budgets": budgets})
        return job_id

    def update_job(self, job_id: str, status: str, checkpoint: str | None = None) -> None:
        now = utc_now()
        completed = now if status in {"COMPLETED", "FAILED", "BUDGET_STOPPED"} else None
        with self._connect() as connection:
            connection.execute(
                "UPDATE jobs SET status=?, checkpoint=COALESCE(?, checkpoint), updated_at=?, completed_at=COALESCE(?, completed_at) WHERE id=?",
                (status, checkpoint, now, completed, job_id),
            )

    def latest_resumable_job(self) -> dict | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM jobs WHERE status IN ('RUNNING','FAILED','BUDGET_STOPPED') ORDER BY started_at DESC LIMIT 1"
            ).fetchone()
        return dict(row) if row else None

    def audit(self, job_id: str | None, product_id: str | None, event_type: str, stage: str, detail: dict | None = None) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO audit_events (job_id, product_id, event_type, stage, detail_json, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (job_id, product_id, event_type, stage, json.dumps(detail or {}, ensure_ascii=False), utc_now()),
            )

    def record_usage(self, job_id: str, product_id: str | None, provider: str, metric: str, amount: float, metadata: dict | None = None) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO usage_ledger (job_id, product_id, provider, metric, amount, metadata_json, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (job_id, product_id, provider, metric, amount, json.dumps(metadata or {}, ensure_ascii=False), utc_now()),
            )

    def usage_totals(self, job_id: str | None = None, product_id: str | None = None) -> list[dict]:
        where, params = [], []
        if job_id:
            where.append("job_id=?")
            params.append(job_id)
        if product_id:
            where.append("product_id=?")
            params.append(product_id)
        clause = " WHERE " + " AND ".join(where) if where else ""
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT provider, metric, SUM(amount) AS amount FROM usage_ledger" + clause + " GROUP BY provider, metric ORDER BY provider, metric",
                tuple(params),
            ).fetchall()
        return [dict(row) for row in rows]

    def save_snapshot(self, url: str, raw_content: str, normalized_content: str | None = None,
                      source_type: str = "official_product_page", http_metadata: dict | None = None) -> tuple[int, bool]:
        canonical_url = canonicalize_url(url)
        normalized = normalized_content if normalized_content is not None else raw_content
        digest = hashlib.sha256(raw_content.encode("utf-8", errors="replace")).hexdigest()
        now = utc_now()
        with self._connect() as connection:
            existing = connection.execute(
                "SELECT id FROM source_snapshots WHERE canonical_url=? AND content_hash=?",
                (canonical_url, digest),
            ).fetchone()
            if existing:
                return int(existing["id"]), False
            cursor = connection.execute(
                "INSERT INTO source_snapshots (url, canonical_url, source_type, content_hash, raw_content, normalized_content, http_metadata_json, fetched_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (url, canonical_url, source_type, digest, raw_content, normalized, json.dumps(http_metadata or {}, ensure_ascii=False), now),
            )
            return int(cursor.lastrowid), True

    def latest_snapshot(self, url: str) -> dict | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM source_snapshots WHERE canonical_url=? ORDER BY id DESC LIMIT 1",
                (canonicalize_url(url),),
            ).fetchone()
        return dict(row) if row else None

    def upsert_canonical_product(self, brand: str, model: str, variant: str = "", taxonomy: str = "UNKNOWN/NEW_TYPE",
                                 status: str = "NEEDS_REVIEW", schema_version: str = "1") -> str:
        product_id = canonical_product_id(brand, model, variant)
        normalized_model = re.sub(r"[^A-Z0-9]", "", model.upper())
        now = utc_now()
        with self._connect() as connection:
            connection.execute(
                """INSERT INTO canonical_products (id, brand, normalized_model, variant_key, taxonomy, status, schema_version, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET taxonomy=excluded.taxonomy, status=excluded.status,
                     schema_version=excluded.schema_version, updated_at=excluded.updated_at""",
                (product_id, brand, normalized_model, variant, taxonomy, status, schema_version, now, now),
            )
        return product_id

    def link_product_source(self, product_id: str, snapshot_id: int, priority: int, applicability: dict | None = None) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT OR REPLACE INTO product_sources (product_id, snapshot_id, applicability_json, priority, created_at) VALUES (?, ?, ?, ?, ?)",
                (product_id, snapshot_id, json.dumps(applicability or {}, ensure_ascii=False), priority, utc_now()),
            )

    def save_fact(self, *, product_id: str, field_path: str, value, source_url: str, source_type: str,
                  evidence: str, extraction_method: str, confidence: float, parser_version: str,
                  schema_version: str, normalized_value=None, unit: str | None = None,
                  original_name: str | None = None, fetched_at: str | None = None,
                  resolution_status: str = "CANDIDATE") -> None:
        with self._connect() as connection:
            connection.execute(
                """INSERT OR IGNORE INTO facts
                   (product_id, field_path, original_name, value_json, normalized_value_json, unit, source_url,
                    source_type, evidence, extraction_method, confidence, fetched_at, parser_version,
                    schema_version, resolution_status, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (product_id, field_path, original_name, json.dumps(value, ensure_ascii=False),
                 json.dumps(normalized_value, ensure_ascii=False) if normalized_value is not None else None,
                 unit, source_url, source_type, evidence, extraction_method, max(0.0, min(1.0, confidence)),
                 fetched_at, parser_version, schema_version, resolution_status, utc_now()),
            )

    def save_unmapped_attribute(self, *, product_id: str, original_name: str, value, source_url: str,
                                evidence: str, parser_version: str, schema_version: str,
                                unit: str | None = None, proposed_field: str | None = None,
                                extraction_method: str = "html", confidence: float = 0.0,
                                fetched_at: str | None = None) -> None:
        with self._connect() as connection:
            connection.execute(
                """INSERT OR IGNORE INTO unmapped_attributes
                   (product_id, original_name, value_json, unit, source_url, evidence, proposed_field,
                    extraction_method, confidence, fetched_at, parser_version, schema_version, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (product_id, original_name, json.dumps(value, ensure_ascii=False), unit, source_url,
                 evidence, proposed_field, extraction_method, max(0.0, min(1.0, confidence)), fetched_at,
                 parser_version, schema_version, utc_now()),
            )

    def put_stage_cache(self, stage: str, input_hash: str, version: str, output: dict) -> str:
        cache_key = hashlib.sha256(f"{stage}:{version}:{input_hash}".encode()).hexdigest()
        with self._connect() as connection:
            connection.execute(
                "INSERT OR REPLACE INTO stage_cache (cache_key, stage, input_hash, version, output_json, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (cache_key, stage, input_hash, version, json.dumps(output, ensure_ascii=False), utc_now()),
            )
        return cache_key

    def get_stage_cache(self, stage: str, input_hash: str, version: str) -> dict | None:
        cache_key = hashlib.sha256(f"{stage}:{version}:{input_hash}".encode()).hexdigest()
        with self._connect() as connection:
            row = connection.execute("SELECT output_json FROM stage_cache WHERE cache_key=?", (cache_key,)).fetchone()
        return json.loads(row["output_json"]) if row else None

    def save_brand_candidate(self, domain: str, brand_name: str, source_url: str,
                             region: str | None = None, evidence: str | None = None) -> None:
        now = utc_now()
        with self._connect() as connection:
            connection.execute(
                """INSERT INTO brand_candidates
                   (canonical_domain, brand_name, source_url, region, evidence, discovered_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(canonical_domain) DO UPDATE SET brand_name=excluded.brand_name,
                     source_url=excluded.source_url, region=COALESCE(excluded.region, brand_candidates.region),
                     evidence=COALESCE(excluded.evidence, brand_candidates.evidence), updated_at=excluded.updated_at""",
                (domain, brand_name, source_url, region, evidence, now, now),
            )

    def enqueue_frontier(self, url: str, parent_url: str | None, kind: str, depth: int,
                         max_depth: int = 3) -> bool:
        if depth > max_depth:
            return False
        canonical = canonicalize_url(url)
        domain = urlsplit(canonical).hostname or ""
        with self._connect() as connection:
            cursor = connection.execute(
                """INSERT OR IGNORE INTO discovery_frontier
                   (url, parent_url, kind, depth, canonical_domain, discovered_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (canonical, parent_url, kind, depth, domain, utc_now(), utc_now()),
            )
        return bool(cursor.rowcount)

    def frontier_items(self, kind: str | None = None, limit: int = 100) -> list[dict]:
        query = "SELECT * FROM discovery_frontier WHERE status='QUEUED'"
        params: list = []
        if kind:
            query += " AND kind=?"
            params.append(kind)
        query += " ORDER BY depth, discovered_at LIMIT ?"
        params.append(limit)
        with self._connect() as connection:
            return [dict(row) for row in connection.execute(query, tuple(params)).fetchall()]

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, factory=ClosingConnection)
        connection.row_factory = sqlite3.Row
        return connection

    def save(self, record: ProductRecord) -> None:
        if record.status not in {"VERIFIED", "DATA_VERIFIED", "PUBLISHABLE_PARTIAL", "PUBLISH_READY", "NEEDS_REVIEW"}:
            raise ValueError("Only validated products may be saved to the repository")
        brand = record.product.identity.brand.value
        model = record.product.identity.model.value
        source_url = record.product.sources.manufacturer_url
        if not all(isinstance(value, str) and value for value in (brand, model, source_url)):
            raise ValueError("Verified product requires brand, model, and manufacturer URL")
        payload = record.product.model_dump_json(exclude_none=True)
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO products (brand, model, status, source_url, product_json, quality_status)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(brand, model) DO UPDATE SET
                    status=excluded.status,
                    source_url=excluded.source_url,
                    product_json=excluded.product_json,
                    quality_status=excluded.quality_status,
                    updated_at=CURRENT_TIMESTAMP
                """,
                (
                    brand, model, record.status, source_url, payload,
                    "DATA_VERIFIED" if record.status == "VERIFIED" else record.status,
                ),
            )

    def get(self, brand: str, model: str) -> WaterFilterProduct | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT product_json FROM products WHERE brand=? AND model=?",
                (brand, model),
            ).fetchone()
        return WaterFilterProduct.model_validate_json(row["product_json"]) if row else None

    def get_by_source_url(self, source_url: str) -> WaterFilterProduct | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT product_json FROM products WHERE source_url=?",
                (source_url,),
            ).fetchone()
        return WaterFilterProduct.model_validate_json(row["product_json"]) if row else None

    def all_products(self) -> list[WaterFilterProduct]:
        with self._connect() as connection:
            rows = connection.execute("SELECT product_json FROM products ORDER BY id").fetchall()
        return [WaterFilterProduct.model_validate_json(row["product_json"]) for row in rows]

    def product_rows(self, brand: str | None = None) -> list[dict]:
        query = "SELECT brand, model, status, quality_status, source_url, product_json FROM products"
        parameters: tuple = ()
        if brand:
            query += " WHERE lower(brand)=lower(?)"
            parameters = (brand,)
        query += " ORDER BY id"
        with self._connect() as connection:
            return [dict(row) for row in connection.execute(query, parameters).fetchall()]

    def save_extraction_trial(
        self,
        *,
        brand: str | None,
        model: str | None,
        source_url: str,
        provider: str,
        model_chain: list[str],
        status: str,
        product: WaterFilterProduct | None,
        metrics: dict,
    ) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO extraction_trials
                (brand, model, source_url, provider, model_chain, status, product_json, metrics_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    brand,
                    model,
                    source_url,
                    provider,
                    json.dumps(model_chain),
                    status,
                    product.model_dump_json(exclude_none=True) if product else None,
                    json.dumps(metrics, ensure_ascii=False),
                ),
            )
            return int(cursor.lastrowid)

    def update_extraction_trial_audit(
        self,
        trial_id: int,
        status: str,
        metrics: dict,
        product: WaterFilterProduct | None = None,
    ) -> None:
        with self._connect() as connection:
            if product is None:
                connection.execute(
                    "UPDATE extraction_trials SET status=?, metrics_json=? WHERE id=?",
                    (status, json.dumps(metrics, ensure_ascii=False), trial_id),
                )
            else:
                connection.execute(
                    "UPDATE extraction_trials SET status=?, metrics_json=?, product_json=? WHERE id=?",
                    (
                        status,
                        json.dumps(metrics, ensure_ascii=False),
                        product.model_dump_json(exclude_none=True),
                        trial_id,
                    ),
                )

    def get_extraction_trial(self, trial_id: int) -> dict | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM extraction_trials WHERE id=?", (trial_id,)
            ).fetchone()
        return dict(row) if row else None

    def latest_extraction_trial_by_source(self, source_url: str) -> dict | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM extraction_trials WHERE source_url=? ORDER BY id DESC LIMIT 1",
                (source_url,),
            ).fetchone()
        return dict(row) if row else None

    def enqueue_urls(self, urls: list[str], source_url: str, provider: str | None = None) -> int:
        inserted = 0
        with self._connect() as connection:
            for url in urls:
                cursor = connection.execute(
                    "INSERT OR IGNORE INTO url_queue (url, source_url) VALUES (?, ?)",
                    (url, source_url),
                )
                inserted += cursor.rowcount
                if provider:
                    connection.execute(
                        """
                        INSERT OR IGNORE INTO url_discovery_sources (url, provider, source_url)
                        VALUES (?, ?, ?)
                        """,
                        (url, provider, source_url),
                    )
        return inserted

    def sync_discovered_urls(self, urls: list[str], source_url: str) -> int:
        """Replace stale paths from one discovery source with its canonical set."""
        canonical = set(urls)
        with self._connect() as connection:
            existing = connection.execute(
                "SELECT url FROM url_queue WHERE source_url=?",
                (source_url,),
            ).fetchall()
            for row in existing:
                if row["url"] not in canonical:
                    connection.execute("DELETE FROM url_queue WHERE url=?", (row["url"],))
        return self.enqueue_urls(sorted(canonical), source_url)

    def queued_urls(self, limit: int = 100) -> list[str]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT url FROM url_queue WHERE status='QUEUED' ORDER BY id LIMIT ?",
                (limit,),
            ).fetchall()
        return [row["url"] for row in rows]

    def work_urls(self, limit: int = 100) -> list[str]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT url FROM url_queue
                WHERE status='IDENTIFIED'
                ORDER BY id
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [row["url"] for row in rows]

    def resumable_urls(self, limit: int = 100) -> list[str]:
        with self._connect() as connection:
            rows = connection.execute(
                """SELECT url FROM url_queue
                   WHERE status IN ('IDENTIFIED', 'EXTRACTING', 'DRAFT', 'ERROR')
                   ORDER BY CASE status WHEN 'EXTRACTING' THEN 0 WHEN 'ERROR' THEN 1
                                        WHEN 'DRAFT' THEN 2 ELSE 3 END, id
                   LIMIT ?""",
                (limit,),
            ).fetchall()
        return [row["url"] for row in rows]

    def work_urls_by_source(self, source_url: str, limit: int = 100) -> list[str]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT url FROM url_queue
                WHERE source_url=? AND status='IDENTIFIED'
                ORDER BY id
                LIMIT ?
                """,
                (source_url, limit),
            ).fetchall()
        return [row["url"] for row in rows]

    def update_queue_status(self, url: str, status: str, reason: str = "") -> None:
        allowed = {"QUEUED", "IDENTIFIED", "SKIPPED", "EXTRACTING", "SAVED", "DRAFT", "ERROR"}
        if status not in allowed:
            raise ValueError(f"Unsupported queue status: {status}")
        with self._connect() as connection:
            connection.execute(
                "UPDATE url_queue SET status=?, reason=?, updated_at=CURRENT_TIMESTAMP WHERE url=?",
                (status, reason, url),
            )

    def classify_url(self, url: str, classification: str, reason: str) -> None:
        if classification not in {"SYSTEM", "SKIP"}:
            raise ValueError("classification must be SYSTEM or SKIP")
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE url_queue
                SET classification=?, status=?, reason=?, updated_at=CURRENT_TIMESTAMP
                WHERE url=?
                """,
                (
                    classification,
                    "IDENTIFIED" if classification == "SYSTEM" else "SKIPPED",
                    reason,
                    url,
                ),
            )

    def queue_summary(self) -> dict[str, int]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT status, COUNT(*) AS count FROM url_queue GROUP BY status"
            ).fetchall()
        return {row["status"]: row["count"] for row in rows}

    def start_discovery_run(self, provider: str, query: str, country: str, language: str) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO discovery_runs (provider, query, country, language) VALUES (?, ?, ?, ?)",
                (provider, query, country, language),
            )
            return int(cursor.lastrowid)

    def record_discovery_result(
        self,
        run_id: int,
        provider: str,
        query: str,
        rank: int,
        title: str,
        result_url: str,
        canonical_domain: str,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO discovery_results
                (run_id, provider, query, rank, title, result_url, canonical_domain)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (run_id, provider, query, rank, title, result_url, canonical_domain),
            )

    def finish_discovery_run(self, run_id: int, status: str = "COMPLETED") -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE discovery_runs
                SET status=?, completed_at=CURRENT_TIMESTAMP
                WHERE id=?
                """,
                (status, run_id),
            )

    def discovery_provider_stats(self) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT provider,
                       COUNT(DISTINCT canonical_domain) AS unique_domains,
                       COUNT(DISTINCT result_url) AS unique_urls,
                       COUNT(DISTINCT run_id) AS runs
                FROM discovery_results
                GROUP BY provider
                ORDER BY provider
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def discovery_domain_sets(self) -> dict[str, set[str]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT provider, canonical_domain FROM discovery_results"
            ).fetchall()
        result: dict[str, set[str]] = {}
        for row in rows:
            result.setdefault(row["provider"], set()).add(row["canonical_domain"])
        return result

    def record_discovered_site(self, provider: str, canonical_domain: str, home_url: str) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO discovered_sites (provider, canonical_domain, home_url)
                VALUES (?, ?, ?)
                """,
                (provider, canonical_domain, home_url),
            )

    def discovery_product_stats(self) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT s.provider,
                       COUNT(DISTINCT s.source_url) AS crawled_sites,
                       COUNT(DISTINCT s.url) AS discovered_products,
                       COUNT(DISTINCT CASE WHEN q.status='SAVED' THEN s.url END) AS saved_products
                FROM url_discovery_sources s
                JOIN url_queue q ON q.url=s.url
                GROUP BY s.provider
                ORDER BY s.provider
                """
            ).fetchall()
        return [dict(row) for row in rows]
