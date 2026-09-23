from typing import Optional, List, Union, Literal
from pydantic import BaseModel, Field


# ============================================================
# BASIC TYPES
# ============================================================

ScalarValue = Union[str, int, float, bool]


class Evidence(BaseModel):
    """
    Evidence supporting a fact.
    """

    source_url: str

    source_type: Literal[
        "manufacturer_page",
        "manufacturer_datasheet",
        "manual",
        "certification_database",
        "laboratory_report",
        "authorized_retailer",
        "retailer",
        "other"
    ] = "manufacturer_page"

    original_text: Optional[str] = None

    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0
    )

    verification_status: Literal[
        "certified",
        "independent_lab_test",
        "tested_to_standard",
        "official_specification",
        "manufacturer_claim",
        "retailer_claim",
        "conflicting_sources",
        "unverified"
    ] = "unverified"

    checked_at: Optional[str] = None

    extraction_method: Optional[Literal[
        "json_ld", "html", "http", "firecrawl", "pdf", "gemini", "manual"
    ]] = None

    fetched_at: Optional[str] = None

    parser_version: Optional[str] = None

    schema_version: Optional[str] = None


class ProductValue(BaseModel):
    """
    Normalized value plus evidence.
    """

    value: Optional[ScalarValue] = None

    unit: Optional[str] = None

    evidence: List[Evidence] = Field(
        default_factory=list
    )

    verification_status: Literal[
        "certified",
        "independent_lab_test",
        "tested_to_standard",
        "official_specification",
        "manufacturer_claim",
        "retailer_claim",
        "conflicting_sources",
        "unverified"
    ] = "unverified"

    checked_at: Optional[str] = None


# ============================================================
# PRODUCT IMAGE
# ============================================================

class ProductImage(BaseModel):

    url: Optional[str] = None

    source_url: Optional[str] = None

    alt_text: Optional[str] = None

    role: Optional[Literal["primary", "gallery", "diagram", "brand_logo", "other"]] = None

    product_model: Optional[str] = None


# ============================================================
# IDENTITY
# ============================================================

class ProductIdentity(BaseModel):

    brand: ProductValue = Field(default_factory=ProductValue)

    model: ProductValue = Field(default_factory=ProductValue)

    series: ProductValue = Field(default_factory=ProductValue)

    product_name: ProductValue = Field(default_factory=ProductValue)

    sku_mpn: ProductValue = Field(default_factory=ProductValue)

    product_status: ProductValue = Field(default_factory=ProductValue)

    market_region: ProductValue = Field(default_factory=ProductValue)

    manufacturer_name: ProductValue = Field(default_factory=ProductValue)

    manufacturer_country: ProductValue = Field(default_factory=ProductValue)

    brand_logo: ProductImage = Field(default_factory=ProductImage)


# ============================================================
# SYSTEM / INSTALLATION
# ============================================================

class SystemConfiguration(BaseModel):

    technology: ProductValue = Field(default_factory=ProductValue)

    installation_type: ProductValue = Field(default_factory=ProductValue)

    tankless: ProductValue = Field(default_factory=ProductValue)

    separate_faucet_required: ProductValue = Field(default_factory=ProductValue)

    electricity_required: ProductValue = Field(default_factory=ProductValue)

    professional_installation_required: ProductValue = Field(
        default_factory=ProductValue
    )

    built_in_pump: ProductValue = Field(default_factory=ProductValue)


# ============================================================
# FILTRATION
# ============================================================

class FiltrationStage(BaseModel):

    stage_number: Optional[int] = None

    name: Optional[str] = None

    technology: Optional[str] = None

    micron_rating: Optional[float] = None

    description: Optional[str] = None

    evidence: List[Evidence] = Field(default_factory=list)


class FiltrationSystem(BaseModel):

    advertised_stage_count: ProductValue = Field(
        default_factory=ProductValue
    )

    physical_filter_count: ProductValue = Field(
        default_factory=ProductValue
    )

    stages: List[FiltrationStage] = Field(default_factory=list)

    membrane_type: ProductValue = Field(default_factory=ProductValue)

    membrane_brand: ProductValue = Field(default_factory=ProductValue)

    membrane_model: ProductValue = Field(default_factory=ProductValue)

    membrane_pore_size_micron: ProductValue = Field(
        default_factory=ProductValue
    )

    membrane_capacity_gpd: ProductValue = Field(
        default_factory=ProductValue
    )


