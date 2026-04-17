from phantomscope.models.schemas import CertificateObservation, DomainInfrastructure, DomainVariation, RiskSignal


def score_asset(
    variation: DomainVariation,
    certificates: list[CertificateObservation],
    infrastructure: DomainInfrastructure,
) -> tuple[int, str, list[RiskSignal]]:
    score = 0
    signals: list[RiskSignal] = []

    if variation.technique in {"homoglyph", "character-swap", "character-duplication"}:
        score += 30
        signals.append(
            RiskSignal(
                code="lookalike-technique",
                severity="high",
                reason=f"Domain uses {variation.technique} to mimic the target.",
                weight=30,
            )
        )

    if variation.technique in {"brand-prefix", "security-lure"}:
        score += 20
        signals.append(
            RiskSignal(
                code="credential-lure-pattern",
                severity="medium",
                reason="Domain contains wording commonly used in phishing login lures.",
                weight=20,
            )
        )

    if certificates:
        score += 25
        signals.append(
            RiskSignal(
                code="certificate-observed",
                severity="high",
                reason="Certificate Transparency data shows the domain has active certificate activity.",
                weight=25,
            )
        )

    if "Privacy" in (infrastructure.rdap_org or ""):
        score += 10
        signals.append(
            RiskSignal(
                code="privacy-registrant",
                severity="medium",
                reason="Registration details suggest privacy shielding.",
                weight=10,
            )
        )

    if infrastructure.ip_addresses:
        score += 10
        signals.append(
            RiskSignal(
                code="resolves-to-ip",
                severity="medium",
                reason="Domain resolves to routable infrastructure.",
                weight=10,
            )
        )

    if infrastructure.reputation_tags:
        bonus = min(15, len(infrastructure.reputation_tags) * 5)
        score += bonus
        signals.append(
            RiskSignal(
                code="reputation-tags",
                severity="medium",
                reason=f"Basic reputation heuristics produced tags: {', '.join(infrastructure.reputation_tags)}.",
                weight=bonus,
            )
        )

    priority = "low"
    if score >= 70:
        priority = "high"
    elif score >= 40:
        priority = "medium"

    return min(score, 100), priority, signals

