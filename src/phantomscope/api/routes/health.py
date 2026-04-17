from fastapi import APIRouter

from phantomscope.core.config import get_settings
from phantomscope.models.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def healthcheck() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        version="0.1.0",
        environment=settings.env,
        offline_mode=settings.offline_mode,
    )
