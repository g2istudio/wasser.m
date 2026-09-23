from dataclasses import dataclass
from urllib.parse import urldefrag, urljoin, urlparse
import re

from playwright.async_api import async_playwright

from crawler.page_collector import PageSnapshot, product_json_ld_documents


@dataclass(frozen=True)
class Classification:
    value: str
    reason: str


@dataclass(frozen=True)
class CatalogCandidate:
    url: str
    label: str
    score: int


SYSTEM_TERMS = (
    "reverse osmosis system",
    "ro system",
    "ro water system",
    "water filtration system",
    "water filter system",
    "undersink water filter",
    "under sink water filter",
    "countertop water filter",
    "countertop ro",
    "umkehrosmoseanlage",
    "umkehrosmose anlage",
    "osmoseanlage",
    "wasserfiltersystem",
    "wasserfilter system",
    "trinkwasserfilter",
    "wasseraufbereitungsanlage",
)

SKIP_TERMS = (
    "replacement",
    "replacement filter",
    "replacement for",
    "filter replacement",
    "cartridge",
    "faucet",
    "pump",
    "adapter",
    "remineralization filter",
    "alkaline filter",
    "ice maker kit",
    "installation kit",
    "filter set",
    "ersatzfilter",
    "ersatzpatrone",
    "filterpatrone",
    "zubehör",
    "wasserhahn",
    "armatur",
    "membran ersatz",
    "check valve",
    "ball valve",
    "shut off valve",
    "quick fitting",
    "drain saddle",
    "mounting kit",
    "sliding tray",
    "housing wrench",
    "filter timer",
    "leak detector",
)

STRONG_ACCESSORY_TERMS = (
    "replacement", "cartridge", "filter set", "kit for", "valve",
    "adapter", "quick fitting", "drain saddle", "mounting kit",
    "sliding tray", "housing wrench", "filter timer", "leak detector",
)

CATALOG_TERMS = (
    "water filter", "filtration", "reverse osmosis", "ro system",
    "systems", "products", "shop", "solutions", "catalog",
    "undersink", "under sink", "countertop", "whole house",
    "produkte", "wasserfilter", "filtersysteme", "umkehrosmose",
    "osmoseanlagen", "wasseraufbereitung", "trinkwasser", "anlagen",
)

CATALOG_PATH_TERMS = (
    "/collections/", "/collection/", "/categories/", "/category/",
    "/product-category/", "/produkt-kategorie/", "/catalog", "/shop",
    "/systems", "/solutions", "/products",
)

NAVIGATION_EXCLUSIONS = (
    "blog", "news", "support", "contact", "about", "privacy", "terms",
    "account", "login", "cart", "manual", "faq", "track", "warranty",
)


def _canonical_product_url(url: str) -> str | None:
    parsed = urlparse(url)
    match = re.search(r"/(?:products|product|produkt)/([^/]+)", parsed.path)
    if not match:
        return None
    prefix = match.group(0).split("/")[1]
    return f"{parsed.scheme}://{parsed.netloc}/{prefix}/{match.group(1)}"


def is_likely_system_url(url: str) -> bool:
    """Cheap sitemap prefilter; page classification remains authoritative."""
    slug = urlparse(url).path.lower().replace("-", "_").replace("/", " ")
    text = slug.replace("_", " ")
    if any(term in text for term in SKIP_TERMS):
        return False
    return any(term in text for term in SYSTEM_TERMS)


def _catalog_score(label: str, url: str) -> int:
    text = f"{label} {url}".lower()
    if any(term in text for term in NAVIGATION_EXCLUSIONS):
        return -1
    score = sum(3 for term in CATALOG_TERMS if term in label.lower())
    score += sum(2 for term in CATALOG_PATH_TERMS if term in url.lower())
    if any(term in text for term in ("replacement", "accessories", "parts")):
        score -= 5
    return score


async def discover_catalogs(home_url: str, limit: int = 12) -> list[CatalogCandidate]:
    """Find likely product catalogs without assuming a fixed menu name or path."""
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 1200})
        await page.goto(home_url, wait_until="domcontentloaded", timeout=60_000)
        await page.wait_for_timeout(4_000)
        anchors = await page.locator("a[href]").evaluate_all(
            "elements => elements.map(element => ({href: element.href, label: (element.innerText || element.getAttribute('aria-label') || '').trim()}))"
        )
        await browser.close()

    host = urlparse(home_url).netloc.lower()
    by_url: dict[str, CatalogCandidate] = {}
    for anchor in anchors:
        url = urldefrag(urljoin(home_url, anchor["href"]))[0].rstrip("/")
        parsed = urlparse(url)
        if (
            parsed.netloc.lower() != host
            or _canonical_product_url(url)
            or "add-to-cart" in parsed.query.lower()
        ):
            continue
        # Menu ref/UTM parameters describe navigation attribution, not a
        # different catalog.
        url = parsed._replace(query="").geturl().rstrip("/")
        score = _catalog_score(anchor["label"], url)
        if score < 2:
            continue
        candidate = CatalogCandidate(url=url, label=anchor["label"], score=score)
        previous = by_url.get(url)
        if previous is None or candidate.score > previous.score:
            by_url[url] = candidate
    return sorted(by_url.values(), key=lambda item: (-item.score, item.url))[:limit]


