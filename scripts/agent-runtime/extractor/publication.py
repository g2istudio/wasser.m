from dataclasses import dataclass, field

from models.product import WaterFilterProduct


@dataclass
class PublicationAssessment:
    ready: bool
    profile: str
    missing: list[str] = field(default_factory=list)


def assess_publication(product: WaterFilterProduct) -> PublicationAssessment:
    """Category-aware minimum completeness gate for public model pages."""
    name = str(product.identity.product_name.value or "").lower()
    technology = str(product.system.technology.value or "").lower()
    combined = f"{name} {technology}"
    if "reverse osmosis" in combined or "umkehrosmose" in combined or " ro " in f" {combined} ":
        profile = "reverse_osmosis"
        required = {
            "system.installation_type": product.system.installation_type.value,
            "filtration.advertised_stage_count": product.filtration.advertised_stage_count.value,
            "performance.rated_capacity_gpd_or_dispensing_flow_lpm": (
                product.performance.rated_capacity_gpd.value
                or product.performance.dispensing_flow_lpm.value
            ),
        }
    elif "whole house" in combined:
        profile = "whole_house"
        required = {
            "system.installation_type": product.system.installation_type.value,
            "filtration.advertised_stage_count": product.filtration.advertised_stage_count.value,
            "performance.dispensing_flow_lpm": product.performance.dispensing_flow_lpm.value,
        }
    elif "under sink" in combined or "undersink" in combined:
        profile = "under_sink"
        required = {
            "system.installation_type": product.system.installation_type.value,
            "filtration.advertised_stage_count": product.filtration.advertised_stage_count.value,
        }
    else:
        profile = "generic_system"
        required = {
            "system.installation_type": product.system.installation_type.value,
            "filtration.advertised_stage_count": product.filtration.advertised_stage_count.value,
        }

    universal = {
        "identity.brand": product.identity.brand.value,
        "identity.model": product.identity.model.value,
        "identity.product_name": product.identity.product_name.value,
        "system.technology": product.system.technology.value,
        "physical.dimensions_raw": product.physical.dimensions_raw.value,
        "identity.brand_logo": product.identity.brand_logo.url,
        "primary_image": product.images[0].url if len(product.images) == 1 else None,
        "sources.manufacturer_url": product.sources.manufacturer_url,
    }
    missing = [path for path, value in {**universal, **required}.items() if value is None or value == ""]
    return PublicationAssessment(ready=not missing, profile=profile, missing=missing)
