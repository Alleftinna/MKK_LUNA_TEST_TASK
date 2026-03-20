from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.routers import system as system_module
from src.routers.system import set_app_instance, system_router


def create_test_app() -> FastAPI:
    app = FastAPI()
    app.include_router(system_router)
    set_app_instance(app)
    return app


def test_liveness_probe_returns_ok() -> None:
    app = create_test_app()
    client = TestClient(app)

    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_probe_returns_ready(monkeypatch) -> None:
    async def fake_db_health() -> bool:
        return True

    monkeypatch.setattr(system_module, "is_db_healthy", fake_db_health)
    app = create_test_app()
    client = TestClient(app)

    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_readiness_probe_returns_503_when_db_unavailable(monkeypatch) -> None:
    async def fake_db_health() -> bool:
        return False

    monkeypatch.setattr(system_module, "is_db_healthy", fake_db_health)
    app = create_test_app()
    client = TestClient(app)

    response = client.get("/health/ready")
    assert response.status_code == 503
    assert response.json() == {"detail": "Database is not ready"}


def test_openapi_json_endpoint_returns_schema() -> None:
    app = create_test_app()
    client = TestClient(app)

    response = client.get("/openapi.json")
    assert response.status_code == 200
    payload = response.json()
    assert "openapi" in payload