# ============================================================
# PREFILTRATION / PRETREATMENT
# ============================================================

class Prefiltration(BaseModel):

    built_in_prefiltration: ProductValue = Field(
        default_factory=ProductValue
    )

    prefilter_stage_count: ProductValue = Field(
        default_factory=ProductValue
    )

    prefilter_type: ProductValue = Field(
        default_factory=ProductValue
    )

    prefilter_micron_rating: ProductValue = Field(
        default_factory=ProductValue
    )

    membrane_protection: ProductValue = Field(
        default_factory=ProductValue
    )

    external_pretreatment_required: ProductValue = Field(
        default_factory=ProductValue
    )

    softener_required_or_recommended: ProductValue = Field(
        default_factory=ProductValue
    )

    sediment_prefilter_required: ProductValue = Field(
        default_factory=ProductValue
    )

    pretreatment_notes: ProductValue = Field(
        default_factory=ProductValue
    )


# ============================================================
# PERFORMANCE
# ============================================================

class Performance(BaseModel):

    rated_capacity_gpd: ProductValue = Field(
        default_factory=ProductValue
    )

    dispensing_flow_lpm: ProductValue = Field(
        default_factory=ProductValue
    )

    recovery_rate_percent: ProductValue = Field(
        default_factory=ProductValue
    )

    pure_to_drain_ratio: ProductValue = Field(
        default_factory=ProductValue
    )

    wastewater_per_liter_pure: ProductValue = Field(
        default_factory=ProductValue
    )

    minimum_inlet_pressure: ProductValue = Field(
        default_factory=ProductValue
    )

    maximum_inlet_pressure: ProductValue = Field(
        default_factory=ProductValue
    )

    minimum_feed_temperature: ProductValue = Field(
        default_factory=ProductValue
    )

    maximum_feed_temperature: ProductValue = Field(
        default_factory=ProductValue
    )

    feed_tds_min: ProductValue = Field(default_factory=ProductValue)

    feed_tds_max: ProductValue = Field(default_factory=ProductValue)

    tds_reduction_percent: ProductValue = Field(
        default_factory=ProductValue
    )

    maximum_hardness: ProductValue = Field(
        default_factory=ProductValue
    )


# ============================================================
# WATER OUTPUT
# ============================================================

class WaterOutput(BaseModel):

    remineralization: ProductValue = Field(default_factory=ProductValue)

    remineralization_type: ProductValue = Field(
        default_factory=ProductValue
    )

    added_minerals: ProductValue = Field(default_factory=ProductValue)

    ambient_water: ProductValue = Field(default_factory=ProductValue)

    cold_water: ProductValue = Field(default_factory=ProductValue)

    hot_water: ProductValue = Field(default_factory=ProductValue)

    minimum_output_temperature: ProductValue = Field(
        default_factory=ProductValue
    )

    maximum_output_temperature: ProductValue = Field(
        default_factory=ProductValue
    )

    temperature_levels: ProductValue = Field(
        default_factory=ProductValue
    )

    portion_control: ProductValue = Field(default_factory=ProductValue)

    minimum_portion_ml: ProductValue = Field(
        default_factory=ProductValue
    )

    maximum_portion_ml: ProductValue = Field(
        default_factory=ProductValue
    )


# ============================================================
# TANKS
# ============================================================

class TankConfiguration(BaseModel):

    raw_water_tank_l: ProductValue = Field(
        default_factory=ProductValue
    )

    purified_water_tank_l: ProductValue = Field(
        default_factory=ProductValue
    )

    pressure_tank_l: ProductValue = Field(
        default_factory=ProductValue
    )

    cold_water_tank_l: ProductValue = Field(
        default_factory=ProductValue
    )

    hot_water_tank_l: ProductValue = Field(
        default_factory=ProductValue
    )


# ============================================================
# HYGIENE / PROTECTION
# ============================================================

