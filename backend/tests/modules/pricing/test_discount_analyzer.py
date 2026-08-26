from decimal import Decimal
from types import SimpleNamespace

from app.modules.pricing.services.discount_analyzer import DiscountAnalyzer


def make_history(*amounts):
    return [
        SimpleNamespace(amount=Decimal(amount))
        for amount in amounts
    ]


def test_no_discount_when_reference_price_is_missing():
    analyzer = DiscountAnalyzer()

    result = analyzer.analyze(
        current_amount=Decimal("2000.00"),
        reference_amount=None,
        history=make_history(
            "2100.00",
            "2050.00",
            "2000.00",
        ),
    )

    assert result.status == "NO_DISCOUNT"
    assert result.advertised_discount_percent is None
    assert result.reference_price_supported is None


def test_no_discount_when_reference_price_is_not_higher():
    analyzer = DiscountAnalyzer()

    result = analyzer.analyze(
        current_amount=Decimal("2000.00"),
        reference_amount=Decimal("2000.00"),
        history=make_history(
            "2000.00",
            "2050.00",
            "2100.00",
        ),
    )

    assert result.status == "NO_DISCOUNT"
    assert result.advertised_discount_percent == Decimal("0.00")


def test_insufficient_data_for_discount_analysis():
    analyzer = DiscountAnalyzer(
        minimum_history_points=3,
    )

    result = analyzer.analyze(
        current_amount=Decimal("2000.00"),
        reference_amount=Decimal("3000.00"),
        history=make_history(
            "2050.00",
            "2000.00",
        ),
    )

    assert result.status == "INSUFFICIENT_DATA"
    assert result.reference_price_supported is None
    assert result.advertised_discount_percent == Decimal("33.33")


def test_supported_reference_price():
    analyzer = DiscountAnalyzer(
        reference_price_tolerance_percent=Decimal("20"),
        minimum_history_points=3,
    )

    result = analyzer.analyze(
        current_amount=Decimal("2000.00"),
        reference_amount=Decimal("2200.00"),
        history=make_history(
            "2100.00",
            "2150.00",
            "2200.00",
        ),
    )

    assert result.status == "SUPPORTED"
    assert result.reference_price_supported is True
    assert result.advertised_discount_percent == Decimal("9.09")


def test_suspicious_reference_price():
    analyzer = DiscountAnalyzer(
        reference_price_tolerance_percent=Decimal("20"),
        minimum_history_points=3,
    )

    result = analyzer.analyze(
        current_amount=Decimal("2000.00"),
        reference_amount=Decimal("3000.00"),
        history=make_history(
            "2050.00",
            "2000.00",
            "2100.00",
            "2050.00",
        ),
    )

    assert result.status == "SUSPICIOUS"
    assert result.reference_price_supported is False
    assert result.advertised_discount_percent == Decimal("33.33")


def test_historical_statistics_are_calculated():
    analyzer = DiscountAnalyzer()

    result = analyzer.analyze(
        current_amount=Decimal("2000.00"),
        reference_amount=None,
        history=make_history(
            "1500.00",
            "1600.00",
            "1700.00",
        ),
    )

    assert result.historical_lowest_price == Decimal("1500.00")
    assert result.historical_highest_price == Decimal("1700.00")
    assert result.historical_average_price == Decimal("1600.00")