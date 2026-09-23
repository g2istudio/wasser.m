"""Small, task-scoped Gemini requests for ambiguous or unmapped facts."""

from __future__ import annotations

import json
import re

from sources.gemini_client import GeminiClient


SEMANTIC_SCHEMA = {
    "type": "object",
    "properties": {
        "taxonomy": {"type": "string"},
        "resolutions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "field_path": {"type": "string"},
                    "value": {},
                    "unit": {"type": ["string", "null"]},
                    "source_url": {"type": "string"},
                    "evidence": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "required": ["field_path", "value", "source_url", "evidence", "reason"],
            },
        },
        "unmapped_attributes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "original_name": {"type": "string"},
                    "value": {},
                    "unit": {"type": ["string", "null"]},
                    "source_url": {"type": "string"},
                    "evidence": {"type": "string"},
                    "proposed_field": {"type": ["string", "null"]},
                },
                "required": ["original_name", "value", "source_url", "evidence"],
            },
        },
        "unresolved_conflicts": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["taxonomy", "resolutions", "unmapped_attributes", "unresolved_conflicts"],
}


KEYWORDS = re.compile(
    r"model|sku|mpn|flow|gpd|l/min|capacity|stage|filter|membrane|dimension|weight|"
    r"voltage|power|watt|pressure|temperature|tank|uv|mineral|osmos|waste|ratio|"
    r"modell|leistung|durchfluss|stufe|abmess|gewicht|spannung|druck|temperatur",
    re.I,
)


def minimal_fragments(text: str, model: str, issues: list[str], max_chars: int = 12_000) -> str:
    needles = [part.casefold() for part in re.split(r"\W+", model) if len(part) > 2]
    needles += [part.casefold() for issue in issues for part in re.split(r"\W+", issue) if len(part) > 4]
    selected: list[str] = []
    total = 0
    for raw in text.splitlines():
        line = " ".join(raw.split())
        lower = line.casefold()
        if len(line) < 3 or not (KEYWORDS.search(line) or any(word in lower for word in needles)):
            continue
        if line in selected:
            continue
        if total + len(line) + 1 > max_chars:
            break
        selected.append(line)
        total += len(line) + 1
    return "\n".join(selected)


def resolve_semantics(*, brand: str, model: str, source_url: str,
                      evidence_text: str, issues: list[str],
                      additional_sources: list[tuple[str, str]] | None = None) -> tuple[dict, object, int]:
    sources = [(source_url, evidence_text), *(additional_sources or [])]
    fragment_blocks = []
    for candidate_url, candidate_text in sources:
        selected = minimal_fragments(candidate_text, model, issues, max_chars=max(2000, 12000 // len(sources)))
        if selected:
            fragment_blocks.append(f"[SOURCE {candidate_url}]\n{selected}")
    fragments = "\n\n".join(fragment_blocks)[:12000]
    prompt = f"""Resolve only the listed issues for one water-treatment product.
Brand: {brand}
Model: {model}
Primary source: {source_url}
Issues: {json.dumps(issues, ensure_ascii=False)}

Use only the fragments below. Evidence must be copied verbatim from them. Do not invent values.
Every resolution and unmapped attribute must include the exact SOURCE URL printed above its evidence.
If a conflict cannot be resolved from product/variant/market context, place it in unresolved_conflicts.
Unknown attributes must be preserved in unmapped_attributes; proposing a field does not change schema.

FRAGMENTS:
{fragments}
"""
    raw, usage = GeminiClient().generate_json(prompt, SEMANTIC_SCHEMA)
    return json.loads(raw), usage, len(fragments)
