import json
import os
import re
import unicodedata
from pathlib import Path


def _load_local_env(path: str | Path = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        os.environ.setdefault(name.strip(), value.strip())


def normalized_identity_part(value: str) -> str:
    folded = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"[^a-z0-9]+", "", folded)


def _same_model(candidate: str, catalog_value: str) -> bool:
    wanted = normalized_identity_part(candidate)
    existing = normalized_identity_part(catalog_value)
    if wanted == existing:
        return True
    if any(char.isdigit() for char in wanted):
        code_tokens = re.findall(
            r"[A-Za-z]*\d[A-Za-z0-9]*(?:[.-][A-Za-z0-9]+)*",
            catalog_value,
        )
        return wanted in {normalized_identity_part(token) for token in code_tokens}
    return len(wanted) >= 3 and wanted in existing


def _identity(product: dict) -> tuple[str, str]:
    imported = product.get("agent_import", {}).get("identity", {})
    brand = imported.get("brand") or product.get("brand") or ""
    model = imported.get("model") or product.get("name") or ""
    return str(brand), str(model)


def load_site_catalog(path: str | Path | None = None) -> list[dict]:
    _load_local_env()
    configured = path or os.getenv("WASSER_MARKET_PRODUCTS_JSON")
    if not configured:
        raise RuntimeError(
            "WASSER_MARKET_PRODUCTS_JSON is required; parsing is blocked until the current site catalog can be checked"
        )
    catalog_path = Path(configured)
    if not catalog_path.is_file():
        raise RuntimeError(f"Wasser.Market catalog not found: {catalog_path}")
    payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise RuntimeError("Wasser.Market products.json must contain a product list")
    return payload


def find_existing_site_product(
    brand: str,
    model: str,
    path: str | Path | None = None,
) -> dict | None:
    wanted_brand = normalized_identity_part(brand)
    for product in load_site_catalog(path):
        existing_brand, existing_model = _identity(product)
        catalog_brand = normalized_identity_part(existing_brand)
        catalog_model = normalized_identity_part(existing_model)
        same_brand = (
            catalog_brand == wanted_brand
            or len(catalog_brand) >= 4 and catalog_brand in wanted_brand
            or len(wanted_brand) >= 4 and wanted_brand in catalog_brand
        )
        same_model = _same_model(model, existing_model)
        if same_model and same_brand:
            return product
    return None
