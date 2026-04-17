from __future__ import annotations

from phantomscope.models.schemas import CertificateObservation, DomainInfrastructure, DomainVariation
from phantomscope.collectors.ct_logs import CTLogCollector
from phantomscope.providers.ctlog import CrtShProvider
from phantomscope.providers.enrichment import CompositeEnrichmentProvider


class EnrichmentService:
    def __init__(self, ct_provider: CrtShProvider, enrichment_provider: CompositeEnrichmentProvider) -> None:
        self.ct_collector = CTLogCollector(ct_provider)
        self.enrichment_provider = enrichment_provider

    async def enrich_asset(
        self, variation: DomainVariation
    ) -> tuple[DomainVariation, list[CertificateObservation], DomainInfrastructure]:
        certificates = await self.ct_collector.collect(variation.domain)
        infrastructure = await self.enrichment_provider.enrich(variation.domain)
        return variation, certificates, infrastructure
