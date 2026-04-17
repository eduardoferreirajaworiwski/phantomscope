from fastapi import APIRouter, Depends, HTTPException

from phantomscope.api.dependencies import get_analysis_service
from phantomscope.models.schemas import AnalysisResult, TargetRequest
from phantomscope.services.analysis import AnalysisService

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.post("", response_model=AnalysisResult)
async def create_analysis(
    request: TargetRequest,
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalysisResult:
    return await service.analyze(request)


@router.get("/{analysis_id}", response_model=AnalysisResult)
async def get_analysis(
    analysis_id: str,
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalysisResult:
    result = service.get_analysis(analysis_id)
    if result is None:
        raise HTTPException(status_code=404, detail="analysis not found")
    return result

