from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.modules.pricing.repositories.price_repository import PriceRepository
from app.modules.pricing.schemas.discount_analysis import DiscountAnalysis
from app.modules.pricing.schemas.price_observation import PriceObservation
from app.modules.pricing.services.discount_analyzer import DiscountAnalyzer


class PriceService:
    """
    Business logic for marketplace pricing.

    Responsibilities:
    - Record marketplace price observations.
    - Maintain CurrentPrice.
    - Create immutable PriceHistory records.
    - Retrieve historical pricing data.
    - Orchestrate discount analysis.
    """

    def __init__(
        self,
        repository: PriceRepository,
        discount_analyzer: DiscountAnalyzer | None = None,
    ) -> None:
        self.repository = repository
        self.discount_analyzer = (
            discount_analyzer or DiscountAnalyzer()
        )

    # ---------------------------------------------------------
    # Price observation
    # ---------------------------------------------------------

    def record_observation(
        self,
        observation: PriceObservation,
    ):
        """
        Record a normalized marketplace price observation.
        """

        current_price = self.repository.get_current_price(
            observation.marketplace_product_id
        )

        try:
            # First observation
            if current_price is None:
                current_price = self.repository.create_current_price(
                    marketplace_product_id=(
                        observation.marketplace_product_id
                    ),
                    amount=observation.amount,
                    reference_amount=observation.reference_amount,
                    currency_code=observation.currency_code,
                    price_type=observation.price_type,
                    availability_status=observation.availability_status,
                    captured_at=observation.captured_at,
                )

                self.repository.create_price_history(
                    marketplace_product_id=(
                        observation.marketplace_product_id
                    ),
                    amount=observation.amount,
                    reference_amount=observation.reference_amount,
                    currency_code=observation.currency_code,
                    price_type=observation.price_type,
                    availability_status=observation.availability_status,
                    captured_at=observation.captured_at,
                    raw_marketplace_payload=(
                        observation.raw_marketplace_payload
                    ),
                )

                self.repository.commit()

                return current_price

            # Determine meaningful change
            pricing_state_changed = (
                current_price.amount != observation.amount
                or current_price.reference_amount
                != observation.reference_amount
                or current_price.currency_code
                != observation.currency_code
                or current_price.price_type
                != observation.price_type
                or current_price.availability_status
                != observation.availability_status
            )

            # No meaningful change
            if not pricing_state_changed:
                current_price.captured_at = observation.captured_at

                self.repository.commit()

                return current_price

            # Meaningful change
            self.repository.create_price_history(
                marketplace_product_id=(
                    observation.marketplace_product_id
                ),
                amount=observation.amount,
                reference_amount=observation.reference_amount,
                currency_code=observation.currency_code,
                price_type=observation.price_type,
                availability_status=observation.availability_status,
                captured_at=observation.captured_at,
                raw_marketplace_payload=(
                    observation.raw_marketplace_payload
                ),
            )

            current_price = self.repository.update_current_price(
                current_price,
                amount=observation.amount,
                reference_amount=observation.reference_amount,
                currency_code=observation.currency_code,
                price_type=observation.price_type,
                availability_status=observation.availability_status,
                captured_at=observation.captured_at,
            )

            self.repository.commit()

            return current_price

        except Exception:
            self.repository.rollback()
            raise

    # ---------------------------------------------------------
    # Historical pricing
    # ---------------------------------------------------------

    def get_price_history(
        self,
        marketplace_product_id: UUID,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
    ):
        """
        Retrieve historical price observations.
        """

        return self.repository.get_price_history(
            marketplace_product_id=marketplace_product_id,
            start_at=start_at,
            end_at=end_at,
        )

    # ---------------------------------------------------------
    # Discount analysis
    # ---------------------------------------------------------

    def analyze_discount(
        self,
        marketplace_product_id: UUID,
        *,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
    ) -> DiscountAnalysis:
        """
        Analyze the current marketplace discount against
        observed historical prices.
        """

        current_price = self.repository.get_current_price(
            marketplace_product_id
        )

        if current_price is None:
            raise ValueError(
                "Current price not found for marketplace product"
            )

        history = self.repository.get_price_history(
            marketplace_product_id=marketplace_product_id,
            start_at=start_at,
            end_at=end_at,
        )

        return self.discount_analyzer.analyze(
            current_amount=current_price.amount,
            reference_amount=current_price.reference_amount,
            history=history,
        )