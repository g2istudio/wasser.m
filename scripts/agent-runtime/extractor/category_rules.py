"""Deterministic category and installation rules for official product pages.

These rules return normalized values plus the exact source quote. Brand-specific
adapters may enrich them, but the baseline remains platform and brand neutral.
"""

from __future__ import annotations

from collections.abc import Callable


QuoteFinder = Callable[..., str]
Lookup = Callable[..., tuple[str, str] | None]
ManualQuote = Callable[..., tuple[str, str] | None]


def classify_technology(
    source_url: str,
    scoped_text: str,
    visible_text: str,
    evidence_text: str,
    specs: dict[str, tuple[str, str]],
    *,
    find_quote: QuoteFinder,
    lookup: Lookup,
) -> tuple[str, str] | None:
    quote = find_quote(
        scoped_text, "reverse osmosis", "umkehrosmose", "osmoseanlage", "RO membrane", "RO filtration"
    )
    if quote and quote not in visible_text:
        quote = find_quote(
            visible_text, "reverse osmosis", "umkehrosmose", "osmoseanlage", "RO membrane", "RO filtration"
        )
    if not quote:
        membrane = lookup(specs, "ro membrane", "reverse osmosis membrane", "umkehrosmosemembran")
        if membrane and str(membrane[0]).strip().casefold() in {"yes", "ja", "true", "included", "vorhanden"}:
            quote = find_quote(evidence_text, "RO membrane", "reverse osmosis membrane", "Umkehrosmosemembran")
    if quote:
        return "Reverse Osmosis", quote

    url = source_url.casefold()
    candidates: tuple[str, tuple[str, ...], str] | None = None
    if "/reverse-osmosis/" in url:
        candidates = ("Reverse Osmosis", ("Reverse Osmosis",), "Reverse Osmosis")
    elif "/softener/" in url:
        candidates = ("Ion Exchange Water Softening", ("ion exchange process", "water softener"), "Ion Exchange Water Softening")
    elif any(marker in url for marker in ("/water-dispenser/", "/plumbed-in-water-dispenser/")):
        quote = find_quote(visible_text, "Water Dispenser", "drinking water filter system", "water filtration system")
        if quote:
            return ("Water Dispenser" if "dispenser" in quote.casefold() else "Water Filtration"), quote
    elif "/under-the-sink-solutions/" in url:
        candidates = (
            "Water Filtration",
            ("drinking water filtration system", "drinking water filter system", "under sink water filter system"),
            "Water Filtration",
        )
    if candidates:
        value, terms, _ = candidates
        quote = find_quote(visible_text, *terms)
        if quote:
            return value, quote
    return None


def classify_installation(
    source_url: str,
    scoped_text: str,
    visible_text: str,
    specs: dict[str, tuple[str, str]],
    manuals: list[tuple[str, str]],
    *,
    find_quote: QuoteFinder,
    lookup: Lookup,
    manual_quote: ManualQuote,
) -> tuple[str, str, str] | None:
    explicit = lookup(specs, "installation type", "installation", "installationsart", "montageart")
    if explicit:
        return explicit[0], explicit[1], source_url
    for terms, normalized in (
        (("countertop", "auftisch", "tischgeraet", "tischgerät", "tischwasserspender"), "Tabletop"),
        (("under sink", "under-sink", "undersink", "untertisch"), "Under-counter"),
    ):
        quote = find_quote(scoped_text, *terms)
        if quote:
            return normalized, quote, source_url

    combined = manual_quote(manuals, "unter der Spüle oder auf der Arbeitsfläche")
    under_counter = manual_quote(manuals, "Installationsdiagramm unter der Spüle", "Untertischeinbau")
    if combined:
        return "Under-counter / countertop", combined[0], combined[1]
    if under_counter:
        return "Under-counter", under_counter[0], under_counter[1]

    url = source_url.casefold()
    if any(marker in url for marker in ("/reverse-osmosis/", "/water-dispenser/", "/under-the-sink-solutions/")):
        quote = find_quote(
            visible_text,
            "fitted under the sink",
            "Under the sink drinking water filter system",
            "under sink water filter system",
            "under the sink solution",
        )
        if quote:
            return "Under-counter", quote, source_url
    return None
