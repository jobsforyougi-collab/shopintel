from fastapi import FastAPI

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

    # -----------------------------
    # Root Endpoint
    # -----------------------------
    @app.get("/", tags=["Root"])
    async def root():
        return {
            "message": f"Welcome to {settings.app_name}"
        }

    # -----------------------------
    # Health Endpoint
    # -----------------------------
    @app.get("/health", tags=["Health"])
    async def health():
        return {
            "status": "healthy",
            "version": settings.app_version,
            "debug": settings.debug
        }

    return app


app = create_app()