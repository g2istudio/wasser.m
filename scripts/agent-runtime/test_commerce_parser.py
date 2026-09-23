import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

from crawler.candidate_worker import _model_from_official_title
from crawler.page_collector import PageSnapshot
from extractor.commerce_parser import _specs, detect_platform, extract_commerce_product


class CommerceParserTests(unittest.TestCase):
    def test_platform_detection(self):
        cases = {
            "shopify": '<script src="https://cdn.shopify.com/a.js"></script>',
            "woocommerce": '<body class="woocommerce single-product">',
            "shopware": '<meta name="application-name" content="Shopware 6">',
            "magento": '<script>window.mage-cache-storage={}</script>',
            "prestashop": '<meta name="generator" content="PrestaShop">',
            "bigcommerce": '<script src="stencil-utils.min.js"></script>',
            "generic-jsonld": '<script type="application/ld+json">{}</script>',
        }
        for expected, html in cases.items():
            self.assertEqual(detect_platform(html), expected)

    def test_indexes_bullet_separated_specs(self):
        soup = BeautifulSoup(
            "<p>Technische Daten: • Durchflussrate: 2,6 L/min • Maße: 15 × 43 × 43 cm</p>",
            "lxml",
        )
        specs = _specs(soup)
        self.assertEqual(specs["durchflussrate"][0], "2,6 L/min")
        self.assertEqual(specs["masse"][0], "15 × 43 × 43 cm")

    def test_uses_leading_official_title_identity(self):
        cases = {
            "SYDROS Pureflow RO-Tischwasserspender mit UV-C, H2 – Sydros": "Pureflow",
            "SYDROS RO 600 VITA – Tanklose 5-Stufen-Umkehrosmose – Sydros": "RO 600 VITA",
            "SYDROS RO 800 – Kompakte 6-Stufen-Umkehrosmose – Sydros": "RO 800",
        }
        for title, expected in cases.items():
            snapshot = PageSnapshot(url="https://www.sydros.de/products/example", title=title, visible_text="")
            self.assertEqual(_model_from_official_title(snapshot, "SYDROS", "H2"), expected)

    def test_extracts_gpd_from_nonstandard_spec_value_and_remineralization_title(self):
        html = """<html><head><title>AQUAPHOR PRO100 M mit Remineralisierung</title>
        <script type="application/ld+json">{"@type":"Product","name":"AQUAPHOR PRO100 M mit Remineralisierung","image":"https://example.com/pro100.jpg"}</script>
        </head><body><dl><dt>Filter PRO 100</dt><dd>100 GPD zur Entsalzung</dd></dl></body></html>"""
        snapshot = PageSnapshot(
            url="https://example.com/pro100-m",
            title="AQUAPHOR PRO100 M mit Remineralisierung",
            visible_text="AQUAPHOR PRO100 M mit Remineralisierung Filter PRO 100: 100 GPD zur Entsalzung",
            raw_content=html,
        )
        with patch("extractor.commerce_parser._official_manuals", return_value=[]):
            product, _, _ = extract_commerce_product(snapshot.url, "AQUAPHOR", "PRO100 M", snapshot=snapshot)
        self.assertEqual(product.performance.rated_capacity_gpd.value, 100)
        self.assertEqual(product.performance.rated_capacity_gpd.unit, "GPD")
        self.assertTrue(product.water_output.remineralization.value)

    def test_keeps_conflicting_page_and_manual_values(self):
        html = """<html><head><title>Example RO 1</title>
        <script type="application/ld+json">{"@type":"Product","name":"Example RO 1","image":"https://example.com/1.jpg"}</script>
        </head><body><dl><dt>Dimensions</dt><dd>15 x 43 x 43 cm</dd>
        <dt>Rated power</dt><dd>2200 W</dd></dl></body></html>"""
        snapshot = PageSnapshot(url="https://example.com/ro1", title="Example RO 1",
                                visible_text="Example RO 1 Dimensions 15 x 43 x 43 cm Rated power 2200 W",
                                raw_content=html)
        manual = "Dimensions 405 x 142 x 415 mm Nennleistung: 75 W"
        with patch("extractor.commerce_parser._official_manuals", return_value=[("https://example.com/manual.pdf", manual)]):
            product, _, _ = extract_commerce_product(snapshot.url, "Example", "RO1", snapshot=snapshot)
        names = {item.original_name for item in product.unmapped_attributes}
        self.assertIn("conflict.physical.dimensions_raw.page", names)
        self.assertIn("conflict.physical.dimensions_raw.manual", names)
        self.assertIn("conflict.electrical.maximum_power_w.page", names)
        self.assertIn("conflict.electrical.maximum_power_w.manual", names)
        self.assertIsNone(product.physical.dimensions_raw.value)
        self.assertIsNone(product.electrical.maximum_power_w.value)


if __name__ == "__main__":
    unittest.main()
