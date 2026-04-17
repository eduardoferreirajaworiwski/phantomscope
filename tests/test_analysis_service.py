import asyncio

from phantomscope.core.config import Settings
from phantomscope.models.schemas import TargetRequest
from phantomscope.services.analysis import AnalysisService


def test_analysis_service_returns_ranked_assets(tmp_path) -> None:
    settings = Settings(
        database_url=f"sqlite:///{tmp_path}/phantomscope-test.db",
        offline_mode=True,
    )
    service = AnalysisService(settings)
    request = TargetRequest(target="acme", target_type="brand", offline_mode=True, max_variants=8)
    result = asyncio.run(service.analyze(request))
    assert result.assets
    assert result.summary.headline
    assert result.report_markdown.startswith("# PhantomScope Report")
    assert result.metadata["mock_assets"] >= 1
    assert all(asset.score_rationale for asset in result.assets)
    assert result.summary.grounding_notes
    assert any(asset.infrastructure.origin.value == "mock" for asset in result.assets)
