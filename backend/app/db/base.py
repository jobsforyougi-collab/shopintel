from app.db.base_class import Base


# Import all ORM models here so Alembic can discover them.
#
# This file is intentionally separate from base_class.py.
# base_class.py must contain only the DeclarativeBase definition
# and must never import ORM models.

from app.modules.catalog.models.marketplace import Marketplace
from app.modules.catalog.models.marketplace_region import MarketplaceRegion
from app.modules.catalog.models.marketplace_product import MarketplaceProduct
from app.modules.catalog.models.marketplace_seller import MarketplaceSeller
from app.modules.catalog.models.brand import Brand
from app.modules.catalog.models.category import Category
from app.modules.catalog.models.product import Product
from app.modules.catalog.models.seller import Seller
from app.modules.catalog.models.current_price import CurrentPrice
from app.modules.catalog.models.price_history import PriceHistory


__all__ = [
    "Base",
    "Marketplace",
    "MarketplaceRegion",
    "MarketplaceProduct",
    "MarketplaceSeller",
    "Brand",
    "Category",
    "Product",
    "Seller",
    "CurrentPrice",
    "PriceHistory",
]