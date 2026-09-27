import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("agent-auto-import.py")
SPEC = importlib.util.spec_from_file_location("agent_auto_import", SCRIPT)
IMPORTER = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(IMPORTER)


def evidenced(value, source):
    return {
        "value": value,
        "verification_status": "official_specification",
        "evidence": [{
            "source_url": source,
            "source_type": "manufacturer_page",
            "original_text": value,
            "verification_status": "official_specification",
        }],
    }


class BrandBootstrapTests(unittest.TestCase):
    def setUp(self):
        self.original_root = IMPORTER.ROOT
        self.temp = tempfile.TemporaryDirectory()
        IMPORTER.ROOT = Path(self.temp.name)
        (IMPORTER.ROOT / "brands").mkdir()
        self.source = "https://manufacturer.example/products/model-1"
        self.product = {
            "identity": {
                "manufacturer_name": evidenced("Example", self.source),
                "brand_logo": {
                    "url": "https://cdn.example/logo.png",
                    "source_url": self.source,
                    "role": "brand_logo",
                    "product_model": "Model 1",
                },
            },
        }

    def tearDown(self):
        IMPORTER.ROOT = self.original_root
        self.temp.cleanup()

    def test_prepares_new_brand_without_writing_files(self):
        brands = []
        record, created = IMPORTER.brand_profile(
            self.product, "Example", "Model 1", self.source, brands
        )
        self.assertTrue(created)
        self.assertEqual(record["slug"], "example")
        self.assertEqual(record["logo"], "https://cdn.example/logo.png")
        self.assertEqual(len(brands), 1)
        self.assertFalse((IMPORTER.ROOT / "brands" / "example.html").exists())

    def test_rejects_brand_without_matching_manufacturer_evidence(self):
        self.product["identity"]["manufacturer_name"] = evidenced("Another", self.source)
        with self.assertRaisesRegex(ValueError, "matching manufacturer evidence"):
            IMPORTER.brand_profile(self.product, "Example", "Model 1", self.source, [])

    def test_rejects_logo_from_unrelated_source(self):
        self.product["identity"]["brand_logo"]["source_url"] = "https://unrelated.example/page"
        with self.assertRaisesRegex(ValueError, "official HTTPS logo"):
            IMPORTER.brand_profile(self.product, "Example", "Model 1", self.source, [])


if __name__ == "__main__":
    unittest.main()