class ProtectionHygiene(BaseModel):

    backflow_protection: ProductValue = Field(
        default_factory=ProductValue
    )

    backflow_protection_type: ProductValue = Field(
        default_factory=ProductValue
    )

    manufacturer_backflow_technology_name: ProductValue = Field(
        default_factory=ProductValue
    )

    leak_detection: ProductValue = Field(
        default_factory=ProductValue
    )

    automatic_shutoff: ProductValue = Field(
        default_factory=ProductValue
    )

    automatic_flush: ProductValue = Field(
        default_factory=ProductValue
    )

    stagnation_protection: ProductValue = Field(
        default_factory=ProductValue
    )

    uv_disinfection: ProductValue = Field(
        default_factory=ProductValue
    )

    uv_stage_count: ProductValue = Field(
        default_factory=ProductValue
    )

    microbiological_protection: ProductValue = Field(
        default_factory=ProductValue
    )

    antimicrobial_materials: ProductValue = Field(
        default_factory=ProductValue
    )


# ============================================================
# CONTAMINANT REDUCTION
# ============================================================

class ContaminantReduction(BaseModel):

    contaminant: str

    reduction_percent: Optional[float] = None

    influent_value: Optional[float] = None
    influent_unit: Optional[str] = None

    effluent_value: Optional[float] = None
    effluent_unit: Optional[str] = None

    claim_type: Literal[
        "manufacturer_claim",
        "certified",
        "independent_lab_test",
        "tested_to_standard",
        "other"
    ] = "manufacturer_claim"

    standard: Optional[str] = None

    evidence: List[Evidence] = Field(default_factory=list)


# ============================================================
# CERTIFICATIONS
# ============================================================

class Certification(BaseModel):

    organization: Optional[str] = None

    standard: Optional[str] = None

    scope: Literal[
        "whole_system",
        "component",
        "material",
        "tested_to_standard",
        "unknown"
    ] = "unknown"

    status: Literal[
        "certified",
        "listed",
        "tested",
        "manufacturer_claim",
        "unknown"
    ] = "unknown"

    certificate_number: Optional[str] = None

    verification_url: Optional[str] = None

    evidence: List[Evidence] = Field(default_factory=list)


# ============================================================
# REPLACEMENT FILTERS
# ============================================================

class ReplacementFilter(BaseModel):

    name: Optional[str] = None

    model_number: Optional[str] = None

    filter_type: Optional[str] = None

    lifetime_months: Optional[float] = None

    capacity_liters: Optional[float] = None

    price: Optional[float] = None

    currency: Optional[str] = None

    source_url: Optional[str] = None

    evidence: List[Evidence] = Field(default_factory=list)


# ============================================================
# ELECTRICAL
# ============================================================

class ElectricalSpecifications(BaseModel):

    voltage: ProductValue = Field(default_factory=ProductValue)

    frequency_hz: ProductValue = Field(default_factory=ProductValue)

    standby_power_w: ProductValue = Field(default_factory=ProductValue)

    filtration_power_w: ProductValue = Field(default_factory=ProductValue)

    heating_power_w: ProductValue = Field(default_factory=ProductValue)

    cooling_power_w: ProductValue = Field(default_factory=ProductValue)

    maximum_power_w: ProductValue = Field(default_factory=ProductValue)

    ip_rating: ProductValue = Field(default_factory=ProductValue)


# ============================================================
# PHYSICAL SPECIFICATIONS
# ============================================================

class PhysicalSpecifications(BaseModel):

    dimensions_raw: ProductValue = Field(default_factory=ProductValue)

    width_mm: ProductValue = Field(default_factory=ProductValue)

    depth_mm: ProductValue = Field(default_factory=ProductValue)

    height_mm: ProductValue = Field(default_factory=ProductValue)

    weight_kg: ProductValue = Field(default_factory=ProductValue)

    noise_db: ProductValue = Field(default_factory=ProductValue)


# ============================================================
# SMART FEATURES
# ============================================================

class SmartFeatures(BaseModel):

    display: ProductValue = Field(default_factory=ProductValue)

    inlet_tds_display: ProductValue = Field(default_factory=ProductValue)

    outlet_tds_display: ProductValue = Field(default_factory=ProductValue)

    filter_life_indicator: ProductValue = Field(
        default_factory=ProductValue
    )

    smart_faucet: ProductValue = Field(default_factory=ProductValue)

    wifi: ProductValue = Field(default_factory=ProductValue)

    mobile_app: ProductValue = Field(default_factory=ProductValue)

    error_alerts: ProductValue = Field(default_factory=ProductValue)


# ============================================================
# COMMERCIAL DATA
# ============================================================

class CommercialData(BaseModel):

    current_price: ProductValue = Field(default_factory=ProductValue)

    msrp: ProductValue = Field(default_factory=ProductValue)

    currency: ProductValue = Field(default_factory=ProductValue)

    warranty_years: ProductValue = Field(default_factory=ProductValue)


