from phantomscope.models.schemas import DomainVariation, TargetProfile

COMMON_TLDS = ("com", "net", "org", "co", "io", "biz")
HOMOGLYPHS = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "5"}


def generate_domain_variants(profile: TargetProfile, limit: int = 10) -> list[DomainVariation]:
    keyword = profile.brand_keyword
    variants: list[DomainVariation] = []

    def add(candidate: str, technique: str) -> None:
        if len(variants) >= limit:
            return
        if not any(item.domain == candidate for item in variants):
            variants.append(
                DomainVariation(domain=candidate, technique=technique, source_target=profile.normalized_target)
            )

    for tld in COMMON_TLDS:
        add(f"{keyword}-{tld}.{tld}", "tld-combination")
        add(f"login-{keyword}.{tld}", "brand-prefix")
        add(f"{keyword}-secure.{tld}", "security-lure")

    if len(keyword) > 3:
        add(f"{keyword[:-1]}0.{COMMON_TLDS[0]}", "character-swap")
        add(f"{keyword}{keyword[-1]}.{COMMON_TLDS[0]}", "character-duplication")

    for original, replacement in HOMOGLYPHS.items():
        if original in keyword and len(variants) < limit:
            add(f"{keyword.replace(original, replacement, 1)}.{COMMON_TLDS[0]}", "homoglyph")

    if profile.root_domain:
        add(profile.root_domain, "exact-domain")

    return variants[:limit]

