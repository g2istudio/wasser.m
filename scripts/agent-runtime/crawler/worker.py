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
from crawler.official_sites import canonical_domain, official_site_for_url
from crawler.page_collector import collect_page
from database.repository import ProductRepository
from extractor.product_extractor import extract_product
from extractor.commerce_parser import extract_commerce_product
from extractor.validation import validate_product
from extractor.publication import assess_publication
from models.product import Evidence, ProductRecord, ProductValue
from provenance import persist_product_facts
from runtime_control import BudgetExceeded, RuntimeMeter, calculated_confidence, source_priority
from semantic_resolution import minimal_fragments, resolve_semantics
from sources.brave_search import BraveSearchProvider
from sources.firecrawl_search import FirecrawlSearchProvider


@dataclass
class WorkResult:
    url: str
    status: str
    detail: str


def _apply_semantic_resolution(product, item: dict, source_url: str, evidence_text: str,
                               source_type: str = "manufacturer_page") -> bool:
    path = str(item.get("field_path") or "").removeprefix("product.")
    parts = path.split(".")
    if len(parts) < 2 or item.get("value") is None:
        return False
    target = product
    for part in parts[:-1]:
        if not hasattr(target, part):
            return False
        target = getattr(target, part)
    leaf = parts[-1]
    current = getattr(target, leaf, None)
    evidence = str(item.get("evidence") or "")
    if not isinstance(current, ProductValue) or current.value is not None or not evidence or evidence not in evidence_text:
        return False
    confidence = calculated_confidence(
        source_type=source_type,
        exact_model_match=True,
        verbatim_evidence=True,
        conflicting=False,
        extraction_method="gemini",
    )
    if confidence < 0.8:
        return False
    setattr(target, leaf, ProductValue(
        value=item.get("value"),
        unit=item.get("unit"),
        evidence=[Evidence(
            source_url=source_url,
            source_type=source_type,
            original_text=evidence,
            confidence=confidence,
            verification_status="manufacturer_claim",
            extraction_method="gemini",
            parser_version="2",
            schema_version=product.schema_version,
        )],
        verification_status="manufacturer_claim",
    ))
    return True


