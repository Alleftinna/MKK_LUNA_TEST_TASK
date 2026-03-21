import pytest
from fastapi.testclient import TestClient

from src.main import app

API_HEADERS = {"X-API-Key": "test-api-key"}


@pytest.mark.xfail(
    reason="Directory API endpoints are not implemented yet",
    strict=False,
)
def test_get_organization_by_id_contract() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/organizations/1", headers=API_HEADERS)
    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 1
    assert "name" in payload
    assert "building" in payload
    assert "phones" in payload
    assert "activities" in payload


@pytest.mark.xfail(
    reason="Directory API endpoints are not implemented yet",
    strict=False,
)
def test_list_organizations_by_building_contract() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/organizations/by-building/1", headers=API_HEADERS)
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)


@pytest.mark.xfail(
    reason="Directory API endpoints are not implemented yet",
    strict=False,
)
def test_list_organizations_by_activity_contract() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/organizations/by-activity/1", headers=API_HEADERS)
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)


@pytest.mark.xfail(
    reason="Directory API endpoints are not implemented yet",
    strict=False,
)
def test_search_organizations_by_name_contract() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/organizations/search",
        params={"name": "Roga"},
        headers=API_HEADERS,
    )
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)


@pytest.mark.xfail(
    reason="Directory API endpoints are not implemented yet",
    strict=False,
)
def test_search_organizations_by_radius_contract() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/organizations/geo/radius",
        params={"latitude": 55.7558, "longitude": 37.6176, "radius_m": 1000},
        headers=API_HEADERS,
    )
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)


@pytest.mark.xfail(
    reason="Directory API endpoints are not implemented yet",
    strict=False,
)
def test_search_organizations_by_bbox_contract() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/organizations/geo/bbox",
        params={"min_lat": 55.5, "max_lat": 56.0, "min_lon": 37.0, "max_lon": 38.0},
        headers=API_HEADERS,
    )
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)


@pytest.mark.xfail(
    reason="Directory API endpoints are not implemented yet",
    strict=False,
)
def test_list_buildings_contract() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/buildings", headers=API_HEADERS)
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
