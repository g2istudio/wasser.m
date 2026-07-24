#!/usr/bin/env python3
"""Ensure product pages have a useful, non-stuffed semantic heading hierarchy."""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def esc(value):
    return html.escape(str(value or ""), quote=True)


def slug_for(product):
    if product.get("slug"):
        return product["slug"]
    return (product.get("url") or "").removeprefix("products/").removesuffix(".html")


def specs_for(product):
    specs = product.get("specs") or product.get("specifications") or {}
    return [(str(key).replace("_", " "), str(value)) for key, value in specs.items()]


def main():
    products = json.loads((ROOT / "data/products.json").read_text())
    changed = 0

    for product in products:
        slug = slug_for(product)
        page = ROOT / "products" / f"{slug}.html"
        if not slug or not page.exists():
            continue

        source = page.read_text()
        h2_count = len(re.findall(r"<h2\b", source, re.I))
        h3_count = len(re.findall(r"<h3\b", source, re.I))
        if h2_count >= 3 and h3_count >= 1:
            continue

        brand = product.get("brand") or "Hersteller"
        name = product.get("name") or slug.replace("-", " ").title()
        category = product.get("category") or "Wasseraufbereitungssystem"
        specs = specs_for(product)
        highlights = "; ".join(f"{key}: {value}" for key, value in specs[:3])
        if not highlights:
            highlights = "Leistung, Filtertechnik, Abmessungen und Wartungsbedarf"

        section = (
            f'<section class="product-seo-guide" aria-labelledby="product-guide-{esc(slug)}">'
            f'<h2 id="product-guide-{esc(slug)}">{esc(brand)} {esc(name)}: Einsatz und Auswahl</h2>'
            f'<h3>Für welche Anwendung ist das Modell gedacht?</h3>'
            f'<p>{esc(name)} gehört zur Produktkategorie {esc(category)}. '
            f'Die Einordnung hilft dabei, das Modell mit technisch ähnlichen Wasserfiltern '
            f'und Wasseraufbereitungssystemen zu vergleichen.</p>'
            f'<h3>Welche technischen Angaben sind besonders wichtig?</h3>'
            f'<p>Für den direkten Produktvergleich sind insbesondere folgende Herstellerangaben relevant: '
            f'{esc(highlights)}. Die Werte sollten immer zusammen mit Wasserqualität, verfügbarem Platz, '
            f'Anschlussbedingungen und gewünschter Ausgabemenge bewertet werden.</p>'
            f'<h3>Was sollte vor der Auswahl geprüft werden?</h3>'
            f'<p>Vor der Entscheidung sollten Installationsart, Filterwechsel, laufende Kosten, '
            f'Ersatzteilversorgung und die Eignung für die örtliche Wasseranalyse geprüft werden. '
            f'Die verlinkte Herstellerquelle enthält die jeweils aktuellen Varianten und Hinweise.</p>'
            f'</section>'
        )

        marker = "</section><aside>"
        if marker in source:
            source = source.replace(marker, section + marker, 1)
        elif '</section><section class="panel product-knowledge-links">' in source:
            source = source.replace('</section><section class="panel product-knowledge-links">', section + '</section><section class="panel product-knowledge-links">', 1)
        else:
            print(f"skip (layout marker missing): {page}")
            continue
        page.write_text(source)
        changed += 1

    print(f"Updated semantic heading structure on {changed} product pages")


if __name__ == "__main__":
    main()
