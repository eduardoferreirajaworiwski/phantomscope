from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

from phantomscope.models.schemas import CertificateObservation, DataOrigin, DomainInfrastructure

DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "mock"
CT_FIXTURES = json.loads((DATA_DIR / "ct_observations.json").read_text())
INFRA_FIXTURES = json.loads((DATA_DIR / "infrastructure_profiles.json").read_text())


def mock_certificate_observations(domain: str) -> list[CertificateObservation]:
    now = datetime.now(UTC)
    profile = _select_profile(domain, CT_FIXTURES)
    observations: list[CertificateObservation] = []
    for item in profile:
        identities = [entry.format(domain=domain) for entry in item.get("matching_identities", [domain])]
        observations.append(
            CertificateObservation(
                logged_at=now - timedelta(days=item.get("days_ago", 2)),
                issuer_name=item.get("issuer_name", "Mock CA"),
                common_name=domain,
                matching_identities=identities,
                source="offline-fixture",
                origin=DataOrigin.MOCK,
            )
        )
    return observations


def mock_infrastructure(domain: str) -> DomainInfrastructure:
    profile = _select_profile(domain, INFRA_FIXTURES)
    return DomainInfrastructure(
        ip_addresses=profile.get("ip_addresses", []),
        name_servers=profile.get("name_servers", []),
        rdap_org=profile.get("rdap_org"),
        registrar=profile.get("registrar"),
        asn=profile.get("asn"),
        asn_org=profile.get("asn_org"),
        hosted_country=profile.get("hosted_country"),
        reputation_tags=profile.get("reputation_tags", []),
        source="offline-fixture",
        origin=DataOrigin.MOCK,
    )


def _select_profile(domain: str, fixtures: dict[str, object]) -> object:
    for key, value in fixtures.items():
        if key != "fallback" and key in domain:
            return value
    return fixtures["fallback"]
