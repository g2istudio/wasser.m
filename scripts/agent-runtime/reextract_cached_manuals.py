"""Re-run deterministic extraction from cached product pages and manuals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from unittest.mock import patch

from crawler.page_collector import PageSnapshot
from database.repository import ProductRepository
from extractor.commerce_parser import extract_commerce_product
from extractor.publication import assess_publication
from extractor.validation import validate_product
from models.product import ProductRecord, WaterFilterProduct
from provenance import persist_product_facts


def populated_fact_count(product: WaterFilterProduct) -> int:
    count = 0

    def visit(value: object) -> None:
        nonlocal count
        if isinstance(value, dict):
            if {"value", "evidence", "verification_status"}.issubset(value):
                count += int(value.get("value") is not None)
                return
            for key, item in value.items():
                if key not in {"calculated", "unmapped_attributes"}:
                    visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    visit(product.model_dump(mode="json"))
    return count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--brand", required=True)
    parser.add_argument("--models", nargs="+", required=True)
    args = parser.parse_args()

    repository = ProductRepository(args.db)
    wanted = {model.casefold() for model in args.models}
    results = []
    for row in repository.product_rows(args.brand):
        if row["model"].casefold() not in wanted:
            continue
        current = WaterFilterProduct.model_validate_json(row["product_json"])
        source = repository.latest_snapshot(row["source_url"])
        if not source:
            results.append({"model": row["model"], "status": "NO_PRODUCT_SNAPSHOT"})
            continue
        manuals = []
        for url in current.sources.additional_urls:
            if ".pdf" not in url.casefold():
                continue
            snapshot = repository.latest_snapshot(url)
            if snapshot and snapshot.get("normalized_content"):
                manuals.append((url, snapshot["normalized_content"]))
        page = PageSnapshot(
            url=row["source_url"],
            title="",
            visible_text=source["normalized_content"],
            raw_content=source["raw_content"],
            fetch_method="cache",
            http_metadata=json.loads(source.get("http_metadata_json") or "{}"),
        )
        with patch("extractor.commerce_parser._official_manuals", return_value=manuals):
            product, combined, platform = extract_commerce_product(
                row["source_url"], row["brand"], row["model"], snapshot=page
            )
        product.schema_version = current.schema_version
        product.taxonomy = current.taxonomy
        product.canonical_product_id = current.canonical_product_id
        report = validate_product(product, combined.evidence_text, row["source_url"])
        publication = assess_publication(product)
        status = (
            "PUBLISH_READY"
            if report.valid and publication.ready and product.taxonomy != "UNKNOWN/NEW_TYPE"
            else "NEEDS_REVIEW"
        )
        product_id = repository.upsert_canonical_product(
            row["brand"], row["model"], taxonomy=product.taxonomy,
            status=status, schema_version=product.schema_version,
        )
        product.canonical_product_id = product_id
        repository.save(ProductRecord(
            product=product,
            status=status,
            needs_review=status == "NEEDS_REVIEW",
            source_conflict=False,
        ))
        facts = persist_product_facts(repository, product_id, product, platform)
        results.append({
            "model": row["model"],
            "status": status,
            "manuals": len(manuals),
            "facts": populated_fact_count(product),
            "evidence_records": report.evidence_records,
            "validation_errors": report.errors,
            "missing": publication.missing,
            "persisted_facts": facts,
        })

    missing_models = wanted - {item["model"].casefold() for item in results}
    for model in sorted(missing_models):
        results.append({"model": model, "status": "NOT_FOUND"})
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 1 if any(item["status"] in {"NOT_FOUND", "NO_PRODUCT_SNAPSHOT"} for item in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
