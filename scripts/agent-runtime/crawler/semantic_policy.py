"""Small deterministic policy helpers that decide when semantic work is needed."""

from semantic_resolution import minimal_fragments


def has_source_conflict(value) -> bool:
    """Return true only when an extracted value actually carries a conflict."""
    if isinstance(value, dict):
        if value.get("verification_status") == "conflicting_sources":
            return True
        if str(value.get("original_name") or "").startswith("conflict."):
            return True
        return any(has_source_conflict(item) for item in value.values())
    if isinstance(value, list):
        return any(has_source_conflict(item) for item in value)
    return False


def semantic_fragments_available(evidence_text: str, model: str, issues: list[str]) -> bool:
    """Avoid an LLM call when no relevant, source-backed fragment exists."""
    return bool(minimal_fragments(evidence_text, model, issues))
