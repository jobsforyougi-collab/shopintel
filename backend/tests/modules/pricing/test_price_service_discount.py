from decimal import Decimal
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.modules.catalog.models.current_price import CurrentPrice
from app.modules.pricing.schemas.discount_analysis import DiscountAnalysis
from app.modules.pricing.services.discount_analyzer import DiscountAnalyzer
from app.modules.pricing.services.price_service import PriceService


def test_analyze_discount_uses_current_price_and_history():
    repository = Mock()

    marketplace_product_id = uuid4()

    current_price = Mock(spec=CurrentPrice)
    current_price.amount = Decimal("2000.00")
    current_price.reference_amount = Decimal("3000.00")

    repository.get_current_price.return_value = current_price
    repository.get_price_history.return_value = []

    analyzer = Mock(spec=DiscountAnalyzer)

    expected = DiscountAnalysis(
        advertised_discount_percent=Decimal("33.33"),
        historical_lowest_price=Decimal("2000.00"),
        historical_highest_price=Decimal("2000.00"),
        historical_average_price=Decimal("2000.00"),
        reference_price_supported=None,
        status="INSUFFICIENT_DATA",
        confidence=Decimal("0.00"),
    )

    analyzer.analyze.return_value = expected

    service = PriceService(
        repository=repository,
        discount_analyzer=analyzer,
    )

    result = service.analyze_discount(
        marketplace_product_id=marketplace_product_id,
    )

    assert result is expected

    repository.get_current_price.assert_called_once_with(
        marketplace_product_id
    )

    repository.get_price_history.assert_called_once_with(
        marketplace_product_id=marketplace_product_id,
        start_at=None,
        end_at=None,
    )

    analyzer.analyze.assert_called_once_with(
        current_amount=Decimal("2000.00"),
        reference_amount=Decimal("3000.00"),
        history=[],
    )


def test_analyze_discount_passes_date_range():
    repository = Mock()

    marketplace_product_id = uuid4()

    current_price = Mock(spec=CurrentPrice)
    current_price.amount = Decimal("2000.00")
    current_price.reference_amount = Decimal("3000.00")

    repository.get_current_price.return_value = current_price
    repository.get_price_history.return_value = []

    analyzer = Mock(spec=DiscountAnalyzer)

    expected = Mock(spec=DiscountAnalysis)
    analyzer.analyze.return_value = expected

    service = PriceService(
        repository=repository,
        discount_analyzer=analyzer,
    )

    service.analyze_discount(
        marketplace_product_id=marketplace_product_id,
        start_at=None,
        end_at=None,
    )

    repository.get_price_history.assert_called_once()


def test_analyze_discount_raises_when_current_price_missing():
    repository = Mock()

    marketplace_product_id = uuid4()

    repository.get_current_price.return_value = None

    analyzer = Mock(spec=DiscountAnalyzer)

    service = PriceService(
        repository=repository,
        discount_analyzer=analyzer,
    )

    with pytest.raises(
        ValueError,
        match="Current price not found",
    ):
        service.analyze_discount(
            marketplace_product_id=marketplace_product_id,
        )

    repository.get_price_history.assert_not_called()
    analyzer.analyze.assert_not_called()