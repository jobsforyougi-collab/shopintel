from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.pricing.repositories.price_repository import PriceRepository
from app.modules.pricing.schemas.price_history import PriceHistoryResponse
from app.modules.pricing.services.price_service import PriceService


router = APIRouter(
    prefix="/pricing",
    tags=["Pricing"],
)


def get_price_service(
    db: Session = Depends(get_db),
) -> PriceService:
    """
    Build the pricing service for the current request.
    """

    repository = PriceRepository(db)

    return PriceService(
        repository=repository,
    )


@router.get(
    "/{marketplace_product_id}/history",
    response_model=PriceHistoryResponse,
)
def get_price_history(
    marketplace_product_id: UUID,
    start_at: datetime | None = Query(
        default=None,
        description="Optional inclusive start timestamp",
    ),
    end_at: datetime | None = Query(
        default=None,
        description="Optional inclusive end timestamp",
    ),
    service: PriceService = Depends(get_price_service),
) -> PriceHistoryResponse:
    """
    Return historical prices for a marketplace product.

    Used by the frontend price-history graph.
    """

    if start_at is not None and end_at is not None:
        if start_at > end_at:
            raise HTTPException(
                status_code=400,
                detail="start_at must be earlier than or equal to end_at",
            )

    history = service.get_price_history(
        marketplace_product_id=marketplace_product_id,
        start_at=start_at,
        end_at=end_at,
    )

    return PriceHistoryResponse(
        marketplace_product_id=marketplace_product_id,
        start_at=start_at,
        end_at=end_at,
        count=len(history),
        items=[
            {
                "id": item.id,
                "amount": item.amount,
                "reference_amount": item.reference_amount,
                "currency_code": item.currency_code,
                "price_type": item.price_type,
                "availability_status": item.availability_status,
                "captured_at": item.captured_at,
            }
            for item in history
        ],
    )


@router.get(
    "/{marketplace_product_id}/discount-analysis",
)
def analyze_discount(
    marketplace_product_id: UUID,
    start_at: datetime | None = Query(
        default=None,
        description="Optional inclusive start timestamp for historical analysis",
    ),
    end_at: datetime | None = Query(
        default=None,
        description="Optional inclusive end timestamp for historical analysis",
    ),
    service: PriceService = Depends(get_price_service),
):
    """
    Analyze the marketplace's current discount claim
    against observed historical prices.
    """

    if start_at is not None and end_at is not None:
        if start_at > end_at:
            raise HTTPException(
                status_code=400,
                detail="start_at must be earlier than or equal to end_at",
            )

    try:
        analysis = service.analyze_discount(
            marketplace_product_id=marketplace_product_id,
            start_at=start_at,
            end_at=end_at,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return {
        "marketplace_product_id": marketplace_product_id,
        "analysis": analysis.model_dump(),
    }