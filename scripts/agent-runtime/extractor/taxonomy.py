"""Configuration-driven product classification and profile requirements."""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path


CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "product_profiles.json"


@lru_cache(maxsize=1)
def load_profiles() -> tuple[dict, ...]:
    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    profiles = tuple(data.get("profiles") or ())
    if not profiles or profiles[-1].get("name") != "generic_system":
        raise ValueError("product profile configuration must end with generic_system")
    return profiles


def value_at(product, path: str):
    current = product
    for part in path.split("."):
        current = getattr(current, part, None)
        if current is None:
            return None
    return getattr(current, "value", current)


def profile_for(product) -> dict:
    name = str(product.identity.product_name.value or "").lower()
    technology = str(product.system.technology.value or "").lower()
    combined = f" {name} {technology} "
    for profile in load_profiles():
        terms = profile.get("terms") or []
        if not terms or any(term.lower() in combined for term in terms):
            return profile
    return load_profiles()[-1]


def missing_profile_fields(product, profile: dict) -> list[str]:
    missing: list[str] = []
    for alternatives in profile.get("required") or []:
        if not any(value_at(product, path) not in (None, "") for path in alternatives):
            parents = {path.rsplit(".", 1)[0] for path in alternatives}
            if len(alternatives) > 1 and len(parents) == 1:
                parent = parents.pop()
                missing.append(parent + "." + "_or_".join(path.rsplit(".", 1)[1] for path in alternatives))
            else:
                missing.append("_or_".join(alternatives))
    return missing


def minimum_publishable_fields(profile_name: str) -> int:
    profile = next((item for item in load_profiles() if item.get("name") == profile_name), None)
    return int((profile or load_profiles()[-1]).get("minimum_publishable_evidence_fields", 4))
