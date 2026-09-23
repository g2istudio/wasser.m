from bs4 import BeautifulSoup
import requests

from crawler.page_collector import PageSnapshot


def collect_page_http(url: str, max_visible_chars: int = 30_000) -> PageSnapshot:
    response = requests.get(
        url,
        headers={"User-Agent": "WasserMarketAgent/0.1"},
        timeout=30,
    )
    response.raise_for_status()
    if not response.encoding or response.encoding.lower() in {"iso-8859-1", "ascii"}:
        response.encoding = response.apparent_encoding or "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    json_ld = [
        node.get_text()
        for node in soup.select('script[type="application/ld+json"]')
        if node.get_text().strip()
    ]
    for node in soup.select("script, style, noscript, svg"):
        node.decompose()
    return PageSnapshot(
        url=str(response.url),
        title=title,
        visible_text=soup.get_text("\n", strip=True)[:max_visible_chars],
        json_ld=json_ld,
    )
