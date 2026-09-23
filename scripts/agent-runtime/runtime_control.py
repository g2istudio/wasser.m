"""Budgets, provenance helpers and deterministic runtime accounting."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from time import monotonic
from typing import Any


class BudgetExceeded(RuntimeError):
    pass


@dataclass(frozen=True)
class Budgets:
    max_brave_queries: int = 10
    max_http_requests: int = 100
    max_firecrawl_credits: int = 20
    max_gemini_tokens: int = 50_000
    max_products: int = 25
    max_runtime_seconds: int = 1800

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


class RuntimeMeter:
    """Fail-closed accounting shared by all stages of one job."""

    LIMITS = {
        ("brave", "queries"): "max_brave_queries",
        ("http", "requests"): "max_http_requests",
        ("firecrawl", "credits"): "max_firecrawl_credits",
        ("gemini", "tokens"): "max_gemini_tokens",
        ("pipeline", "products"): "max_products",
    }

    def __init__(self, repository, job_id: str, budgets: Budgets):
        self.repository = repository
        self.job_id = job_id
        self.budgets = budgets
        self.started = monotonic()
        self.totals: dict[tuple[str, str], float] = {}

    def check_runtime(self) -> None:
        elapsed = monotonic() - self.started
        if elapsed > self.budgets.max_runtime_seconds:
            raise BudgetExceeded(
                f"Runtime budget exceeded: {elapsed:.1f}s > {self.budgets.max_runtime_seconds}s"
            )

    def consume(self, provider: str, metric: str, amount: float = 1,
                product_id: str | None = None, metadata: dict[str, Any] | None = None) -> None:
        self.check_runtime()
        key = (provider, metric)
        total = self.totals.get(key, 0) + amount
        limit_name = self.LIMITS.get(key)
        if limit_name and total > getattr(self.budgets, limit_name):
            raise BudgetExceeded(
                f"Budget exceeded for {provider}.{metric}: {total:g} > {getattr(self.budgets, limit_name):g}"
            )
        self.totals[key] = total
        self.repository.record_usage(
            self.job_id, product_id, provider, metric, amount, metadata or {}
        )

    def event(self, event_type: str, stage: str, product_id: str | None = None,
              detail: dict[str, Any] | None = None) -> None:
        self.repository.audit(self.job_id, product_id, event_type, stage, detail or {})


SOURCE_PRIORITY = {
    "official_product_page": 10,
    "manufacturer_page": 10,
    "manufacturer_datasheet": 20,
    "manual": 20,
    "certification_database": 30,
    "laboratory_report": 30,
    "authorized_retailer": 40,
    "retailer": 50,
    "other": 100,
}


def source_priority(source_type: str) -> int:
    return SOURCE_PRIORITY.get(source_type, 100)


def calculated_confidence(*, source_type: str, exact_model_match: bool,
                          verbatim_evidence: bool, conflicting: bool,
                          extraction_method: str) -> float:
    """Deterministic confidence; never trusts a model's self-reported score."""
    score = 1.0 - min(source_priority(source_type), 100) / 250
    if exact_model_match:
        score += 0.08
    if verbatim_evidence:
        score += 0.05
    if extraction_method == "gemini":
        score -= 0.12
    if conflicting:
        score -= 0.45
    return round(max(0.0, min(1.0, score)), 3)
