"""Standalone WasserMarket Agent CLI. No Codex/OpenAI runtime dependency."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit

from crawler.discovery import discover_site_product_urls
from crawler.official_sites import canonical_domain, load_official_registry, official_site_for_url
from crawler.sitemap import discover_sitemap_product_urls
from crawler.worker import process_url, run_batch
from database.repository import ProductRepository
from extractor.publication import assess_publication
from extractor.validation import validate_product
from models.product import ProductRecord, WaterFilterProduct
from provenance import persist_product_facts
from runtime_control import BudgetExceeded, Budgets, RuntimeMeter
from sources.brave_search import BraveSearchProvider, load_local_env
from sources.wasser_market_api import WasserMarketApiClient


ROOT = Path(__file__).resolve().parent
DEFAULT_SITE = ROOT.parents[1] if ROOT.name == "agent-runtime" else Path.cwd()


def budgets_from_args(args) -> Budgets:
    return Budgets(
        max_brave_queries=args.max_brave_queries,
        max_http_requests=args.max_http_requests,
        max_firecrawl_credits=args.max_firecrawl_credits,
        max_gemini_tokens=args.max_gemini_tokens,
        max_products=args.max_products,
        max_runtime_seconds=args.max_runtime,
    )


def brand_token(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def inferred_brand(title: str, domain: str) -> str:
    first = re.split(r"[|–—:\-]", title)[0].strip()
    if 1 < len(first.split()) <= 4 and len(first) <= 50:
        return first
    return domain.removeprefix("www.").split(".")[0].replace("-", " ").title()


async def discover_brands(repository, meter, args) -> dict:
    provider = BraveSearchProvider()
    registry = load_official_registry(str(ROOT / "config" / "official_brand_domains.json"))
    query = args.query or f'{args.category} water filtration systems manufacturer official {args.region}'
    meter.consume("brave", "queries", 1, metadata={"query": query})
    results = provider.search(query, count=min(args.search_limit, 20), country=args.country, search_lang=args.language)
    accepted = []
    seen_domains = set()
    denied = {"amazon.", "ebay.", "walmart.", "alibaba.", "idealo.", "otto.", "kaufland."}
    for result in results:
        domain = canonical_domain(result.url)
        if not domain or domain in seen_domains or any(item in domain for item in denied):
            continue
        seen_domains.add(domain)
        official = official_site_for_url(result.url, registry)
        if official:
            name = str(official["brand"]).split(" / ")[0].strip()
        else:
            label = domain.split(".")[0].replace("-", " ")
            if label.casefold().endswith("filter") and len(label) > len("filter") + 3:
                label = label[:-len("filter")]
            name = label.title()
        repository.save_brand_candidate(domain, name, result.url, args.region, result.description)
        repository.enqueue_frontier(result.url, None, "brand", 0, args.max_depth)
        accepted.append({"brand": name, "domain": domain})
    meter.event("BRANDS_DISCOVERED", "brand_discovery", detail={"count": len(accepted), "query": query})
    return {"job_id": meter.job_id, "brands": accepted}


async def discover_products(repository, meter, args) -> dict:
    provider = BraveSearchProvider()
    query = args.query or f'{args.brand} {args.category} official products models'
    meter.consume("brave", "queries", 1, metadata={"query": query})
    results = provider.search(query, count=min(args.search_limit, 20), country=args.country, search_lang=args.language)
    registry = load_official_registry(str(ROOT / "config" / "official_brand_domains.json"))
    token = brand_token(args.brand)
    roots = []
    for result in results:
        domain = canonical_domain(result.url)
        official = official_site_for_url(result.url, registry)
        if (official and brand_token(official["brand"]) == token) or (token and token in brand_token(domain)):
            root = f"{urlsplit(result.url).scheme or 'https'}://{urlsplit(result.url).netloc}/"
            if root not in roots:
                roots.append(root)
    if args.domain:
        roots.insert(0, args.domain if args.domain.endswith("/") else args.domain + "/")
    products = []
    for root in roots[:args.domain_limit]:
        meter.consume("http", "requests", 1, metadata={"url": root, "purpose": "sitemap"})
        found = await discover_sitemap_product_urls(root)
        if not found:
            meter.consume("http", "requests", 1, metadata={"url": root, "purpose": "catalog"})
            _, found = await discover_site_product_urls(root, catalog_limit=args.max_depth * 2)
        accepted_for_root = []
        remaining = max(0, args.max_products - len(products))
        for url in found[:remaining]:
            accepted_for_root.append(url)
            if repository.enqueue_frontier(url, root, "product", 1, args.max_depth):
                products.append(url)
        repository.enqueue_urls(accepted_for_root, root, provider="brave")
    meter.event("PRODUCT_URLS_DISCOVERED", "product_discovery", detail={"brand": args.brand, "count": len(products)})
    return {"job_id": meter.job_id, "brand": args.brand, "product_urls": len(products), "roots": roots}


async def process_model(repository, meter, args) -> dict:
    url = args.url
    if not url:
        query = f'"{args.brand}" "{args.model}" official product'
        meter.consume("brave", "queries", 1, metadata={"query": query})
        results = BraveSearchProvider().search(query, count=min(args.search_limit, 20), country=args.country, search_lang=args.language)
        registry = load_official_registry(str(ROOT / "config" / "official_brand_domains.json"))
        token = brand_token(args.brand)
        for result in results:
            official = official_site_for_url(result.url, registry)
            if (official and brand_token(official["brand"]) == token) or token in brand_token(canonical_domain(result.url)):
                url = result.url
                break
    if not url:
        raise RuntimeError(f"No official product URL found for {args.brand} {args.model}")
    repository.enqueue_urls([url], url, provider="brave")
    result = await process_url(
        repository,
        url,
        meter=meter,
        force=args.force,
        expected_brand=args.brand,
        expected_model=args.model,
    )
    return {"job_id": meter.job_id, "result": result.__dict__, "usage": repository.usage_totals(meter.job_id)}


async def process_pending(repository, meter, args) -> dict:
    if args.command == "resume":
        results = []
        for url in repository.resumable_urls(min(args.limit, args.max_products)):
            meter.consume("pipeline", "products", 1)
            results.append(await process_url(repository, url, meter=meter, force=args.force))
            repository.update_job(meter.job_id, "RUNNING", url)
    else:
        results = await run_batch(repository, min(args.limit, args.max_products), meter=meter, force=args.force)
    return {"job_id": meter.job_id, "results": [item.__dict__ for item in results],
            "usage": repository.usage_totals(meter.job_id)}


def reprocess(repository, meter, args) -> dict:
    results = []
    for row in repository.product_rows(args.brand)[:args.max_products]:
        product = WaterFilterProduct.model_validate_json(row["product_json"])
        snapshot = repository.latest_snapshot(row["source_url"])
        if not snapshot:
            results.append({"brand": row["brand"], "model": row["model"], "status": "NO_SNAPSHOT"})
            continue
        product.schema_version = args.schema_version
        product_id = repository.upsert_canonical_product(row["brand"], row["model"], taxonomy=product.taxonomy,
                                                         status=row["quality_status"], schema_version=args.schema_version)
        facts = persist_product_facts(repository, product_id, product, "reprocess")
        # Some commerce servers replace the multiplication sign in visible
        # dimension text with U+FFFD while the structured value remains intact.
        # Repair only the unambiguous numeric separator for evidence matching.
        evidence_text = re.sub(
            r"(?<=\d)\s*\N{REPLACEMENT CHARACTER}\s*(?=\d)",
            " × ",
            snapshot["normalized_content"],
        )
        report = validate_product(product, evidence_text, row["source_url"])
        publication = assess_publication(product)
        status = (
            "PUBLISH_READY"
            if report.valid and publication.ready and product.taxonomy != "UNKNOWN/NEW_TYPE"
            and not bool(row.get("source_conflict"))
            else "NEEDS_REVIEW"
        )
        repository.upsert_canonical_product(row["brand"], row["model"], taxonomy=product.taxonomy,
                                             status=status, schema_version=args.schema_version)
        repository.save(ProductRecord(
            product=product,
            status=status,
            needs_review=status == "NEEDS_REVIEW",
            source_conflict=bool(row.get("source_conflict")),
        ))
        meter.consume("pipeline", "products", 1, product_id)
        meter.event("PRODUCT_REPROCESSED", "reprocess", product_id,
                    {"schema_version": args.schema_version, "facts": facts, "status": status})
        results.append({"brand": row["brand"], "model": row["model"], "status": status, "facts": facts})
    return {"job_id": meter.job_id, "results": results}


def publish(args) -> dict:
    repository = ProductRepository(args.db)
    if bool(args.brand) != bool(args.model):
        raise RuntimeError("Targeted publication requires both --brand and --model")
    eligible = [
        row for row in repository.product_rows()
        if row["status"] == args.status and row["quality_status"] == args.status
    ]
    if args.brand and args.model:
        eligible = [
            row for row in eligible
            if row["brand"].casefold() == args.brand.casefold()
            and row["model"].casefold() == args.model.casefold()
        ]
        if len(eligible) != 1:
            raise RuntimeError(
                f"Expected exactly one PUBLISH_READY target for {args.brand} {args.model}; found {len(eligible)}"
            )
    else:
        eligible = eligible[:args.limit]

    if args.transport == "api" or args.transport == "auto" and os.getenv("WASSER_MARKET_API_URL"):
        client = WasserMarketApiClient()
        published = []
        for row in eligible:
            payload = json.loads(row["product_json"])
            product_id = payload.get("canonical_product_id") or f"{row['brand']}:{row['model']}"
            version = payload.get("schema_version") or "1"
            if args.apply:
                response = client.import_product(payload, product_id, version)
            else:
                response = {"dry_run": True}
            published.append({"canonical_product_id": product_id, "response": response})
        return {"transport": "api", "mode": "apply" if args.apply else "dry-run", "products": published}

    script = args.site / "scripts" / "agent-auto-publish.ps1"
    command = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script),
               "-Database", str(args.db), "-Limit", str(args.limit)]
    if args.brand and args.model:
        command.extend(["-ProductId", str(eligible[0]["id"])])
    if not args.apply:
        command.append("-DryRun")
    completed = subprocess.run(command, cwd=args.site, text=True, capture_output=True)
    if completed.returncode:
        raise RuntimeError(completed.stderr[-2000:] or "Publication command failed")
    return {"transport": "git", "mode": "apply" if args.apply else "dry-run", "output": completed.stdout[-4000:]}


def add_budget_args(parser):
    parser.add_argument("--max-brave-queries", type=int, default=10)
    parser.add_argument("--max-http-requests", type=int, default=100)
    parser.add_argument("--max-firecrawl-credits", type=int, default=20)
    parser.add_argument("--max-gemini-tokens", type=int, default=50_000)
    parser.add_argument("--max-products", type=int, default=25)
    parser.add_argument("--max-runtime", type=int, default=1800)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="wasser-agent")
    root.add_argument("--db", default=str(ROOT / "data" / "wasser_market.db"))
    root.add_argument("--site", type=Path, default=DEFAULT_SITE)
    root.add_argument("--allow-gemini", action=argparse.BooleanOptionalAction, default=True)
    sub = root.add_subparsers(dest="command", required=True)

    brands = sub.add_parser("discover-brands")
    brands.add_argument("--region", default="germany")
    brands.add_argument("--category", default="drinking water filtration")
    brands.add_argument("--query")
    brands.add_argument("--country", default="DE")
    brands.add_argument("--language", default="de")
    brands.add_argument("--search-limit", type=int, default=20)
    brands.add_argument("--max-depth", type=int, default=2)

    discover = sub.add_parser("discover")
    discover.add_argument("--brand", required=True)
    discover.add_argument("--category", default="reverse-osmosis")
    discover.add_argument("--query")
    discover.add_argument("--domain")
    discover.add_argument("--country", default="DE")
    discover.add_argument("--language", default="de")
    discover.add_argument("--search-limit", type=int, default=20)
    discover.add_argument("--domain-limit", type=int, default=2)
    discover.add_argument("--max-depth", type=int, default=3)

    process = sub.add_parser("process")
    process.add_argument("--brand", required=True)
    process.add_argument("--model", required=True)
    process.add_argument("--url")
    process.add_argument("--country", default="DE")
    process.add_argument("--language", default="de")
    process.add_argument("--search-limit", type=int, default=10)
    process.add_argument("--force", action="store_true")

    pending = sub.add_parser("process-pending")
    pending.add_argument("--limit", type=int, default=10)
    pending.add_argument("--force", action="store_true")

    resume = sub.add_parser("resume")
    resume.add_argument("--limit", type=int, default=10)
    resume.add_argument("--force", action="store_true")

    again = sub.add_parser("reprocess")
    again.add_argument("--schema-version", required=True)
    again.add_argument("--brand")

    validate = sub.add_parser("validate")
    validate.add_argument("--pending", action="store_true")

    pub = sub.add_parser("publish")
    pub.add_argument("--status", choices=["PUBLISH_READY"], default="PUBLISH_READY")
    pub.add_argument("--limit", type=int, default=10)
    pub.add_argument("--brand")
    pub.add_argument("--model")
    pub.add_argument("--apply", action="store_true")
    pub.add_argument("--transport", choices=["auto", "api", "git"], default="auto")

    costs = sub.add_parser("costs")
    costs.add_argument("--job-id")
    costs.add_argument("--product-id")

    for item in (brands, discover, process, pending, resume, again, validate):
        add_budget_args(item)
    return root


async def run(args) -> dict:
    env_file = Path(os.getenv("WASSER_AGENT_ENV_FILE", str(ROOT / ".env")))
    load_local_env(env_file)
    os.environ["WASSER_ALLOW_AI"] = "true" if args.allow_gemini else "false"
    os.environ["WASSER_AI_PROVIDER"] = "gemini"
    os.environ.setdefault("WASSER_AI_FALLBACK_LOCAL", "false")
    repository = ProductRepository(args.db)
    if args.command == "costs":
        return {"usage": repository.usage_totals(args.job_id, args.product_id)}
    if args.command == "publish":
        job_id = repository.start_job("publish", {key: str(value) for key, value in vars(args).items()}, {})
        try:
            result = publish(args)
            repository.audit(job_id, None, "PUBLICATION_FINISHED", "publish", result)
            repository.update_job(job_id, "COMPLETED", "publish")
            return {"job_id": job_id, **result}
        except Exception:
            repository.update_job(job_id, "FAILED", "publish")
            raise

    budgets = budgets_from_args(args)
    kind = "process-pending" if args.command == "resume" else args.command
    parameters = {key: str(value) if isinstance(value, Path) else value for key, value in vars(args).items()}
    job_id = repository.start_job(kind, parameters, budgets.to_dict())
    meter = RuntimeMeter(repository, job_id, budgets)
    try:
        if args.command == "discover-brands":
            result = await discover_brands(repository, meter, args)
        elif args.command == "discover":
            result = await discover_products(repository, meter, args)
        elif args.command == "process":
            result = await process_model(repository, meter, args)
        elif args.command in {"process-pending", "resume"}:
            result = await process_pending(repository, meter, args)
        elif args.command == "reprocess":
            result = reprocess(repository, meter, args)
        elif args.command == "validate":
            args.schema_version = "current"
            args.brand = None
            result = reprocess(repository, meter, args)
        else:
            raise RuntimeError(f"Unsupported command: {args.command}")
        repository.update_job(job_id, "COMPLETED", args.command)
        return result
    except BudgetExceeded as error:
        repository.update_job(job_id, "BUDGET_STOPPED", args.command)
        return {"job_id": job_id, "status": "BUDGET_STOPPED", "reason": str(error),
                "usage": repository.usage_totals(job_id)}
    except Exception:
        repository.update_job(job_id, "FAILED", args.command)
        raise


def main() -> int:
    args = parser().parse_args()
    try:
        print(json.dumps(asyncio.run(run(args)), ensure_ascii=False, indent=2, default=str))
        return 0
    except Exception as error:
        print(json.dumps({"status": "ERROR", "error": f"{type(error).__name__}: {error}"}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
