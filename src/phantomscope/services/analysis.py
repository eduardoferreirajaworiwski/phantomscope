from __future__ import annotations

import asyncio
import logging

from phantomscope.core.config import Settings
from phantomscope.db.repository import AnalysisRepository
from phantomscope.discovery.domain_variants import generate_domain_variants
from phantomscope.discovery.targets import build_target_profile
from phantomscope.enrichment.service import EnrichmentService
from phantomscope.models.schemas import AnalysisResult, ScoredAsset, TargetRequest
from phantomscope.providers.ctlog import CrtShProvider
from phantomscope.providers.enrichment import CompositeEnrichmentProvider
from phantomscope.reporting.exporters import build_markdown_report
from phantomscope.scoring.rules import score_asset
from phantomscope.summarization.service import AnalystSummaryService

logger = logging.getLogger(__name__)


class AnalysisService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.repository = AnalysisRepository(settings.database_url)
        self.summary_service = AnalystSummaryService()

    async def analyze(self, request: TargetRequest) -> AnalysisResult:
        offline_mode = self.settings.offline_mode if request.offline_mode is None else request.offline_mode
        target_profile = build_target_profile(request)
        variations = generate_domain_variants(target_profile, request.max_variants)
        enrichment_service = EnrichmentService(
            ct_provider=CrtShProvider(self.settings, offline_mode=offline_mode),
            enrichment_provider=CompositeEnrichmentProvider(self.settings, offline_mode=offline_mode),
        )

        tasks = [enrichment_service.enrich_asset(variation) for variation in variations]
        enriched_assets = await asyncio.gather(*tasks)

        scored_assets: list[ScoredAsset] = []
        for variation, certificates, infrastructure in enriched_assets:
            score, priority, signals = score_asset(variation, certificates, infrastructure)
            if score == 0:
                continue
            scored_assets.append(
                ScoredAsset(
                    domain=variation.domain,
                    technique=variation.technique,
                    score=score,
                    priority=priority,
                    certificate_observations=certificates,
                    infrastructure=infrastructure,
                    risk_signals=signals,
                )
            )

        scored_assets.sort(key=lambda item: item.score, reverse=True)
        summary = self.summary_service.build_summary(target_profile, scored_assets)
        draft = AnalysisResult(
            target_profile=target_profile,
            assets=scored_assets,
            summary=summary,
            report_markdown="",
            metadata={"offline_mode": offline_mode, "generated_variants": len(variations)},
        )
        result = draft.model_copy(update={"report_markdown": build_markdown_report(draft)})
        self.repository.save(result)
        logger.info(
            "analysis_completed",
            extra={
                "event": "analysis_completed",
                "analysis_id": result.analysis_id,
                "target": target_profile.normalized_target,
            },
        )
        return result

    def get_analysis(self, analysis_id: str) -> AnalysisResult | None:
        return self.repository.get(analysis_id)

