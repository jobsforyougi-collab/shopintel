"""Tests for the global exception handler and default 404 behaviour.

The global handler in ``app.core.exceptions`` catches base ``Exception`` and
returns ``{"success": False, "message": "Internal Server Error"}`` with a 500
status. To exercise it without touching feature/business code, we register the
handler on a throwaway app that has a route which raises.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.exceptions import register_exception_handlers


@pytest.fixture
def error_client() -> TestClient:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/boom")
    async def boom():
        raise RuntimeError("kaboom")

    # raise_server_exceptions=False so the handler's response is returned
    # instead of the exception being re-raised into the test.
    return TestClient(app, raise_server_exceptions=False)


def test_global_exception_handler_shape(error_client):
    resp = error_client.get("/boom")

    assert resp.status_code == 500
    assert resp.json() == {
        "success": False,
        "message": "Internal Server Error",
    }


def test_unknown_route_returns_404(client):
    resp = client.get("/api/v1/this-route-does-not-exist")

    assert resp.status_code == 404
