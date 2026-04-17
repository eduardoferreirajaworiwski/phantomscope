from fastapi import APIRouter, Depends, HTTPException, Query

from phantomscope.api.dependencies import get_analysis_service
from phantomscope.models.schemas import AnalysisListResponse, AnalysisResult, ApiError, TargetRequest
from phantomscope.services.analysis import AnalysisService

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.post("", response_model=AnalysisResult, responses={500: {"model": ApiError}})
async def create_analysis(
    request: TargetRequest,
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalysisResult:
    return await service.analyze(request)


@router.get("", response_model=AnalysisListResponse)
async def list_analyses(
    limit: int = Query(default=10, ge=1, le=50),
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalysisListResponse:
    return AnalysisListResponse(analyses=service.list_recent_analyses(limit))


@router.get("/{analysis_id}", response_model=AnalysisResult, responses={404: {"model": ApiError}})
async def get_analysis(
    analysis_id: str,
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalysisResult:
    result = service.get_analysis(analysis_id)
    if result is None:
        raise HTTPException(status_code=404, detail="analysis not found")
    return result
