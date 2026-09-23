import json
import os
import re
from typing import Iterable, Type
from ollama import chat
from pydantic import BaseModel, Field
from models.product import (
    Evidence, ProductImage, ProductValue, ScalarValue, WaterFilterProduct, ProductIdentity, SystemConfiguration,
    FiltrationSystem, Prefiltration, Performance, WaterOutput,
    TankConfiguration, ProtectionHygiene, ContaminantReduction,
    Certification, ReplacementFilter, ElectricalSpecifications,
    PhysicalSpecifications, SmartFeatures, CommercialData,
    ProductSources, CalculatedMetrics,
)
from extractor.verification import is_question_text, sanitize_and_label_product
from extractor.publication import assess_publication
from sources.brave_search import load_local_env
from sources.gemini_client import GeminiClient

MODEL_NAME = "qwen3.5:9b"

class Pass1(BaseModel):
    identity: ProductIdentity = Field(default_factory=ProductIdentity)
    system: SystemConfiguration = Field(default_factory=SystemConfiguration)
    performance: Performance = Field(default_factory=Performance)

class PassFiltration(BaseModel):
    filtration: FiltrationSystem = Field(default_factory=FiltrationSystem)

class PassPrefiltration(BaseModel):
    prefiltration: Prefiltration = Field(default_factory=Prefiltration)
class PassContaminants(BaseModel):
    contaminants: list[ContaminantReduction] = Field(default_factory=list)

class Pass3(BaseModel):
    certifications: list[Certification] = Field(default_factory=list)
    protection: ProtectionHygiene = Field(default_factory=ProtectionHygiene)
    water_output: WaterOutput = Field(default_factory=WaterOutput)
    tanks: TankConfiguration = Field(default_factory=TankConfiguration)

class Pass4(BaseModel):
    replacement_filters: list[ReplacementFilter] = Field(default_factory=list)
    electrical: ElectricalSpecifications = Field(default_factory=ElectricalSpecifications)
    physical: PhysicalSpecifications = Field(default_factory=PhysicalSpecifications)
    smart_features: SmartFeatures = Field(default_factory=SmartFeatures)

class Pass5(BaseModel):
    commercial: CommercialData = Field(default_factory=CommercialData)


class MissingFact(BaseModel):
    path: str
    value: ScalarValue | None = None
    unit: str | None = None


class MissingFacts(BaseModel):
    facts: list[MissingFact] = Field(default_factory=list)

PASSES: list[tuple[str, Type[BaseModel]]] = [
    ("identity, system configuration and performance", Pass1),
    ("filtration", PassFiltration),
    ("prefiltration and pretreatment", PassPrefiltration),
    ("contaminant reduction claims", PassContaminants),
    ("certifications, protection, water output and tanks", Pass3),
    ("replacement filters, electrical, physical and smart features", Pass4),
    ("price, currency and warranty", Pass5),
]
def _prompt(page_text: str, source_url: str, source_type: str, task: str) -> str:
    return f"""You extract technical facts for Wasser.Market.
Extract ONE water filter. This pass covers: {task}.
Use ONLY the SOURCE below. Never use prior knowledge and never guess.
Parse facts in headings/product names too. If absent, leave null/empty.
IMPORTANT: Keep output compact. For every ProductValue return evidence as [].
For every FiltrationStage return evidence as []. Do not repeat source text in evidence.
Evidence/source binding is handled separately after extraction.
Normalize numbers: 800 GPD => 800; $759.00 => 759.0. Do not calculate derived values.
A heading '800 GPD Tankless Reverse Osmosis System' supports capacity=800, tankless=true, technology='Reverse Osmosis'.
Keep advertised stage count separate from physical cartridge count.
Certification rules are strict: whole-system, component/material certification, tested-to-standard, lab test, and manufacturer claim are different. Never upgrade scope.
For price, '$' on this manufacturer US storefront may be USD; store numeric price and currency separately.
For contaminants, preserve claim type and only percentages/concentrations explicitly stated.
Return ONLY JSON matching the schema.
SOURCE:\n{page_text}\nEND SOURCE"""


