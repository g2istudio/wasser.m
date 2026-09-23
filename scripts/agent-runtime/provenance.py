"""Persist product facts without losing their supporting evidence."""

from __future__ import annotations

from pydantic import BaseModel

from models.product import ProductValue, WaterFilterProduct
from runtime_control import calculated_confidence


PARSER_VERSION = "2"
SCHEMA_VERSION = "2"


def persist_product_facts(repository, product_id: str, product: WaterFilterProduct,
                          extraction_method: str = "html") -> int:
    saved = 0

    def visit(value: object, path: str = "product") -> None:
        nonlocal saved
        if isinstance(value, ProductValue):
            if value.value is None:
                return
            for evidence in value.evidence:
                repository.save_fact(
                    product_id=product_id,
                    field_path=path.removeprefix("product."),
                    value=value.value,
                    normalized_value=value.value,
                    unit=value.unit,
                    source_url=evidence.source_url,
                    source_type=evidence.source_type,
                    evidence=evidence.original_text or "",
                    extraction_method=evidence.extraction_method or extraction_method,
                    confidence=calculated_confidence(
                        source_type=evidence.source_type,
                        exact_model_match=True,
                        verbatim_evidence=bool(evidence.original_text),
                        conflicting=evidence.verification_status == "conflicting_sources",
                        extraction_method=evidence.extraction_method or extraction_method,
                    ),
                    fetched_at=evidence.fetched_at or evidence.checked_at,
                    parser_version=evidence.parser_version or PARSER_VERSION,
                    schema_version=evidence.schema_version or product.schema_version or SCHEMA_VERSION,
                    resolution_status=(
                        "CONFLICT" if evidence.verification_status == "conflicting_sources" else "ACCEPTED"
                    ),
                )
                saved += 1
            return
        if isinstance(value, BaseModel):
            for name in value.__class__.model_fields:
                visit(getattr(value, name), f"{path}.{name}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                visit(item, f"{path}[{index}]")

    visit(product)
    for attribute in product.unmapped_attributes:
        repository.save_unmapped_attribute(
            product_id=product_id,
            original_name=attribute.original_name,
            value=attribute.value,
            unit=attribute.unit,
            source_url=attribute.source_url,
            evidence=attribute.evidence,
            proposed_field=attribute.proposed_field,
            extraction_method=attribute.extraction_method,
            confidence=attribute.confidence,
            fetched_at=attribute.fetched_at,
            parser_version=attribute.parser_version or PARSER_VERSION,
            schema_version=attribute.schema_version or product.schema_version or SCHEMA_VERSION,
        )
    return saved
