from app.db.base_class import Base
from app.shared.database.mixins.soft_delete_mixin import SoftDeleteMixin
from app.shared.database.mixins.timestamp_mixin import TimestampMixin
from app.shared.database.mixins.uuid_mixin import UUIDMixin


class BaseModel(
    UUIDMixin,
    TimestampMixin, #empty as of now
    SoftDeleteMixin,
    Base,
):
    """
    Base class for all ShopIntel ORM models.

    Provides:
    - UUID primary key
    - Created timestamp
    - Updated timestamp
    - Soft delete support
    """

    __abstract__ = True