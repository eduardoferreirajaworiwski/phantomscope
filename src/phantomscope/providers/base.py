from __future__ import annotations

from typing import Protocol

from phantomscope.models.schemas import CertificateObservation, DomainInfrastructure


class CTLogProvider(Protocol):
    async def fetch(self, domain: str) -> list[CertificateObservation]: ...


class EnrichmentProvider(Protocol):
    async def enrich(self, domain: str) -> DomainInfrastructure: ...

