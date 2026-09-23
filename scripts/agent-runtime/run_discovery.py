import argparse
import asyncio
import sys
from urllib.parse import urlparse

from crawler.discovery import discover_site_product_urls
from crawler.official_sites import canonical_domain, load_official_registry, official_site_for_url
from crawler.sitemap import discover_sitemap_product_urls
from database.repository import ProductRepository
from sources.brave_search import BraveSearchProvider
from sources.firecrawl_search import FirecrawlSearchProvider


QUERY = "water filtration systems manufacturer official"


def home_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme or 'https'}://{parsed.netloc}/"


def search_and_store(repository, provider, query, limit, country, language, location):
    run_id = repository.start_discovery_run(provider.name, query, country, language)
    try:
        if provider.name == "brave":
            results = provider.search(query, count=limit, country=country, search_lang=language)
        else:
            results = provider.search(query, limit=limit, location=location)
        for result in results:
            domain = canonical_domain(result.url)
            repository.record_discovery_result(
                run_id, provider.name, query, result.rank, result.title, result.url, domain
            )
        repository.finish_discovery_run(run_id)
        return results
    except Exception:
        repository.finish_discovery_run(run_id, "FAILED")
        raise


async def main(
    db: str,
    search_limit: int,
    domain_limit: int,
    query: str,
    country: str,
    language: str,
    location: str,
    official_registry: str,
):
    repository = ProductRepository(db)
    registry = load_official_registry(official_registry)
    provider_results = {}
    provider_errors = {}
    for provider_class in (BraveSearchProvider, FirecrawlSearchProvider):
        try:
            provider = provider_class()
            provider_results[provider.name] = search_and_store(
                repository, provider, query, search_limit, country, language, location
            )
        except Exception as error:
            provider_errors[provider_class.__name__] = f"{type(error).__name__}: {error}"
    if not provider_results:
        raise RuntimeError(f"No search provider succeeded: {provider_errors}")
    domains: dict[str, dict] = {}
    rejected_domains: set[str] = set()
    for provider, results in provider_results.items():
        for result in results:
            domain = canonical_domain(result.url)
            if not domain:
                continue
            official = official_site_for_url(result.url, registry)
            if official is None:
                rejected_domains.add(domain)
                continue
            entry = domains.setdefault(domain, {
                "home": home_url(result.url),
                "providers": set(),
                "brand": official["brand"],
            })
            entry["providers"].add(provider)

    total = 0
    for domain, entry in list(domains.items())[:domain_limit]:
        root = entry["home"]
        products = await discover_sitemap_product_urls(root)
        method = "sitemap"
        if not products:
            _, products = await discover_site_product_urls(root, catalog_limit=6)
            method = "catalog"
        for provider in entry["providers"]:
            repository.record_discovered_site(provider, domain, root)
            repository.enqueue_urls(products, root, provider=provider)
        total += len(products)
        print(
            f"{entry['brand']} ({domain}): {len(products)} product URLs via {method}; "
            f"sources={','.join(sorted(entry['providers']))}"
        )

    print("Discovery stats:", repository.discovery_product_stats())
    print(f"Domains processed={min(domain_limit, len(domains))}; product URLs found={total}")
    print(f"Non-official result domains excluded before crawl={len(rejected_domains)}")
    if provider_errors:
        print("Unavailable search providers:", provider_errors)
    if rejected_domains:
        print("Excluded:", ", ".join(sorted(rejected_domains)))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/wasser_market.db")
    parser.add_argument("--search-limit", type=int, default=10)
    parser.add_argument("--domain-limit", type=int, default=3)
    parser.add_argument("--query", default=QUERY)
    parser.add_argument("--country", default="US")
    parser.add_argument("--language", default="en")
    parser.add_argument("--location", default="United States")
    parser.add_argument("--official-registry", default="config/official_brand_domains.json")
    args = parser.parse_args()
    asyncio.run(main(
        args.db,
        args.search_limit,
        args.domain_limit,
        args.query,
        args.country,
        args.language,
        args.location,
        args.official_registry,
    ))
