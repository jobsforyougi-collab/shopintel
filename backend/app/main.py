from fastapi import FastAPI

from app.api.router import router as api_router
from app.config.settings import settings


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