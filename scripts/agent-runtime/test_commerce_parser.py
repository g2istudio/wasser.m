import unittest

from bs4 import BeautifulSoup

from crawler.candidate_worker import _model_from_official_title
from crawler.page_collector import PageSnapshot
from extractor.commerce_parser import _specs, detect_platform


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


if __name__ == "__main__":
    unittest.main()
