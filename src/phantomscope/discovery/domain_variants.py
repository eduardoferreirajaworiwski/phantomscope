from phantomscope.models.schemas import DomainVariation, TargetProfile

COMMON_TLDS = ("com", "net", "org", "co", "io", "biz")
HOMOGLYPHS = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "5"}
LURE_TERMS = ("login", "secure", "verify", "portal")


def generate_domain_variants(profile: TargetProfile, limit: int = 10) -> list[DomainVariation]:
    keyword = profile.brand_keyword
    variants: list[DomainVariation] = []

    def add(candidate: str, technique: str, *tags: str) -> None:
        if len(variants) >= limit or "." not in candidate:
            return
        if candidate == profile.root_domain:
            return
        if not any(item.domain == candidate for item in variants):
            variants.append(
                DomainVariation(
                    domain=candidate,
                    technique=technique,
                    source_target=profile.normalized_target,
                    risk_context_tags=list(tags),
                )
            )

    for tld in COMMON_TLDS:
        for lure in LURE_TERMS:
            add(f"{lure}-{keyword}.{tld}", "brand-prefix", "credential-lure")
        add(f"{keyword}-support.{tld}", "support-lure", "support-theme")
        add(f"{keyword}-secure.{tld}", "security-lure", "credential-lure")
        add(f"{keyword}{tld}.{tld}", "tld-blend", "brand-concatenation")

    if len(keyword) > 3:
        add(f"{keyword[:-1]}.{COMMON_TLDS[0]}", "character-omission", "typing-error")
        add(f"{keyword}{keyword[-1]}.{COMMON_TLDS[0]}", "character-duplication", "typing-error")
        add(f"{keyword[:-1]}0.{COMMON_TLDS[0]}", "character-swap", "homoglyph-risk")

    for original, replacement in HOMOGLYPHS.items():
        if original in keyword and len(variants) < limit:
            add(
                f"{keyword.replace(original, replacement, 1)}.{COMMON_TLDS[0]}",
                "homoglyph",
                "homoglyph-risk",
            )

    return variants[:limit]
