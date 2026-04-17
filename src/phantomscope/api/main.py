import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from phantomscope.api.routes.analyses import router as analyses_router
from phantomscope.api.routes.health import router as health_router
from phantomscope.core.config import get_settings
from phantomscope.core.logging import configure_logging

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PhantomScope API",
    description=(
        "Defensive OSINT analysis platform for phishing infrastructure "
        "and brand impersonation."
    ),
    version="0.1.0",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    logger.warning(
        "request_validation_failed",
        extra={
            "event": "request_validation_failed",
            "path": str(request.url.path),
            "errors": exc.errors(),
        },
    )
    return JSONResponse(
        status_code=422,
        content={"detail": "request validation failed", "error_code": "validation_error"},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "unhandled_api_exception",
        extra={
            "event": "unhandled_api_exception",
            "path": str(request.url.path),
            "error": str(exc),
        },
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "internal server error", "error_code": "internal_error"},
    )

app.include_router(health_router, prefix="/api/v1")
app.include_router(analyses_router, prefix="/api/v1")
