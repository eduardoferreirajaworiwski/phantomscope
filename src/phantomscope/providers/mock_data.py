from __future__ import annotations

from datetime import UTC, datetime, timedelta

from phantomscope.models.schemas import CertificateObservation, DomainInfrastructure


def mock_certificate_observations(domain: str) -> list[CertificateObservation]:
    now = datetime.now(UTC)
    if "login" in domain or "secure" in domain or domain.endswith("0.com"):
        return [
            CertificateObservation(
                logged_at=now - timedelta(days=2),
                issuer_name="Let's Encrypt",
                common_name=domain,
                matching_identities=[domain],
            )
        ]
    return []


def mock_infrastructure(domain: str) -> DomainInfrastructure:
    tags: list[str] = []
    if "login" in domain:
        tags.append("credential-harvest-theme")
    if "secure" in domain:
        tags.append("brand-abuse-lure")
    if domain.endswith("0.com"):
        tags.append("fresh-lookalike")
    return DomainInfrastructure(
        ip_addresses=["198.51.100.23"] if tags else [],
        name_servers=["ns1.example-hosting.test", "ns2.example-hosting.test"] if tags else [],
        rdap_org="Privacy Protected LLC" if tags else "Example Corp",
        registrar="Namecheap" if tags else "Cloudflare",
        asn="AS64500" if tags else None,
        asn_org="Demo VPS Provider" if tags else None,
        reputation_tags=tags,
    )

