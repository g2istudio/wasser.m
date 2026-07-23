#!/usr/bin/env python3
"""Import the official product batch supplied on 2026-07-23."""

import argparse
import html
import json
import re
import subprocess
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = Path("/tmp/wasser-august-products")
SITE = "https://wasser.market"

URLS = [
    "https://www.bela-aqua.de/shop/product/bao4200-bela-aqua-oblige-minerale-directflow-osmoseanlage-1732",
    "https://www.bela-aqua.de/shop/product/bae7100-bela-aqua-evolution-classic-osmoseanlage-mit-tank-229",
    "https://www.bela-aqua.de/shop/product/hg0001-hydrogen-trinkflasche-1570",
    "https://happyfilter.de/ONE",
    "https://neueswasser.de/shop/sprudelux-power-soda-untertisch-11404",
    "https://neueswasser.de/shop/untertischanlage-inox-silent-11401",
    "https://neueswasser.de/shop/umkehrosmoseanlage-sprudelux-juman-supreme-11562",
    "https://neueswasser.de/shop/umkehrosmoseanlage-sprudelux-pro-touch-11609",
    "https://neueswasser.de/shop/sprudelux-power-soda-auftisch-11406",
    "https://neueswasser.de/shop/sprudelux-power-soda-osmose-untertisch-11405",
    "https://neueswasser.de/shop/sprudelux-nuovo-untertisch-osmoseanlage-11402",
    "https://neueswasser.de/shop/sprudelux-ultra-flat-untertisch-trinkwassersystem-11408",
    "https://neueswasser.de/shop/umkehrosmoseanlage-aora-gt600-11471",
    "https://neueswasser.de/shop/umkehrosmoseanlage-aora-w12-4370",
    "https://neueswasser.de/shop/umkehrosmoseanlage-aora-w23-mit-tank-11411",
    "https://neueswasser.de/shop/stillundlaut-home-soda-premium-untertisch-umkehrosmoseanlage-sprudel-kuhlung-nur-10-cm-hoch-edelstahl-12251",
    "https://www.wasserladen.de/collections/umkehrosmose-gerate/products/h2o-rowa-select?variant=56031297896823",
    "https://www.wasserladen.de/collections/umkehrosmose-gerate/products/h2o-economy-3-blue?variant=45877347942679",
    "https://www.wasserladen.de/collections/umkehrosmose-gerate/products/wp-a01-all-in-one-umkehr-osmose-auftischfilter?variant=57011215434103",
    "https://www.wasserladen.de/collections/carbonit-filtergerate/products/sanuno-classic?variant=45877519581463",
    "https://www.wasserladen.de/collections/carbonit-filtergerate/products/sanuno-grande-sparset?variant=45877371207959",
    "https://www.filterzentrale.com/Shop/Umkehrosmoseanlagen/Untertischanlagen/Ultimate-Plus-Superflow/RO910",
    "https://www.filterzentrale.com/Shop/Umkehrosmoseanlagen/Untertischanlagen/Ultimate-Plus/RO900",
    "https://www.filterzentrale.com/Shop/Umkehrosmoseanlagen/Untertischanlagen/Profi/ROP050-VATER",
    "https://www.filterzentrale.com/Shop/Umkehrosmoseanlagen/Untertischanlagen/Hobby/ROH050-VATER",
    "https://www.filterzentrale.com/Shop/Umkehrosmoseanlagen/Untertischanlagen/Puraqua-Touch/SO800",
    "https://www.filterzentrale.com/Shop/Umkehrosmoseanlagen/Untertischanlagen/Aqua-Smart-Duo/RO500.BASE",
    "https://www.filterzentrale.com/Shop/Umkehrosmoseanlagen/Untertischanlagen/Pura/SO100",
    "https://www.filterzentrale.com/Shop/Umkehrosmoseanlagen/Untertischanlagen/Aqua-Quell/RO200",
    "https://www.filterzentrale.com/Shop/Umkehrosmoseanlagen/Untertischanlagen/Aqua-Tower/RO100.20.Base",
    "https://www.filterzentrale.com/Shop/Umkehrosmoseanlagen/Untertischanlagen/Vista/RO44DF",
    "https://www.filterzentrale.com/Shop/Umkehrosmoseanlagen/Untertischanlagen/Puraqua-Max-800/SORC800G",
    "https://www.filterzentrale.com/Shop/Umkehrosmoseanlagen/Untertischanlagen/Aqua-Smart-Duo-evo-I/RO600.GREY",
    "https://www.filterzentrale.com/Shop/Umkehrosmoseanlagen/Untertischanlagen/Aqua-Smart-Duo-evo-II/RO600.CHROME",
    "https://www.filterzentrale.com/Shop/Umkehrosmoseanlagen/Auftischanlagen/Aqua-Vita/SO500.90-VATER",
    "https://www.filterzentrale.com/Shop/Umkehrosmoseanlagen/Auftischanlagen/Pura-Up/SO110",
    "https://www.filterzentrale.com/Shop/Umkehrosmoseanlagen/Auftischanlagen/Aqua-Vita-B-Ware/SO500.90.bware-VATER",
]