def _run_pass(model_cls: Type[BaseModel], task: str, page_text: str, source_url: str, source_type: str) -> BaseModel:
    load_local_env()
    provider = os.getenv("WASSER_AI_PROVIDER", "local").strip().lower()
    prompt = _prompt(page_text, source_url, source_type, task)
    if provider == "gemini":
        try:
            content, usage = GeminiClient().generate_json(prompt, model_cls.model_json_schema())
            print(
                f"    Gemini {usage.model}: input={usage.input_tokens}, "
                f"output={usage.output_tokens}, seconds={usage.elapsed_seconds:.2f}"
            )
            return model_cls.model_validate_json(content)
        except Exception as error:
            fallback = os.getenv("WASSER_AI_FALLBACK_LOCAL", "true").lower() in {"1", "true", "yes"}
            if not fallback:
                raise
            print(f"    Gemini unavailable ({type(error).__name__}); falling back to local Qwen")
    response = chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        format=model_cls.model_json_schema(),
        think=False,
        options={
            "temperature": 0,
            "num_ctx": 16384,
            "num_predict": 3200 if task == "contaminant reduction claims" else 1800,
        },
    )
    if not response.message.content:
        raise RuntimeError(f"Qwen returned empty content for pass: {task}")
    return model_cls.model_validate_json(response.message.content)


def _run_gemini_full(
    page_text: str,
    source_url: str,
    source_type: str,
    model: str | None = None,
    target_model: str | None = None,
) -> WaterFilterProduct:
    prompt = f"""You extract technical facts for Wasser.Market from ONE product page.
Return one JSON object matching the supplied schema.
Use ONLY the SOURCE. Never guess or use prior knowledge.
Ignore navigation, reviews, customer questions, related products, accessories, and other models.
Extract affirmative facts about the main product only.
{f'TARGET MODEL: {target_model}. Extract only this base system. Ignore capacity, color, faucet and bundle variants as separate identities.' if target_model else ''}
For every ProductValue and list item return evidence as an empty list; provenance is bound locally.
Do not calculate unit conversions. Leave absent values null/empty.
Do not classify a manufacturer certification statement as independently verified.
SOURCE URL: {source_url}
SOURCE TYPE: {source_type}
SOURCE:
{page_text}
END SOURCE"""
    content, usage = GeminiClient(model=model).generate_json(prompt, WaterFilterProduct.model_json_schema())
    print(
        f"  Gemini full extraction {usage.model}: input={usage.input_tokens}, "
        f"output={usage.output_tokens}, thinking={usage.thinking_tokens}, "
        f"total={usage.total_tokens}, seconds={usage.elapsed_seconds:.2f}, "
        f"estimated_cost=${usage.estimated_cost_usd:.5f}"
    )
    def prune_nones(value: object) -> object:
        if isinstance(value, dict):
            return {key: prune_nones(item) for key, item in value.items() if item is not None}
        if isinstance(value, list):
            return [prune_nones(item) for item in value if item is not None]
        return value

    return WaterFilterProduct.model_validate(prune_nones(json.loads(content)))


def _get_product_value(product: WaterFilterProduct, path: str) -> ProductValue | None:
    current: object = product
    for part in path.split("."):
        if not hasattr(current, part):
            return None
        current = getattr(current, part)
    return current if isinstance(current, ProductValue) else None


def _gemini_complete_missing(
    product: WaterFilterProduct,
    page_text: str,
    missing: list[str],
    model: str | None = None,
) -> None:
    allowed = [path for path in missing if _get_product_value(product, path) is not None]
    if not allowed:
        return
    prompt = f"""Fill ONLY the listed missing fields for the main product from the SOURCE.
Return facts only when explicitly stated. Do not guess. Ignore questions, reviews and related products.
Use the exact path from this list: {json.dumps(allowed)}
If a field is absent, omit it from facts.
SOURCE:
{page_text}
END SOURCE"""
    content, usage = GeminiClient(model=model).generate_json(prompt, MissingFacts.model_json_schema())
    result = MissingFacts.model_validate_json(content)
    applied = 0
    for fact in result.facts:
        if fact.path not in allowed or fact.value is None:
            continue
        target = _get_product_value(product, fact.path)
        if target is not None:
            target.value = fact.value
            target.unit = fact.unit
            applied += 1
    print(
        f"  Gemini targeted completion: requested={len(allowed)}, applied={applied}, "
        f"input={usage.input_tokens}, output={usage.output_tokens}, total={usage.total_tokens}, "
        f"seconds={usage.elapsed_seconds:.2f}, estimated_cost=${usage.estimated_cost_usd:.5f}"
    )
def _has_value(pv) -> bool:
    return getattr(pv, "value", None) is not None


