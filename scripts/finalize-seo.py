#!/usr/bin/env python3
"""Normalize SEO metadata after static catalog generators have run."""

from collections import Counter
from html import escape, unescape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://wasser.market"
TEXT_EXTENSIONS = {".html", ".xml", ".txt", ".js", ".cjs", ".mjs", ".py", ".json"}


def plain(value):
    return " ".join(unescape(re.sub(r"<[^>]+>", " ", value or "")).split())


def trim_words(value, limit):
    value = plain(value)
    if len(value) <= limit:
        return value
    shortened = value[: limit + 1].rsplit(" ", 1)[0].rstrip(" ,;:–—-|")
    return shortened or value[:limit].rstrip()


def page_kind(path):
    if "products" in path.parts:
        return "product"
    if "brands" in path.parts:
        return "brand"
    if "articles" in path.parts:
        return "article"
    if "professionals" in path.parts:
        return "professional"
    return "page"


def optimized_title(path, current, h1):
    kind = page_kind(path)
    base = plain(h1 or current.split("|", 1)[0].split(" – ", 1)[0])
    if kind == "product":
        base = re.sub(
            r"\b(?:Tankloser |Smart |Alkalischer |Mineralisierender )*"
            r"(?:Untertisch-?)?(?:Umkehrosmose(?:anlage|-System)?|RO-?)"
            r"(?:-?Wasserfilter(?:anlage)?|-?System)?\b",
            "RO-System",
            base,
            flags=re.I,
        )
        suffix = " – Daten & Preis"
        return trim_words(base, 60 - len(suffix)) + suffix
    if kind == "brand":
        return trim_words(base, 38) + " – Wasserfilter & Produkte"
    if kind == "article":
        return trim_words(current, 60)
    if path.name == "reviews.html":
        return "Wasserfilter-Erfahrungen & Bewertungen | WASSER.MARKET"
    if len(current) < 30:
        return trim_words(base, 39) + " | WASSER.MARKET"
    return trim_words(current, 60)


def optimized_description(path, current, h1):
    kind = page_kind(path)
    base = plain(current)
    name = plain(h1) or "Wassertechnik"
    if path.name == "reviews.html":
        return "Erfahrungen und Bewertungen zu Wasserfiltern, Umkehrosmoseanlagen und Wassertechnik in der Community von WASSER.MARKET entdecken."
    short_name = trim_words(name, 52)
    if kind == "product":
        return trim_words(
            f"Technische Daten zu {short_name}: Filterleistung, Ausstattung, Abmessungen, Wartung und Preis. Offizielle Herstellerangaben transparent dokumentiert.",
            160,
        ).rstrip(" .… ,;:–—-") + "."
    if kind == "brand":
        return trim_words(
            f"{short_name}: Markenprofil, Wasserfilter, Modelle und technische Eigenschaften. Produkte in der unabhängigen WASSER.MARKET Datenbank vergleichen.",
            160,
        ).rstrip(" .… ,;:–—-") + "."
    if kind == "article":
        return trim_words(
            f"{short_name}: ausführlicher Ratgeber zu Funktionsweise, Einsatzbereichen, Vorteilen, Grenzen, Wartung und Auswahl passender Wasserfilter.",
            160,
        ).rstrip(" .… ,;:–—-") + "."
    if kind == "professional":
        return trim_words(
            f"{short_name}: Leistungen, Einsatzgebiet, Spezialisierungen, Richtpreise und Bewertungen für Wassertechnik und Sanitärarbeiten ansehen.",
            160,
        ).rstrip(" .… ,;:–—-") + "."
    base = re.sub(r"\.{2,}$", ".", base)
    if 120 <= len(base) <= 160:
        return base
    return trim_words(
        f"{short_name}: Informationen, Vergleiche und nachvollziehbare Daten zu Wasserfiltern, Umkehrosmoseanlagen und moderner Wassertechnik.",
        160,
    ).rstrip(" .… ,;:–—-") + "."


def set_meta(html, name, value, property_meta=False):
    attr = "property" if property_meta else "name"
    pattern = re.compile(
        rf"<meta\b(?=[^>]*\b{attr}=[\"']{re.escape(name)}[\"'])[^>]*>",
        re.I,
    )
    tag = f'<meta {attr}="{name}" content="{escape(value, quote=True)}">'
    if pattern.search(html):
        return pattern.sub(tag, html, count=1)
    return html.replace("</head>", tag + "</head>", 1)


def canonical_for(path):
    rel = path.relative_to(ROOT).as_posix()
    return SITE + ("/" if rel == "index.html" else f"/{rel}")


html_files = sorted(ROOT.rglob("*.html"))

# The production identity must survive reruns of older import scripts.
for path in ROOT.rglob("*"):
    if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
        text = path.read_text(errors="ignore")
        if "https://wasser.market" in text:
            path.write_text(text.replace("https://wasser.market", SITE))

