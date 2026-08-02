from fastapi import APIRouter

from app.config.settings import settings

router = APIRouter()


@router.get("/", tags=["Root"])
async def root():
    return {
        "message": f"Welcome to {settings.app_name}"
    }


 