from sqlalchemy.orm import sessionmaker

from app.db.engine import engine


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

from collections.abc import Generator


def get_db() -> Generator:
    """Provide a database session for each request."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()