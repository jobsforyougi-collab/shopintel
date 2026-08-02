from fastapi import APIRouter

from app.config.settings import settings

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
        "version": settings.app_version,
        "debug": settings.debug,
    }