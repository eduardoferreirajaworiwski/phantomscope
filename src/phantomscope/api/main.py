from fastapi import FastAPI

from phantomscope.api.routes.analyses import router as analyses_router
from phantomscope.api.routes.health import router as health_router
from phantomscope.core.config import get_settings
from phantomscope.core.logging import configure_logging

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(
    title="PhantomScope API",
    description="Defensive OSINT analysis platform for phishing infrastructure and brand impersonation.",
    version="0.1.0",
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(analyses_router, prefix="/api/v1")