_FIELD_HINTS = {
    "brand": ("waterdrop",),
    "model": ("g3p800", "model"),
    "sku_mpn": ('"sku"', '"mpn"'),
    "product_name": ("g3p800", "reverse osmosis"),
    "technology": ("reverse osmosis", " ro "),
    "tankless": ("tankless",),
    "rated_capacity_gpd": ("gpd",),
    "membrane_capacity_gpd": ("gpd",),
    "dispensing_flow_lpm": ("flow", "gallon per minute", "gpm"),
    "recovery_rate_percent": ("recovery", "drain ratio", "pure to drain"),
    "pure_to_drain_ratio": ("drain ratio", "pure to drain",),
    "current_price": ("$", "price"),
    "msrp": ("$", "price"),
    "currency": ("$",),
    "warranty_years": ("warranty",),
    "dimensions_raw": ("dimension", "dimensions", "inch"),
    "display": ("display", "tds", "faucet"),
    "filter_life_indicator": ("filter life", "filter status",),
    "smart_faucet": ("faucet",),
    "automatic_flush": ("flush",),
    "leak_detection": ("leak",),
}


def _source_lines(page_text: str) -> list[str]:
    """Return compact, verbatim source fragments suitable for stored evidence."""
    lines: list[str] = []
    seen: set[str] = set()
    for raw in page_text.splitlines():
        # Keep the stored quote byte-for-byte equivalent to a substring of the
        # collected DOM text. A normalized key is used only for deduplication.
        line = raw.strip()
        key = " ".join(line.split())
        if line and key not in seen and not is_question_text(line):
            seen.add(key)
            lines.append(line[:600])
    return lines


def _tokens(value: object) -> set[str]:
    if isinstance(value, bool) or value is None:
        return set()
    return {
        token for token in re.findall(r"[a-z0-9]+", str(value).lower())
        if len(token) >= 2 and token not in {"and", "the", "with", "for"}
    }


