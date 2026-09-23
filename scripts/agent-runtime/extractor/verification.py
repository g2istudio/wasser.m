import re
from datetime import date

from pydantic import BaseModel

from models.product import Evidence, ProductValue, WaterFilterProduct


QUESTION_STARTS = (
    "can ", "could ", "does ", "do ", "did ", "is ", "are ",
    "will ", "would ", "what ", "which ", "how ", "why ", "when ",
)
CLAIM_VERBS = re.compile(
    r"\b(remove[sd]?|reduc(?:e[sd]?|tion)|eliminate[sd]?|filter[sed]*|"
    r"certif(?:y|ied)|tested|complies?|rated|captures?|protects?)\b",
    re.IGNORECASE,
)


def is_question_text(text: str | None) -> bool:
    normalized = " ".join((text or "").strip().split()).lower()
    return not normalized or "?" in normalized or normalized.startswith(QUESTION_STARTS)


def is_assertive_claim(text: str | None) -> bool:
    return not is_question_text(text) and bool(CLAIM_VERBS.search(text or ""))


def evidence_status(evidence: Evidence, claim: bool = False) -> str:
    if evidence.source_type == "certification_database":
        return "certified"
    if evidence.source_type == "laboratory_report":
        return "independent_lab_test"
    if evidence.source_type in {"manufacturer_page", "manufacturer_datasheet", "manual"}:
        return "manufacturer_claim" if claim else "official_specification"
    if evidence.source_type in {"authorized_retailer", "retailer"}:
        return "retailer_claim"
    return "unverified"


def sanitize_and_label_product(product: WaterFilterProduct) -> dict[str, int]:
    """Apply universal provenance labels and remove non-assertive evidence."""
    today = date.today().isoformat()
    removed_questions = 0
    removed_contaminants = 0

    def visit(value: object) -> None:
        nonlocal removed_questions
        if isinstance(value, ProductValue):
            clean = []
            for item in value.evidence:
                if is_question_text(item.original_text):
                    removed_questions += 1
                    continue
                item.verification_status = evidence_status(item, claim=False)
                item.checked_at = item.checked_at or today
                clean.append(item)
            value.evidence = clean
            if value.value is not None and not clean:
                value.value = None
                value.unit = None
                value.verification_status = "unverified"
                value.checked_at = today
            elif clean:
                value.verification_status = clean[0].verification_status
                value.checked_at = today
            return
        if isinstance(value, BaseModel):
            own_evidence = getattr(value, "evidence", None)
            if isinstance(own_evidence, list):
                clean = []
                for item in own_evidence:
                    if is_question_text(item.original_text):
                        removed_questions += 1
                        continue
                    item.verification_status = evidence_status(item, claim=False)
                    item.checked_at = item.checked_at or today
                    clean.append(item)
                value.evidence = clean
            for name in value.__class__.model_fields:
                if name not in {"evidence", "verification_status", "checked_at"}:
                    visit(getattr(value, name),)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    visit(product)

    clean_contaminants = []
    for contaminant in product.contaminants:
        clean_evidence = []
        for item in contaminant.evidence:
            if not is_assertive_claim(item.original_text):
                removed_questions += 1
                continue
            item.verification_status = evidence_status(item, claim=True)
            item.checked_at = item.checked_at or today
            clean_evidence.append(item)
        contaminant.evidence = clean_evidence
        if not clean_evidence:
            removed_contaminants += 1
            continue
        statuses = {item.verification_status for item in clean_evidence}
        if "certified" in statuses:
            contaminant.claim_type = "certified"
        elif "independent_lab_test" in statuses:
            contaminant.claim_type = "independent_lab_test"
        elif contaminant.standard and any("tested" in (e.original_text or "").lower() for e in clean_evidence):
            contaminant.claim_type = "tested_to_standard"
        else:
            # A manufacturer's certification statement is still a claim until
            # the exact model is matched in the certification body's database.
            contaminant.claim_type = "manufacturer_claim"
        clean_contaminants.append(contaminant)
    product.contaminants = clean_contaminants

    for certification in product.certifications:
        statuses = set()
        for item in certification.evidence:
            item.verification_status = evidence_status(item, claim=True)
            item.checked_at = item.checked_at or today
            statuses.add(item.verification_status)
        if "certified" in statuses:
            certification.status = "certified"
        elif "independent_lab_test" in statuses:
            certification.status = "tested"
        else:
            certification.status = "manufacturer_claim"

    # Reject a technology copied from related products when the official name
    # of the actual model does not contain that technology at all.
    name = str(product.identity.product_name.value or "").lower()
    technology = str(product.system.technology.value or "").lower()
    if "reverse osmosis" in technology and not re.search(r"\breverse osmosis\b|\bro\b", name):
        product.system.technology.value = None
        product.system.technology.unit = None
        product.system.technology.evidence = []
        product.system.technology.verification_status = "unverified"

    return {
        "removed_question_evidence": removed_questions,
        "removed_contaminants": removed_contaminants,
    }


def display_marker(status: str) -> tuple[str, str]:
    """Stable UI contract; translated labels belong to the website."""
    if status in {"certified", "independent_lab_test"}:
        return "✓", status
    if status == "tested_to_standard":
        return "◇", status
    if status in {"manufacturer_claim", "retailer_claim", "unverified"}:
        return "*", status
    if status == "conflicting_sources":
        return "⚠", status
    return "ℹ", status