async def discover_site_product_urls(home_url: str, catalog_limit: int = 12) -> tuple[list[CatalogCandidate], list[str]]:
    catalogs = await discover_catalogs(home_url, limit=catalog_limit)
    urls: set[str] = set()
    for catalog in catalogs:
        urls.update(await discover_product_urls(catalog.url))
    return catalogs, sorted(urls)


async def discover_product_urls(catalog_url: str) -> list[str]:
    """Collect unique same-domain product links from an official catalog page."""
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 1200})
        await page.goto(catalog_url, wait_until="domcontentloaded", timeout=60_000)
        await page.wait_for_timeout(4_000)
        hrefs = await page.locator("a[href]").evaluate_all(
            "elements => elements.map(element => element.href)"
        )
        await browser.close()

    catalog_host = urlparse(catalog_url).netloc.lower()
    urls = set()
    fallback_urls = set()
    catalog_path = urlparse(catalog_url).path.rstrip("/")
    catalog_depth = len([part for part in catalog_path.split("/") if part])
    for href in hrefs:
        url = urldefrag(urljoin(catalog_url, href))[0]
        parsed = urlparse(url)
        if parsed.netloc.lower() != catalog_host:
            continue
        # Shopify can expose one product through many collection paths. Keep
        # only the global product handle and drop variant/configuration queries.
        canonical = _canonical_product_url(url)
        if canonical:
            urls.add(canonical)
            continue
        # Some commerce engines (for example Shopware) place product pages
        # directly below a category path without /product/ or /produkt/.
        # Keep only direct descendants here; page-level Product JSON-LD and
        # standalone-system classification remain the authoritative gates.
        clean_path = parsed.path.rstrip("/")
        depth = len([part for part in clean_path.split("/") if part])
        if (
            catalog_path
            and clean_path.startswith(catalog_path + "/")
            and depth == catalog_depth + 1
            and not any(term in clean_path.lower() for term in NAVIGATION_EXCLUSIONS)
        ):
            fallback_urls.add(parsed._replace(query="", fragment="").geturl().rstrip("/"))
    return sorted(urls or fallback_urls)


def classify_snapshot(snapshot: PageSnapshot) -> Classification:
    """Classify a product page as a standalone system or something to skip."""
    documents = product_json_ld_documents(snapshot)
    if not documents:
        return Classification("SKIP", "No Product JSON-LD")

    node = documents[0]
    haystack = " ".join(
        str(node.get(key, "")) for key in ("name", "description", "sku", "mpn")
    ).lower()
    # Product JSON-LD can contain only a short variant name while the page
    # title states the actual product class (common in Shopware stores).
    haystack = f"{haystack} {snapshot.title} {urlparse(snapshot.url).path}".lower()
    name = str(node.get("name", "")).lower()

    # A complete system may legitimately include a faucet, pump or alkaline
    # filter. Only strong accessory wording overrides explicit system wording.
    if any(term in name for term in STRONG_ACCESSORY_TERMS):
        return Classification("SKIP", "Accessory or replacement product name")
    if any(term in haystack for term in SYSTEM_TERMS):
        return Classification("SYSTEM", "Standalone filtration system terminology")
    if any(term in name for term in SKIP_TERMS):
        return Classification("SKIP", "Accessory or replacement product name")
    return Classification("SKIP", "No explicit standalone-system terminology")


def identify_snapshot(snapshot: PageSnapshot) -> tuple[str | None, str | None]:
    """Resolve brand/model cheaply from official Product JSON-LD before AI."""
    documents = product_json_ld_documents(snapshot)
    if not documents:
        return None, None
    node = documents[0]
    name = str(node.get("name") or "").strip()
    raw_brand = node.get("brand")
    brand = raw_brand.get("name") if isinstance(raw_brand, dict) else raw_brand
    if not isinstance(brand, str) or not brand.strip() or brand.strip() == name or len(brand.strip()) > 60:
        match = re.match(r"^([A-Za-z][A-Za-z0-9.&'-]{1,39})\s+", name)
        brand = match.group(1) if match else None
    explicit = re.search(r"\bmodel\s+([A-Z0-9][A-Z0-9-]{1,24})\b", name, re.IGNORECASE)
    if explicit:
        return str(brand).strip() if brand else None, explicit.group(1).upper()
    tokens = re.findall(r"\b(?=[A-Z0-9-]*[A-Z])(?=[A-Z0-9-]*\d)[A-Z][A-Z0-9-]{1,24}\b", name.upper())
    excluded = {"GPD", "RO", "UV", "NSF", "ANSI", "3IN1", "2IN1"}
    model = next((token for token in tokens if token not in excluded), None)
    return str(brand).strip() if brand else None, model