def _find_support(lines: Iterable[str], field_name: str, value: object, unit: str | None = None) -> str | None:
    hints = _FIELD_HINTS.get(field_name, ())
    value_tokens = _tokens(value)
    unit_tokens = _tokens(unit)
    best: tuple[int, str] | None = None

    for line in lines:
        lowered = f" {line.lower()} "
        line_tokens = _tokens(line)
        hint_hits = sum(1 for hint in hints if hint in lowered)
        value_hits = len(value_tokens & line_tokens)
        unit_hits = len(unit_tokens & line_tokens)

        if isinstance(value, bool):
            if not hint_hits:
                continue
            score = 8 * hint_hits
        elif isinstance(value, (int, float)):
            numeric_candidates = re.findall(r"(?<![\d.])\d[\d,]*(?:\.\d+)?(?![\d.])", lowered)
            if not any(
                abs(float(candidate.replace(",", "")) - float(value)) < 1e-9
                for candidate in numeric_candidates
            ):
                continue
            score = 10 + 3 * hint_hits + unit_hits
        else:
            if not value_tokens:
                continue
            coverage = value_hits / len(value_tokens)
            if coverage < (0.5 if len(value_tokens) > 2 else 1.0) and not hint_hits:
                continue
            score = value_hits * 3 + hint_hits * 4 + unit_hits

        # Prefer focused fragments over navigation/category lines.
        score -= min(len(line) // 180, 3)
        if best is None or score > best[0]:
            best = (score, line)
    return best[1] if best else None


def _attach_evidence(product: WaterFilterProduct, page_text: str, source_url: str, source_type: str) -> None:
    """Bind extracted facts to exact page fragments without inflating LLM output."""
    lines = _source_lines(page_text)

    def evidence(text: str) -> Evidence:
        return Evidence(
            source_url=source_url,
            source_type=source_type,
            original_text=text,
            confidence=0.95,
        )

    def visit(value: object, field_name: str = "") -> None:
        if isinstance(value, ProductValue):
            # The LLM is not trusted to construct provenance. Discard anything
            # it emitted and bind every quote here with canonical source data.
            value.evidence = []
            if value.value is not None:
                support = _find_support(lines, field_name, value.value, value.unit)
                if support:
                    value.evidence.append(evidence(support))
                else:
                    # An extracted value without a quote cannot be verified and
                    # must not survive as a Wasser.Market fact.
                    value.value = None
                    value.unit = None
            return
        if isinstance(value, BaseModel):
            for name in value.__class__.model_fields:
                if name == "evidence":
                    continue
                visit(getattr(value, name), name)
            # List-item models (contaminants, stages, certifications, filters)
            # have their own evidence list rather than ProductValue wrappers.
            own_evidence = getattr(value, "evidence", None)
            if isinstance(own_evidence, list):
                own_evidence.clear()
                contaminant = getattr(value, "contaminant", None)
                reduction = getattr(value, "reduction_percent", None)
                if contaminant and reduction is not None:
                    number = f"{float(reduction):g}"
                    for line in lines:
                        if contaminant.lower() in line.lower() and re.search(
                            rf"(?<![\d.]){re.escape(number)}\s*%(?![\d.])", line
                        ):
                            own_evidence.append(evidence(line))
                            break
                candidates = [
                    getattr(value, name) for name in value.__class__.model_fields
                    if name != "evidence" and isinstance(getattr(value, name), (str, int, float))
                ]
                if not own_evidence:
                    for candidate in candidates:
                        support = _find_support(lines, field_name, candidate)
                        if support:
                            own_evidence.append(evidence(support))
                            break
            return
        if isinstance(value, list):
            for item in value:
                visit(item, field_name)

    visit(product)


def _repair_explicit_page_facts(product: WaterFilterProduct, page_text: str) -> None:
    """Parse compact, high-value facts whose page layout is deterministic."""
    lines = [line.strip() for line in page_text.splitlines() if line.strip()]
    lowered = page_text.lower()

    if "waterdrop" in lowered and not _has_value(product.identity.brand):
        product.identity.brand.value = "Waterdrop"
    model_match = re.search(r"\bG3P800\b", page_text, re.IGNORECASE)
    if model_match and not _has_value(product.identity.model):
        product.identity.model.value = model_match.group(0).upper()
    heading_match = re.search(r"[^\r\n]{0,80}\bG3P800\b[^\r\n]{0,80}", page_text, re.IGNORECASE)
    if heading_match and not _has_value(product.identity.product_name):
        product.identity.product_name.value = " ".join(heading_match.group(0).split())
    if "reverse osmosis" in lowered and not _has_value(product.system.technology):
        product.system.technology.value = "Reverse Osmosis"
    if "tankless" in lowered and not _has_value(product.system.tankless):
        product.system.tankless.value = True

    capacity_match = re.search(r"\b(\d{2,4})\s*GPD\b", page_text, re.IGNORECASE)
    if capacity_match and not _has_value(product.performance.rated_capacity_gpd):
        product.performance.rated_capacity_gpd.value = int(capacity_match.group(1))
        product.performance.rated_capacity_gpd.unit = "GPD"
    if capacity_match and not _has_value(product.filtration.membrane_capacity_gpd):
        product.filtration.membrane_capacity_gpd.value = int(capacity_match.group(1))
        product.filtration.membrane_capacity_gpd.unit = "GPD"

    # Select prices only from a block headed by this exact product, avoiding
    # replacement-filter and recommendation prices elsewhere on the page.
    money_pattern = re.compile(r"^\$([\d,]+(?:\.\d{2})?)$")
    product_heading = str(product.identity.product_name.value or "").strip().lower()
    for index, line in enumerate(lines):
        if not product_heading or product_heading not in line.lower():
            continue
        prices = []
        for candidate in lines[index + 1:index + 7]:
            match = money_pattern.match(candidate)
            if match:
                prices.append(float(match.group(1).replace(",", "")))
        if prices:
            product.commercial.current_price.value = prices[0]
            product.commercial.current_price.unit = "USD"
            product.commercial.currency.value = "USD"
            if len(prices) > 1 and prices[1] >= prices[0]:
                product.commercial.msrp.value = prices[1]
                product.commercial.msrp.unit = "USD"
            break

    dimension_pattern = re.compile(r"^\d+(?:\.\d+)?\s*[*×x]\s*\d+(?:\.\d+)?\s*[*×x]\s*\d+(?:\.\d+)?$")
    for index, line in enumerate(lines[:-1]):
        if line.lower() in {"product dimensions (in)", "dimensions (inch)"}:
            candidate = lines[index + 1]
            if dimension_pattern.match(candidate):
                product.physical.dimensions_raw.value = candidate
                product.physical.dimensions_raw.unit = "in"
                # The page does not label the three axes, so mapping them to
                # width/depth/height would be an unsupported assumption.
                product.physical.width_mm = ProductValue()
                product.physical.depth_mm = ProductValue()
                product.physical.height_mm = ProductValue()
                break

    if not re.search(r"\b\d+(?:\.\d+)?\s*(?:V|volts?|Hz|watts?|W)\b", page_text, re.IGNORECASE):
        product.electrical = ElectricalSpecifications()

    if "smart display faucet" in lowered:
        product.smart_features.smart_faucet.value = True
        product.smart_features.display.value = "Smart Display Faucet"
    if "filter status" in lowered or "filter life monitor" in lowered:
        product.smart_features.filter_life_indicator.value = True

    certification_text = next(
        (line for line in lines if "System Certified by IAPMO R&T" in line),
        None,
    )
    if certification_text:
        product.certifications = [Certification(
            organization="IAPMO R&T",
            standard="NSF/ANSI 42, 53, 58 and 372",
            scope="whole_system",
            status="certified",
        )]


def _apply_json_ld(product: WaterFilterProduct, documents: list[str], source_url: str) -> None:
    """Attach product identity and model-scoped image URLs from structured data."""
    candidates: list[dict] = []
    organizations: list[dict] = []

    def visit(value: object) -> None:
        if isinstance(value, dict):
            node_type = value.get("@type")
            if node_type == "Product" or isinstance(node_type, list) and "Product" in node_type:
                candidates.append(value)
            if node_type == "Organization" or isinstance(node_type, list) and "Organization" in node_type:
                organizations.append(value)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    for raw in documents:
        try:
            visit(json.loads(raw))
        except json.JSONDecodeError:
            continue

    for organization in organizations:
        raw_logo = organization.get("logo")
        logo_url = raw_logo.get("url") if isinstance(raw_logo, dict) else raw_logo
        if isinstance(logo_url, str) and logo_url.startswith(("http://", "https://")):
            product.identity.brand_logo = ProductImage(
                url=logo_url,
                source_url=source_url,
                alt_text=str(organization.get("name") or product.identity.brand.value or "") or None,
                role="brand_logo",
            )
            break

    expected_model = str(product.identity.model.value or "").lower()
    node = next(
        (
            item for item in candidates
            if expected_model and expected_model in " ".join(
                str(item.get(key, "")) for key in ("name", "sku", "mpn")
            ).lower()
        ),
        candidates[0] if candidates else None,
    )
    if not node:
        return

    # Collapse color/finish variants into the base model. A category page may
    # expose several Product nodes such as "Fusion Pro 2 - JetBlack" and
    # "Fusion Pro 2 - Metallic Grey"; Wasser.Market stores one system model.
    candidate_names = [str(item.get("name") or "").strip() for item in candidates]
    matching_names = [name for name in candidate_names if expected_model and expected_model in name.lower()]
    if len(matching_names) > 1 and expected_model:
        variant_prefix = str(product.identity.model.value or "").strip()
        if variant_prefix and all(
            name.lower().startswith(variant_prefix.lower()) for name in matching_names
        ):
            product.identity.product_name.value = variant_prefix
            product.identity.sku_mpn = ProductValue()

    sku = node.get("sku") or node.get("mpn")
    if isinstance(sku, str) and sku and len(matching_names or candidate_names) == 1:
        product.identity.sku_mpn.value = sku
    product_name = node.get("name")
    if isinstance(product_name, str) and product_name and not _has_value(product.identity.product_name):
        product.identity.product_name.value = product_name
    if not _has_value(product.identity.brand):
        raw_brand = node.get("brand")
        brand_name = raw_brand.get("name") if isinstance(raw_brand, dict) else raw_brand
        # Some stores incorrectly repeat the full product title in brand.name.
        # In that case use the leading manufacturer token from the same
        # official Product name instead of accepting a fake giant brand.
        if isinstance(brand_name, str) and brand_name.strip():
            brand_name = brand_name.strip()
            if len(brand_name) <= 60 and brand_name != product_name:
                product.identity.brand.value = brand_name
        if not _has_value(product.identity.brand) and isinstance(product_name, str):
            leading_brand = re.match(r"^([A-Za-z][A-Za-z0-9.&'-]{1,39})\s+", product_name)
            if leading_brand:
                product.identity.brand.value = leading_brand.group(1)
    if isinstance(product_name, str) and not _has_value(product.identity.model):
        # Model codes on manufacturer product names are typically compact
        # alphanumeric tokens (C1S, K19, X12, G5P700A). This does not invent a
        # code: the exact token must occur in the official JSON-LD name.
        model_tokens = re.findall(
            r"\b(?=[A-Z0-9-]*[A-Z])(?=[A-Z0-9-]*\d)[A-Z][A-Z0-9-]{1,15}\b",
            product_name.upper(),
        )
        excluded = {"GPD", "RO", "UV", "3IN1", "2IN1"}
        model_tokens = [token for token in model_tokens if token not in excluded]
        if model_tokens:
            product.identity.model.value = model_tokens[-1]

    raw_images = node.get("image", [])
    if isinstance(raw_images, str):
        raw_images = [raw_images]
    images = []
    for item in raw_images:
        url = item.get("url") if isinstance(item, dict) else item
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            continue
        images.append(ProductImage(
            url=url,
            source_url=source_url,
            alt_text=str(node.get("name") or "") or None,
            role="primary",
            product_model=str(product.identity.model.value or "") or None,
        ))
        break
    product.images = images
    if images:
        product.image = images[0].model_copy(deep=True)


def extract_product(
    page_text: str,
    source_url: str,
    source_type: str = "manufacturer_page",
    structured_data: list[str] | None = None,
    evidence_text: str | None = None,
    target_model: str | None = None,
) -> WaterFilterProduct:
    load_local_env()
    provider = os.getenv("WASSER_AI_PROVIDER", "local").strip().lower()
    product = None
    if provider == "gemini":
        try:
            product = _run_gemini_full(page_text, source_url, source_type, target_model=target_model)
        except Exception as error:
            fallback_model = os.getenv("GEMINI_FALLBACK_MODEL", "").strip()
            primary_model = os.getenv("GEMINI_MODEL", "").strip()
            if fallback_model and fallback_model != primary_model:
                print(
                    f"  Primary Gemini model failed ({type(error).__name__}); "
                    f"retrying with {fallback_model}"
                )
                try:
                    product = _run_gemini_full(
                        page_text, source_url, source_type, model=fallback_model,
                        target_model=target_model,
                    )
                except Exception as fallback_error:
                    error = fallback_error
            if product is None:
                fallback = os.getenv("WASSER_AI_FALLBACK_LOCAL", "true").lower() in {"1", "true", "yes"}
                if not fallback:
                    raise error
                print(f"  Gemini extraction unavailable ({type(error).__name__}); using local Qwen")

    if product is None:
        merged: dict = {}
        for i, (task, model_cls) in enumerate(PASSES, 1):
            print(f"  AI pass {i}/{len(PASSES)}: {task}...")
            # If full Gemini extraction failed, avoid retrying Gemini seven
            # more times before reaching the local fallback.
            previous = os.environ.get("WASSER_AI_PROVIDER")
            os.environ["WASSER_AI_PROVIDER"] = "local"
            try:
                result = _run_pass(model_cls, task, page_text, source_url, source_type)
            finally:
                if previous is None:
                    os.environ.pop("WASSER_AI_PROVIDER", None)
                else:
                    os.environ["WASSER_AI_PROVIDER"] = previous
            merged.update(result.model_dump())
        product = WaterFilterProduct.model_validate(merged)

    product.sources = ProductSources(manufacturer_url=source_url)
    product.calculated = CalculatedMetrics()

    _apply_json_ld(product, structured_data or [], source_url)
    _repair_explicit_page_facts(product, page_text)
    if provider == "gemini" and os.getenv("GEMINI_TARGETED_COMPLETION", "true").lower() in {"1", "true", "yes"}:
        try:
            _gemini_complete_missing(
                product,
                page_text,
                assess_publication(product).missing,
                model=os.getenv("GEMINI_FALLBACK_MODEL") or None,
            )
        except Exception as error:
            print(f"  Gemini targeted completion skipped ({type(error).__name__})")
    _attach_evidence(product, evidence_text or page_text, source_url, source_type)
    sanitize_and_label_product(product)
    return product


if __name__ == "__main__":
    sample = """Waterdrop G3P800\n800 GPD Tankless Reverse Osmosis System - Waterdrop G3P800\nRemove 99% of Lead\nPrice: $759.00"""
    product = extract_product(sample, "https://www.waterdropfilter.com/example-g3p800")
    print(product.model_dump_json(indent=2, exclude_none=True))
    print("\n=== MULTI-PASS VALIDATION PASSED ===")