def clean(value):
    value = re.sub(r"<(?:script|style)\b.*?</(?:script|style)>", " ", str(value or ""), flags=re.I | re.S)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", value)).split())


def slugify(value):
    value = value.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def esc(value):
    return html.escape(str(value or ""), quote=True)


def money(value):
    return "Preis auf Anfrage" if value is None else f"{value:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def fetch(url, path):
    url = urllib.parse.quote(url, safe=":/?=&%")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 WASSER.MARKET catalog research"})
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            path.write_bytes(response.read())
    except Exception:
        subprocess.run(["curl", "-L", "-sS", "--fail", url, "-o", str(path)], check=True)


def json_products(page):
    found = []
    for raw in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', page, re.I | re.S):
        try:
            data = json.loads(html.unescape(raw))
        except Exception:
            continue
        queue = data if isinstance(data, list) else data.get("@graph", [data]) if isinstance(data, dict) else []
        for item in queue:
            if isinstance(item, dict) and item.get("@type") == "Product":
                found.append(item)
    return found


def first(pattern, page):
    match = re.search(pattern, page, re.I | re.S)
    return clean(match.group(1)) if match else ""


def offer_price(product, page):
    offers = product.get("offers") if product else None
    if isinstance(offers, list):
        offers = offers[0] if offers else None
    if isinstance(offers, dict):
        try:
            return float(str(offers.get("price", "")).replace(",", "."))
        except ValueError:
            pass
    for pattern in [
        r'<meta[^>]+property=["\']product:price:amount["\'][^>]+content=["\']([^"\']+)',
        r'itemprop=["\']price["\'][^>]+content=["\']([^"\']+)',
        r'\bprice:\s*([0-9]+(?:\.[0-9]+)?)',
    ]:
        raw = first(pattern, page)
        if raw:
            raw = raw.replace(".", "").replace(",", ".") if "," in raw else raw
            try:
                return float(raw)
            except ValueError:
                pass
    variant = re.search(r'"variants"\s*:\s*\[\{.*?"price"\s*:\s*([0-9]+)', page, re.I | re.S)
    if variant:
        return int(variant.group(1)) / 100
    return None


