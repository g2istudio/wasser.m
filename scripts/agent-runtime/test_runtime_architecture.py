import tempfile
import unittest
from pathlib import Path

from database.repository import ProductRepository, canonical_product_id, canonicalize_url
from crawler.page_collector import PageSnapshot
from extractor.commerce_parser import extract_commerce_product
from extractor.publication import assess_publication
from extractor.validation import _evidence_in_text
from models.product import Evidence, ProductValue, UnmappedAttribute, WaterFilterProduct
from provenance import persist_product_facts
from runtime_control import BudgetExceeded, Budgets, RuntimeMeter, calculated_confidence
from semantic_resolution import minimal_fragments
from sources.wasser_market_api import WasserMarketApiClient


class RuntimeArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.repository = ProductRepository(Path(self.temp.name) / "agent.db")

    def tearDown(self):
        self.temp.cleanup()

    def test_canonical_identity_normalizes_model_spelling(self):
        ids = {
            canonical_product_id("Waterdrop", "G3P800"),
            canonical_product_id("Waterdrop", "G3 P800"),
            canonical_product_id("Waterdrop", "G3-P800"),
        }
        self.assertEqual(ids, {"waterdrop:g3p800"})
        self.assertNotEqual(
            canonical_product_id("Waterdrop", "G3P800", "EU 220V"),
            canonical_product_id("Waterdrop", "G3P800", "US 110V"),
        )
        self.assertEqual(canonical_product_id("Grünbeck", "X 1"), "grunbeck:x1")

    def test_url_and_snapshot_deduplication(self):
        self.assertEqual(
            canonicalize_url("https://www.example.com/product/?utm_source=x&a=1"),
            "https://example.com/product?a=1",
        )
        first, created = self.repository.save_snapshot("https://example.com/product", "same")
        second, repeated = self.repository.save_snapshot("https://www.example.com/product/", "same")
        self.assertTrue(created)
        self.assertFalse(repeated)
        self.assertEqual(first, second)

    def test_budget_stops_without_losing_job(self):
        budgets = Budgets(max_brave_queries=1)
        job = self.repository.start_job("test", {}, budgets.to_dict())
        meter = RuntimeMeter(self.repository, job, budgets)
        meter.consume("brave", "queries")
        with self.assertRaises(BudgetExceeded):
            meter.consume("brave", "queries")
        self.assertEqual(self.repository.usage_totals(job)[0]["amount"], 1)

    def test_facts_and_unmapped_attributes_keep_evidence(self):
        product = WaterFilterProduct()
        product.identity.brand = ProductValue(
            value="Example",
            evidence=[Evidence(source_url="https://example.com/p", original_text="Brand: Example",
                               verification_status="official_specification")],
        )
        product.unmapped_attributes.append(UnmappedAttribute(
            original_name="Electropositive media",
            value="enabled",
            source_url="https://example.com/p",
            evidence="Electropositive media: enabled",
            extraction_method="html",
            confidence=0.9,
        ))
        product_id = self.repository.upsert_canonical_product("Example", "X1")
        self.assertEqual(persist_product_facts(self.repository, product_id, product), 1)
        with self.repository._connect() as connection:
            fact = connection.execute("SELECT evidence FROM facts").fetchone()
            unknown = connection.execute("SELECT original_name FROM unmapped_attributes").fetchone()
        self.assertEqual(fact["evidence"], "Brand: Example")
        self.assertEqual(unknown["original_name"], "Electropositive media")

    def test_confidence_is_deterministic_and_penalizes_conflict(self):
        clean = calculated_confidence(source_type="manufacturer_page", exact_model_match=True,
                                      verbatim_evidence=True, conflicting=False, extraction_method="html")
        conflict = calculated_confidence(source_type="manufacturer_page", exact_model_match=True,
                                         verbatim_evidence=True, conflicting=True, extraction_method="gemini")
        self.assertGreater(clean, conflict)

    def test_semantic_context_is_small_and_relevant(self):
        text = "noise\n" * 10000 + "G3P800 pure water flow 2.1 L/min\nDimensions 45 x 15 x 40 cm"
        selected = minimal_fragments(text, "G3P800", ["flow rate"], max_chars=500)
        self.assertLessEqual(len(selected), 500)
        self.assertIn("2.1 L/min", selected)

    def test_unknown_specification_is_preserved(self):
        html = """<html><head><title>Example X1 water filter</title>
        <script type="application/ld+json">{"@type":"Product","name":"Example X1","image":"https://example.com/x1.jpg"}</script>
        </head><body><h1>Example X1</h1><dl>
        <dt>Electropositive media</dt><dd>Enabled</dd>
        <dt>Dimensions</dt><dd>10 x 20 x 30 cm</dd>
        </dl></body></html>"""
        snapshot = PageSnapshot(url="https://example.com/x1", title="Example X1 water filter",
                                visible_text="Example X1 Electropositive media Enabled Dimensions 10 x 20 x 30 cm",
                                raw_content=html)
        product, _, _ = extract_commerce_product(snapshot.url, "Example", "X1", snapshot=snapshot)
        self.assertEqual(product.unmapped_attributes[0].original_name, "electropositive media")
        self.assertEqual(product.unmapped_attributes[0].value, "Enabled")

    def test_protected_api_signature_is_repeatable(self):
        client = WasserMarketApiClient("https://wasser.market/api", "key", "secret")
        first = client.signed_headers(b"{}", "example:x1:2", timestamp="1", nonce="n")
        second = client.signed_headers(b"{}", "example:x1:2", timestamp="1", nonce="n")
        self.assertEqual(first["X-Wasser-Signature"], second["X-Wasser-Signature"])
        self.assertEqual(first["Idempotency-Key"], "example:x1:2")

    def test_missing_characteristics_do_not_block_publication(self):
        product = WaterFilterProduct()
        product.identity.brand.value = "Example"
        product.identity.model.value = "RO100"
        product.identity.product_name.value = "Example RO100 reverse osmosis system"
        product.system.technology.value = "Reverse Osmosis"
        product.image.url = "https://example.com/ro100.jpg"
        product.images = [product.image]
        product.sources.manufacturer_url = "https://example.com/ro100"
        assessment = assess_publication(product)
        self.assertTrue(assessment.ready)
        self.assertIn("system.installation_type", assessment.missing)
        self.assertIn("filtration.advertised_stage_count", assessment.missing)
        self.assertEqual(assessment.blocking, [])

    def test_evidence_matching_ignores_html_layout_whitespace(self):
        self.assertTrue(_evidence_in_text(
            "37,00 × 37,00 × 33,00 cm",
            "37,00 ×\n                  37,00 ×\n33,00 cm",
        ))


if __name__ == "__main__":
    unittest.main()
