from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.catalog.models.current_price import CurrentPrice
from app.modules.catalog.models.price_history import PriceHistory


class PriceRepository:
    """
    Repository for CurrentPrice and PriceHistory persistence.

    Responsibilities:
    - Query current prices.
    - Create current price records.
    - Update current price records.
    - Create immutable price history records.
    - Retrieve historical price observations.

    Business rules belong in the service layer.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    # ---------------------------------------------------------
    # Current Price
    # ---------------------------------------------------------

    def get_current_price(
        self,
        marketplace_product_id: UUID,
    ) -> CurrentPrice | None:
        """
        Return the current price for a marketplace product.
        """

        statement = select(CurrentPrice).where(
            CurrentPrice.marketplace_product_id == marketplace_product_id,
            CurrentPrice.deleted_at.is_(None),
        )

        return self.db.scalar(statement)

    def create_current_price(
        self,
        marketplace_product_id: UUID,
        amount: Decimal,
        reference_amount: Decimal | None,
        currency_code: str,
        price_type: str,
        availability_status: str,
        captured_at: datetime,
    ) -> CurrentPrice:
        """
        Create a new current-price snapshot.
        """

        current_price = CurrentPrice(
            marketplace_product_id=marketplace_product_id,
            amount=amount,
            reference_amount=reference_amount,
            currency_code=currency_code,
            price_type=price_type,
            availability_status=availability_status,
            captured_at=captured_at,
        )

        self.db.add(current_price)
        self.db.flush()

        return current_price

    def update_current_price(
        self,
        current_price: CurrentPrice,
        *,
        amount: Decimal,
        reference_amount: Decimal | None,
        currency_code: str,
        price_type: str,
        availability_status: str,
        captured_at: datetime,
    ) -> CurrentPrice:
        """
        Update an existing current-price snapshot.

        The service layer decides whether an update is necessary.
        """

        current_price.amount = amount
        current_price.reference_amount = reference_amount
        current_price.currency_code = currency_code
        current_price.price_type = price_type
        current_price.availability_status = availability_status
        current_price.captured_at = captured_at

        self.db.flush()

        return current_price

    # ---------------------------------------------------------
    # Price History - Write
    # ---------------------------------------------------------

    def create_price_history(
        self,
        marketplace_product_id: UUID,
        amount: Decimal,
        reference_amount: Decimal | None,
        currency_code: str,
        price_type: str,
        availability_status: str,
        captured_at: datetime,
        raw_marketplace_payload: dict[str, Any] | None = None,
    ) -> PriceHistory:
        """
        Append a new immutable price-history record.
        """

        price_history = PriceHistory(
            marketplace_product_id=marketplace_product_id,
            amount=amount,
            reference_amount=reference_amount,
            currency_code=currency_code,
            price_type=price_type,
            availability_status=availability_status,
            captured_at=captured_at,
            raw_marketplace_payload=raw_marketplace_payload,
        )

        self.db.add(price_history)
        self.db.flush()

        return price_history

    # ---------------------------------------------------------
    # Price History - Read
    # ---------------------------------------------------------

    def get_price_history(
        self,
        marketplace_product_id: UUID,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
    ) -> list[PriceHistory]:
        """
        Retrieve historical price observations for a marketplace product.

        Results are ordered chronologically by captured_at.

        Optional:
        - start_at: inclusive lower time boundary
        - end_at: inclusive upper time boundary

        Soft-deleted records are excluded.
        """

        statement = (
            select(PriceHistory)
            .where(
                PriceHistory.marketplace_product_id
                == marketplace_product_id,
                PriceHistory.deleted_at.is_(None),
            )
            .order_by(PriceHistory.captured_at.asc())
        )

        if start_at is not None:
            statement = statement.where(
                PriceHistory.captured_at >= start_at
            )

        if end_at is not None:
            statement = statement.where(
                PriceHistory.captured_at <= end_at
            )

        return list(self.db.scalars(statement).all())

    # ---------------------------------------------------------
    # Transaction
    # ---------------------------------------------------------

    def commit(self) -> None:
        """
        Commit the current transaction.
        """

        self.db.commit()

    def rollback(self) -> None:
        """
        Roll back the current transaction.
        """

        self.db.rollback()