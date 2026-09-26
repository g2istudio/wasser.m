import json
import re
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
LOGO_URL = "https://nuaquasystems.com/cdn/shop/files/nu_aqua_logo_transparent_195x@2x.png?v=1683309062"
DESCRIPTION_DE = "US-amerikanische Marke für Umkehrosmose-, RODI- und Wasserfiltersysteme."
DESCRIPTION_EN = "US brand offering reverse-osmosis, RODI, and water-filtration systems."


def write_text(path: Path, value: str) -> None:
    path.write_text(value, encoding="utf-8")


def main() -> None:
    logo_path = ROOT / "assets" / "brands" / "nu-aqua.png"
    response = requests.get(LOGO_URL, headers={"User-Agent": "WasserMarketAgent/0.1"}, timeout=30)
    response.raise_for_status()
    if not response.headers.get("Content-Type", "").startswith("image/"):
        raise RuntimeError("NU Aqua logo response is not an image")
    logo_path.write_bytes(response.content)

    brands_path = ROOT / "data" / "brands.json"
    brands = json.loads(brands_path.read_text(encoding="utf-8"))
    payload = {
        "slug": "nu-aqua",
        "name": "NU Aqua",
        "country": "United States",
        "founded": None,
        "website": "https://nuaquasystems.com",
        "group": "Reverse Osmosis",
        "description_de": DESCRIPTION_DE,
        "description_en": DESCRIPTION_EN,
        "products_count": 0,
        "rating": None,
        "logo": "assets/brands/nu-aqua.png",
        "description": DESCRIPTION_DE,
    }
    record = next((item for item in brands if item.get("slug") == "nu-aqua"), None)
    if record is None:
        brands.append(payload)
    else:
        record.update(payload)
    write_text(brands_path, json.dumps(brands, ensure_ascii=False, indent=2) + "\n")

    sources_path = ROOT / "data" / "brand-logo-sources.json"
    sources = json.loads(sources_path.read_text(encoding="utf-8"))
    sources["nu-aqua"] = {
        "path": "assets/brands/nu-aqua.png",
        "source": LOGO_URL,
        "website": "https://nuaquasystems.com",
    }
    write_text(sources_path, json.dumps(sources, ensure_ascii=False, indent=2) + "\n")

    template = (ROOT / "brands" / "aquatru.html").read_text(encoding="utf-8")
    page = template.replace("AquaTru", "NU Aqua").replace("aquatru", "nu-aqua")
    page = page.replace("https://nu-aquawater.com", "https://nuaquasystems.com")
    page = page.replace(
        "Marke für einfach installierbare Auftisch-Umkehrosmosegeräte.",
        DESCRIPTION_DE,
    )
    page = re.sub(r"(<dt>Modelle</dt><dd>)\d+(</dd>)", r"\g<1>0\2", page)
    page = re.sub(
        r'<section class="panel"><h2>Produkte in der Datenbank</h2>.*?</section>',
        '<section class="panel"><h2>Produkte in der Datenbank</h2><div class="product-grid"></div></section>',
        page,
        flags=re.S,
    )
    write_text(ROOT / "brands" / "nu-aqua.html", page)

    directory_path = ROOT / "brands.html"
    directory = directory_path.read_text(encoding="utf-8")
    if 'href="/brands/nu-aqua"' not in directory:
        card = (
            '<a class="brand-directory-card" href="/brands/nu-aqua" data-brand-name="nu aqua" '
            'data-brand-country="united states"><div class="brand-logo-wrap"><img '
            'src="/assets/brands/nu-aqua.png" alt="NU Aqua Logo" loading="lazy"></div><div '
            'class="brand-card-body"><span class="badge">Reverse Osmosis</span><h3>NU Aqua</h3>'
            f'<p>{DESCRIPTION_DE}</p><span class="brand-meta">United States · 0 Modelle</span>'
            '<span class="brand-link">Profil ansehen →</span></div></a>'
        )
        directory = directory.replace(
            '<div class="brand-directory-grid" id="brandDirectoryGrid">',
            '<div class="brand-directory-grid" id="brandDirectoryGrid">' + card,
            1,
        )
        write_text(directory_path, directory)

    print(json.dumps({"brand": "NU Aqua", "logo_bytes": logo_path.stat().st_size}))


if __name__ == "__main__":
    main()
