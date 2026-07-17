#!/usr/bin/env python3
"""Split page CSS and normalize static SEO/performance attributes."""
from pathlib import Path
import html as html_lib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
VERSION = "20260717-opt1"
PRODUCTS = {item.get("url", "").split("/")[-1]: item for item in json.loads((ROOT / "data/products.json").read_text())}
BRANDS = {item.get("slug"): item for item in json.loads((ROOT / "data/brands.json").read_text())}


def split_css():
    source = (ASSETS / "styles.css").read_text()
    markers = {
        "content": ("/* Community and rich review system */", "/* Contextual clear button for all search fields */"),
        "brand": ("/* Brand directory v2.2 */", "/* Product rating system */"),
        "product": ("/* Product rating system */", None),
    }
    extracted = {}
    base = source
    for name, (start_marker, end_marker) in markers.items():
        start = source.find(start_marker)
        end = len(source) if end_marker is None else source.find(end_marker, start)
        if start < 0 or end < 0:
            raise RuntimeError(f"CSS marker missing for {name}")
        extracted[name] = source[start:end].strip() + "\n"
    for block in extracted.values():
        base = base.replace(block.rstrip("\n"), "")
    css_dir = ASSETS / "css"
    css_dir.mkdir(exist_ok=True)
    (css_dir / "core.css").write_text(base.strip() + "\n")
    for name, block in extracted.items():
        (css_dir / f"{name}.css").write_text(block)


def meta_content(text, key, value):
    def replace_tag(match):
        tag = match.group(0)
        if not re.search(rf'\b{key}=["\']{re.escape(value)}["\']', tag, flags=re.I):
            return tag
        content = TITLE_DESC[value]
        if re.search(r'\bcontent=["\'][^"\']*["\']', tag, flags=re.I):
            return re.sub(r'\bcontent=["\'][^"\']*["\']', f'content="{content}"', tag, count=1, flags=re.I)
        return tag[:-1] + f' content="{content}">'
    return re.sub(r'<meta\b[^>]*>', replace_tag, text, flags=re.I)


TITLE_DESC = {}


