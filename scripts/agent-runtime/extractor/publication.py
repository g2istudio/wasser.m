from dataclasses import dataclass, field

from models.product import WaterFilterProduct
from extractor.taxonomy import missing_profile_fields, profile_for


@dataclass
class PublicationAssessment:
    ready: bool
    profile: str
    missing: list[str] = field(default_factory=list)
    blocking: list[str] = field(default_factory=list)


def assess_publication(product: WaterFilterProduct) -> PublicationAssessment:
    """Category-aware minimum completeness gate for public model pages."""
    profile_config = profile_for(product)
    profile = str(profile_config["name"])

    # Identity, classification, source and primary image are required to avoid
    # publishing the wrong product. Missing technical characteristics are
    # allowed after enrichment is exhausted and are rendered as an em dash.
    blocking_fields = {
        "identity.brand": product.identity.brand.value,
        "identity.model": product.identity.model.value,
        "identity.product_name": product.identity.product_name.value,
        "system.technology": product.system.technology.value,
        "primary_image": product.images[0].url if len(product.images) == 1 else None,
        "sources.manufacturer_url": product.sources.manufacturer_url,
    }
    optional_fields = {
        "physical.dimensions_raw": product.physical.dimensions_raw.value,
        "identity.brand_logo": product.identity.brand_logo.url,
    }
    blocking = [path for path, value in blocking_fields.items() if value is None or value == ""]
    missing = [path for path, value in optional_fields.items() if value is None or value == ""]
    missing.extend(path for path in missing_profile_fields(product, profile_config) if path not in missing)
    return PublicationAssessment(ready=not blocking, profile=profile, missing=missing, blocking=blocking)
