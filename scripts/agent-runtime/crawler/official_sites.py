import json
from pathlib import Path
from urllib.parse import urlparse


def canonical_domain(value: str) -> str:
    parsed = urlparse(value if "://" in value else f"https://{value}")
    host = (parsed.hostname or "").lower().rstrip(".")
    return host[4:] if host.startswith("www.") else host


def load_official_registry(path: str | Path) -> dict[str, dict]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    sites = payload.get("sites", [])
    registry: dict[str, dict] = {}
    for site in sites:
        domain = canonical_domain(str(site.get("domain", "")))
        if not domain or not site.get("brand") or not site.get("evidence_url"):
            raise ValueError("Every official site needs domain, brand, and evidence_url")
        registry[domain] = site
    return registry


def official_site_for_url(url: str, registry: dict[str, dict]) -> dict | None:
    domain = canonical_domain(url)
    return registry.get(domain)
