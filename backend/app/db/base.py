from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass

# Import all ORM models here so Alembic can discover them
from app.modules.catalog.models.marketplace import Marketplace
from app.modules.catalog.models.brand import Brand
from app.modules.catalog.models.category import Category