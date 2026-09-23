import json
import os
import re
from dataclasses import dataclass, field
from html import unescape
from urllib.parse import urlparse

import requests


def _decode_html(response) -> str:
    candidates = []
    for encoding in (response.encoding, response.apparent_encoding, "utf-8", "cp1252"):
        if not encoding or encoding in {item[0] for item in candidates}:
            continue
        try:
            value = response.content.decode(encoding, errors="replace")
        except (LookupError, UnicodeError):
            continue
        penalty = value.count("�") * 100 + value.count("Ã") * 5 + value.count("â€") * 5
        candidates.append((encoding, value, penalty))
    return min(candidates, key=lambda item: item[2])[1] if candidates else response.text

from playwright.async_api import async_playwright


@dataclass
class PageSnapshot:
    url: str
    title: str
    visible_text: str
    json_ld: list[str] = field(default_factory=list)
    raw_content: str = ""
    fetch_method: str = "http"
    http_metadata: dict = field(default_factory=dict)

    @property
    def evidence_text(self) -> str:
        structured = []
        for raw in self.json_ld:
            try:
                structured.append(json.dumps(json.loads(raw), indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                structured.append(raw)
        return self.visible_text + "\n" + "\n".join(structured)


async def collect_page(url: str, max_visible_chars: int = 30_000) -> PageSnapshot:
    # Cheapest path first. Most commerce platforms render useful JSON-LD in the
    # initial HTML, so a browser or Firecrawl credit is usually unnecessary.
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "WasserMarketAgent/0.2", "Accept": "text/html,application/xhtml+xml"},
            timeout=30,
        )
        response.raise_for_status()
        raw = _decode_html(response)[:2_000_000]
        final_url = str(response.url)
        metadata = {"status": response.status_code, "content_type": response.headers.get("Content-Type"),
                    "etag": response.headers.get("ETag"), "last_modified": response.headers.get("Last-Modified")}
        scripts = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', raw, re.I | re.S)
        title_match = re.search(r"<title[^>]*>(.*?)</title>", raw, re.I | re.S)
        title = unescape(re.sub(r"<[^>]+>", " ", title_match.group(1))).strip() if title_match else ""
        body = re.sub(r"<(script|style|noscript)\b[^>]*>.*?</\1>", " ", raw, flags=re.I | re.S)
        text = unescape(re.sub(r"<[^>]+>", "\n", body))
        text = "\n".join(line.strip() for line in text.splitlines() if line.strip())[:max_visible_chars]
        if len(text) >= 500 and (scripts or re.search(r"product|produkt|filter|osmos", text, re.I)):
            return PageSnapshot(url=final_url, title=title, visible_text=text, json_ld=scripts,
                                raw_content=raw, fetch_method="http", http_metadata=metadata)
    except Exception:
        pass

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = None
        last_error = None
        for attempt in range(2):
            if page:
                await page.close()
            page = await browser.new_page(viewport={"width": 1440, "height": 1200})
            try:
                await page.goto(
                    url,
                    wait_until="domcontentloaded" if attempt == 0 else "commit",
                    timeout=60_000,
                )
                await page.wait_for_timeout(5_000 if attempt == 0 else 8_000)
                break
            except Exception as error:
                last_error = error
        else:
            await browser.close()
            if os.getenv("FIRECRAWL_API_KEY"):
                from sources.firecrawl_search import FirecrawlSearchProvider
                data = FirecrawlSearchProvider().scrape(url)
                metadata = data.get("metadata") or {}
                raw = str(data.get("html") or "")
                visible = str(data.get("markdown") or "")[:max_visible_chars]
                return PageSnapshot(url=str(metadata.get("sourceURL") or url),
                                    title=str(metadata.get("title") or ""), visible_text=visible,
                                    raw_content=raw or visible, fetch_method="firecrawl",
                                    http_metadata=metadata)
            raise last_error

        json_ld = await page.locator('script[type="application/ld+json"]').all_text_contents()
        header_images = await page.locator("header img, .header-logo-main-img").evaluate_all(
            "elements => elements.map(element => ({src: element.currentSrc || element.src || '', alt: element.alt || '', cls: String(element.className || '')}))"
        )
        logo = next((item for item in header_images if "logo" in (
            f"{item.get('src', '')} {item.get('alt', '')} {item.get('cls', '')}".lower()
        )), None)
        if logo and str(logo.get("src", "")).startswith(("http://", "https://")):
            host_brand = (urlparse(page.url).hostname or "").removeprefix("www.").split(".")[0]
            raw_alt = str(logo.get("alt") or "").replace("Logo", "").strip()
            brand_name = raw_alt if host_brand.lower() in raw_alt.lower() else host_brand
            json_ld.append(json.dumps({
                "@context": "https://schema.org",
                "@type": "Organization",
                "name": brand_name,
                "logo": logo["src"],
            }, ensure_ascii=False))

        snapshot = PageSnapshot(
            url=page.url,
            title=await page.title(),
            visible_text=(await page.locator("body").inner_text())[:max_visible_chars],
            json_ld=json_ld,
            raw_content=await page.content(),
            fetch_method="browser",
            http_metadata={"status": 200},
        )
        await browser.close()
        return snapshot


def product_json_ld_documents(snapshot: PageSnapshot) -> list[dict]:
    products: list[dict] = []

    def visit(value):
        if isinstance(value, dict):
            node_type = value.get("@type")
            if node_type == "Product" or isinstance(node_type, list) and "Product" in node_type:
                products.append(value)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    for raw in snapshot.json_ld:
        try:
            visit(json.loads(raw))
        except json.JSONDecodeError:
            continue
    return products
