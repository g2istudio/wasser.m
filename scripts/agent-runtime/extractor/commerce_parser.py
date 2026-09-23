"""Deterministic product extraction for common commerce platforms.

The parser deliberately uses only data printed by the official product page:
JSON-LD, OpenGraph metadata, specification tables/lists and visible text.  It
never calls a language model.  Unknown or ambiguous values remain empty so the
publication gate can hold the record for review.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import re
from typing import Iterable
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

from crawler.page_collector import PageSnapshot, product_json_ld_documents
from models.product import Evidence, ProductImage, ProductSources, ProductValue, WaterFilterProduct


TODAY = datetime.now(timezone.utc).date().isoformat()
USER_AGENT = "WasserMarketAgent/1.0 (+https://wasser.market)"


@dataclass(frozen=True)
class CommercePage:
    platform: str
    soup: BeautifulSoup
    snapshot: PageSnapshot
    product: dict
    specs: dict[str, tuple[str, str]]


def _clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _key(value: object) -> str:
    text = _clean(value).casefold().rstrip(":")
    return text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")


def _number(value: str | None) -> float | None:
    match = re.search(r"(?<!\d)(\d+(?:[.,]\d+)?)(?!\d)", value or "")
    return float(match.group(1).replace(",", ".")) if match else None


def _integer(value: str | None) -> int | None:
    parsed = _number(value)
    return int(parsed) if parsed is not None else None


def _single_integer(value: str | None) -> int | None:
    numbers = re.findall(r"(?<!\d)\d+(?!\d)", value or "")
    return int(numbers[0]) if len(set(numbers)) == 1 else None


def _boolean(value: str | None) -> bool | None:
    cleaned = _key(value)
    if cleaned in {"yes", "ja", "true", "included", "vorhanden"}:
        return True
    if cleaned in {"no", "nein", "false", "not included", "nicht vorhanden"}:
        return False
    return None


def _evidence(value, quote: str, url: str, unit: str | None = None) -> ProductValue:
    return ProductValue(
        value=value,
        unit=unit,
        verification_status="official_specification",
        checked_at=TODAY,
        evidence=[Evidence(
            source_url=url,
            source_type="manufacturer_page",
            original_text=_clean(quote),
            confidence=0.98,
            verification_status="official_specification",
            checked_at=TODAY,
        )],
    )


def detect_platform(html: str, headers: dict[str, str] | None = None) -> str:
    text = html.casefold()
    powered = str((headers or {}).get("x-powered-by", "")).casefold()
    if "cdn.shopify.com" in text or "shopify.theme" in text or "shopify-section" in text:
        return "shopify"
    if "woocommerce" in text or "wp-content/plugins/woocommerce" in text:
        return "woocommerce"
    if "shopware" in text or "data-shopware" in text or "sw-product" in text:
        return "shopware"
    if "magento" in text or "mage-cache" in text:
        return "magento"
    if "prestashop" in text:
        return "prestashop"
    if "bigcommerce" in text or "stencil-utils" in text:
        return "bigcommerce"
    if "woocommerce" in powered:
        return "woocommerce"
    return "generic-jsonld"


def _walk_json(value: object) -> Iterable[dict]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_json(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_json(child)


def _json_documents(soup: BeautifulSoup) -> list[object]:
    result = []
    for node in soup.select('script[type="application/ld+json"]'):
        try:
            result.append(json.loads(node.get_text()))
        except (json.JSONDecodeError, TypeError):
            continue
    return result


def _product_node(documents: list[object], model: str) -> dict:
    products = []
    for document in documents:
        for node in _walk_json(document):
            node_type = node.get("@type")
            if node_type == "Product" or isinstance(node_type, list) and "Product" in node_type:
                products.append(node)
    expected = _key(model)
    matching = [item for item in products if expected and expected in _key(item.get("name"))]
    return (matching or products or [{}])[0]


def _specs(soup: BeautifulSoup) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}

    def add(label: object, value: object) -> None:
        raw_label, raw_value = _clean(label), _clean(value)
        key = _key(raw_label)
        if key and raw_value and len(key) <= 120 and len(raw_value) <= 500:
            result.setdefault(key, (raw_value, raw_value))

    for row in soup.select("tr"):
        cells = [_clean(cell.get_text(" ", strip=True)) for cell in row.select("th,td")]
        if len(cells) >= 2:
            add(cells[0], cells[1])
    for term in soup.select("dt"):
        definition = term.find_next_sibling("dd")
        if definition:
            add(term.get_text(" ", strip=True), definition.get_text(" ", strip=True))
    for item in soup.select("li, p"):
        text = _clean(item.get_text(" ", strip=True))
        if ":" in text:
            label, value = text.split(":", 1)
            add(label, value)
    return result


def _lookup(specs: dict[str, tuple[str, str]], *labels: str) -> tuple[str, str] | None:
    wanted = [_key(label) for label in labels]
    for label in wanted:
        if label in specs:
            return specs[label]
    for key, value in specs.items():
        if any(label in key for label in wanted if len(label) >= 5):
            return value
    return None


def _meta(soup: BeautifulSoup, *names: str) -> str:
    for name in names:
        node = soup.find("meta", attrs={"property": name}) or soup.find("meta", attrs={"name": name})
        if node and node.get("content"):
            return _clean(node.get("content"))
    return ""


def _absolute_image(value: object, url: str) -> str:
    if isinstance(value, list):
        value = value[0] if value else ""
    if isinstance(value, dict):
        value = value.get("url") or value.get("contentUrl") or ""
    candidate = urljoin(url, _clean(value))
    if not candidate.startswith("https://") or candidate.rstrip("/") == url.rstrip("/"):
        return ""
    path = candidate.split("?", 1)[0].casefold()
    image_markers = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif", "/cdn/", "/media/", "/image/")
    return candidate if any(marker in path for marker in image_markers) else ""


def _find_quote(text: str, *terms: str) -> str:
    for term in terms:
        match = re.search(re.escape(term), text, re.I)
        if match:
            return match.group(0)
    return ""


def _brand_logo(documents: list[object], soup: BeautifulSoup, url: str) -> str:
    for document in documents:
        for node in _walk_json(document):
            node_type = node.get("@type")
            if node_type in {"Organization", "Brand"}:
                logo = _absolute_image(node.get("logo"), url)
                if logo:
                    return logo
    for image in soup.select("header img, img.logo, .logo img, [class*=logo] img"):
        attrs = " ".join((_clean(image.get("src")), _clean(image.get("alt")), _clean(image.get("class"))))
        if "logo" in attrs.casefold():
            logo = _absolute_image(image.get("src") or image.get("data-src"), url)
            if logo:
                return logo
    return ""


def load_commerce_page(url: str, model: str) -> CommercePage:
    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=35)
    response.raise_for_status()
    if not response.encoding or response.encoding.casefold() in {"ascii", "iso-8859-1"}:
        response.encoding = response.apparent_encoding or "utf-8"
    if "�" in response.text and response.apparent_encoding:
        response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "lxml")
    documents = _json_documents(soup)
    snapshot = PageSnapshot(
        url=str(response.url),
        title=_clean(soup.title.get_text(" ", strip=True) if soup.title else ""),
        visible_text=_clean(soup.get_text("\n", strip=True))[:100_000],
        json_ld=[json.dumps(item, ensure_ascii=False) for item in documents],
    )
    return CommercePage(
        platform=detect_platform(response.text, dict(response.headers)),
        soup=soup,
        snapshot=snapshot,
        product=_product_node(documents, model),
        specs=_specs(soup),
    )


def _set_boolean(target, attr: str, item: tuple[str, str] | None, url: str, invert: bool = False) -> None:
    if not item:
        return
    parsed = _boolean(item[0])
    if parsed is not None:
        setattr(target, attr, _evidence(not parsed if invert else parsed, item[1], url))


def _set_number(target, attr: str, item: tuple[str, str] | None, url: str, unit: str) -> None:
    if item and _number(item[0]) is not None:
        setattr(target, attr, _evidence(_number(item[0]), item[1], url, unit))


def extract_commerce_product(url: str, brand: str, model: str) -> tuple[WaterFilterProduct, PageSnapshot, str]:
    page = load_commerce_page(url, model)
    soup, node, specs = page.soup, page.product, page.specs
    source = page.snapshot.url
    title = _clean(node.get("name")) or _clean((soup.select_one("h1") or soup.title).get_text(" ", strip=True))
    image = _absolute_image(node.get("image"), source) or _absolute_image(_meta(soup, "og:image", "twitter:image"), source)
    documents = _json_documents(soup)
    logo = _brand_logo(documents, soup, source)

    product = WaterFilterProduct()
    product.identity.brand = _evidence(brand, brand, source)
    product.identity.model = _evidence(model, model if model in page.snapshot.evidence_text else title, source)
    product.identity.product_name = _evidence(title, title, source)
    product.identity.manufacturer_name = _evidence(brand, brand, source)
    sku = _clean(node.get("mpn") or node.get("sku"))
    if sku:
        product.identity.sku_mpn = _evidence(sku, sku, source)
    product.identity.brand_logo = ProductImage(url=logo or None, source_url=source, alt_text=brand, role="brand_logo", product_model=model)
    product.image = ProductImage(url=image or None, source_url=source, alt_text=title, role="primary", product_model=model)
    product.images = [product.image] if image else []

    structured_description = _clean(node.get("description"))
    scoped_text = f"{title} {structured_description}"
    haystack = scoped_text.casefold()
    technology_quote = _find_quote(scoped_text, "reverse osmosis", "umkehrosmose", "osmoseanlage", "RO membrane")
    if not technology_quote:
        ro_membrane = _lookup(specs, "ro membrane", "reverse osmosis membrane", "umkehrosmosemembran")
        if ro_membrane and _boolean(ro_membrane[0]) is True:
            technology_quote = _find_quote(page.snapshot.evidence_text, "RO membrane", "reverse osmosis membrane", "Umkehrosmosemembran")
    if technology_quote:
        product.system.technology = _evidence("Reverse Osmosis", technology_quote, source)

    installation = _lookup(specs, "installation type", "installation", "installationsart", "montageart")
    if installation:
        product.system.installation_type = _evidence(installation[0], installation[1], source)
    else:
        for terms, normalized in ((('countertop', 'auftisch'), 'Tabletop'), (('under sink', 'under-sink', 'undersink', 'untertisch'), 'Under-counter')):
            quote = _find_quote(scoped_text, *terms)
            if quote:
                product.system.installation_type = _evidence(normalized, quote, source)
                break

    _set_boolean(product.system, "tankless", _lookup(specs, "tankless", "tanklos"), source)
    _set_boolean(product.system, "tankless", _lookup(specs, "tank available", "tank vorhanden"), source, invert=True)
    _set_boolean(product.system, "electricity_required", _lookup(specs, "power connection required", "stromanschluss erforderlich"), source)
    _set_boolean(product.system, "built_in_pump", _lookup(specs, "booster pump", "integrated pump", "pumpe"), source)

    stages = _lookup(specs, "filtration stages", "filter stages", "filterstufen", "anzahl filterstufen")
    if not stages:
        matches = list(re.finditer(r"\b(\d{1,2})[- ](?:stage|stufige|stufen)\b", scoped_text, re.I))
        values = {match.group(1) for match in matches}
        stages = (matches[0].group(1), matches[0].group(0)) if len(values) == 1 else None
    if stages and _single_integer(stages[0]) is not None:
        stage_count = _single_integer(stages[0])
        product.filtration.advertised_stage_count = _evidence(stage_count, stages[1], source)
        product.filtration.physical_filter_count = _evidence(stage_count, stages[1], source)
    if technology_quote:
        product.filtration.membrane_type = _evidence("Reverse Osmosis", technology_quote, source)

    capacity = _lookup(specs, "ro membrane capacity", "membrane capacity", "membranleistung", "capacity gpd")
    if not capacity:
        matches = list(re.finditer(r"\b(\d{2,4})\s*GPD\b", scoped_text, re.I))
        values = {match.group(1) for match in matches}
        capacity = (matches[0].group(1), matches[0].group(0)) if len(values) == 1 else None
    if capacity and _integer(capacity[0]) is not None:
        gpd = _integer(capacity[0])
        product.filtration.membrane_capacity_gpd = _evidence(gpd, capacity[1], source, "GPD")
        product.performance.rated_capacity_gpd = _evidence(gpd, capacity[1], source, "GPD")

    flow = _lookup(specs, "clear water flow rate", "purified water flow rate", "flow rate", "durchfluss", "wasserleistung")
    if flow:
        value = _number(flow[0])
        if value is not None:
            if re.search(r"(?:l/h|liter.*hour|litre.*hour)", flow[0], re.I):
                value = round(value / 60, 3)
            product.performance.dispensing_flow_lpm = _evidence(value, flow[1], source, "L/min")
    ratio = _lookup(specs, "pure water-to-drain ratio", "pure to drain ratio", "reinwasser-abwasser-verhaeltnis", "wastewater ratio")
    if ratio:
        product.performance.pure_to_drain_ratio = _evidence(ratio[0], ratio[1], source)

    dimensions = _lookup(specs, "dimensions product", "product dimensions", "dimensions", "abmessungen", "masse")
    if not dimensions:
        match = re.search(r"\b\d+(?:[.,]\d+)?\s*[x×]\s*\d+(?:[.,]\d+)?\s*[x×]\s*\d+(?:[.,]\d+)?\s*(?:cm|mm|in(?:ch(?:es)?)?)\b", page.snapshot.visible_text, re.I)
        dimensions = (match.group(0), match.group(0)) if match else None
    if dimensions:
        normalized_dimensions = re.sub(r"(?<=\d)\s*[^\w\s.,]\s*(?=\d)", " × ", dimensions[0])
        product.physical.dimensions_raw = _evidence(normalized_dimensions, dimensions[1], source)
    _set_number(product.physical, "weight_kg", _lookup(specs, "net weight", "weight", "gewicht netto", "gewicht"), source, "kg")
    _set_boolean(product.water_output, "remineralization", _lookup(specs, "remineralization", "remineralisierung"), source)
    _set_boolean(product.water_output, "hot_water", _lookup(specs, "hot water", "heisswasser"), source)
    _set_boolean(product.water_output, "cold_water", _lookup(specs, "active water cooling", "cold water", "kaltwasser"), source)
    _set_boolean(product.protection, "uv_disinfection", _lookup(specs, "uv disinfection", "uv sterilization", "uv-desinfektion"), source)
    _set_boolean(product.smart_features, "display", _lookup(specs, "display"), source)
    _set_boolean(product.smart_features, "filter_life_indicator", _lookup(specs, "filter replacement indicator", "filterstatusanzeige"), source)
    _set_boolean(product.smart_features, "outlet_tds_display", _lookup(specs, "tds display", "tds-anzeige"), source)

    voltage = _lookup(specs, "mains voltage", "voltage", "spannung")
    if voltage:
        product.electrical.voltage = _evidence(voltage[0], voltage[1], source)
    _set_number(product.electrical, "maximum_power_w", _lookup(specs, "power watt", "rated power", "max power", "leistung"), source, "W")

    offers = node.get("offers") or {}
    if isinstance(offers, list):
        offers = offers[0] if offers else {}
    if isinstance(offers, dict):
        price = offers.get("price") or offers.get("lowPrice")
        currency = _clean(offers.get("priceCurrency"))
        if price is not None and _number(str(price)) is not None:
            product.commercial.current_price = _evidence(_number(str(price)), str(price), source, currency or None)
        if currency:
            product.commercial.currency = _evidence(currency, currency, source)
    product.sources = ProductSources(manufacturer_url=source)
    return product, page.snapshot, page.platform
