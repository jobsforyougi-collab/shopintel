"""Tests for the health endpoint (GET /api/v1/health)."""

from app.config.settings import settings


def test_health_returns_200_and_expected_body(client):
    resp = client.get("/api/v1/health")

    assert resp.status_code == 200
    assert resp.json() == {
        "status": "healthy",
        "version": settings.app_version,
        "debug": settings.debug,
    }
