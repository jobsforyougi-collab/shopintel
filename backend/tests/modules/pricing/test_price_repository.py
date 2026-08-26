from datetime import datetime, timezone
from unittest.mock import Mock
from uuid import uuid4

from app.modules.catalog.models.price_history import PriceHistory
from app.modules.pricing.repositories.price_repository import PriceRepository


def test_get_price_history_returns_records_in_chronological_order():
    db = Mock()

    marketplace_product_id = uuid4()

    older = Mock(spec=PriceHistory)
    older.captured_at = datetime(
        2026,
        8,
        10,
        10,
        0,
        tzinfo=timezone.utc,
    )

    newer = Mock(spec=PriceHistory)
    newer.captured_at = datetime(
        2026,
        8,
        15,
        10,
        0,
        tzinfo=timezone.utc,
    )

    scalars = Mock()
    scalars.all.return_value = [older, newer]

    db.scalars.return_value = scalars

    repository = PriceRepository(db)

    result = repository.get_price_history(
        marketplace_product_id=marketplace_product_id,
    )

    assert result == [older, newer]
    db.scalars.assert_called_once()


def test_get_price_history_accepts_date_range():
    db = Mock()

    scalars = Mock()
    scalars.all.return_value = []

    db.scalars.return_value = scalars

    repository = PriceRepository(db)

    result = repository.get_price_history(
        marketplace_product_id=uuid4(),
        start_at=datetime(
            2026,
            8,
            1,
            tzinfo=timezone.utc,
        ),
        end_at=datetime(
            2026,
            8,
            16,
            tzinfo=timezone.utc,
        ),
    )

    assert result == []
    db.scalars.assert_called_once()


def test_get_price_history_without_date_range():
    db = Mock()

    scalars = Mock()
    scalars.all.return_value = []

    db.scalars.return_value = scalars

    repository = PriceRepository(db)

    result = repository.get_price_history(
        marketplace_product_id=uuid4(),
    )

    assert result == []
    db.scalars.assert_called_once()