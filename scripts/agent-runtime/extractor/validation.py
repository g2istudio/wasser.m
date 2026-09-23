from dataclasses import dataclass, field
import re

from pydantic import BaseModel

from models.product import ProductValue, WaterFilterProduct
from extractor.verification import is_question_text


@dataclass
class ValidationReport:
    valid: bool
    populated_fields: int = 0
    evidence_records: int = 0
    errors: list[str] = field(default_factory=list)


def _evidence_in_text(quote: str | None, evidence_text: str) -> bool:
    if not quote:
        return False
    if quote in evidence_text:
        return True
    # HTML tables often insert newlines or indentation between adjacent cells.
    # Collapsing whitespace preserves the words and punctuation while allowing
    # the same verbatim statement to survive layout normalization.
    return re.sub(r"\s+", " ", quote).strip() in re.sub(r"\s+", " ", evidence_text).strip()


def validate_product(
    product: WaterFilterProduct,
    evidence_text: str,
    source_url: str,
    source_type: str = "manufacturer_page",
) -> ValidationReport:
    report = ValidationReport(valid=True)
    allowed_source_urls = {
        source_url,
        *product.sources.additional_urls,
        *product.sources.certification_urls,
        *product.sources.laboratory_report_urls,
    }

    required = {
        "identity.brand": product.identity.brand.value,
        "identity.model": product.identity.model.value,
        "identity.product_name": product.identity.product_name.value,
        "sources.manufacturer_url": product.sources.manufacturer_url,
    }
    for path, value in required.items():
        if value is None or not str(value).strip():
            report.errors.append(f"Missing required field: {path}")

    if product.sources.manufacturer_url != source_url:
        report.errors.append("Manufacturer URL does not match crawled URL")
    if len(product.images) != 1 or product.images[0].role != "primary":
        report.errors.append("Exactly one primary product image is required")
    elif product.images[0].source_url != source_url:
        report.errors.append("Primary image source URL mismatch")

    def visit(value: object, path: str = "product") -> None:
        if isinstance(value, ProductValue):
            if value.value is not None:
                report.populated_fields += 1
                if not value.evidence:
                    report.errors.append(f"Missing evidence: {path}")
                for item in value.evidence:
                    report.evidence_records += 1
                    if item.source_url not in allowed_source_urls:
                        report.errors.append(f"Wrong evidence URL: {path}")
                    expected_types = {source_type}
                    if item.source_url in product.sources.additional_urls or item.source_url == product.sources.manual_url:
                        expected_types.update({"manual", "manufacturer_datasheet", "manufacturer_page", "authorized_retailer"})
                    if item.source_type not in expected_types:
                        report.errors.append(f"Wrong evidence type: {path}")
                    if not _evidence_in_text(item.original_text, evidence_text):
                        report.errors.append(f"Non-verbatim evidence: {path}")
                    if is_question_text(item.original_text):
                        report.errors.append(f"Question cannot support a fact: {path}")
                    if item.verification_status == "unverified":
                        report.errors.append(f"Missing verification status: {path}")
            return
        if isinstance(value, BaseModel):
            own_evidence = getattr(value, "evidence", None)
            if isinstance(own_evidence, list):
                for item in own_evidence:
                    report.evidence_records += 1
                    expected_types = {source_type}
                    if item.source_url in product.sources.additional_urls or item.source_url == product.sources.manual_url:
                        expected_types.update({"manual", "manufacturer_datasheet", "manufacturer_page", "authorized_retailer"})
                    if item.source_url not in allowed_source_urls or item.source_type not in expected_types:
                        report.errors.append(f"Invalid object evidence source: {path}")
                    if not _evidence_in_text(item.original_text, evidence_text):
                        report.errors.append(f"Non-verbatim object evidence: {path}")
                    if is_question_text(item.original_text):
                        report.errors.append(f"Question cannot support an object claim: {path}")
            for name in value.__class__.model_fields:
                if name != "evidence":
                    visit(getattr(value, name), f"{path}.{name}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                visit(item, f"{path}[{index}]")

    visit(product)
    report.valid = not report.errors
    return report