async def _enrich_missing(repository, meter: RuntimeMeter | None, *, brand: str, model: str,
                          primary_snapshot, product, product_id: str, issues: list[str]) -> tuple[dict | None, object | None]:
    if not issues or not meter:
        return None, None
    # Keep the discovery query short. Search engines often return no results for
    # a quoted model plus every missing field, while the semantic stage already
    # knows which fields it must resolve from the returned pages.
    query = f"{brand} {model} Umkehrosmose Datenblatt technische Daten"
    meter.consume("brave", "queries", 1, product_id, {"query": query, "purpose": "missing_fields"})
    results = BraveSearchProvider().search(query, count=10, country="DE", search_lang="de")
    registry = load_official_registry("config/official_brand_domains.json")
    brand_key = "".join(ch for ch in brand.casefold() if ch.isalnum())
    primary_domain = canonical_domain(primary_snapshot.url)
    model_key = "".join(ch for ch in model.casefold() if ch.isalnum())
    sources: list[tuple[str, str]] = []
    source_meta: dict[str, tuple[str, str]] = {}
    seen = {primary_snapshot.url}
    for result in results:
        if len(sources) >= 3:
            break
        url = result.url
        domain = canonical_domain(url)
        result_key = "".join(
            ch for ch in f"{result.title} {result.url} {result.description}".casefold()
            if ch.isalnum()
        )
        official = official_site_for_url(url, registry)
        domain_key = "".join(ch for ch in domain.casefold() if ch.isalnum())
        allowed = domain == primary_domain or brand_key in domain_key or (
            official and brand_key in "".join(ch for ch in str(official["brand"]).casefold() if ch.isalnum())
        )
        if (not allowed or url in seen or not url.startswith("https://")
                or model_key not in result_key):
            continue
        seen.add(url)
        try:
            if ".pdf" in url.casefold():
                data = FirecrawlSearchProvider().scrape(url)
                meter.consume("firecrawl", "credits", 1, product_id, {"url": url, "purpose": "enrichment_pdf"})
                text = str(data.get("markdown") or "")
                raw = str(data.get("html") or text)
                metadata = data.get("metadata") or {}
                source_type = "manufacturer_datasheet" if official else "authorized_retailer"
            else:
                candidate = await collect_page(url)
                meter.consume(
                    "firecrawl" if candidate.fetch_method == "firecrawl" else "http",
                    "credits" if candidate.fetch_method == "firecrawl" else "requests",
                    1,
                    product_id,
                    {"url": url, "purpose": "enrichment", "method": candidate.fetch_method},
                )
                text = candidate.evidence_text
                raw = candidate.raw_content or text
                metadata = candidate.http_metadata
                source_type = "manufacturer_page" if official or domain == primary_domain else "authorized_retailer"
                fetched_identity = "".join(
                    ch for ch in f"{candidate.title} {candidate.url}".casefold()
                    if ch.isalnum()
                )
                if model_key not in fetched_identity:
                    meter.event("ENRICHMENT_IDENTITY_REJECTED", "enrichment", product_id,
                                {"url": url, "title": candidate.title, "expected_model": model})
                    continue
            if len(text) < 100:
                continue
            snapshot_id, created = repository.save_snapshot(url, raw, text, source_type, metadata)
            repository.link_product_source(product_id, snapshot_id, source_priority(source_type), {"model": model})
            if url not in product.sources.additional_urls:
                product.sources.additional_urls.append(url)
            sources.append((url, text))
            source_meta[url] = (text, source_type)
            meter.event("ENRICHMENT_SOURCE_STORED" if created else "ENRICHMENT_SOURCE_REUSED",
                        "enrichment", product_id, {"url": url, "source_type": source_type})
        except Exception as error:
            meter.event("ENRICHMENT_SOURCE_FAILED", "enrichment", product_id,
                        {"url": url, "error": f"{type(error).__name__}: {error}"})
    if not sources:
        meter.event("ENRICHMENT_NO_SOURCES", "enrichment", product_id,
                    {"query": query, "issues": issues})
        return None, None
    result, usage, fragment_chars = resolve_semantics(
        brand=brand,
        model=model,
        source_url=primary_snapshot.url,
        evidence_text=primary_snapshot.evidence_text,
        issues=issues,
        additional_sources=sources,
    )
    meter.consume("gemini", "tokens", usage.total_tokens, product_id,
                  {"model": usage.model, "fragment_chars": fragment_chars, "purpose": "enrichment",
                   "estimated_cost_usd": usage.estimated_cost_usd})
    applied = 0
    for item in result.get("resolutions", []):
        item_url = str(item.get("source_url") or primary_snapshot.url)
        item_text, item_type = source_meta.get(
            item_url, (primary_snapshot.evidence_text, "manufacturer_page")
        )
        evidence = str(item.get("evidence") or "")
        if not evidence or evidence not in item_text:
            continue
        confidence = calculated_confidence(
            source_type=item_type, exact_model_match=True, verbatim_evidence=True,
            conflicting=False, extraction_method="gemini",
        )
        repository.save_fact(
            product_id=product_id, field_path=str(item.get("field_path") or "unknown"),
            value=item.get("value"), normalized_value=item.get("value"), unit=item.get("unit"),
            source_url=item_url, source_type=item_type, evidence=evidence,
            extraction_method="gemini", confidence=confidence, parser_version="2",
            schema_version=product.schema_version, resolution_status="PROPOSED",
        )
        applied += int(_apply_semantic_resolution(
            product, item, item_url, item_text, source_type=item_type
        ))
    for item in result.get("unmapped_attributes", []):
        item_url = str(item.get("source_url") or primary_snapshot.url)
        item_text, item_type = source_meta.get(
            item_url, (primary_snapshot.evidence_text, "manufacturer_page")
        )
        evidence = str(item.get("evidence") or "")
        if item.get("value") is None or not evidence or evidence not in item_text:
            continue
        repository.save_unmapped_attribute(
            product_id=product_id, original_name=str(item.get("original_name") or "unknown"),
            value=item.get("value"), unit=item.get("unit"), source_url=item_url,
            evidence=evidence, proposed_field=item.get("proposed_field"), extraction_method="gemini",
            confidence=calculated_confidence(
                source_type=item_type, exact_model_match=True, verbatim_evidence=True,
                conflicting=False, extraction_method="gemini",
            ), parser_version="2", schema_version=product.schema_version,
        )
    meter.event("ENRICHMENT_COMPLETED", "enrichment", product_id,
                {"sources": len(sources), "applied": applied, "issues": issues})
    return result, usage


