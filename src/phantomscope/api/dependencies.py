from functools import lru_cache

from phantomscope.core.config import Settings, get_settings
from phantomscope.services.analysis import AnalysisService


@lru_cache(maxsize=1)
def get_analysis_service() -> AnalysisService:
    settings: Settings = get_settings()
    return AnalysisService(settings)

