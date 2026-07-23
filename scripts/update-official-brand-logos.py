#!/usr/bin/env python3
"""Fetch official brand artwork and propagate it through static brand pages."""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LOGOS = {
    "aora": {
        "path": "assets/products/aora-gt600-umkehrosmose-wasserfilter-ohne-tank-1-57-l-min.webp",
        "source": "https://neueswasser.de/shop/umkehrosmoseanlage-aora-gt600-11471",
        "website": "https://neueswasser.de",
    },
    "happyfilter": {
        "path": "assets/brands/happyfilter.svg",
        "source": "https://happyfilter.de/media/a7/0d/fd/1762519196/Logo_HappyFilter.svg?ts=1762519196",
        "website": "https://happyfilter.de",
    },
    "osmotech": {
        "path": "assets/brands/osmotech.jpg",
        "source": "https://www.filterzentrale.com/media/87/02/80/1781682454/Banner%20Osmotech.jpg?1782213996",
        "website": "https://www.filterzentrale.com/UEber-uns/Marke-Osmotech/",
    },
    "rowa-4-you": {
        "path": "assets/brands/rowa-4-you.webp",
        "source": "https://www.wasserladen.de/cdn/shop/files/Select1025_MoodLogo.webp?crop=center&height=150&v=1774462998&width=150",
        "website": "https://www.wasserladen.de",
    },
    "sonvita": {
        "path": "assets/brands/sonvita.jpg",
        "source": "https://rdl-group.de/wp-content/uploads/2016/03/banner_sonvita-03-2016.jpg",
        "website": "https://rdl-group.de/marken/sonvita",
    },
    "sprudelux": {
        "path": "assets/brands/sprudelux.webp",
        "source": "https://sprudelux.berenshosting.de/web/image/website/2/logo?unique=738b1f1",
        "website": "https://sprudelux.de",
    },
    "wasserladen": {
        "path": "assets/brands/wasserladen.png",
        "source": "https://www.wasserladen.de/cdn/shop/files/WebLogo_grossesR.png?v=1784109131&width=500",
        "website": "https://www.wasserladen.de",
    },
    "stillundlaut": {
        "path": "assets/brands/stillundlaut.png",
        "source": "https://stillundlaut.de/web/image/website/2/social_default_image?unique=c3d04e8",
        "website": "https://stillundlaut.de",
    },
    "franke": {
        "path": "assets/brands/franke.svg",
        "source": "https://assets.franke.com/is/content/frankemanagement/franke-logo-footer-1",
        "website": "https://www.franke.com",
    },
    "blanco": {
        "path": "assets/brands/blanco.svg",
        "source": "https://www.blanco.de/_nuxt/logo-white.120..svg",
        "website": "https://www.blanco.de",
    },
}


def fetch(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        target.write_bytes(response.read())


def update_brand_directory(html: str, slug: str, logo: str) -> str:
    pattern = re.compile(
        rf'(<a class="brand-directory-card" href="brands/{re.escape(slug)}\.html".*?</a>)',
        re.DOTALL,
    )
    match = pattern.search(html)
    if not match:
        return html
    card = re.sub(r'(<div class="brand-logo-wrap"><img src=")[^"]+', rf"\g<1>{logo}", match.group(1), count=1)
    return html[: match.start()] + card + html[match.end() :]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()

    if args.fetch:
        for item in LOGOS.values():
            if item["path"].startswith("assets/brands/"):
                fetch(item["source"], ROOT / item["path"])

    brands_path = ROOT / "data" / "brands.json"
    brands = json.loads(brands_path.read_text())
    by_slug = {brand["slug"]: brand for brand in brands}
    directory_path = ROOT / "brands.html"
    directory = directory_path.read_text()

    for slug, item in LOGOS.items():
        brand = by_slug.get(slug)
        if not brand:
            continue
        old_logo = brand.get("logo", "")
        brand["logo"] = item["path"]
        brand["website"] = item["website"]

        page_path = ROOT / "brands" / f"{slug}.html"
        if page_path.exists():
            page = page_path.read_text()
            page = page.replace(f"../{old_logo}", f"../{item['path']}")
            page = re.sub(
                r'(<a[^>]+class="site-brand"[^>]*><img[^>]+src=")[^"]+',
                r"\g<1>../assets/img/wasser-market-logo.jpg",
                page,
                count=1,
            )
            page = re.sub(r"brand\.css\?v=[^\"]+", "brand.css?v=20260723-logos1", page)
            page = re.sub(
                r'(<a class="btn primary" href=")[^"]+(" target="_blank" rel="nofollow noopener">Offizielle Website)',
                rf"\g<1>{item['website']}\g<2>",
                page,
                count=1,
            )
            page_path.write_text(page)
        directory = update_brand_directory(directory, slug, item["path"])

    directory = re.sub(r"brand\.css\?v=[^\"]+", "brand.css?v=20260723-logos1", directory)
    brands_path.write_text(json.dumps(brands, ensure_ascii=False, indent=2) + "\n")
    directory_path.write_text(directory)
    (ROOT / "data" / "brand-logo-sources.json").write_text(
        json.dumps(LOGOS, ensure_ascii=False, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