# ============================================================
# CALCULATED WASSER.MARKET VALUES
# These should NOT be generated by AI.
# Python calculates them later.
# ============================================================

class CalculatedMetrics(BaseModel):

    rated_capacity_l_day: Optional[float] = None

    rated_capacity_l_hour: Optional[float] = None

    theoretical_flow_lpm: Optional[float] = None

    calculated_wastewater_per_liter: Optional[float] = None

    estimated_filter_cost_per_year: Optional[float] = None

    estimated_cost_3_years: Optional[float] = None

    estimated_cost_5_years: Optional[float] = None

    estimated_cost_per_1000_l: Optional[float] = None


# ============================================================
# SOURCE INFORMATION
# ============================================================

class ProductSources(BaseModel):

    manufacturer_url: Optional[str] = None

    manual_url: Optional[str] = None

    datasheet_url: Optional[str] = None

    certification_urls: List[str] = Field(default_factory=list)

    laboratory_report_urls: List[str] = Field(default_factory=list)

    additional_urls: List[str] = Field(default_factory=list)


class UnmappedAttribute(BaseModel):
    original_name: str
    value: ScalarValue
    unit: Optional[str] = None
    source_url: str
    evidence: str
    extraction_method: Literal["json_ld", "html", "http", "firecrawl", "pdf", "gemini", "manual"]
    confidence: float = Field(ge=0.0, le=1.0)
    fetched_at: Optional[str] = None
    proposed_field: Optional[str] = None
    parser_version: Optional[str] = None
    schema_version: Optional[str] = None


# ============================================================
# MAIN WATER FILTER PRODUCT
# ============================================================

class WaterFilterProduct(BaseModel):

    canonical_product_id: Optional[str] = None

    canonical_variant_id: Optional[str] = None

    taxonomy: str = "UNKNOWN/NEW_TYPE"

    schema_version: str = "1"

    identity: ProductIdentity = Field(default_factory=ProductIdentity)

    image: ProductImage = Field(default_factory=ProductImage)

    images: List[ProductImage] = Field(default_factory=list)

    system: SystemConfiguration = Field(
        default_factory=SystemConfiguration
    )

    filtration: FiltrationSystem = Field(
        default_factory=FiltrationSystem
    )

    prefiltration: Prefiltration = Field(
        default_factory=Prefiltration
    )

    performance: Performance = Field(
        default_factory=Performance
    )

    water_output: WaterOutput = Field(
        default_factory=WaterOutput
    )

    tanks: TankConfiguration = Field(
        default_factory=TankConfiguration
    )

    protection: ProtectionHygiene = Field(
        default_factory=ProtectionHygiene
    )

    contaminants: List[ContaminantReduction] = Field(
        default_factory=list
    )

    certifications: List[Certification] = Field(
        default_factory=list
    )

    replacement_filters: List[ReplacementFilter] = Field(
        default_factory=list
    )

    electrical: ElectricalSpecifications = Field(
        default_factory=ElectricalSpecifications
    )

    physical: PhysicalSpecifications = Field(
        default_factory=PhysicalSpecifications
    )

    smart_features: SmartFeatures = Field(
        default_factory=SmartFeatures
    )

    commercial: CommercialData = Field(
        default_factory=CommercialData
    )

    sources: ProductSources = Field(
        default_factory=ProductSources
    )

    calculated: CalculatedMetrics = Field(
        default_factory=CalculatedMetrics
    )

    unmapped_attributes: List[UnmappedAttribute] = Field(default_factory=list)


# ============================================================
# INTERNAL AGENT RECORD
#
# IMPORTANT:
# Qwen should NOT decide these values.
# Python/database logic manages them.
# ============================================================

class ProductRecord(BaseModel):

    product: WaterFilterProduct

    status: Literal[
        "FOUND",
        "COLLECTED",
        "AI_EXTRACTED",
        "VERIFIED",
        "DATA_VERIFIED",
        "PUBLISHABLE_PARTIAL",
        "PUBLISH_READY",
        "NEEDS_REVIEW",
        "CONFLICT",
        "DRAFT",
        "PUBLISHED"
    ] = "FOUND"

    needs_review: bool = True

    last_verified: Optional[str] = None

    source_conflict: bool = False
