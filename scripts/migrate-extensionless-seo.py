#!/usr/bin/env python3
"""Migrate public URLs to extensionless routes and complete core page SEO."""

from datetime import date
from html import escape, unescape
from pathlib import Path
from urllib.parse import urljoin
import json
import re

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://wasser.market"
TODAY = date.today().isoformat()


def plain(value):
    return " ".join(unescape(re.sub(r"<[^>]+>", " ", value or "")).split())


def canonical_for(path):
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return SITE + "/"
    return SITE + "/" + rel.removesuffix(".html")


def without_html(value):
    """Remove .html only from local/public site URLs, never manufacturer URLs."""
    value = re.sub(
        r"(https?://(?:www\.)?(?:wasser\.market|hitmoda\.ru)/[^\"'<>\s?#]+)\.html(?=([?#]|$))",
        r"\1",
        value,
        flags=re.I,
    )
    if not re.match(r"^(?:[a-z]+:)?//", value, re.I):
        value = re.sub(r"\.html(?=([?#]|$))", "", value, flags=re.I)
    value = re.sub(r"(^|/)index(?=([?#]|$))", lambda match: "/" if match.group(1) == "/" else "./", value, flags=re.I)
    return value


def rewrite_internal_attributes(source):
    pattern = re.compile(
        r'(?P<prefix>\b(?:href|action|data-[\w-]*url)=["\'])(?P<url>[^"\']+)(?P<suffix>["\'])',
        re.I,
    )
    return pattern.sub(
        lambda match: match.group("prefix") + without_html(match.group("url")) + match.group("suffix"),
        source,
    )


def set_meta(source, name, value, property_meta=False):
    attr = "property" if property_meta else "name"
    pattern = re.compile(rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(name)}["\'])[^>]*>', re.I)
    tag = f'<meta {attr}="{name}" content="{escape(value, quote=True)}">'
    return pattern.sub(tag, source, count=1) if pattern.search(source) else source.replace("</head>", tag + "</head>", 1)


def absolute_image(path, canonical, source):
    match = re.search(
        r'<div\b[^>]*class=["\'][^"\']*\bdevice-photo\b[^"\']*["\'][^>]*>.*?<img\b[^>]*\bsrc=["\']([^"\']+)',
        source,
        re.I | re.S,
    )
    if not match:
        match = re.search(r'<main\b.*?<img\b[^>]*\bsrc=["\']([^"\']+)', source, re.I | re.S)
    if not match:
        return SITE + "/assets/img/wasser-market-logo.jpg"
    image = match.group(1)
    return image if re.match(r"https?://", image, re.I) else urljoin(canonical, image)


def enrich_json_ld(source, canonical, image, h1, is_product):
    scripts = list(re.finditer(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', source, re.I | re.S))
    replacements = []
    has_breadcrumb = False
    has_webpage = False

    for match in scripts:
        try:
            data = json.loads(unescape(match.group(1)))
        except Exception:
            continue
        items = data if isinstance(data, list) else data.get("@graph", []) if isinstance(data, dict) and "@graph" in data else [data]
        changed = False
        for item in items:
            if not isinstance(item, dict):
                continue
            kind = item.get("@type")
            has_breadcrumb = has_breadcrumb or kind == "BreadcrumbList"
            has_webpage = has_webpage or kind in ("WebPage", "ItemPage")
            if kind == "Product":
                item["@id"] = canonical + "#product"
                item["url"] = canonical
                item["mainEntityOfPage"] = canonical
                item["image"] = image
                changed = True
            elif kind in ("WebPage", "ItemPage"):
                item["url"] = canonical
                item["@id"] = canonical + "#webpage"
                item["dateModified"] = TODAY
                changed = True
            elif kind == "BreadcrumbList":
                for crumb in item.get("itemListElement", []):
                    if isinstance(crumb, dict) and isinstance(crumb.get("item"), str):
                        crumb["item"] = without_html(crumb["item"])
                changed = True
        if changed:
            payload = data
            replacements.append((match.start(1), match.end(1), json.dumps(payload, ensure_ascii=False, separators=(",", ":"))))

    for start, end, payload in reversed(replacements):
        source = source[:start] + payload + source[end:]

    if is_product and not has_breadcrumb:
        section = canonical[len(SITE):].strip("/").split("/")
        slug = section[-1]
        breadcrumb = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Startseite", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Produkte", "item": SITE + "/products"},
                {"@type": "ListItem", "position": 3, "name": h1 or slug.replace("-", " "), "item": canonical},
            ],
        }
        source = source.replace("</head>", f'<script type="application/ld+json">{json.dumps(breadcrumb, ensure_ascii=False, separators=(",", ":"))}</script></head>', 1)

    if is_product and not has_webpage:
        webpage = {
            "@context": "https://schema.org",
            "@type": "ItemPage",
            "@id": canonical + "#webpage",
            "url": canonical,
            "name": h1,
            "dateModified": TODAY,
            "primaryImageOfPage": image,
            "mainEntity": {"@id": canonical + "#product"},
        }
        source = source.replace("</head>", f'<script type="application/ld+json">{json.dumps(webpage, ensure_ascii=False, separators=(",", ":"))}</script></head>', 1)
    return source


