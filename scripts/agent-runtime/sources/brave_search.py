import json
import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_URL = "https://api.search.brave.com/res/v1/web/search"


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    description: str
    rank: int


def load_local_env(path: str | Path = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        os.environ.setdefault(name.strip(), value.strip())


class BraveSearchProvider:
    name = "brave"

    def __init__(self, api_key: str | None = None):
        load_local_env()
        self.api_key = api_key or os.getenv("BRAVE_SEARCH_API_KEY")
        if not self.api_key:
            raise RuntimeError("BRAVE_SEARCH_API_KEY is not configured")

    def search(
        self,
        query: str,
        count: int = 10,
        country: str = "US",
        search_lang: str = "en",
    ) -> list[SearchResult]:
        if not query.strip():
            raise ValueError("Search query must not be empty")
        params = urlencode({
            "q": query,
            "count": max(1, min(count, 20)),
            "country": country,
            "search_lang": search_lang,
        })
        request = Request(
            f"{API_URL}?{params}",
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "identity",
                "X-Subscription-Token": self.api_key,
                "User-Agent": "WasserMarketAgent/0.1",
            },
        )
        with urlopen(request, timeout=30) as response:
            payload = json.load(response)
        results = payload.get("web", {}).get("results", [])
        return [
            SearchResult(
                title=str(item.get("title", "")),
                url=str(item.get("url", "")),
                description=str(item.get("description", "")),
                rank=index,
            )
            for index, item in enumerate(results, start=1)
            if item.get("url")
        ]
