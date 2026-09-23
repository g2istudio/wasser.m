from dataclasses import dataclass
import os

from crawler.candidate_worker import (
    _canonical_official_brand,
    _looks_like_accessory,
    _model_from_official_title,
    _model_from_visible_properties,
    _official_page_system,
)
from crawler.catalog_guard import find_existing_site_product
from crawler.discovery import classify_snapshot, identify_snapshot
from crawler.official_sites import load_official_registry
from crawler.page_collector import collect_page
from database.repository import ProductRepository
from extractor.product_extractor import extract_product
from extractor.commerce_parser import extract_commerce_product
from extractor.validation import validate_product
from extractor.publication import assess_publication
from models.product import ProductRecord


@dataclass
class WorkResult:
    url: str
    status: str
    detail: str


async def process_url(repository: ProductRepository, url: str) -> WorkResult:
    try:
        snapshot = await collect_page(url)
        if _looks_like_accessory(snapshot):
            detail = "Accessory, replacement filter, vessel, or service add-on"
            repository.classify_url(url, "SKIP", detail)
            return WorkResult(url, "SKIPPED", detail)
        classification = classify_snapshot(snapshot)
        official_fallback = classification.value == "SKIP" and _official_page_system(snapshot)
        if classification.value == "SKIP" and not official_fallback:
            repository.classify_url(url, classification.value, classification.reason)
            return WorkResult(url, "SKIPPED", classification.reason)
        repository.classify_url(
            url,
            "SYSTEM",
            classification.reason if not official_fallback else "Official product page system terminology",
        )

        brand, model = identify_snapshot(snapshot)
        registry = load_official_registry("config/official_brand_domains.json")
        brand = _canonical_official_brand(snapshot.url, brand, registry)
        model = _model_from_visible_properties(snapshot) or model
        model = _model_from_official_title(snapshot, brand, model)
        if not brand or not model:
            detail = "Identity unavailable before extraction; blocked to prevent an unchecked duplicate"
            repository.update_queue_status(url, "DRAFT", detail)
            return WorkResult(url, "DRAFT", detail)

        existing_site_product = find_existing_site_product(brand, model)
        if existing_site_product is not None:
            detail = (
                f"Already exists on Wasser.Market: {brand} {model} "
                f"(site id={existing_site_product.get('id', 'unknown')})"
            )
            repository.update_queue_status(url, "SKIPPED", detail)
            return WorkResult(url, "SKIPPED", detail)

        existing_identity = repository.get(brand, model)
        if existing_identity is not None:
            detail = f"Duplicate identity resolves to existing agent product {brand} {model}"
            repository.update_queue_status(url, "SKIPPED", detail)
            return WorkResult(url, "SKIPPED", detail)

        existing = repository.get_by_source_url(snapshot.url)
        if existing is not None:
            detail = (
                f"Duplicate source resolves to existing "
                f"{existing.identity.brand.value} {existing.identity.model.value}"
            )
            repository.update_queue_status(url, "SKIPPED", detail)
            return WorkResult(url, "SKIPPED", detail)

        repository.update_queue_status(url, "EXTRACTING", "Running deterministic commerce extraction")
        platform = "unknown"
        try:
            product, deterministic_snapshot, platform = extract_commerce_product(snapshot.url, brand, model)
            report = validate_product(product, deterministic_snapshot.evidence_text, deterministic_snapshot.url)
            snapshot = deterministic_snapshot
        except Exception as deterministic_error:
            if os.getenv("WASSER_ALLOW_AI", "false").casefold() not in {"1", "true", "yes"}:
                detail = f"Deterministic extraction failed: {type(deterministic_error).__name__}: {deterministic_error}"
                repository.update_queue_status(url, "DRAFT", detail[:1000])
                return WorkResult(url, "DRAFT", detail)
            product = extract_product(
                page_text=snapshot.visible_text,
                source_url=snapshot.url,
                source_type="manufacturer_page",
                structured_data=snapshot.json_ld,
                evidence_text=snapshot.evidence_text,
            )
            report = validate_product(product, snapshot.evidence_text, snapshot.url)
            platform = "ai-fallback"
        if not report.valid:
            detail = "; ".join(report.errors[:5])
            repository.update_queue_status(url, "DRAFT", detail)
            return WorkResult(url, "DRAFT", detail)

        publication = assess_publication(product)
        record_status = "PUBLISH_READY" if publication.ready else "DATA_VERIFIED"
        repository.save(ProductRecord(
            product=product,
            status=record_status,
            needs_review=not publication.ready,
        ))
        detail = (
            f"{product.identity.brand.value} {product.identity.model.value}; "
            f"platform={platform}; evidence={report.evidence_records}; quality={record_status}"
        )
        if publication.missing:
            detail += f"; missing={','.join(publication.missing)}"
        repository.update_queue_status(url, "SAVED", detail)
        return WorkResult(url, "SAVED", detail)
    except Exception as error:
        detail = f"{type(error).__name__}: {error}"
        repository.update_queue_status(url, "ERROR", detail[:1000])
        return WorkResult(url, "ERROR", detail)


async def run_batch(repository: ProductRepository, limit: int = 1) -> list[WorkResult]:
    results = []
    for url in repository.work_urls(limit=limit):
        results.append(await process_url(repository, url))
    return results