def official_image(product, page):
    image = product.get("image") if product else None
    if isinstance(image, list):
        image = image[0] if image else None
    if isinstance(image, dict):
        image = image.get("url")
    if not image:
        image = first(r'featured_image"\s*:\s*\{\s*"src"\s*:\s*"([^"]+)', page)
    if not image:
        image = first(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', page)
    if image and image.startswith("//"):
        image = "https:" + image
    return image


def extract_specs(page):
    specs = {}

    def add(key, value):
        key, value = clean(key).strip(" :"), clean(value)
        if not key or not value or len(key) > 75 or len(value) > 650:
            return
        if key.lower() in {"kriterium", "option", "menge", "preis"}:
            return
        if key not in specs:
            specs[key] = value

    for key, value in re.findall(
        r'class=["\'][^"\']*\bspec-row\b[^"\']*["\'][^>]*>.*?class=["\'][^"\']*\bsk\b[^"\']*["\'][^>]*>(.*?)</span>.*?class=["\'][^"\']*\bsv\b[^"\']*["\'][^>]*>(.*?)</span>',
        page,
        re.I | re.S,
    ):
        add(key, value)
    for key, value in re.findall(r"<dl\b[^>]*>.*?<dt\b[^>]*>(.*?)</dt>.*?<dd\b[^>]*>(.*?)</dd>.*?</dl>", page, re.I | re.S):
        add(key, value)
    for row in re.findall(r"<tr\b[^>]*>(.*?)</tr>", page, re.I | re.S):
        cells = re.findall(r"<(?:th|td)\b[^>]*>(.*?)</(?:th|td)>", row, re.I | re.S)
        if len(cells) == 2:
            add(cells[0], cells[1])

    bullets = []
    block = re.search(r'class=["\'][^"\']*product-custom-bullet-points[^"\']*["\'][^>]*>(.*?)</div>', page, re.I | re.S)
    if block:
        bullets = [clean(x) for x in re.findall(r"<li\b[^>]*>(.*?)</li>", block.group(1), re.I | re.S)]
    if bullets:
        specs.setdefault("Highlights", "; ".join(bullets))
    return specs


def manufacturer(product, page, url, name):
    brand = product.get("brand") if product else None
    if isinstance(brand, dict):
        brand = brand.get("name")
    if not brand:
        brand = first(r'"brand"\s*:\s*"([^"]+)"', page)
    if not brand:
        brand = first(r'<div[^>]+class=["\'][^"\']*\btext-primary\b[^"\']*["\'][^>]*>(.*?)</div>', page)
    if "bela-aqua" in url:
        return "Bela Aqua"
    if "happyfilter" in url:
        return "HappyFilter"
    if "neueswasser" in url:
        upper = name.upper()
        if "AORA" in upper:
            return "AORA"
        if "STILLUNDLAUT" in upper:
            return "stillundlaut"
        return "SPRUDELUX"
    if "wasserladen" in url:
        normalized = {
            "Carbonit Filtertechnik GmbH": "CARBONIT",
            "Hurom Europe GmbH": "Wasserladen",
        }
        return normalized.get(clean(brand), clean(brand) or "Wasserladen")
    return clean(brand) or ("Osmotech" if "filterzentrale" in url else "Wasserladen")


def category(name, specs, url):
    text = f"{name} {' '.join(specs.values())} {url}".lower()
    if "hydrogen" in text:
        return "Hydrogen Bottles"
    if "auftisch" in text or "all-in-one" in text or "aqua-vita" in text or "pura-up" in text or "happyfilter" in text:
        return "Countertop RO" if "osmose" in text or "reverse" in text else "Water Dispenser"
    if "sprudel" in text or "soda" in text:
        return "Water Dispenser"
    if "carbonit" in text or "sanuno" in text or "ultrafiltration" in text:
        return "Drinking Water Filter"
    return "Direct Flow RO"


def extract(url, page):
    products = json_products(page)
    structured = products[0] if products else {}
    shopify_name = first(r'ProductName\s*=\s*"([^"]+)"', page) if "wasserladen" in url else ""
    name = shopify_name or clean(structured.get("name")) or first(r'<h1\b[^>]*>(.*?)</h1>', page) or first(r"<title[^>]*>(.*?)</title>", page)
    name = re.sub(r"\s*\|\s*(?:Made in|20 L/Std\.).*$", "", name, flags=re.I)
    brand = manufacturer(structured, page, url, name)
    specs = extract_specs(page)
    sku = clean(structured.get("sku")) or first(r"(?:Artikel-Nr\.?|Produktnummer)\s*:?\s*</?[^>]*>\s*([^<\n]+)", page)
    if sku:
        specs.setdefault("Artikelnummer", sku)
    if "bae7100-" in url:
        specs = {
            "Bauart": "Untertisch-Umkehrosmoseanlage mit Vorratstank",
            "Steuerung": "Computergesteuerte 9-in-1-Technologie mit LCD-Display",
            "Vorfilter": "Sedimentfilter ST-05",
            "Aktivkohlefilter": "Carbon-Blockfilter ST-CTO",
            "Ultrafiltration": "ST-HF; Herstellerangabe zur Rückhalterate 99,9999 %",
            "RO-Membran": "TFC ST-RO 75; 0,0001 µm",
            "Nachfilter": "Carbon-Nachfilter ST-3",
            "Filterwechsel": "Gekapselte Quick-Filter mit Wasserstoppfunktion",
            "Membranspülung": "Automatisch",
            "Pumpe": "Selbstansaugende, elektronisch geregelte Hochleistungspumpe",
            "Überwachung": "Wasserqualität, einzelne Filter und Membran",
            "Sicherheit": "Automatische Strom- und Wasserabschaltung; Fehler-Warnton",
            "Abmessungen": "24,5 × 39,0 × 39,0 cm (B × T × H)",
            "Armatur": "Evolution-Wasserhahn; laut Hersteller nach NSF-Anforderungen",
            "Artikelnummer": "BAE7100",
        }
    if "hg0001-" in url:
        specs = {
            "Produktart": "Tragbare Wasserstoff-Trinkflasche",
            "Inhalt": "450 ml",
            "Gewicht": "318 g",
            "Wasserstoffkonzentration": "> 600 bis 1.000 ppb",
            "Technologie": "SPE / PEM",
            "Aufbereitungszeit": "Ca. 5 Minuten",
            "Ladegerät": "DC 5 V / 1 A; USB-Ladekabel enthalten",
            "Ladezeit": "2–3 Stunden",
            "Akkukapazität": "Ca. 1.000 mAh",
            "Abmessungen": "70 × 70 × 240 mm",
            "Material": "BPA-/BPS-freier Kunststoff",
            "Bedienung": "Ein-Tasten-Bedienung; Powerbutton 3 Sekunden halten",
            "Anzeige": "Integrierter LED-Farbwechsel während der Ionisierung",
            "Artikelnummer": "HG0001",
        }
    summary = clean(structured.get("description"))
    meta_desc = first(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', page)
    if len(summary) < 70:
        summary = meta_desc
    if len(summary) < 70 or summary.lower() == name.lower():
        summary = f"{name}: Wasseraufbereitungssystem von {brand} mit den auf der offiziellen Produktseite veröffentlichten Leistungs-, Filter- und Ausstattungsdaten."
    summary = summary[:450].rsplit(" ", 1)[0].rstrip(" ,;:") + "." if len(summary) > 450 else summary.rstrip(".") + "."
    brand_slug = slugify(brand)
    base_slug = slugify(name)
    if len(base_slug) > 72:
        base_slug = "-".join(base_slug.split("-")[:10])
    slug = f"{brand_slug}-{base_slug}" if not base_slug.startswith(brand_slug) else base_slug
    remote_image = official_image(structured, page)
    if not remote_image and "bela-aqua" in url:
        remote_image = first(r'<img[^>]+src=["\']([^"\']+)["\'][^>]+class=["\'][^"\']*product_detail_img', page)
        if remote_image.startswith("/"):
            remote_image = "https://www.bela-aqua.de" + remote_image
    return {
        "id": slug,
        "slug": slug,
        "brand": brand,
        "brandSlug": brand_slug,
        "name": name,
        "category": category(name, specs, url),
        "price": 97.0 if "hg0001-" in url else offer_price(structured, page),
        "currency": "EUR",
        "rating": None,
        "reviews": 0,
        "image": f"assets/products/{slug}.webp",
        "source": url,
        "summary": summary,
        "specs": specs or {"Produktart": category(name, specs, url), "Datenquelle": "Offizielle Produktseite"},
        "_remote_image": remote_image,
    }


def header(depth=".."):
    return f'''<div class="topbar"><div class="container"><span>Unabhängige Datenbank für Wassertechnologie</span><span>Erfahrungen · Vergleiche · Labordaten</span></div></div><header class="site-header"><div class="header-shell container"><a aria-label="WASSER.MARKET Startseite" class="site-brand" href="{depth}/index.html"><img alt="WASSER.MARKET" src="{depth}/assets/img/wasser-market-logo.jpg" loading="eager"></a><nav class="desktop-nav"><a href="{depth}/products.html">Produkte</a><a href="{depth}/brands.html">Marken</a><a href="{depth}/compare.html">Vergleichen</a><a href="{depth}/community.html">Community</a><div class="nav-more"><button class="nav-more-btn" type="button">Wissen</button><div class="nav-more-menu"><a href="{depth}/knowledge.html">Wasserwissen</a><a href="{depth}/technologies.html">Technologien</a></div></div></nav><div class="header-tools"><a class="btn primary compact-compare" href="{depth}/compare.html">⇄ <span>Vergleichen</span></a><button aria-expanded="false" aria-label="Menü öffnen" class="icon-btn mobile-menu-btn" type="button">☰</button></div></div><div aria-hidden="true" class="mobile-nav-panel"><div class="container mobile-nav-inner"><a href="{depth}/products.html">Produkte</a><a href="{depth}/brands.html">Marken</a><a href="{depth}/compare.html">Vergleichen</a><a href="{depth}/community.html">Community</a><a href="{depth}/knowledge.html">Wasserwissen</a></div></div></header>'''


def footer(depth=".."):
    return f'''<footer class="site-footer"><div class="footer-bottom"><div class="container"><span>© WASSER.MARKET</span><span>Unabhängige Datenbank für Wassertechnologie</span></div></div></footer><script defer src="{depth}/assets/i18n.js"></script><script defer src="{depth}/assets/app.js"></script>'''


def make_product_page(p):
    schema = {"@context": "https://schema.org", "@type": "Product", "name": f'{p["brand"]} {p["name"]}', "image": f'{SITE}/{p["image"]}', "brand": {"@type": "Brand", "name": p["brand"]}, "category": p["category"], "description": p["summary"]}
    if p["price"] is not None:
        schema["offers"] = {"@type": "Offer", "priceCurrency": "EUR", "price": str(p["price"]), "url": p["source"]}
    rows = "".join(f"<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>" for k, v in p["specs"].items())
    title = f'{p["brand"]} {p["name"]} – Daten & Preis'
    return f'''<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(p["summary"])}"><link rel="stylesheet" href="../assets/css/core.css?v=20260723-seo"><link rel="stylesheet" href="../assets/css/product.css?v=20260723-seo"><link rel="canonical" href="{SITE}/products/{esc(p["slug"])}.html"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head><body class="wm-v2">{header()}<main><div class="container"><div class="breadcrumbs"><a href="../index.html">Home</a> / <a href="../products.html">Produkte</a> / {esc(p["name"])}</div><section class="device-layout"><div class="device-photo"><img alt="{esc(p["brand"])} {esc(p["name"])}" src="../{esc(p["image"])}" loading="eager"></div><div class="device-info"><span class="badge">{esc(p["category"])}</span><h1>{esc(p["brand"])} {esc(p["name"])}</h1><p class="lead">{esc(p["summary"])}</p><div class="price">{esc(money(p["price"]))}</div><p><a class="btn primary" href="{esc(p["source"])}" target="_blank" rel="nofollow noopener">Offizielle Produktseite ↗</a></p></div></section><div class="content-grid"><section class="panel"><h2>Technische Daten</h2><table class="spec-table">{rows}</table><h2>Beschreibung</h2><p>{esc(p["summary"])}</p><h2>Datenhinweis</h2><p>Preis, Bild und technische Angaben stammen von der verlinkten offiziellen Produktseite. Varianten und Verfügbarkeit können sich ändern.</p></section><aside><div class="panel"><h3>Einordnung</h3><table class="spec-table"><tr><td>Marke</td><td><a href="../brands/{esc(p["brandSlug"])}.html">{esc(p["brand"])}</a></td></tr><tr><td>Kategorie</td><td>{esc(p["category"])}</td></tr><tr><td>Preisstatus</td><td>{esc("Offizieller Shoppreis bei Recherche" if p["price"] is not None else "Preis auf Anfrage")}</td></tr></table></div></aside></div></div></main>{footer()}</body></html>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()
    CACHE.mkdir(exist_ok=True)
    products = []
    stale_slugs = {
        "rowa-4-you-wir-hinterlassen-eine-sauberere-welt",
        "wasserladen-wir-hinterlassen-eine-sauberere-welt",
        "carbonit-wir-hinterlassen-eine-sauberere-welt",
    }
    for stale in stale_slugs:
        for stale_path in [ROOT / "products" / f"{stale}.html", ROOT / "assets" / "products" / f"{stale}.webp"]:
            stale_path.unlink(missing_ok=True)
    for index, url in enumerate(URLS, 1):
        cache = CACHE / f"{index:02d}.html"
        if args.fetch or not cache.exists():
            fetch(url, cache)
        page = cache.read_text(errors="ignore")
        product = extract(url, page)
        if not product["name"]:
            raise RuntimeError(f"No product name extracted from {url}")
        products.append(product)
        print(f'{index:02d} {product["brand"]}: {product["name"]} | {product["price"]} | {len(product["specs"])} specs')

    # Download and normalize official product images.
    from PIL import Image
    for product in products:
        remote = product.pop("_remote_image", None)
        target = ROOT / product["image"]
        if remote:
            raw = CACHE / f'{product["slug"]}.image'
            try:
                fetch(remote, raw)
                with Image.open(raw) as image:
                    image.thumbnail((1200, 1200))
                    if image.mode not in ("RGB", "RGBA"):
                        image = image.convert("RGB")
                    target.parent.mkdir(parents=True, exist_ok=True)
                    image.save(target, "WEBP", quality=84, method=6)
            except Exception as error:
                print(f"Image warning {product['slug']}: {error}")

    products_path = ROOT / "data/products.json"
    all_products = json.loads(products_path.read_text())
    all_products = [item for item in all_products if item.get("slug") not in stale_slugs]
    for product in products:
        same = next((i for i, item in enumerate(all_products) if (item.get("source") or "").split("?")[0] == product["source"].split("?")[0] or item.get("slug") == product["slug"]), -1)
        if same < 0:
            all_products.append(product)
        else:
            all_products[same] = {**all_products[same], **product}
    products_path.write_text(json.dumps(all_products, ensure_ascii=False, indent=2) + "\n")

    brands_path = ROOT / "data/brands.json"
    brands = json.loads(brands_path.read_text())
    websites = {
        "Bela Aqua": "https://www.bela-aqua.de",
        "HappyFilter": "https://happyfilter.de",
        "SPRUDELUX": "https://neueswasser.de",
        "AORA": "https://neueswasser.de",
        "stillundlaut": "https://neueswasser.de",
        "ROWA 4 you": "https://www.wasserladen.de",
        "Wasserladen": "https://www.wasserladen.de",
        "CARBONIT": "https://www.wasserladen.de",
        "Osmotech": "https://www.filterzentrale.com",
    }
    for name in sorted({p["brand"] for p in products}):
        brand_slug = slugify(name)
        description = f"{name} bietet Systeme und Produkte für Trinkwasserfiltration, Umkehrosmose und Wasseraufbereitung. Die Datenbank führt die offiziell veröffentlichten Modelle und technischen Eigenschaften."
        record = {"slug": brand_slug, "name": name, "country": "Germany", "website": websites.get(name, ""), "group": "Water Filtration", "description": description, "founded": None, "description_de": description, "description_en": description, "products_count": 0, "rating": None, "logo": "assets/img/wasser-market-logo.jpg"}
        existing = next((i for i, b in enumerate(brands) if b.get("slug") == brand_slug or b.get("name", "").lower() == name.lower()), -1)
        if existing < 0:
            brands.append(record)
        else:
            logo = brands[existing].get("logo")
            brands[existing] = {**brands[existing], **record}
            if logo:
                brands[existing]["logo"] = logo
    for brand in brands:
        brand["products_count"] = sum(1 for p in all_products if p.get("brandSlug") == brand["slug"] or p.get("brand") == brand["name"])
    brands_path.write_text(json.dumps(brands, ensure_ascii=False, indent=2) + "\n")

    for product in products:
        (ROOT / "products" / f'{product["slug"]}.html').write_text(make_product_page(product))

    # Brand pages for all brands represented in this batch.
    for brand_name in sorted({p["brand"] for p in products}):
        brand = next(b for b in brands if b["name"].lower() == brand_name.lower())
        items = [p for p in all_products if p.get("brandSlug") == brand["slug"] or p.get("brand") == brand["name"]]
        cards = "".join(f'''<div class="product-card"><a class="photo" href="../products/{esc(p["slug"])}.html"><img src="../{esc(p["image"])}" alt="{esc(p["brand"])} {esc(p["name"])}" loading="lazy"></a><div class="brand">{esc(p["brand"])}</div><h3>{esc(p["name"])}</h3><div class="price">{esc(money(p.get("price")))}</div><div class="actions"><a class="btn small" href="../products/{esc(p["slug"])}.html">Alle Daten</a></div></div>''' for p in items)
        page = f'''<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(brand["name"])} – Wasserfilter & Produkte</title><meta name="description" content="{esc(brand["description_de"])}"><link rel="stylesheet" href="../assets/css/core.css?v=20260723-seo"><link rel="stylesheet" href="../assets/css/brand.css?v=20260723-seo"><link rel="stylesheet" href="../assets/css/product.css?v=20260723-seo"><link rel="canonical" href="{SITE}/brands/{esc(brand["slug"])}.html"></head><body class="wm-v2">{header()}<main><div class="container"><div class="breadcrumbs"><a href="../index.html">Home</a> / <a href="../brands.html">Marken</a> / {esc(brand["name"])}</div><section class="brand-hero"><div class="brand-hero-primary"><div class="brand-hero-logo"><img src="../{esc(brand["logo"])}" alt="{esc(brand["name"])} Logo"></div><div class="brand-hero-copy"><span class="badge">Wasserfiltration</span><h1>{esc(brand["name"])}</h1><p class="lead">{esc(brand["description_de"])}</p></div></div><aside class="brand-hero-details"><h2>Markenprofil</h2><dl><div><dt>Land</dt><dd>{esc(brand["country"])}</dd></div><div><dt>Modelle</dt><dd>{len(items)}</dd></div></dl><a class="btn primary" href="{esc(brand["website"])}" target="_blank" rel="nofollow noopener">Offizielle Website ↗</a></aside></section><section class="panel"><h2>Produkte in der Datenbank</h2><div class="product-grid">{cards}</div></section></div></main>{footer()}</body></html>'''
        (ROOT / "brands" / f'{brand["slug"]}.html').write_text(page)

    # Keep every newly represented brand discoverable in the brand directory.
    directory_path = ROOT / "brands.html"
    directory = directory_path.read_text()
    for brand_name in sorted({p["brand"] for p in products}):
        brand = next(b for b in brands if b["name"].lower() == brand_name.lower())
        if f'brands/{brand["slug"]}.html' in directory:
            continue
        card = f'''<a class="brand-directory-card" href="brands/{esc(brand["slug"])}.html" data-brand-name="{esc(brand["name"].lower())}" data-brand-country="{esc(brand["country"].lower())}"><div class="brand-logo-wrap"><img src="{esc(brand["logo"])}" alt="{esc(brand["name"])} Logo" loading="lazy"></div><div class="brand-card-body"><span class="badge">Wasserfiltration</span><h3>{esc(brand["name"])}</h3><p class="brand-meta">{esc(brand["country"])} · {brand["products_count"]} Modelle</p><p>{esc(brand["description_de"])}</p><span class="brand-link">Marke ansehen →</span></div></a>'''
        marker = '<div class="panel brand-empty"'
        position = directory.find(marker)
        grid_end = directory.rfind("</div>", 0, position)
        directory = directory[:grid_end] + card + directory[grid_end:]
    directory = re.sub(r'\d+ bekannte Hersteller', f'{len(brands)} bekannte Hersteller', directory)
    directory = re.sub(r'<span id="brandDirectoryCount" class="brand-count-badge">\d+ Marken</span>', f'<span id="brandDirectoryCount" class="brand-count-badge">{len(brands)} Marken</span>', directory)
    directory_path.write_text(directory)

    # Register products in the comparison data used by catalog buttons.
    app_path = ROOT / "assets/app.js"
    app = app_path.read_text()
    for p in products:
        line = "{id:" + json.dumps(p["id"]) + ",brand:" + json.dumps(p["brand"], ensure_ascii=False) + ",name:" + json.dumps(p["name"], ensure_ascii=False) + ",cat:" + json.dumps(p["category"]) + ",price:" + json.dumps(money(p["price"]), ensure_ascii=False) + ",priceValue:" + (str(p["price"]) if p["price"] is not None else "null") + ",features:[],ppb:null,flow:" + json.dumps(p["specs"].get("Durchfluss", p["specs"].get("Leistung", "Not published")), ensure_ascii=False) + ",maint:" + json.dumps(p["specs"].get("Filterwechsel", "Not published"), ensure_ascii=False) + ",liter:'—',membrane:" + json.dumps(p["specs"].get("RO-Membran", p["specs"].get("Filtration", "Not published")), ensure_ascii=False) + ",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:" + json.dumps(p["specs"].get("Max. Leistungsaufnahme (Kühlung)", p["specs"].get("Leistung & Verbrauch", "Not published")), ensure_ascii=False) + ",warranty:'Not published',country:'Germany',image:" + json.dumps(p["image"]) + ",url:" + json.dumps("products/" + p["slug"] + ".html") + "}"
        pattern = re.compile(r"\{id:[\"']" + re.escape(p["id"]) + r"[\"'][^\n]*\}")
        if pattern.search(app):
            app = pattern.sub(lambda _: line, app)
        else:
            app = app.replace("\n];", ",\n" + line + "\n];")
    app_path.write_text(app)

    # Preserve this batch for future full catalog rebuilds.
    additions_path = ROOT / "data/catalog-additions.json"
    additions = json.loads(additions_path.read_text())
    additions["products"] = [item for item in additions["products"] if item.get("slug") not in stale_slugs]
    for brand_name in sorted({p["brand"] for p in products}):
        brand = next(b for b in brands if b["name"].lower() == brand_name.lower())
        record = {"slug": brand["slug"], "name": brand["name"], "country": brand["country"], "website": brand["website"], "group": brand["group"], "description": brand["description_de"]}
        index = next((i for i, item in enumerate(additions["brands"]) if item.get("slug") == brand["slug"]), -1)
        if index < 0:
            additions["brands"].append(record)
        else:
            additions["brands"][index] = record
    for product in products:
        record = {**product, "specs": list(product["specs"].items())}
        index = next((i for i, p in enumerate(additions["products"]) if p.get("slug") == product["slug"]), -1)
        if index < 0:
            additions["products"].append(record)
        else:
            additions["products"][index] = record
    additions_path.write_text(json.dumps(additions, ensure_ascii=False, indent=2) + "\n")
    print(f"Imported {len(products)} official product pages; catalog now has {len(all_products)} products")


if __name__ == "__main__":
    main()