async def process_url(
    repository: ProductRepository,
    url: str,
    meter: RuntimeMeter | None = None,
    force: bool = False,
    expected_brand: str | None = None,
    expected_model: str | None = None,
) -> WorkResult:
    try:
        snapshot = await collect_page(url)
        if meter:
            meter.consume(
                "firecrawl" if snapshot.fetch_method == "firecrawl" else "http",
                "credits" if snapshot.fetch_method == "firecrawl" else "requests",
                1,
                metadata={"url": snapshot.url, "method": snapshot.fetch_method},
            )
            meter.event("SOURCE_FETCHED", "fetch", detail={"url": snapshot.url, "method": snapshot.fetch_method})
        snapshot_id, created = repository.save_snapshot(
            snapshot.url,
            snapshot.raw_content or snapshot.evidence_text,
            snapshot.evidence_text,
            "official_product_page",
            snapshot.http_metadata,
        )
        if meter:
            meter.event("SNAPSHOT_STORED" if created else "SNAPSHOT_REUSED", "fetch", detail={"snapshot_id": snapshot_id})
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
        brand = expected_brand or brand
        model = expected_model or model
        if not brand or not model:
            detail = "Identity unavailable before extraction; blocked to prevent an unchecked duplicate"
            repository.update_queue_status(url, "DRAFT", detail)
            return WorkResult(url, "DRAFT", detail)

        existing_site_product = find_existing_site_product(brand, model)
        if existing_site_product is not None and not force:
            detail = (
                f"Already exists on Wasser.Market: {brand} {model} "
                f"(site id={existing_site_product.get('id', 'unknown')})"
            )
            repository.update_queue_status(url, "SKIPPED", detail)
            return WorkResult(url, "SKIPPED", detail)

        existing_identity = repository.get(brand, model)
        if existing_identity is not None and not force:
            detail = f"Duplicate identity resolves to existing agent product {brand} {model}"
            repository.update_queue_status(url, "SKIPPED", detail)
            return WorkResult(url, "SKIPPED", detail)

        existing = repository.get_by_source_url(snapshot.url)
        if existing is not None and not force:
            detail = (
                f"Duplicate source resolves to existing "
                f"{existing.identity.brand.value} {existing.identity.model.value}"
            )
            repository.update_queue_status(url, "SKIPPED", detail)
            return WorkResult(url, "SKIPPED", detail)

        repository.update_queue_status(url, "EXTRACTING", "Running deterministic commerce extraction")
        platform = "unknown"
        manual_documents: list[tuple[str, str, dict]] = []
        try:
            product, deterministic_snapshot, platform = extract_commerce_product(
                snapshot.url,
                brand,
                model,
                snapshot=snapshot,
                request_hook=(
                    (lambda requested_url: meter.consume(
                        "http", "requests", 1,
                        metadata={"url": requested_url, "purpose": "official_manual"},
                    )) if meter else None
                ),
                document_hook=lambda manual_url, text, metadata: manual_documents.append(
                    (manual_url, text, metadata)
                ),
            )
            report = validate_product(product, deterministic_snapshot.evidence_text, deterministic_snapshot.url)
            snapshot = deterministic_snapshot
        except Exception as deterministic_error:
            if os.getenv("WASSER_ALLOW_AI", "false").casefold() not in {"1", "true", "yes"}:
                detail = f"Deterministic extraction failed: {type(deterministic_error).__name__}: {deterministic_error}"
                repository.update_queue_status(url, "DRAFT", detail[:1000])
                return WorkResult(url, "DRAFT", detail)
            fallback_fragments = minimal_fragments(
                snapshot.evidence_text,
                model,
                [f"deterministic extraction failed: {type(deterministic_error).__name__}"],
            )
            try:
                product = extract_product(
                    page_text=fallback_fragments,
                    source_url=snapshot.url,
                    source_type="manufacturer_page",
                    structured_data=[item[:5000] for item in snapshot.json_ld[:2]],
                    evidence_text=snapshot.evidence_text,
                )
            except Exception as ai_error:
                detail = f"Semantic fallback unavailable: {type(ai_error).__name__}: {ai_error}"
                repository.update_queue_status(url, "DRAFT", detail[:1000])
                if meter:
                    meter.event("SEMANTIC_RESOLUTION_FAILED", "extraction", detail={"error": detail})
                return WorkResult(url, "NEEDS_REVIEW", detail)
            report = validate_product(product, snapshot.evidence_text, snapshot.url)
            platform = "ai-fallback"
        publication = assess_publication(product)
        taxonomy = publication.profile if publication.profile != "generic_system" else "UNKNOWN/NEW_TYPE"
        product_id = repository.upsert_canonical_product(
            brand,
            model,
            taxonomy=taxonomy,
            status="DATA_VERIFIED" if report.valid else "NEEDS_REVIEW",
            schema_version=product.schema_version,
        )
        product.canonical_product_id = product_id
        product.taxonomy = taxonomy
        repository.link_product_source(
            product_id,
            snapshot_id,
            source_priority("official_product_page"),
            {"market": product.identity.market_region.value, "model": model},
        )
        for manual_url, manual_text, manual_metadata in manual_documents:
            manual_snapshot_id, manual_created = repository.save_snapshot(
                manual_url,
                manual_text,
                manual_text,
                "manual",
                manual_metadata,
            )
            repository.link_product_source(
                product_id,
                manual_snapshot_id,
                source_priority("manual"),
                {"market": product.identity.market_region.value, "model": model},
            )
            if meter:
                meter.event(
                    "MANUAL_STORED" if manual_created else "MANUAL_REUSED",
                    "fetch",
                    product_id,
                    {"url": manual_url, "snapshot_id": manual_snapshot_id},
                )

        product_dump = product.model_dump(mode="json")
        has_conflict = "conflicting_sources" in str(product_dump)
        semantic_issues = list(report.errors) + list(publication.missing)
        semantic_issues.extend(
            f"unmapped attribute: {item.original_name}" for item in product.unmapped_attributes[:20]
        )
        if has_conflict:
            semantic_issues.append("conflicting values in source evidence")
        semantic_result = None
        if semantic_issues and os.getenv("WASSER_ALLOW_AI", "false").casefold() in {"1", "true", "yes"}:
            try:
                semantic_result, usage, fragment_chars = resolve_semantics(
                    brand=brand,
                    model=model,
                    source_url=snapshot.url,
                    evidence_text=snapshot.evidence_text,
                    issues=semantic_issues,
                )
                if meter:
                    meter.consume("gemini", "tokens", usage.total_tokens, product_id,
                                  {"model": usage.model, "fragment_chars": fragment_chars,
                                   "estimated_cost_usd": usage.estimated_cost_usd})
                    meter.event("GEMINI_REQUESTED", "semantic_resolution", product_id,
                                {"issues": semantic_issues, "fragment_chars": fragment_chars})
                for item in semantic_result.get("resolutions", []):
                    evidence = str(item.get("evidence") or "")
                    item_source_url = str(item.get("source_url") or snapshot.url)
                    if evidence and evidence in snapshot.evidence_text:
                        repository.save_fact(
                            product_id=product_id,
                            field_path=str(item.get("field_path") or "unknown"),
                            value=item.get("value"),
                            normalized_value=item.get("value"),
                            unit=item.get("unit"),
                            source_url=item_source_url,
                            source_type="manufacturer_page",
                            evidence=evidence,
                            extraction_method="gemini",
                            confidence=0.7,
                            parser_version="2",
                            schema_version=product.schema_version,
                            resolution_status="PROPOSED",
                        )
                        _apply_semantic_resolution(product, item, item_source_url, snapshot.evidence_text)
                for item in semantic_result.get("unmapped_attributes", []):
                    evidence = str(item.get("evidence") or "")
                    item_source_url = str(item.get("source_url") or snapshot.url)
                    if item.get("value") is not None and evidence and evidence in snapshot.evidence_text:
                        repository.save_unmapped_attribute(
                            product_id=product_id,
                            original_name=str(item.get("original_name") or "unknown"),
                            value=item.get("value"),
                            unit=item.get("unit"),
                            source_url=item_source_url,
                            evidence=evidence,
                            proposed_field=item.get("proposed_field"),
                            extraction_method="gemini",
                            confidence=calculated_confidence(
                                source_type="manufacturer_page",
                                exact_model_match=True,
                                verbatim_evidence=True,
                                conflicting=False,
                                extraction_method="gemini",
                            ),
                            parser_version="2",
                            schema_version=product.schema_version,
                        )
            except Exception as semantic_error:
                if meter:
                    meter.event("SEMANTIC_RESOLUTION_FAILED", "semantic_resolution", product_id,
                                {"error": f"{type(semantic_error).__name__}: {semantic_error}"})

        if semantic_result is not None:
            report = validate_product(product, snapshot.evidence_text, snapshot.url)
            publication = assess_publication(product)
            semantic_issues = list(report.errors) + list(publication.missing)
            semantic_issues.extend(
                f"unmapped attribute: {item.original_name}" for item in product.unmapped_attributes[:20]
            )

        enrichment_result = None
        if semantic_issues and os.getenv("WASSER_ALLOW_AI", "false").casefold() in {"1", "true", "yes"}:
            try:
                enrichment_result, _ = await _enrich_missing(
                    repository,
                    meter,
                    brand=brand,
                    model=model,
                    primary_snapshot=snapshot,
                    product=product,
                    product_id=product_id,
                    issues=semantic_issues,
                )
                if enrichment_result is not None:
                    report = validate_product(product, "\n".join(
                        [snapshot.evidence_text] + [
                            str(repository.latest_snapshot(url)["normalized_content"])
                            for url in product.sources.additional_urls
                            if repository.latest_snapshot(url)
                        ]
                    ), snapshot.url)
                    publication = assess_publication(product)
                    semantic_issues = list(report.errors) + list(publication.missing)
                    semantic_issues.extend(
                        f"unmapped attribute: {item.original_name}" for item in product.unmapped_attributes[:20]
                    )
            except BudgetExceeded:
                raise
            except Exception as enrichment_error:
                if meter:
                    meter.event("ENRICHMENT_FAILED", "enrichment", product_id,
                                {"error": f"{type(enrichment_error).__name__}: {enrichment_error}"})

        if not report.valid:
            detail = "; ".join(report.errors[:5])
            repository.audit(meter.job_id if meter else None, product_id, "VALIDATION_FAILED", "validation",
                             {"errors": report.errors})
            repository.update_queue_status(url, "DRAFT", detail)
            return WorkResult(url, "NEEDS_REVIEW", detail)

        persisted = persist_product_facts(repository, product_id, product, platform)
        unresolved = bool(
            semantic_result and semantic_result.get("unresolved_conflicts")
            or enrichment_result and enrichment_result.get("unresolved_conflicts")
        )
        if publication.ready and taxonomy != "UNKNOWN/NEW_TYPE" and not has_conflict and not unresolved:
            record_status = "PUBLISH_READY"
        elif semantic_issues or taxonomy == "UNKNOWN/NEW_TYPE":
            record_status = "NEEDS_REVIEW"
        else:
            record_status = "DATA_VERIFIED"
        repository.upsert_canonical_product(
            brand, model, taxonomy=taxonomy, status=record_status, schema_version=product.schema_version
        )
        repository.save(ProductRecord(
            product=product,
            status=record_status,
            needs_review=record_status == "NEEDS_REVIEW",
            source_conflict=has_conflict or unresolved,
        ))
        repository.audit(meter.job_id if meter else None, product_id, "PRODUCT_VALIDATED", "validation",
                         {"status": record_status, "facts": persisted, "missing": publication.missing})
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


async def run_batch(repository: ProductRepository, limit: int = 1,
                    meter: RuntimeMeter | None = None, force: bool = False) -> list[WorkResult]:
    results = []
    for url in repository.work_urls(limit=limit):
        if meter:
            meter.consume("pipeline", "products", 1)
        results.append(await process_url(repository, url, meter=meter, force=force))
        if meter:
            repository.update_job(meter.job_id, "RUNNING", url)
    return results
