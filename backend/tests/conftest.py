"""Shared pytest fixtures and test environment setup.

Environment variables required by ``app.config.settings.Settings`` are set here
*before* the application is imported, so settings load without a real
``.env.development`` file. Values are harmless test placeholders; no real
database connection is made at import time.
"""

import os

os.environ.setdefault("APP_NAME", "ShopIntel Test")
os.environ.setdefault("APP_VERSION", "0.0.0-test")
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://test:test@localhost:5432/shopintel_test",
)
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """A FastAPI ``TestClient`` bound to the real application."""
    with TestClient(app) as test_client:
        yield test_client
