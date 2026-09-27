import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OLD_ID = "aquatru-classic-countertop-purifier"
NEW_ID = "aquatru-classic-countertop"


def remove_card(page: str, product_id: str) -> str:
    match = re.search(
        r'<div class="product-card"[^>]*data-product-id="' + re.escape(product_id) + r'"[^>]*>',
        page,
    )
    if match:
        start, opening_end = match.start(), match.end()
    else:
        marker = page.find(f"products/{product_id}")
        start = page.rfind('<div class="product-card"', 0, marker) if marker >= 0 else -1
        if start < 0:
            return page
        opening_end = page.find(">", start) + 1
    depth = 1
    for token in re.finditer(r"<div\b[^>]*>|</div\s*>", page[opening_end:]):
        depth += -1 if token.group().startswith("</") else 1
        if depth == 0:
            end = opening_end + token.end()
            return page[:start] + page[end:]
    raise RuntimeError(f"Cannot locate product card end: {product_id}")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def main() -> None:
    products_path = ROOT / "data" / "products.json"
    products = json.loads(products_path.read_text(encoding="utf-8"))
    products = [item for item in products if item.get("id") != OLD_ID]
    write(products_path, json.dumps(products, ensure_ascii=False, indent=2) + "\n")

    catalog_path = ROOT / "products.html"
    catalog = remove_card(catalog_path.read_text(encoding="utf-8"), OLD_ID)
    catalog = re.sub(r'(<h2 id="productResultCount">).*?(</h2>)', rf'\g<1>{len(products)} Modelle\2', catalog)
    catalog = re.sub(r'(<p id="productResultText">).*?(</p>)', rf'\g<1>{len(products)} Produkte in der Datenbank\2', catalog)
    write(catalog_path, catalog)

    brand_path = ROOT / "brands" / "aquatru.html"
    brand_page = remove_card(brand_path.read_text(encoding="utf-8"), OLD_ID)
    brand_page = re.sub(r'(<dt>Modelle</dt><dd>)\d+(</dd>)', r'\g<1>4\2', brand_page)
    write(brand_path, brand_page)

    app_path = ROOT / "assets" / "app.js"
    app = app_path.read_text(encoding="utf-8")
    app = re.sub(
        r'^\{[^\n]*(?:"id"\s*:\s*"|id\s*:\s*")' + re.escape(OLD_ID) + r'"[^\n]*\},?[ \t]*\n?',
        "",
        app,
        flags=re.M,
    )
    write(app_path, app)

    sitemap_path = ROOT / "sitemap.xml"
    sitemap = sitemap_path.read_text(encoding="utf-8")
    sitemap = re.sub(r'<url>[^<]*<loc>https://wasser\.market/products/' + re.escape(OLD_ID) + r'</loc>.*?</url>\s*', "", sitemap, flags=re.S)
    write(sitemap_path, sitemap)

    brands_path = ROOT / "data" / "brands.json"
    brands = json.loads(brands_path.read_text(encoding="utf-8"))
    for brand in brands:
        if brand.get("slug") == "aquatru":
            brand["products_count"] = 4
    write(brands_path, json.dumps(brands, ensure_ascii=False, indent=2) + "\n")

    directory_path = ROOT / "brands.html"
    directory = directory_path.read_text(encoding="utf-8")
    card = re.search(r'<a class="brand-directory-card" href="/brands/aquatru".*?</a>', directory, re.S)
    if card:
        updated = re.sub(r'United States · \d+ Modelle', 'United States · 4 Modelle', card.group(0))
        directory = directory[:card.start()] + updated + directory[card.end():]
        write(directory_path, directory)

    redirect = f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><title>AquaTru Classic</title><link rel="canonical" href="https://wasser.market/products/{NEW_ID}"><meta http-equiv="refresh" content="0;url=/{'products/' + NEW_ID}"><meta name="robots" content="noindex,follow"></head><body><p><a href="/{'products/' + NEW_ID}">Zur aktuellen AquaTru-Classic-Karte</a></p></body></html>'''
    write(ROOT / "products" / f"{OLD_ID}.html", redirect)
    print(json.dumps({"removed_duplicate": OLD_ID, "canonical": NEW_ID, "catalog_products": len(products)}))


if __name__ == "__main__":
    main()