def main():
    html_files = sorted(ROOT.rglob("*.html"))
    sitemap_entries = []

    for path in html_files:
        source = path.read_text(errors="ignore")
        source = rewrite_internal_attributes(source)
        source = re.sub(
            r"https?://(?:www\.)?(?:wasser\.market|hitmoda\.ru)/([^\"'<>\s?#]+)\.html",
            SITE + r"/\1",
            source,
            flags=re.I,
        )

        canonical = canonical_for(path)
        canonical_tag = f'<link rel="canonical" href="{canonical}">'
        canonical_pattern = re.compile(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*>', re.I)
        source = canonical_pattern.sub(canonical_tag, source, count=1) if canonical_pattern.search(source) else source.replace("</head>", canonical_tag + "</head>", 1)

        h1_match = re.search(r"<h1\b[^>]*>(.*?)</h1>", source, re.I | re.S)
        h1 = plain(h1_match.group(1) if h1_match else "")
        is_product = path.parent.name == "products"
        image = absolute_image(path, canonical, source)

        robots_match = re.search(r'<meta\b(?=[^>]*name=["\']robots["\'])[^>]*content=["\']([^"\']+)', source, re.I)
        robots_value = robots_match.group(1) if robots_match else "index,follow"
        if "max-image-preview" not in robots_value:
            robots_value += ",max-image-preview:large,max-snippet:-1"
        source = set_meta(source, "robots", robots_value)

        source = set_meta(source, "og:url", canonical, True)
        if is_product:
            source = set_meta(source, "og:image", image, True)
            source = set_meta(source, "twitter:image", image)
        source = enrich_json_ld(source, canonical, image, h1, is_product)
        path.write_text(source)

        if path.name == "ui-kit.html" or "noindex" in robots_value.lower():
            continue
        sitemap_entries.append((canonical, image if is_product else None, h1))

    # Extensionless routes in runtime product data and comparison JS.
    for relative in ["data/products.json", "assets/app.js"]:
        target = ROOT / relative
        text = target.read_text(errors="ignore")
        text = re.sub(r'(?P<path>(?:products|brands|articles|professionals)/[^"\'\s?#]+)\.html', r"\g<path>", text)
        target.write_text(text)

    # Rebuild a canonical sitemap with product images and modification dates.
    unique = {}
    for canonical, image, title in sitemap_entries:
        unique[canonical] = (image, title)
    rows = []
    for canonical, (image, title) in sorted(unique.items()):
        image_xml = ""
        if image:
            image_xml = f"<image:image><image:loc>{escape(image)}</image:loc><image:title>{escape(title)}</image:title></image:image>"
        rows.append(f"<url><loc>{escape(canonical)}</loc><lastmod>{TODAY}</lastmod>{image_xml}</url>")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
    sitemap += "\n".join(rows) + "\n</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sitemap)
    print(f"Migrated {len(html_files)} HTML files; sitemap contains {len(rows)} extensionless URLs")


if __name__ == "__main__":
    main()
