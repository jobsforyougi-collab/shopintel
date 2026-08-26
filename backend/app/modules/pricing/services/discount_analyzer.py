from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from statistics import mean
from typing import Sequence

from app.modules.catalog.models.price_history import PriceHistory
from app.modules.pricing.schemas.discount_analysis import DiscountAnalysis


class DiscountAnalyzer:
    """
    Analyzes marketplace discount claims against observed price history.

    This class contains no database logic. It receives historical
    PriceHistory records and returns a DiscountAnalysis result.
    """

    def __init__(
        self,
        reference_price_tolerance_percent: Decimal = Decimal("20"),
        minimum_history_points: int = 3,
    ) -> None:
        self.reference_price_tolerance_percent = (
            reference_price_tolerance_percent
        )
        self.minimum_history_points = minimum_history_points

    def analyze(
        self,
        current_amount: Decimal,
        reference_amount: Decimal | None,
        history: Sequence[PriceHistory],
    ) -> DiscountAnalysis:
        """
        Analyze the marketplace's advertised reference price.

        Statuses:
        - NO_DISCOUNT
        - INSUFFICIENT_DATA
        - SUPPORTED
        - SUSPICIOUS
        """

        advertised_discount = self._calculate_advertised_discount(
            current_amount=current_amount,
            reference_amount=reference_amount,
        )

        prices = [
            record.amount
            for record in history
            if record.amount is not None
        ]

        if reference_amount is None or reference_amount <= current_amount:
            return DiscountAnalysis(
                advertised_discount_percent=advertised_discount,
                historical_lowest_price=self._lowest(prices),
                historical_highest_price=self._highest(prices),
                historical_average_price=self._average(prices),
                reference_price_supported=None,
                status="NO_DISCOUNT",
                confidence=Decimal("1.00"),
            )

        if len(prices) < self.minimum_history_points:
            return DiscountAnalysis(
                advertised_discount_percent=advertised_discount,
                historical_lowest_price=self._lowest(prices),
                historical_highest_price=self._highest(prices),
                historical_average_price=self._average(prices),
                reference_price_supported=None,
                status="INSUFFICIENT_DATA",
                confidence=Decimal("0.00"),
            )

        historical_lowest = self._lowest(prices)
        historical_highest = self._highest(prices)
        historical_average = self._average(prices)

        assert historical_highest is not None

        reference_gap_percent = (
            (reference_amount - historical_highest)
            / reference_amount
        ) * Decimal("100")

        reference_gap_percent = self._round(reference_gap_percent)

        if (
            reference_gap_percent
            <= self.reference_price_tolerance_percent
        ):
            status = "SUPPORTED"
            reference_price_supported = True

            confidence = self._calculate_confidence(
                reference_gap_percent=reference_gap_percent,
                history_count=len(prices),
            )
        else:
            status = "SUSPICIOUS"
            reference_price_supported = False

            confidence = self._calculate_confidence(
                reference_gap_percent=reference_gap_percent,
                history_count=len(prices),
            )

        return DiscountAnalysis(
            advertised_discount_percent=advertised_discount,
            historical_lowest_price=historical_lowest,
            historical_highest_price=historical_highest,
            historical_average_price=historical_average,
            reference_price_supported=reference_price_supported,
            status=status,
            confidence=confidence,
        )

    # ---------------------------------------------------------
    # Discount calculation
    # ---------------------------------------------------------

    @staticmethod
    def _calculate_advertised_discount(
        *,
        current_amount: Decimal,
        reference_amount: Decimal | None,
    ) -> Decimal | None:
        if reference_amount is None:
            return None

        if reference_amount <= current_amount:
            return Decimal("0.00")

        discount = (
            (reference_amount - current_amount)
            / reference_amount
        ) * Decimal("100")

        return DiscountAnalyzer._round(discount)

    # ---------------------------------------------------------
    # Historical statistics
    # ---------------------------------------------------------

    @staticmethod
    def _lowest(
        prices: Sequence[Decimal],
    ) -> Decimal | None:
        if not prices:
            return None

        return min(prices)

    @staticmethod
    def _highest(
        prices: Sequence[Decimal],
    ) -> Decimal | None:
        if not prices:
            return None

        return max(prices)

    @staticmethod
    def _average(
        prices: Sequence[Decimal],
    ) -> Decimal | None:
        if not prices:
            return None

        return DiscountAnalyzer._round(
            Decimal(str(mean(prices)))
        )

    # ---------------------------------------------------------
    # Confidence
    # ---------------------------------------------------------

    def _calculate_confidence(
        self,
        *,
        reference_gap_percent: Decimal,
        history_count: int,
    ) -> Decimal:
        """
        Calculate confidence using:

        1. Amount of historical evidence.
        2. Size of the reference-price gap.

        This is intentionally conservative. More sophisticated
        statistical scoring can be added later.
        """

        history_confidence = min(
            Decimal("1.00"),
            Decimal(history_count) / Decimal("10"),
        )

        gap_confidence = min(
            Decimal("1.00"),
            reference_gap_percent / Decimal("50"),
        )

        confidence = (
            history_confidence + gap_confidence
        ) / Decimal("2")

        return self._round(confidence)

    # ---------------------------------------------------------
    # Decimal helper
    # ---------------------------------------------------------

    @staticmethod
    def _round(value: Decimal) -> Decimal:
        return value.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )