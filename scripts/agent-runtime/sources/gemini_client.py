import json
import os
import time
from dataclasses import dataclass
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from sources.brave_search import load_local_env


MODEL_PRICES_PER_MILLION = {
    "gemini-3.1-flash-lite": (0.25, 1.50),
    "gemini-3.5-flash-lite": (0.30, 2.50),
    "gemini-3.5-flash": (0.75, 3.75),
    "gemini-3.6-flash": (0.75, 3.75),
    "gemini-3.7-flash": (0.75, 3.75),
    "gemini-3.8-flash": (0.75, 3.75),
}


@dataclass(frozen=True)
class GeminiUsage:
    model: str
    input_tokens: int
    output_tokens: int
    thinking_tokens: int
    total_tokens: int
    elapsed_seconds: float
    estimated_cost_usd: float


_usage_events: list[GeminiUsage] = []


def clear_usage_events() -> None:
    """Clear process-local usage events before one measured extraction."""
    _usage_events.clear()


def pop_usage_events() -> list[GeminiUsage]:
    """Return and clear usage events recorded since the last reset."""
    events = list(_usage_events)
    _usage_events.clear()
    return events


class GeminiClient:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        load_local_env()
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")

    def generate_json(self, prompt: str, schema: dict) -> tuple[str, GeminiUsage]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "x-goog-api-key": self.api_key,
                "User-Agent": "WasserMarketAgent/0.1",
        }

        def make_request(native_schema: bool) -> Request:
            effective_prompt = prompt
            generation_config = {
                "temperature": 0,
                "responseMimeType": "application/json",
            }
            if native_schema:
                generation_config["responseJsonSchema"] = schema
            else:
                effective_prompt += (
                    "\nReturn JSON matching this schema exactly. Do not add markdown:\n"
                    + json.dumps(schema, ensure_ascii=False)
                )
            body = json.dumps({
                "contents": [{"role": "user", "parts": [{"text": effective_prompt}]}],
                "generationConfig": generation_config,
            }).encode("utf-8")
            return Request(url, data=body, method="POST", headers=headers)

        request = make_request(native_schema=True)
        started = time.perf_counter()
        payload = None
        retryable = {429, 500, 502, 503, 504}
        schema_fallback_used = False
        for attempt in range(5):
            try:
                with urlopen(request, timeout=120) as response:
                    payload = json.load(response)
                break
            except HTTPError as error:
                # Never include request headers or the API key in diagnostics.
                detail = error.read().decode("utf-8", errors="replace")[:1000]
                if error.code == 400 and not schema_fallback_used:
                    request = make_request(native_schema=False)
                    schema_fallback_used = True
                    continue
                if error.code not in retryable or attempt == 4:
                    raise RuntimeError(f"Gemini HTTP {error.code}: {detail}") from None
                time.sleep(2 ** (attempt + 1))
        if payload is None:
            raise RuntimeError("Gemini returned no response")

        candidates = payload.get("candidates") or []
        parts = candidates[0].get("content", {}).get("parts", []) if candidates else []
        text = "".join(str(part.get("text", "")) for part in parts if isinstance(part, dict))
        if not text:
            reason = candidates[0].get("finishReason") if candidates else "no candidate"
            raise RuntimeError(f"Gemini returned no structured content: {reason}")
        metadata = payload.get("usageMetadata", {})
        input_tokens = int(metadata.get("promptTokenCount") or 0)
        output_tokens = int(metadata.get("candidatesTokenCount") or 0)
        thinking_tokens = int(metadata.get("thoughtsTokenCount") or 0)
        default_input_rate, default_output_rate = MODEL_PRICES_PER_MILLION.get(
            self.model, (0.75, 3.75)
        )
        input_rate = float(os.getenv("GEMINI_INPUT_USD_PER_M", str(default_input_rate)))
        output_rate = float(os.getenv("GEMINI_OUTPUT_USD_PER_M", str(default_output_rate)))
        usage = GeminiUsage(
            model=self.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            thinking_tokens=thinking_tokens,
            total_tokens=int(metadata.get("totalTokenCount") or 0),
            elapsed_seconds=time.perf_counter() - started,
            estimated_cost_usd=(
                input_tokens * input_rate
                + (output_tokens + thinking_tokens) * output_rate
            ) / 1_000_000,
        )
        _usage_events.append(usage)
        return text, usage
