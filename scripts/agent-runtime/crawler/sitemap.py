import asyncio
import gzip
import re
import xml.etree.ElementTree as ET
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import Request, urlopen

from crawler.discovery import _canonical_product_url, is_likely_system_url


SITEMAP_HINTS = ("product", "produkt", "shop")


def _download(url: str) -> tuple[bytes, str]:
    request = Request(url, headers={"User-Agent": "WasserMarketAgent/0.1"})
    with urlopen(request, timeout=30) as response:
        data = response.read(10_000_000)
        content_type = response.headers.get("Content-Type", "")
    if url.lower().endswith(".gz") or "gzip" in content_type:
        data = gzip.decompress(data)
    return data, content_type


def _xml_locations(data: bytes) -> tuple[str, list[str]]:
    root = ET.fromstring(data)
    kind = root.tag.rsplit("}", 1)[-1].lower()
    # Only direct <loc> children represent pages/sitemaps. Image sitemap
    # extensions contain their own <image:loc> and must not enter the queue.
    locations = []
    for entry in list(root):
        for node in list(entry):
            if node.tag.rsplit("}", 1)[-1].lower() == "loc" and (node.text or "").strip():
                locations.append((node.text or "").strip())
                break
    return kind, locations


def _urlset_records(data: bytes) -> list[tuple[str, bool]]:
    root = ET.fromstring(data)
    records = []
    for entry in list(root):
        page_url = ""
        has_image = False
        for node in list(entry):
            local_name = node.tag.rsplit("}", 1)[-1].lower()
            namespace = node.tag.split("}", 1)[0].lstrip("{") if "}" in node.tag else ""
            if local_name == "loc" and not page_url:
                page_url = (node.text or "").strip()
            elif local_name == "image" or "sitemap-image" in namespace:
                has_image = True
        if page_url:
            records.append((page_url, has_image))
    return records


def _robots_sitemaps(home_url: str) -> list[str]:
    robots_url = urljoin(home_url, "/robots.txt")
    try:
        data, _ = _download(robots_url)
    except Exception:
        return []
    text = data.decode("utf-8", errors="ignore")
    return [match.strip() for match in re.findall(r"(?im)^sitemap:\s*(\S+)", text)]


def discover_sitemap_product_urls_sync(home_url: str, max_sitemaps: int = 30) -> list[str]:
    """Read sitemap indexes recursively and return canonical product pages."""
    parsed = urlparse(home_url)
    origin = f"{parsed.scheme or 'https'}://{parsed.netloc}"
    host = (parsed.hostname or "").lower()
    pending = _robots_sitemaps(origin) or [urljoin(origin, "/sitemap.xml")]
    seen: set[str] = set()
    products: set[str] = set()

    while pending and len(seen) < max_sitemaps:
        sitemap_url = pending.pop(0)
        if sitemap_url in seen:
            continue
        seen.add(sitemap_url)
        try:
            data, _ = _download(sitemap_url)
            kind, locations = _xml_locations(data)
        except Exception:
            continue
        if kind == "sitemapindex":
            preferred = [url for url in locations if any(hint in url.lower() for hint in SITEMAP_HINTS)]
            pending.extend(preferred or locations)
            continue
        for url, has_product_image in _urlset_records(data):
            if (urlparse(url).hostname or "").lower() != host:
                continue
            canonical = _canonical_product_url(url)
            # Some commerce engines use SEO slugs directly below the domain.
            # An image sitemap entry is a strong deterministic product-page
            # signal and lets us support those stores without domain rules.
            if not canonical and has_product_image:
                clean = urldefrag(url)[0]
                canonical = urlparse(clean)._replace(query="").geturl().rstrip("/")
            if canonical and is_likely_system_url(canonical):
                products.add(canonical)
    return sorted(products)


async def discover_sitemap_product_urls(home_url: str, max_sitemaps: int = 30) -> list[str]:
    return await asyncio.to_thread(discover_sitemap_product_urls_sync, home_url, max_sitemaps)
