from collections.abc import Generator

from sqlalchemy.orm import sessionmaker

from app.db.engine import engine

# Import all ORM models so SQLAlchemy registers every mapper
# before database queries are executed.
import app.db.base  # noqa: F401


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db() -> Generator:
    """Provide a database session for each request."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()