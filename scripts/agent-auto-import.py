"""Deterministic importer for PUBLISH_READY records from WasserMarket Agent.

No language model or external API is used. The importer reads the local SQLite
database, validates evidence, updates the static site, and records source hashes
so repeated runs are idempotent.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import html
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlparse

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = Path(r"C:\wasser-market-agent\data\wasser_market.db")
STATE_PATH = ROOT / "data" / "agent-import-state.json"
REPORT_PATH = ROOT / "data" / "agent-import-report.json"

FIELD_LABELS = {
    "system.technology": "Technologie",
    "system.installation_type": "Installation",
    "system.tankless": "Tanklos",
    "system.electricity_required": "Stromanschluss erforderlich",
    "system.built_in_pump": "Integrierte Pumpe",
    "filtration.advertised_stage_count": "Filterstufen",
    "filtration.physical_filter_count": "Filteranzahl",
    "filtration.membrane_type": "Membrantyp",
    "filtration.membrane_capacity_gpd": "Membranleistung",
    "performance.rated_capacity_gpd": "Nennleistung",
    "performance.dispensing_flow_lpm": "Durchfluss",
    "performance.recovery_rate_percent": "Rückgewinnungsrate",
    "performance.pure_to_drain_ratio": "Reinwasser-Abwasser-Verhältnis",
    "performance.minimum_inlet_pressure": "Min. Eingangsdruck",
    "performance.maximum_inlet_pressure": "Max. Eingangsdruck",
    "performance.minimum_feed_temperature": "Min. Eingangstemperatur",
    "performance.maximum_feed_temperature": "Max. Eingangstemperatur",
    "performance.tds_reduction_percent": "TDS-Reduktion",
    "water_output.remineralization": "Remineralisierung",
    "water_output.ambient_water": "Wasser bei Raumtemperatur",
    "water_output.cold_water": "Kaltwasser",
    "water_output.hot_water": "Heißwasser",
    "water_output.temperature_levels": "Temperaturstufen",
    "tanks.raw_water_tank_l": "Rohwassertank",
    "tanks.purified_water_tank_l": "Reinwassertank",
    "tanks.pressure_tank_l": "Drucktank",
    "protection.leak_detection": "Leckageschutz",
    "protection.automatic_shutoff": "Automatische Abschaltung",
    "protection.automatic_flush": "Automatische Spülung",
    "protection.uv_disinfection": "UV-Desinfektion",
    "electrical.voltage": "Spannung",
    "electrical.standby_power_w": "Standby-Leistung",
    "electrical.filtration_power_w": "Filtrationsleistung",
    "electrical.heating_power_w": "Heizleistung",
    "electrical.cooling_power_w": "Kühlleistung",
    "electrical.maximum_power_w": "Max. Leistungsaufnahme",
    "physical.dimensions_raw": "Abmessungen",
    "physical.width_mm": "Breite",
    "physical.depth_mm": "Tiefe",
    "physical.height_mm": "Höhe",
    "physical.weight_kg": "Gewicht",
    "physical.noise_db": "Geräuschpegel",
    "smart_features.display": "Display",
    "smart_features.inlet_tds_display": "TDS-Anzeige Eingang",
    "smart_features.outlet_tds_display": "TDS-Anzeige Ausgang",
    "smart_features.filter_life_indicator": "Filterstatusanzeige",
    "smart_features.smart_faucet": "Intelligenter Wasserhahn",
    "smart_features.wifi": "WLAN",
    "smart_features.mobile_app": "App",
    "commercial.warranty_years": "Garantie",
}

ALLOWED_EVIDENCE = {
    "manufacturer_page", "manufacturer_datasheet", "manual",
    "certification_database", "laboratory_report", "authorized_retailer",
}
ALLOWED_STATUS = {
    "certified", "independent_lab_test", "tested_to_standard",
    "official_specification", "manufacturer_claim",
}


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, value: str) -> None:
    (ROOT / path).write_text(value, encoding="utf-8")


def dump(path: Path | str, value: object) -> None:
    target = path if isinstance(path, Path) else ROOT / path
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def js(value: object) -> str:
    return json.dumps(value, ensure_ascii=False).replace("<", "\\u003c")


def slugify(value: str) -> str:
    value = value.casefold().replace("+", "-plus-")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def normalized_url(value: str) -> str:
    return quote(value, safe=":/?&=%#[]@!$'()*+,;")


def nested(data: dict, path: str) -> dict:
    value: object = data
    for part in path.split("."):
        if not isinstance(value, dict):
            return {}
        value = value.get(part)
    return value if isinstance(value, dict) else {}


def safe_field(product: dict, path: str) -> dict | None:
    field = nested(product, path)
    if field.get("value") is None or not field.get("evidence"):
        return None
    if field.get("verification_status") not in ALLOWED_STATUS:
        return None
    evidence = []
    for item in field["evidence"]:
        url = item.get("source_url", "")
        if item.get("source_type") not in ALLOWED_EVIDENCE:
            continue
        if item.get("verification_status") not in ALLOWED_STATUS:
            continue
        if urlparse(url).scheme != "https" or not item.get("original_text"):
            continue
        evidence.append(item)
    if not evidence:
        return None
    result = copy.deepcopy(field)
    result["evidence"] = evidence
    return result


def shown(field: dict) -> str:
    value = field["value"]
    if isinstance(value, bool):
        value = "Ja" if value else "Nein"
    unit = field.get("unit") or ""
    return f"{value} {unit}".strip()


def category(product: dict) -> str:
    technology = str((nested(product, "system.technology").get("value") or "Wasseraufbereitung"))
    installation = str((nested(product, "system.installation_type").get("value") or "")).casefold()
    if "counter" in installation or "auftisch" in installation:
        return "Countertop RO" if "osmos" in technology.casefold() else "Countertop"
    if "under" in installation or "untertisch" in installation:
        return "Direct Flow RO" if "osmos" in technology.casefold() else "Under Sink"
    if "whole" in installation or "haus" in installation:
        return "Whole House"
    return technology


def primary_image(product: dict, model: str) -> str:
    candidates = [product.get("image") or {}, *(product.get("images") or [])]
    primary = [item for item in candidates if item.get("role") == "primary" and item.get("url")]
    if len({item["url"] for item in primary}) != 1:
        raise ValueError("requires exactly one distinct primary image")
    item = primary[0]
    if urlparse(item["url"]).scheme != "https":
        raise ValueError("primary image must use HTTPS")
    image_model = str(item.get("product_model") or "")
    if image_model and model.casefold() not in image_model.casefold() and image_model.casefold() not in model.casefold():
        raise ValueError("primary image belongs to another model")
    return normalized_url(item["url"])


def load_ready(db_path: Path) -> list[dict]:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            "SELECT id, brand, model, source_url, product_json, updated_at "
            "FROM products WHERE status='PUBLISH_READY' AND quality_status='PUBLISH_READY' ORDER BY id"
        ).fetchall()
    finally:
        connection.close()
    result = []
    for row in rows:
        item = dict(row)
        item["product"] = json.loads(item.pop("product_json"))
        item["hash"] = hashlib.sha256(
            json.dumps(item["product"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        result.append(item)
    return result


def product_card(product: dict, prefix: str = "") -> str:
    image = product["image"] if product["image"].startswith("https://") else prefix + product["image"]
    specs = "".join(f'<span>{esc(k)}: {esc(v)}</span>' for k, v in list(product["specs"].items())[:3])
    price = "—" if product.get("price") is None else f'{product["price"]:,.0f}'.replace(",", ".") + " €"
    return f'<div class="product-card" data-product-id="{esc(product["id"])}"><a class="photo" href="{prefix}products/{esc(product["slug"])}"><img src="{esc(image)}" alt="{esc(product["brand"] + " " + product["name"])}" loading="lazy"></a><div class="brand">{esc(product["brand"])}</div><h3>{esc(product["name"])}</h3><div class="rating">Herstellerdaten</div><div class="price">{price}</div><div class="specs">{specs}</div><div class="actions"><a class="btn small" href="{prefix}products/{esc(product["slug"])}">Alle Daten</a><button class="btn small" data-compare="{esc(product["id"])}">+ Compare</button></div></div>'


def replace_card(page: str, product: dict, prefix: str = "") -> tuple[str, bool]:
    match = re.search(r'<div class="product-card"[^>]*data-product-id="' + re.escape(product["id"]) + r'"[^>]*>', page)
    if not match:
        return page, False
    depth = 1
    for token in re.finditer(r"<div\b[^>]*>|</div\s*>", page[match.end():]):
        depth += -1 if token.group().startswith("</") else 1
        if depth == 0:
            end = match.end() + token.end()
            return page[:match.start()] + product_card(product, prefix) + page[end:], True
    raise ValueError(f'cannot locate end of card {product["id"]}')


def render_page(product: dict, record: dict, fields: dict) -> str:
    template = read("products/osmofresh-fusion-pro.html")
    header = template[template.index("<body"):template.index("<main")]
    footer = template[template.index("</main>") + 7:]
    title = f'{product["brand"]} {product["name"]}'
    canonical = "https://wasser.market/products/" + product["slug"]
    schema = {"@context": "https://schema.org", "@type": "Product", "name": title,
              "brand": {"@type": "Brand", "name": product["brand"]}, "url": canonical,
              "image": product["image"]}
    if product.get("price") is not None:
        schema["offers"] = {"@type": "Offer", "price": product["price"],
                            "priceCurrency": product["currency"], "url": product["source"]}
    head = template[:template.index("<body")]
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(title)} – Daten &amp; Quellen</title>", head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', "", head, flags=re.S)
    head = re.sub(r'<meta (?:name="(?:description|twitter:[^"]+)"|property="og:[^"]+")[^>]*>', "", head)
    head = re.sub(r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{canonical}">', head)
    head = head.replace("</head>", f'<meta name="description" content="{esc(title)}: technische Daten und Herstellerquellen."><script type="application/ld+json">{js(schema)}</script></head>')
    rows = "".join(f'<tr><th scope="row">{esc(k)}</th><td>{esc(v)}</td></tr>' for k, v in product["specs"].items())
    evidence = ""
    for path, field in fields.items():
        source = field["evidence"][0]
        evidence += f'<details><summary>{esc(FIELD_LABELS[path])}: {esc(shown(field))}</summary><p>ℹ Herstellerangabe · {esc(field.get("checked_at") or record["updated_at"][:10])}</p><blockquote>{esc(source["original_text"])}</blockquote><a href="{esc(source["source_url"])}" target="_blank" rel="noopener nofollow">Quelle beim Hersteller</a></details>'
    price = "—" if product.get("price") is None else f'{product["price"]:,.0f}'.replace(",", ".") + " €"
    brand_slug = product["brandSlug"]
    main = f'''<main><div class="container"><div class="breadcrumbs"><a href="../products">Produkte</a> / {esc(title)}</div><section class="device-layout"><div class="device-photo"><img src="{esc(product["image"])}" alt="{esc(title)}" loading="eager"></div><div class="device-info"><a href="../brands/{brand_slug}"><img src="../assets/brands/{brand_slug}.png" alt="{esc(product["brand"])}" style="max-width:150px;max-height:55px;object-fit:contain"></a><h1>{esc(title)}</h1><span class="badge">{esc(product["category"])}</span><p class="lead">Technische Herstellerdaten mit feldbezogenen Quellen.</p><div class="price">{price}</div><p>Datenabgleich: {esc(record["updated_at"][:10])}.</p><a class="btn primary" href="{esc(product["source"])}" target="_blank" rel="noopener nofollow">Herstellerangebot ↗</a> <button class="btn" data-compare="{esc(product["id"])}">+ Compare</button></div></section><section class="panel"><h2>Technische Daten</h2><table class="spec-table">{rows}</table><p>Nicht verfügbare Herstellerangaben sind mit „—“ gekennzeichnet. Herstellerangaben sind keine unabhängigen Laborprüfungen.</p></section><section class="panel"><h2>Quellen und Datenprüfung</h2><p>ℹ Herstellerangabe · Zertifizierungen werden nur mit eigener überprüfbarer Evidenz übernommen.</p>{evidence}</section></div></main>'''
    return head + header + main + footer


def build_record(row: dict, products: list[dict]) -> tuple[dict, dict, bool]:
    raw = row["product"]
    brand_field = safe_field(raw, "identity.brand")
    model_field = safe_field(raw, "identity.model")
    if not brand_field or not model_field:
        raise ValueError("identity requires supported evidence")
    brand, model = str(brand_field["value"]).strip(), str(model_field["value"]).strip()
    if brand.casefold() != row["brand"].casefold() or model.casefold() != row["model"].casefold():
        raise ValueError("database identity differs from evidenced identity")
    source = row["source_url"]
    if urlparse(source).scheme != "https":
        raise ValueError("manufacturer source must use HTTPS")
    fields = {path: field for path in FIELD_LABELS if (field := safe_field(raw, path))}
    if len(fields) < 4:
        raise ValueError("fewer than four publishable evidenced fields")
    image = primary_image(raw, model)
    brand_slug = slugify(brand)
    if not (ROOT / "brands" / f"{brand_slug}.html").exists():
        raise ValueError(f"brand page is missing: {brand_slug}")

    matches = [p for p in products if
               (p.get("agent_import", {}).get("identity", {}).get("brand", "").casefold() == brand.casefold()
                and p.get("agent_import", {}).get("identity", {}).get("model", "").casefold() == model.casefold())
               or (p.get("brand", "").casefold() == brand.casefold() and p.get("name", "").casefold() == model.casefold())]
    if len(matches) > 1:
        raise ValueError("ambiguous existing product identity")
    created = not matches
    target = matches[0] if matches else {
        "id": slugify(f"{brand}-{model}"), "slug": slugify(f"{brand}-{model}"),
        "brand": brand, "brandSlug": brand_slug, "name": model,
        "rating": None, "reviews": 0, "featured": False,
    }
    target.setdefault("brand", brand)
    target.setdefault("brandSlug", brand_slug)
    target.setdefault("name", model)
    target.setdefault("slug", target["id"])
    target["category"] = category(raw)
    target["source"] = source
    target["image"] = image
    target["summary"] = "Technische Herstellerdaten mit nachvollziehbaren Quellen."
    target["specs"] = {
        label: shown(fields[path]) if path in fields else "—"
        for path, label in FIELD_LABELS.items()
    }

    currency = safe_field(raw, "commercial.currency")
    amount = safe_field(raw, "commercial.current_price")
    if currency and amount and str(currency["value"]).upper() == "EUR":
        target["price"], target["currency"] = float(amount["value"]), "EUR"
    elif created:
        target["price"], target["currency"] = None, "EUR"
    target["agent_import"] = {
        "identity": {"brand": brand, "model": model}, "source_id": row["id"],
        "source_hash": row["hash"], "checked_at": row["updated_at"][:10],
        "source_url": source, "fields": fields, "publication_status": "PUBLISH_READY",
    }
    return target, fields, created


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--ids", nargs="*", type=int)
    args = parser.parse_args()
    if not args.db.exists():
        raise SystemExit(f"Agent database not found: {args.db}")

    state = json.loads(STATE_PATH.read_text(encoding="utf-8")) if STATE_PATH.exists() else {"schema_version": 1, "products": {}}
    products = json.loads(read("data/products.json"))
    original = copy.deepcopy(products)
    ready = load_ready(args.db)
    if args.ids:
        ready = [row for row in ready if row["id"] in args.ids]

    pending, baseline = [], []
    for row in ready:
        key = f'{row["brand"]}::{row["model"]}'
        prior = state["products"].get(key)
        if prior and prior.get("source_hash") == row["hash"]:
            continue
        existing = next((p for p in products if p.get("agent_import", {}).get("identity") == {"brand": row["brand"], "model": row["model"]}), None)
        if prior is None and existing and existing.get("agent_import", {}).get("publication_status"):
            baseline.append((key, row))
            continue
        pending.append((key, row))
    pending = pending[:max(args.limit, 0)]

    accepted, rejected = [], []
    rendered = {}
    for key, row in pending:
        try:
            target, fields, created = build_record(row, products)
            if created:
                if any(p["id"] == target["id"] or p["slug"] == target["slug"] for p in products):
                    raise ValueError("slug collision")
                products.append(target)
            rendered[target["id"]] = render_page(target, row, fields)
            accepted.append({"source_id": row["id"], "brand": row["brand"], "model": row["model"], "action": "create" if created else "update", "target_id": target["id"]})
        except Exception as error:
            rejected.append({"source_id": row["id"], "brand": row["brand"], "model": row["model"], "error": str(error)})

    report = {"mode": "apply" if args.apply else "dry-run", "ready": len(ready), "baseline": len(baseline),
              "pending": len(pending), "accepted": accepted, "rejected": rejected}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not args.apply:
        return 2 if rejected else 0
    if rejected:
        raise SystemExit("Import stopped: one or more records failed validation")

    for key, row in baseline:
        state["products"][key] = {"source_id": row["id"], "source_hash": row["hash"], "imported_at": datetime.now(timezone.utc).isoformat()}
    if not accepted:
        if baseline:
            dump(STATE_PATH, state)
        return 0

    if len({p["id"] for p in products}) != len(products) or len({p["slug"] for p in products}) != len(products):
        raise SystemExit("Duplicate id or slug after import")
    dump("data/products.json", products)
    for product_id, page in rendered.items():
        write(f"products/{product_id}.html", page)

    catalog = read("products.html")
    for item in accepted:
        product = next(p for p in products if p["id"] == item["target_id"])
        catalog, found = replace_card(catalog, product)
        if not found:
            start = catalog.index('id="productResultText"')
            grid = re.search(r'<div class="product-grid"[^>]*>', catalog[start:])
            if not grid:
                raise SystemExit("Catalog product grid not found")
            position = start + grid.end()
            catalog = catalog[:position] + product_card(product) + catalog[position:]
    catalog = re.sub(r'(<h2 id="productResultCount">).*?(</h2>)', rf'\g<1>{len(products)} Modelle\2', catalog)
    catalog = re.sub(r'(<p id="productResultText">).*?(</p>)', rf'\g<1>{len(products)} Produkte in der Datenbank\2', catalog)
    write("products.html", catalog)

    brands = json.loads(read("data/brands.json"))
    for brand in brands:
        affected = [item for item in accepted if item["brand"].casefold() == brand["name"].casefold()]
        if not affected:
            continue
        count = sum(p["brand"].casefold() == brand["name"].casefold() for p in products)
        brand["products_count"] = count
        page = read(f'brands/{brand["slug"]}.html')
        page = re.sub(r'(<dt>Modelle</dt><dd>)\d+(</dd>)', rf'\g<1>{count}\2', page)
        for item in affected:
            product = next(p for p in products if p["id"] == item["target_id"])
            page, found = replace_card(page, product, "../")
            if not found:
                page = page.replace('<div class="product-grid">', '<div class="product-grid">' + product_card(product, "../"), 1)
        write(f'brands/{brand["slug"]}.html', page)
    dump("data/brands.json", brands)

    app = read("assets/app.js")
    for item in accepted:
        product = next(p for p in products if p["id"] == item["target_id"])
        record = {k: "—" for k in ("flow", "maint", "liter", "membrane", "pfas", "viruses", "bacteria", "nitrates", "lead", "arsenic", "micro", "tds", "remin", "noise", "power", "warranty", "country")}
        record.update(id=product["id"], brand=product["brand"], name=product["name"], cat=product["category"],
                      price="—" if product.get("price") is None else f'{product["price"]:,.0f}'.replace(",", ".") + " €",
                      priceValue=product.get("price"), features=[], image=product["image"], url="products/" + product["slug"])
        app = re.sub(r'^\{[^\n]*"id": "' + re.escape(product["id"]) + r'"[^\n]*\},?[ \t]*\n?', "", app, flags=re.M)
        app = app.replace("const products=[", "const products=[\n" + js(record) + ",", 1)
    write("assets/app.js", app)

    sitemap = read("sitemap.xml")
    for item in accepted:
        url = "https://wasser.market/products/" + item["target_id"]
        if f"<loc>{url}</loc>" not in sitemap:
            sitemap = sitemap.replace("</urlset>", f"<url><loc>{url}</loc></url>\n</urlset>")
    write("sitemap.xml", sitemap)
    index = re.sub(r'(<b id="overviewProducts">)\d+(</b>)', rf'\g<1>{len(products)}\2', read("index.html"))
    write("index.html", index)

    for key, row in baseline + pending:
        state["products"][key] = {"source_id": row["id"], "source_hash": row["hash"], "imported_at": datetime.now(timezone.utc).isoformat()}
    dump(STATE_PATH, state)
    report["catalog_before"], report["catalog_after"] = len(original), len(products)
    report["completed_at"] = datetime.now(timezone.utc).isoformat()
    dump(REPORT_PATH, report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
