from __future__ import annotations

from phantomscope.models.schemas import CertificateObservation
from phantomscope.providers.base import CTLogProvider


class CTLogCollector:
    def __init__(self, provider: CTLogProvider) -> None:
        self.provider = provider

    async def collect(self, domain: str) -> list[CertificateObservation]:
        return await self.provider.fetch(domain)
