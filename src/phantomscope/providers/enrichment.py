from __future__ import annotations

import logging
import socket

from phantomscope.core.config import Settings
from phantomscope.models.schemas import DataOrigin, DomainInfrastructure
from phantomscope.providers.http import HttpProvider
from phantomscope.providers.mock_data import mock_infrastructure

logger = logging.getLogger(__name__)


class CompositeEnrichmentProvider:
    def __init__(self, settings: Settings, offline_mode: bool) -> None:
        self.settings = settings
        self.offline_mode = offline_mode
        self.http = HttpProvider(settings)

    async def enrich(self, domain: str) -> DomainInfrastructure:
        if self.offline_mode:
            return mock_infrastructure(domain)

        infrastructure = DomainInfrastructure(source="live-composite", origin=DataOrigin.LIVE)
        infrastructure.ip_addresses = self._resolve_ips(domain)
        infrastructure.name_servers = []

        try:
            rdap_data = await self.http.best_effort(lambda: self.http.get_json(f"{self.settings.rdap_base_url}{domain}"))
            if isinstance(rdap_data, dict):
                infrastructure.registrar = _extract_registrar(rdap_data)
                infrastructure.rdap_org = _extract_org(rdap_data)
                infrastructure.name_servers = [item.get("ldhName", "") for item in rdap_data.get("nameservers", []) if item.get("ldhName")]
        except Exception as exc:
            logger.warning(
                "rdap_lookup_failed",
                extra={"event": "rdap_lookup_failed", "domain": domain, "error": str(exc)},
            )

        if infrastructure.ip_addresses:
            ip_context = await self.http.best_effort(
                lambda: self.http.get_json(f"{self.settings.rdap_ip_base_url}{infrastructure.ip_addresses[0]}")
            )
            if isinstance(ip_context, dict):
                start_autnum = ip_context.get("startAutnum")
                end_autnum = ip_context.get("endAutnum")
                infrastructure.asn = (
                    f"AS{start_autnum}" if isinstance(start_autnum, int) else f"AS{end_autnum}" if isinstance(end_autnum, int) else None
                )
                infrastructure.asn_org = _extract_org(ip_context) or ip_context.get("name")
                country = ip_context.get("country")
                infrastructure.hosted_country = country if isinstance(country, str) else None
            if domain.startswith("login-") or domain.endswith("secure.com") or "verify" in domain:
                infrastructure.reputation_tags.append("recent-hosting-pattern")

        return infrastructure

    @staticmethod
    def _resolve_ips(domain: str) -> list[str]:
        try:
            results = socket.getaddrinfo(domain, 443, proto=socket.IPPROTO_TCP)
        except socket.gaierror:
            return []
        ips = []
        for item in results:
            ip = item[4][0]
            if ip not in ips:
                ips.append(ip)
        return ips


def _extract_registrar(rdap_data: dict) -> str | None:
    entities = rdap_data.get("entities", [])
    for entity in entities:
        roles = entity.get("roles", [])
        if "registrar" in roles:
            vcard = entity.get("vcardArray", [])
            return _flatten_vcard(vcard)
    return None


def _extract_org(rdap_data: dict) -> str | None:
    entities = rdap_data.get("entities", [])
    for entity in entities:
        vcard = entity.get("vcardArray", [])
        org = _flatten_vcard(vcard)
        if org:
            return org
    return None


def _flatten_vcard(vcard_array: list) -> str | None:
    if len(vcard_array) < 2:
        return None
    for row in vcard_array[1]:
        if row[0] in {"fn", "org"} and len(row) >= 4:
            return row[3]
    return None