seen_titles = Counter()
seen_descriptions = Counter()
for path in html_files:
    html = path.read_text(errors="ignore")
    title_match = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    desc_match = re.search(
        r"<meta\b(?=[^>]*\bname=[\"']description[\"'])[^>]*\bcontent=[\"']([^\"']*)[\"'][^>]*>",
        html,
        re.I,
    )
    if not desc_match:
        desc_match = re.search(
            r"<meta\b(?=[^>]*\bcontent=[\"']([^\"']*)[\"'])[^>]*\bname=[\"']description[\"'][^>]*>",
            html,
            re.I,
        )
    h1_match = re.search(r"<h1\b[^>]*>(.*?)</h1>", html, re.I | re.S)
    current_title = plain(title_match.group(1) if title_match else "")
    current_desc = plain(desc_match.group(1) if desc_match else "")
    h1 = plain(h1_match.group(1) if h1_match else "")

    title = optimized_title(path, current_title, h1)
    if seen_titles[title]:
        discriminator = path.stem.replace("-", " ").upper()
        title = trim_words(f"{title.split(' – ')[0]} {discriminator}", 43) + " – Daten & Preis"
    seen_titles[title] += 1

    description = optimized_description(path, current_desc, h1)
    if seen_descriptions[description]:
        description = trim_words(description.rstrip(".") + f" Mehr zu {h1 or path.stem}.", 160) + "."
    seen_descriptions[description] += 1

    if title_match:
        html = re.sub(r"<title>.*?</title>", f"<title>{escape(title)}</title>", html, count=1, flags=re.I | re.S)
    else:
        html = html.replace("</head>", f"<title>{escape(title)}</title></head>", 1)
    html = set_meta(html, "description", description)

    canonical = canonical_for(path)
    if path.name == "reviews.html":
        canonical = SITE + "/community.html"
        html = set_meta(html, "robots", "noindex,follow")
        if not h1_match:
            html = html.replace("<main>", '<main><h1 class="visually-hidden">Wasserfilter-Erfahrungen und Bewertungen</h1>', 1)

    canonical_tag = f'<link rel="canonical" href="{canonical}">'
    canonical_pattern = re.compile(r"<link\b(?=[^>]*\brel=[\"']canonical[\"'])[^>]*>", re.I)
    html = canonical_pattern.sub(canonical_tag, html, count=1) if canonical_pattern.search(html) else html.replace("</head>", canonical_tag + "</head>", 1)

    og_type = "article" if page_kind(path) == "article" else "product" if page_kind(path) == "product" else "website"
    html = set_meta(html, "og:title", title, True)
    html = set_meta(html, "og:description", description, True)
    html = set_meta(html, "og:type", og_type, True)
    html = set_meta(html, "og:url", canonical, True)
    if not re.search(r"<meta\b(?=[^>]*property=[\"']og:image[\"'])", html, re.I):
        html = set_meta(html, "og:image", SITE + "/assets/img/wasser-market-logo.jpg", True)
    html = set_meta(html, "twitter:card", "summary_large_image")
    html = set_meta(html, "twitter:title", title)
    html = set_meta(html, "twitter:description", description)
    if not re.search(r"<meta\b(?=[^>]*name=[\"']twitter:image[\"'])", html, re.I):
        html = set_meta(html, "twitter:image", SITE + "/assets/img/wasser-market-logo.jpg")
    path.write_text(html)

# Resolve any collisions introduced by shortening long names. Use a readable
# discriminator from the file name so every search snippet remains stable.
def current_value(html, pattern):
    match = re.search(pattern, html, re.I | re.S)
    return plain(match.group(1)) if match else ""


title_groups = {}
description_groups = {}
for path in html_files:
    html = path.read_text(errors="ignore")
    title_groups.setdefault(current_value(html, r"<title>(.*?)</title>"), []).append(path)
    description_groups.setdefault(
        current_value(html, r'<meta name="description" content="([^"]*)">'), []
    ).append(path)

for value, paths in title_groups.items():
    if not value or len(paths) == 1:
        continue
    for path in paths[1:]:
        html = path.read_text(errors="ignore")
        h1 = current_value(html, r"<h1\b[^>]*>(.*?)</h1>")
        tail = " ".join(path.stem.replace("-", " ").split()[-3:])
        replacement = trim_words(h1 or value.split(" – ")[0], 39)
        replacement = trim_words(f"{replacement} {tail}", 45) + " – Daten"
        html = re.sub(r"<title>.*?</title>", f"<title>{escape(replacement)}</title>", html, count=1, flags=re.I | re.S)
        html = set_meta(html, "og:title", replacement, True)
        html = set_meta(html, "twitter:title", replacement)
        path.write_text(html)

for value, paths in description_groups.items():
    if not value or len(paths) == 1:
        continue
    for path in paths[1:]:
        html = path.read_text(errors="ignore")
        h1 = current_value(html, r"<h1\b[^>]*>(.*?)</h1>") or path.stem.replace("-", " ")
        replacement = trim_words(
            f"{h1}: {value.rstrip('.')}.", 160
        ).rstrip(" ,;:–—-") + "."
        html = set_meta(html, "description", replacement)
        html = set_meta(html, "og:description", replacement, True)
        html = set_meta(html, "twitter:description", replacement)
        path.write_text(html)

# Rebuild a clean sitemap from indexable canonical pages.
urls = []
for path in html_files:
    if path.name == "ui-kit.html":
        continue
    html = path.read_text(errors="ignore")
    robots = re.search(r"<meta\b(?=[^>]*name=[\"']robots[\"'])[^>]*content=[\"']([^\"']+)", html, re.I)
    if robots and "noindex" in robots.group(1).lower():
        continue
    canonical = re.search(r"<link\b(?=[^>]*rel=[\"']canonical[\"'])[^>]*href=[\"']([^\"']+)", html, re.I)
    if canonical and canonical.group(1).startswith(SITE):
        urls.append(canonical.group(1))

urls = list(dict.fromkeys(urls))
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += "\n".join(f"<url><loc>{escape(url)}</loc></url>" for url in urls)
sitemap += "\n</urlset>\n"
(ROOT / "sitemap.xml").write_text(sitemap)
(ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: https://wasser.market/sitemap.xml\n")

print(f"SEO finalized for {len(html_files)} pages; sitemap contains {len(urls)} unique indexable URLs")
