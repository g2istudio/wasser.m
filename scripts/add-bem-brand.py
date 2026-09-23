import json
import re
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
LOGO_URL = "https://www.bemshop.de/media/0b/95/91/1765990383/Logo%20Bem-Shop%20222x40px.png?ts=1765990383"
DESCRIPTION_DE = "Deutsche Marke für Auftisch- und Untertisch-Umkehrosmoseanlagen sowie Wasserstoffwasser-Systeme."
DESCRIPTION_EN = "German brand offering countertop and under-sink reverse-osmosis systems and hydrogen-water appliances."


def write_text(path: Path, value: str) -> None:
    path.write_text(value, encoding="utf-8")


def main() -> None:
    logo_path = ROOT / "assets" / "brands" / "bem.png"
    response = requests.get(LOGO_URL, headers={"User-Agent": "WasserMarketAgent/0.1"}, timeout=30)
    response.raise_for_status()
    if not response.headers.get("Content-Type", "").startswith("image/"):
        raise RuntimeError("BEM logo response is not an image")
    logo_path.write_bytes(response.content)

    brands_path = ROOT / "data" / "brands.json"
    brands = json.loads(brands_path.read_text(encoding="utf-8"))
    record = next((item for item in brands if item.get("slug") == "bem"), None)
    payload = {
        "slug": "bem",
        "name": "BEM",
        "country": "Germany",
        "founded": None,
        "website": "https://www.bemshop.de",
        "group": "Reverse Osmosis",
        "description_de": DESCRIPTION_DE,
        "description_en": DESCRIPTION_EN,
        "products_count": 0,
        "rating": None,
        "logo": "assets/brands/bem.png",
        "description": DESCRIPTION_DE,
    }
    if record is None:
        brands.append(payload)
    else:
        record.update(payload)
    write_text(brands_path, json.dumps(brands, ensure_ascii=False, indent=2) + "\n")

    sources_path = ROOT / "data" / "brand-logo-sources.json"
    sources = json.loads(sources_path.read_text(encoding="utf-8"))
    sources["bem"] = {
        "path": "assets/brands/bem.png",
        "source": LOGO_URL,
        "website": "https://www.bemshop.de",
    }
    write_text(sources_path, json.dumps(sources, ensure_ascii=False, indent=2) + "\n")

    template = (ROOT / "brands" / "gewapur.html").read_text(encoding="utf-8")
    page = template.replace("Gewapur", "BEM").replace("gewapur", "bem")
    page = page.replace(
        "Anbieter von Direct-Flow-Wasserfiltersystemen und Umkehrosmoseanlagen.",
        DESCRIPTION_DE,
    )
    page = page.replace("https://bem.de", "https://www.bemshop.de")
    page = re.sub(r"(<dt>Modelle</dt><dd>)\d+(</dd>)", r"\g<1>0\2", page)
    page = re.sub(
        r'<section class="panel"><h2>Produkte in der Datenbank</h2>.*?</section>',
        '<section class="panel"><h2>Produkte in der Datenbank</h2><div class="product-grid"></div></section>',
        page,
        flags=re.S,
    )
    write_text(ROOT / "brands" / "bem.html", page)

    directory_path = ROOT / "brands.html"
    directory = directory_path.read_text(encoding="utf-8")
    if 'href="/brands/bem"' not in directory:
        card = (
            '<a class="brand-directory-card" href="/brands/bem" data-brand-name="bem" '
            'data-brand-country="germany"><div class="brand-logo-wrap"><img '
            'src="/assets/brands/bem.png" alt="BEM Logo" loading="lazy"></div><div '
            'class="brand-card-body"><span class="badge">Reverse Osmosis</span><h3>BEM</h3>'
            f'<p>{DESCRIPTION_DE}</p><span class="brand-meta">Germany · 0 Modelle</span>'
            '<span class="brand-link">Profil ansehen →</span></div></a>'
        )
        directory = directory.replace(
            '<div class="brand-directory-grid" id="brandDirectoryGrid">',
            '<div class="brand-directory-grid" id="brandDirectoryGrid">' + card,
            1,
        )
        write_text(directory_path, directory)

    print({"brand": "BEM", "logo_bytes": logo_path.stat().st_size, "brand_page": "brands/bem.html"})


if __name__ == "__main__":
    main()
