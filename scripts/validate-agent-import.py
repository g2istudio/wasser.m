"""Validate catalog invariants after deterministic agent imports."""

import argparse
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument("--network", action="store_true")
args = parser.parse_args()
products = json.loads((ROOT / "data/products.json").read_text(encoding="utf-8"))
state = json.loads((ROOT / "data/agent-import-state.json").read_text(encoding="utf-8"))

ids = [item["id"] for item in products]
slugs = [item["slug"] for item in products]
assert len(ids) == len(set(ids)), "duplicate product id"
assert len(slugs) == len(set(slugs)), "duplicate product slug"

catalog = (ROOT / "products.html").read_text(encoding="utf-8")
sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
app = (ROOT / "assets/app.js").read_text(encoding="utf-8")

agent_products = [item for item in products if item.get("agent_import")]
for item in agent_products:
    identity = item["agent_import"]["identity"]
    key = f'{identity["brand"]}::{identity["model"]}'
    assert key in state["products"], f"missing import state for {key}"
    assert state["products"][key]["source_hash"], f"missing source hash for {key}"
    assert ids.count(item["id"]) == 1
    assert catalog.count(f'data-product-id="{item["id"]}"') == 1, f"catalog card count for {item['id']}"
    assert sitemap.count(f"<loc>https://wasser.market/products/{item['slug']}</loc>") == 1, f"sitemap count for {item['id']}"
    page = (ROOT / "products" / f'{item["slug"]}.html').read_text(encoding="utf-8")
    assert "Quellen und Datenprüfung" in page
    assert item["source"] in page
    assert item["image"] in page
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)
    assert blocks and all(json.loads(block) for block in blocks), f"invalid JSON-LD for {item['id']}"

app_ids = re.findall(r'"id":\s*"([^"]+)"', app)
assert len(app_ids) == len(set(app_ids)), "duplicate comparison id"

if args.network:
    urls = sorted({value for item in agent_products for value in (item["source"], item["image"]) if value.startswith("https://")})
    def check(url):
        request = urllib.request.Request(url, headers={"User-Agent": "WasserMarket import validator/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            response.read(1)
            return url, response.status
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(check, urls))
    assert all(200 <= status < 400 for _, status in results), "unreachable source or image"
else:
    results = []

print(json.dumps({"catalog_products": len(products), "agent_products": len(agent_products),
                  "network_urls": len(results), "validated": True}))
