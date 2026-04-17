from phantomscope.models.schemas import TargetProfile, TargetRequest, TargetType


def build_target_profile(request: TargetRequest) -> TargetProfile:
    normalized = request.target.strip().lower()
    if request.target_type == TargetType.DOMAIN:
        parts = normalized.split(".")
        brand_keyword = parts[0]
        root_domain = normalized
        apex_domain = ".".join(parts[-2:]) if len(parts) >= 2 else normalized
    else:
        brand_keyword = normalized.replace(" ", "")
        root_domain = None
        apex_domain = None
    return TargetProfile(
        original_input=request.target,
        normalized_target=normalized,
        brand_keyword=brand_keyword,
        root_domain=root_domain,
        apex_domain=apex_domain,
    )
