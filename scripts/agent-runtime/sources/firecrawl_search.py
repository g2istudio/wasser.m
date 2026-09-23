import json
import os
from dataclasses import dataclass
from urllib.request import Request, urlopen

from sources.brave_search import load_local_env


API_URL = "https://api.firecrawl.dev/v2/search"


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    description: str
    rank: int


class FirecrawlSearchProvider:
    name = "firecrawl"

    def __init__(self, api_key: str | None = None):
        load_local_env()
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise RuntimeError("FIRECRAWL_API_KEY is not configured")

    def search(
        self,
        query: str,
        limit: int = 10,
        location: str = "United States",
    ) -> list[SearchResult]:
        if not query.strip():
            raise ValueError("Search query must not be empty")
        body = json.dumps({
            "query": query,
            "limit": max(1, min(limit, 100)),
            "sources": ["web"],
            "location": location,
            "highlights": False,
        }).encode("utf-8")
        request = Request(
            API_URL,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": "WasserMarketAgent/0.1",
            },
        )
        with urlopen(request, timeout=60) as response:
            payload = json.load(response)
        if not payload.get("success"):
            raise RuntimeError(f"Firecrawl search failed: {payload.get('error', 'unknown error')}")
        results = payload.get("data", {}).get("web", [])
        return [
            SearchResult(
                title=str(item.get("title", "")),
                url=str(item.get("url", "")),
                description=str(item.get("description", "")),
                rank=int(item.get("position") or index),
            )
            for index, item in enumerate(results, start=1)
            if item.get("url")
        ]

    def scrape(self, url: str) -> dict:
        """Fetch one difficult page only after the ordinary HTTP/browser path fails."""
        body = json.dumps({
            "url": url,
            "formats": ["markdown", "html"],
            "onlyMainContent": False,
        }).encode("utf-8")
        request = Request(
            "https://api.firecrawl.dev/v1/scrape",
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": "WasserMarketAgent/0.2",
            },
        )
        with urlopen(request, timeout=120) as response:
            payload = json.load(response)
        if not payload.get("success"):
            raise RuntimeError(f"Firecrawl scrape failed: {payload.get('error', 'unknown error')}")
        return payload.get("data") or {}
