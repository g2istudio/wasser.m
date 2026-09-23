from dataclasses import dataclass
import re

from crawler.catalog_guard import find_existing_site_product, normalized_identity_part
from crawler.discovery import classify_snapshot, identify_snapshot
from crawler.http_collector import collect_page_http
from crawler.official_sites import load_official_registry, official_site_for_url
from database.repository import ProductRepository


@dataclass
class CandidateResult:
    url: str
    status: str
    brand: str | None
    model: str | None
    detail: str


OFFICIAL_PRODUCT_TERMS = (
    "reverse osmosis",
    "umkehrosmose",
    "osmosis water filter",
    "osmose water filter",
    "ro countertop water filter",
    "drinking water filter",
    "water filtration system",
    "wasserfiltersystem",
    "wasserhahnfilter",
    "untertischfilter",
    "whole house filter",
)

ACCESSORY_TITLE_URL_TERMS = (
    "replacement",
    "ersatz",
    "water pitcher",
    "ersatzfilter",
    "weiteres jahr",
    "additional year",
)


def _looks_like_accessory(snapshot) -> bool:
    text = f"{snapshot.title} {snapshot.url}".casefold().replace("-", " ")
    return any(term in text for term in ACCESSORY_TITLE_URL_TERMS)


def _official_page_system(snapshot) -> bool:
    text = f"{snapshot.title}\n{snapshot.visible_text[:12000]}".casefold()
    return any(term in text for term in OFFICIAL_PRODUCT_TERMS)


def _model_from_visible_properties(snapshot) -> str | None:
    lines = [line.strip() for line in snapshot.visible_text.splitlines() if line.strip()]
    for index, line in enumerate(lines):
        match = re.match(r"(?i)^modell?\s*:\s*(.+)$", line)
        if match and len(match.group(1).strip()) <= 80:
            return match.group(1).strip()
        if re.fullmatch(r"(?i)modell?\s*:?", line) and index + 1 < len(lines):
            value = lines[index + 1]
            if len(value) <= 80:
                return value
    return None


def _model_from_official_title(snapshot, brand: str | None, property_model: str | None) -> str | None:
    title = snapshot.title.split("|", 1)[0].strip()
    if brand:
        title = re.sub(rf"(?i)^{re.escape(brand)}\s+", "", title).strip()
    before_dash = re.split(r"\s+[–—]\s+", title, maxsplit=1)[0].strip()

    if normalized_identity_part(brand or "") != "bem":
        # Prefer the leading identity printed in an official page title over a
        # later alphanumeric feature such as H2, UV-C or a percentage.
        ro_model = re.match(r"(?i)^(RO\s*\d+(?:\s+[A-Z][A-Z0-9.+-]*)?)\b", before_dash)
        if ro_model:
            return re.sub(r"\s+", " ", ro_model.group(1)).upper()
        first = re.match(r"([A-Za-z0-9][A-Za-z0-9.+-]*)\b", before_dash)
        if first and first.group(1).casefold() not in {
            "reverse", "umkehrosmose", "umkehrosmoseanlage", "osmoseanlage", "wasserfilter"
        }:
            return first.group(1)
        return property_model

    if before_dash != title and 1 <= len(before_dash.split()) <= 4:
        return before_dash
    if property_model and "/" not in property_model:
        if normalized_identity_part(property_model) == "unicora" and re.match(r"(?i)^Unicora\s+2\.0\b", title):
            return "Unicora 2.0"
        return property_model
    match = re.match(r"([A-Za-z0-9]+(?:\s+2\.0)?)\b", title)
    return match.group(1) if match else property_model


def _canonical_official_brand(url: str, extracted: str | None, registry: dict[str, dict]) -> str | None:
    site = official_site_for_url(url, registry)
    if site is None:
        return extracted
    return str(site["brand"]).split(" / ")[0].strip()


def preflight_url(
    repository: ProductRepository,
    url: str,
    registry_path: str = "config/official_brand_domains.json",
) -> CandidateResult:
    try:
        registry = load_official_registry(registry_path)
        if official_site_for_url(url, registry) is None:
            detail = "Domain is not in the verified official-brand registry"
            repository.update_queue_status(url, "SKIPPED", detail)
            return CandidateResult(url, "SKIPPED", None, None, detail)

        snapshot = collect_page_http(url)
        if _looks_like_accessory(snapshot):
            detail = "Accessory, replacement filter, vessel, or service add-on"
            repository.classify_url(url, "SKIP", detail)
            return CandidateResult(url, "SKIPPED", None, None, detail)
        classification = classify_snapshot(snapshot)
        official_fallback = (
            classification.value == "SKIP" and _official_page_system(snapshot)
        )
        if classification.value == "SKIP" and not official_fallback:
            repository.classify_url(url, "SKIP", classification.reason)
            return CandidateResult(url, "SKIPPED", None, None, classification.reason)

        brand, model = identify_snapshot(snapshot)
        brand = _canonical_official_brand(snapshot.url, brand, registry)
        model = _model_from_visible_properties(snapshot) or model
        model = _model_from_official_title(snapshot, brand, model)
        if not brand or not model:
            detail = "Identity unavailable without AI; held for manual identity review"
            repository.update_queue_status(url, "DRAFT", detail)
            return CandidateResult(url, "DRAFT", brand, model, detail)

        existing_site = find_existing_site_product(brand, model)
        if existing_site is not None:
            detail = (
                f"Already exists on Wasser.Market: {brand} {model} "
                f"(site id={existing_site.get('id', 'unknown')})"
            )
            repository.classify_url(url, "SYSTEM", detail)
            repository.update_queue_status(url, "SKIPPED", detail)
            return CandidateResult(url, "SKIPPED", brand, model, detail)

        if repository.get(brand, model) is not None:
            detail = f"Already exists in agent database: {brand} {model}"
            repository.classify_url(url, "SYSTEM", detail)
            repository.update_queue_status(url, "SKIPPED", detail)
            return CandidateResult(url, "SKIPPED", brand, model, detail)

        detail = f"New parsing candidate: {brand} {model}; official domain verified; site duplicate absent"
        repository.classify_url(url, "SYSTEM", detail)
        return CandidateResult(url, "IDENTIFIED", brand, model, detail)
    except Exception as error:
        detail = f"{type(error).__name__}: {error}"
        repository.update_queue_status(url, "ERROR", detail[:1000])
        return CandidateResult(url, "ERROR", None, None, detail)
