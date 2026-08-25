"""Tests for the root endpoint (GET /api/v1/)."""

from app.config.settings import settings


def test_root_returns_welcome_message(client):
    resp = client.get("/api/v1/")

    assert resp.status_code == 200
    assert resp.json() == {"message": f"Welcome to {settings.app_name}"}
