from fastapi import FastAPI

from app.api.router import router as api_router
from app.config.settings import settings
from app.core.exceptions import register_exception_handlers
from app.core.cors import register_cors
from app.core.middleware import register_middleware
 
import logging

from app.core.logging import setup_logging

logger = logging.getLogger(__name__)

setup_logging()

logger.info("ShopIntel application is starting...")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI-powered Shopping Intelligence Platform API",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Register all API routes
    app.include_router(api_router)

    return app


app = create_app()

register_exception_handlers(app)

register_cors(app)

register_middleware(app)