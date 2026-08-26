from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.modules.catalog.models.current_price import CurrentPrice
from app.modules.pricing.schemas.price_observation import PriceObservation
from app.modules.pricing.services.price_service import PriceService


def make_observation(
    *,
    amount: str = "1499.00",
    reference_amount: str | None = "2999.00",
    currency_code: str = "PKR",
    price_type: str = "regular",
    availability_status: str = "in_stock",
) -> PriceObservation:
    return PriceObservation(
        marketplace_product_id=uuid4(),
        amount=Decimal(amount),
        reference_amount=(
            Decimal(reference_amount)
            if reference_amount is not None
            else None
        ),
        currency_code=currency_code,
        price_type=price_type,
        availability_status=availability_status,
        captured_at=datetime.now(timezone.utc),
        raw_marketplace_payload={
            "source": "test",
        },
    )


def test_first_observation_creates_current_and_history():
    repository = Mock()
    repository.get_current_price.return_value = None

    current_price = Mock(spec=CurrentPrice)

    repository.create_current_price.return_value = current_price

    service = PriceService(repository)

    observation = make_observation()

    result = service.record_observation(observation)

    assert result is current_price

    repository.create_current_price.assert_called_once()
    repository.create_price_history.assert_called_once()
    repository.commit.assert_called_once()
    repository.rollback.assert_not_called()


def test_unchanged_observation_does_not_create_history():
    repository = Mock()

    observation = make_observation()

    current_price = Mock(spec=CurrentPrice)

    current_price.amount = observation.amount
    current_price.reference_amount = observation.reference_amount
    current_price.currency_code = observation.currency_code
    current_price.price_type = observation.price_type
    current_price.availability_status = observation.availability_status

    repository.get_current_price.return_value = current_price

    service = PriceService(repository)

    result = service.record_observation(observation)

    assert result is current_price

    repository.create_price_history.assert_not_called()
    repository.update_current_price.assert_not_called()
    repository.commit.assert_called_once()
    repository.rollback.assert_not_called()

    assert current_price.captured_at == observation.captured_at


def test_price_change_creates_history_and_updates_current():
    repository = Mock()

    observation = make_observation(amount="1299.00")

    current_price = Mock(spec=CurrentPrice)

    current_price.amount = Decimal("1499.00")
    current_price.reference_amount = Decimal("2999.00")
    current_price.currency_code = "PKR"
    current_price.price_type = "regular"
    current_price.availability_status = "in_stock"

    repository.get_current_price.return_value = current_price
    repository.update_current_price.return_value = current_price

    service = PriceService(repository)

    result = service.record_observation(observation)

    assert result is current_price

    repository.create_price_history.assert_called_once()
    repository.update_current_price.assert_called_once()
    repository.commit.assert_called_once()
    repository.rollback.assert_not_called()


def test_reference_price_change_creates_history():
    repository = Mock()

    observation = make_observation(reference_amount="2499.00")

    current_price = Mock(spec=CurrentPrice)

    current_price.amount = observation.amount
    current_price.reference_amount = Decimal("2999.00")
    current_price.currency_code = observation.currency_code
    current_price.price_type = observation.price_type
    current_price.availability_status = observation.availability_status

    repository.get_current_price.return_value = current_price
    repository.update_current_price.return_value = current_price

    service = PriceService(repository)

    service.record_observation(observation)

    repository.create_price_history.assert_called_once()
    repository.update_current_price.assert_called_once()
    repository.commit.assert_called_once()


def test_availability_change_creates_history():
    repository = Mock()

    observation = make_observation(
        availability_status="out_of_stock",
    )

    current_price = Mock(spec=CurrentPrice)

    current_price.amount = observation.amount
    current_price.reference_amount = observation.reference_amount
    current_price.currency_code = observation.currency_code
    current_price.price_type = observation.price_type
    current_price.availability_status = "in_stock"

    repository.get_current_price.return_value = current_price
    repository.update_current_price.return_value = current_price

    service = PriceService(repository)

    service.record_observation(observation)

    repository.create_price_history.assert_called_once()
    repository.update_current_price.assert_called_once()
    repository.commit.assert_called_once()


def test_service_rolls_back_when_repository_operation_fails():
    repository = Mock()
    repository.get_current_price.return_value = None

    repository.create_current_price.side_effect = RuntimeError(
        "database error"
    )

    service = PriceService(repository)

    observation = make_observation()

    with pytest.raises(RuntimeError, match="database error"):
        service.record_observation(observation)

    repository.commit.assert_not_called()
    repository.rollback.assert_called_once()