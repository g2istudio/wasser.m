import tempfile
import unittest
from pathlib import Path

from wasser_agent import parser as agent_parser
from wasser_panel import PanelStore, TaskRunner, product_summaries, valid_product_url
from database.repository import ProductRepository
from models.product import ProductRecord, WaterFilterProduct


class PanelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.root = Path(self.temp.name)
        self.store = PanelStore(self.root / "panel.db")

    def tearDown(self):
        self.temp.cleanup()

    def test_accepts_only_https_product_urls(self):
        self.assertTrue(valid_product_url("https://example.com/products/x1"))
        self.assertFalse(valid_product_url("http://example.com/products/x1"))
        self.assertFalse(valid_product_url("file:///secret"))
        self.assertFalse(valid_product_url("https://user:password@example.com/x1"))

    def test_queue_survives_restart_and_failed_task_can_retry(self):
        task_id = self.store.enqueue("process_url", {"url": "https://example.com/x1"})
        task = self.store.next_task()
        self.assertEqual(task["id"], task_id)
        self.assertEqual(task["status"], "RUNNING")
        restarted = PanelStore(self.root / "panel.db")
        self.assertEqual(restarted.list()[0]["status"], "QUEUED")
        task = restarted.next_task()
        restarted.finish(task["id"], error="test error")
        self.assertTrue(restarted.retry(task_id))
        self.assertEqual(restarted.list()[0]["status"], "QUEUED")

    def test_completed_task_exposes_pipeline_outcome(self):
        task_id = self.store.enqueue("process_url", {"url": "https://example.com/x1"})
        self.store.next_task()
        self.store.finish(task_id, result={
            "result": {"status": "SKIPPED", "detail": "Already exists on Wasser.Market"}
        })
        item = self.store.list()[0]
        self.assertEqual(item["status"], "COMPLETED")
        self.assertEqual(item["outcome_status"], "SKIPPED")
        self.assertIn("Already exists", item["outcome_detail"])

    def test_runner_builds_argument_list_without_shell(self):
        runner = TaskRunner(self.store, self.root / "agent.db", self.root / "site")
        task = {
            "kind": "process_url",
            "payload": {
                "url": "https://example.com/products/x1",
                "brand": "Example", "model": "X1", "force": False,
                "allow_gemini": False,
                "budgets": {
                    "max_brave_queries": 1, "max_http_requests": 5,
                    "max_firecrawl_credits": 1, "max_gemini_tokens": 1000,
                    "max_runtime": 60,
                },
            },
        }
        command, timeout = runner.command(task)
        self.assertIn("process-url", command)
        self.assertIn("--no-allow-gemini", command)
        self.assertIn("https://example.com/products/x1", command)
        self.assertEqual(timeout, 150)

    def test_cli_keeps_old_process_command_and_adds_direct_url(self):
        old = agent_parser().parse_args(["process", "--brand", "Example", "--model", "X1"])
        direct = agent_parser().parse_args(["process-url", "--url", "https://example.com/x1"])
        self.assertEqual(old.command, "process")
        self.assertEqual(direct.command, "process-url")

    def test_product_summary_works_with_real_product_row(self):
        db = self.root / "agent.db"
        repository = ProductRepository(db)
        product = WaterFilterProduct()
        product.identity.brand.value = "Example"
        product.identity.model.value = "X1"
        product.sources.manufacturer_url = "https://example.com/x1"
        repository.save(ProductRecord(
            product=product, status="NEEDS_REVIEW", needs_review=True, source_conflict=True
        ))
        site = self.root / "site"
        (site / "data").mkdir(parents=True)
        (site / "data" / "products.json").write_text(
            '[{"brand":"Example","name":"X1","slug":"example-x1"}]', encoding="utf-8"
        )
        summaries = product_summaries(db, site)
        self.assertEqual(summaries[0]["brand"], "Example")
        self.assertTrue(summaries[0]["updated_at"])
        self.assertTrue(summaries[0]["published"])
        self.assertEqual(summaries[0]["published_slug"], "example-x1")
        self.assertFalse(summaries[0]["source_conflict"])


if __name__ == "__main__":
    unittest.main()