def optimize_html(path):
    global TITLE_DESC
    text = path.read_text()
    text = text.replace("https://wasser.market/", "https://hitmoda.ru/")
    rel = path.relative_to(ROOT).as_posix()
    prefix = "../" * rel.count("/")
    title_match = re.search(r"<title>(.*?)</title>", text, flags=re.I | re.S)
    title = html_lib.unescape(re.sub(r"\s+", " ", title_match.group(1)).strip()) if title_match else "WASSER.MARKET"
    desc_tag = next((m.group(0) for m in re.finditer(r'<meta\b[^>]*>', text, flags=re.I)
                     if re.search(r'\bname=["\']description["\']', m.group(0), flags=re.I)), None)
    desc_match = re.search(r'\bcontent=["\']([^"\']*)["\']', desc_tag, flags=re.I) if desc_tag else None
    if not desc_match:
        desc_match = re.search(r'<p[^>]*class=["\'][^"\']*lead[^"\']*["\'][^>]*>(.*?)</p>', text, flags=re.I | re.S)
    description = re.sub(r"<[^>]+>", "", html_lib.unescape(desc_match.group(1))).strip() if desc_match else title
    description = re.sub(r"\s+", " ", description)[:300]
    canonical = f"https://hitmoda.ru/{rel if rel != 'index.html' else ''}"

    # Replace the monolithic stylesheet with core + page-type bundles.
    text = re.sub(r'href=["\'](?:\.\./)*assets/css/(core|brand|content|product)\.css\?v=[^"\']+["\']',
                  lambda m: f'href="{prefix}assets/css/{m.group(1)}.css?v={VERSION}"', text, flags=re.I)
    text = re.sub(r'<link\s+(?:href=["\'][^"\']*assets/styles\.css(?:\?[^"\']*)?["\']\s+rel=["\']stylesheet["\']|rel=["\']stylesheet["\']\s+href=["\'][^"\']*assets/styles\.css(?:\?[^"\']*)?["\'])\s*/?>',
                  f'<link rel="stylesheet" href="{prefix}assets/css/core.css?v={VERSION}">', text, flags=re.I)
    bundles = []
    if rel == "index.html" or rel in {"products.html", "hydrogen-bottles.html"} or rel.startswith("products/"):
        bundles.append("product")
    if rel == "brands.html" or rel.startswith("brands/"):
        bundles.extend(["brand", "product"])
    if rel in {"community.html", "reviews.html"} or rel.startswith("reviews/") or "/reviews/" in rel:
        bundles.extend(["content", "product"])
    bundle_links = "".join(f'<link rel="stylesheet" href="{prefix}assets/css/{name}.css?v={VERSION}">' for name in dict.fromkeys(bundles))
    core_link = f'<link rel="stylesheet" href="{prefix}assets/css/core.css?v={VERSION}">'
    if bundle_links and bundle_links not in text:
        text = text.replace(core_link, core_link + bundle_links, 1)

    # Canonical and unique social metadata stay in source HTML.
    canonical_tag = f'<link rel="canonical" href="{canonical}">'
    if re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*>', text, flags=re.I):
        text = re.sub(r'<link[^>]+rel=["\']canonical["\'][^>]*>', canonical_tag, text, count=1, flags=re.I)
    else:
        text = text.replace("</head>", canonical_tag + "</head>", 1)
    if not re.search(r'<meta[^>]+name=["\']description["\']', text, flags=re.I):
        text = text.replace("</title>", f'</title><meta name="description" content="{html_lib.escape(description, quote=True)}">', 1)
    TITLE_DESC = {
        "description": html_lib.escape(description, quote=True),
        "og:title": html_lib.escape(title, quote=True),
        "og:description": html_lib.escape(description, quote=True),
        "og:url": canonical,
        "twitter:title": html_lib.escape(title, quote=True),
        "twitter:description": html_lib.escape(description, quote=True),
    }
    for key in ["description", "twitter:title", "twitter:description"]:
        text = meta_content(text, "name", key)
    for key in ["og:title", "og:description", "og:url"]:
        text = meta_content(text, "property", key)

    def fix_jsonld(match):
        raw = match.group(1)
        try:
            data = json.loads(raw)
        except Exception:
            return match.group(0)
        if data.get("@type") == "WebPage":
            data["@id"] = canonical + "#webpage"
            data["url"] = canonical
            data["name"] = title
            data["description"] = description
            return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>"
        return match.group(0)
    text = re.sub(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', fix_jsonld, text, flags=re.I | re.S)

    json_types = []
    for raw in re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', text, flags=re.I | re.S):
        try:
            json_types.append(json.loads(raw).get("@type"))
        except Exception:
            pass
    if rel.startswith("products/") and "Product" not in json_types:
        product = PRODUCTS.get(path.name)
        if product:
            schema = {"@context":"https://schema.org","@type":"Product","name":product.get("name"),
                      "brand":{"@type":"Brand","name":product.get("brand")},"category":product.get("category"),
                      "description":description,"url":canonical}
            if product.get("image"):
                schema["image"] = "https://hitmoda.ru/" + product["image"]
            if isinstance(product.get("price"), (int, float)):
                schema["offers"] = {"@type":"Offer","price":product["price"],"priceCurrency":product.get("currency", "EUR"),"url":canonical}
            text = text.replace("</head>", '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False, separators=(",", ":")) + "</script></head>", 1)
    if rel.startswith("brands/") and "Brand" not in json_types:
        brand = BRANDS.get(path.stem)
        if brand:
            schema = {"@context":"https://schema.org","@type":"Brand","name":brand.get("name"),
                      "description":brand.get("description_de") or brand.get("description"),"url":canonical}
            if brand.get("logo"):
                schema["logo"] = "https://hitmoda.ru/" + brand["logo"]
            text = text.replace("</head>", '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False, separators=(",", ":")) + "</script></head>", 1)

    # Defer external behavior scripts; keep inline code ordering intact.
    text = re.sub(r'<script(?![^>]*\bdefer\b)([^>]*\bsrc=["\'][^"\']+["\'][^>]*)>', r'<script defer\1>', text, flags=re.I)

    # Native image loading: eager for logo/LCP product image, lazy for the rest.
    def lazy_img(match):
        tag = match.group(0)
        if re.search(r'\bloading=', tag, flags=re.I):
            return tag
        return tag[:-1] + ' loading="lazy" decoding="async">'
    text = re.sub(r'<img\b[^>]*>', lazy_img, text, flags=re.I)
    text = re.sub(r'(<a[^>]+class=["\'][^"\']*site-brand[^"\']*["\'][^>]*>\s*<img[^>]*?)\sloading=["\']lazy["\']', r'\1 loading="eager"', text, count=1, flags=re.I | re.S)
    text = re.sub(r'(<a[^>]+class=["\'][^"\']*site-brand[^"\']*["\'][^>]*>\s*<img[^>]*?)\sfetchpriority=["\']high["\']', r'\1', text, count=1, flags=re.I | re.S)
    text = re.sub(r'(<div[^>]+class=["\'][^"\']*device-photo[^"\']*["\'][^>]*>\s*<img[^>]*?)\sloading=["\']lazy["\']', r'\1 loading="eager" fetchpriority="high"', text, count=1, flags=re.I | re.S)
    path.write_text(text)


def main():
    split_css()
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" not in path.parts:
            optimize_html(path)


if __name__ == "__main__":
    main()
