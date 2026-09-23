"""Authenticated, idempotent Wasser.Market import client."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
import uuid
from urllib.request import Request, urlopen


class WasserMarketApiClient:
    def __init__(self, base_url: str | None = None, api_key: str | None = None,
                 api_secret: str | None = None):
        self.base_url = (base_url or os.getenv("WASSER_MARKET_API_URL") or "").rstrip("/")
        self.api_key = api_key or os.getenv("WASSER_MARKET_API_KEY")
        self.api_secret = api_secret or os.getenv("WASSER_MARKET_API_SECRET")
        if not self.base_url.startswith("https://"):
            raise RuntimeError("WASSER_MARKET_API_URL must use HTTPS")
        if not self.api_key or not self.api_secret:
            raise RuntimeError("Wasser.Market API credentials are not configured")

    def signed_headers(self, body: bytes, idempotency_key: str, timestamp: str | None = None,
                       nonce: str | None = None) -> dict[str, str]:
        timestamp = timestamp or str(int(time.time()))
        nonce = nonce or str(uuid.uuid4())
        digest = hashlib.sha256(body).hexdigest()
        signing_input = f"{timestamp}\n{nonce}\n{idempotency_key}\n{digest}".encode()
        signature = hmac.new(self.api_secret.encode(), signing_input, hashlib.sha256).hexdigest()
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "Idempotency-Key": idempotency_key,
            "X-Wasser-Timestamp": timestamp,
            "X-Wasser-Nonce": nonce,
            "X-Wasser-Signature": f"sha256={signature}",
            "User-Agent": "WasserMarketAgent/0.2",
        }

    def import_product(self, payload: dict, canonical_product_id: str, card_version: str) -> dict:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        key = f"{canonical_product_id}:{card_version}"
        request = Request(
            f"{self.base_url}/imports/products",
            data=body,
            method="POST",
            headers=self.signed_headers(body, key),
        )
        with urlopen(request, timeout=60) as response:
            result = json.load(response)
        if not isinstance(result, dict):
            raise RuntimeError("Wasser.Market API returned a non-object response")
        return result
