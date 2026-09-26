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

    def test_stage_evidence_uses_verbatim_page_punctuation(self):
        html = """<html><head><title>AquaTru Carafe</title><meta name="description" content="4-stage reverse osmosis filtration">
        <script type="application/ld+json">{"@type":"Product","name":"AquaTru Carafe","image":"https://example.com/carafe.jpg"}</script>
        </head><body><p>AquaTru Carafe with 4-stage reverse osmosis filtration.</p></body></html>"""
        snapshot = PageSnapshot(
            url="https://example.com/carafe", title="AquaTru Carafe",
            visible_text="AquaTru Carafe with 4-stage reverse osmosis filtration.", raw_content=html,
        )
        with patch("extractor.commerce_parser._official_manuals", return_value=[]):
            product, _, _ = extract_commerce_product(snapshot.url, "AquaTru", "Carafe", snapshot=snapshot)
        evidence = product.filtration.advertised_stage_count.evidence[0].original_text
        self.assertEqual(evidence, "4-stage")

    def test_uses_product_page_title_when_jsonld_selects_a_filter_variant(self):
        html = """<html><head><title>AquaTru Carafe | Countertop RO Water Purifier</title>
        <meta name="description" content="Compact 4 stage RO filtration">
        <script type="application/ld+json">{"@type":"Product","name":"AquaTru Carafe - Carafe / VOC Carbon Filter","image":"https://example.com/carafe.jpg","description":"Compact 4 stage RO filtration"}</script>
        </head><body><h1>AquaTru Carafe</h1><p>4-stage Ultra Reverse Osmosis filtration</p></body></html>"""
        snapshot = PageSnapshot(url="https://example.com/carafe", title="", visible_text="", raw_content=html)
        with patch("extractor.commerce_parser._official_manuals", return_value=[]):
            product, _, _ = extract_commerce_product(snapshot.url, "AquaTru", "Carafe Countertop", snapshot=snapshot)
        self.assertEqual(product.identity.product_name.value, "AquaTru Carafe | Countertop RO Water Purifier")
        self.assertEqual(product.system.technology.value, "Reverse Osmosis")

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

    def test_liter_capacity_is_not_parsed_as_electrical_power(self):
        html = """<html><head><title>Example RO5 Umkehrosmose</title>
        <script type="application/ld+json">{"@type":"Product","name":"Example RO5","image":"https://example.com/ro5.jpg"}</script>
        </head><body><dl><dt>Leistung</dt><dd>280 Liter pro Tag</dd></dl></body></html>"""
        snapshot = PageSnapshot(
            url="https://example.com/ro5", title="Example RO5 Umkehrosmose",
            visible_text="Example RO5 Umkehrosmose Leistung 280 Liter pro Tag", raw_content=html,
        )
        with patch("extractor.commerce_parser._official_manuals", return_value=[]):
            product, _, _ = extract_commerce_product(snapshot.url, "Example", "RO5", snapshot=snapshot)
        self.assertIsNone(product.electrical.maximum_power_w.value)

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

    def test_extracts_generic_operating_specs_from_official_manual(self):
        html = """<html><head><title>Example PD1200 Tankless Reverse Osmosis</title>
        <script type="application/ld+json">{"@type":"Product","name":"Example PD1200 Tankless Reverse Osmosis","description":"11-stage 1200 GPD under-sink reverse osmosis system.","image":"https://example.com/pd1200.jpg"}</script>
        </head><body><p>11-stage 1200 GPD under-sink reverse osmosis system.</p></body></html>"""
        snapshot = PageSnapshot(
            url="https://example.com/pd1200", title="Example PD1200 Tankless Reverse Osmosis",
            visible_text="Example PD1200 11-stage 1200 GPD under-sink reverse osmosis system.",
            raw_content=html,
        )
        manual = """Min.39ºF,Max 100ºF 110-240VAC 150W Rated Power 50-60HZ
        Rated flow 0.83 gallons/m @25 C Min.20psi Max. 80psi Municipal water
        1st stage PPC filter 2nd stage RO membrane 3rd stage TC filter
        Smart RO Faucet Filter Life Indicator automatically flushed for 30 seconds
        Leakage detection system The system tests the TDS and displays it on the faucet screen
        TDS removing rate for PD1200 is about 94-95%
        ONE YEAR LIMITED FRIZZLIFE WARRANTY tankless RO system"""
        with patch("extractor.commerce_parser._official_manuals", return_value=[("https://example.com/manual.pdf", manual)]):
            product, _, _ = extract_commerce_product(snapshot.url, "Example", "PD1200", snapshot=snapshot)
        self.assertEqual(product.filtration.advertised_stage_count.value, 11)
        self.assertEqual(product.filtration.physical_filter_count.value, 3)
        self.assertAlmostEqual(product.performance.dispensing_flow_lpm.value, 3.142, places=3)
        self.assertEqual(product.performance.minimum_inlet_pressure.value, 20)
        self.assertEqual(product.performance.maximum_inlet_pressure.value, 80)
        self.assertEqual(product.performance.minimum_feed_temperature.value, 39)
        self.assertEqual(product.performance.maximum_feed_temperature.value, 100)
        self.assertEqual(product.electrical.maximum_power_w.value, 150)
        self.assertEqual(product.electrical.voltage.value, "110-240VAC")
        self.assertEqual(product.electrical.frequency_hz.value, "50-60")
        self.assertTrue(product.system.tankless.value)
        self.assertTrue(product.smart_features.smart_faucet.value)
        self.assertTrue(product.smart_features.filter_life_indicator.value)
        self.assertTrue(product.smart_features.outlet_tds_display.value)
        self.assertTrue(product.protection.automatic_flush.value)
        self.assertTrue(product.protection.leak_detection.value)
        self.assertEqual(product.performance.tds_reduction_percent.value, "94–95")
        self.assertEqual(product.commercial.warranty_years.value, 1)

    def test_does_not_treat_tds_faq_question_as_a_display(self):
        html = """<html><head><title>Example PX500-A Reverse Osmosis</title>
        <script type="application/ld+json">{"@type":"Product","name":"Example PX500-A","image":"https://example.com/px500.jpg"}</script>
        </head><body><p>Reverse osmosis system.</p></body></html>"""
        snapshot = PageSnapshot(
            url="https://example.com/px500-a", title="Example PX500-A Reverse Osmosis",
            visible_text="Example PX500-A Reverse osmosis system.", raw_content=html,
        )
        manual = "Why out TDS value of PX500-A is higher than normal RO system? Filter Life Indicator display."
        with patch("extractor.commerce_parser._official_manuals", return_value=[("https://example.com/manual.pdf", manual)]):
            product, _, _ = extract_commerce_product(snapshot.url, "Example", "PX500-A", snapshot=snapshot)
        self.assertIsNone(product.smart_features.outlet_tds_display.value)


if __name__ == "__main__":
    unittest.main()
