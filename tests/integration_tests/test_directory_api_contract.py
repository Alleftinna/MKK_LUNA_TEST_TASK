import pytest
from httpx import AsyncClient

API_HEADERS = {"X-API-Key": "test-api-key"}


@pytest.mark.asyncio
async def test_get_organization_by_id_contract(
    client: AsyncClient,
    seeded_directory_data: dict[str, int],
) -> None:
    response = await client.get(
        f"/api/v1/organizations/{seeded_directory_data['org_food_id']}",
        headers=API_HEADERS,
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == seeded_directory_data["org_food_id"]
    assert "name" in payload
    assert "building" in payload
    assert "phones" in payload
    assert "activities" in payload


@pytest.mark.asyncio
async def test_list_organizations_by_building_contract(
    client: AsyncClient,
    seeded_directory_data: dict[str, int],
) -> None:
    response = await client.get(
        f"/api/v1/organizations/by-building/{seeded_directory_data['building_main_id']}",
        headers=API_HEADERS,
    )
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) == 2


@pytest.mark.asyncio
async def test_list_organizations_by_activity_contract(
    client: AsyncClient,
    seeded_directory_data: dict[str, int],
) -> None:
    response = await client.get(
        f"/api/v1/organizations/by-activity/{seeded_directory_data['activity_food_id']}",
        headers=API_HEADERS,
    )
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert {item["name"] for item in payload} == {'OOO "Roga i Kopyta"'}


@pytest.mark.asyncio
async def test_search_organizations_by_name_contract(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/organizations/search",
        params={"name": "Roga"},
        headers=API_HEADERS,
    )
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]["name"] == 'OOO "Roga i Kopyta"'


@pytest.mark.asyncio
async def test_search_organizations_by_radius_contract(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/organizations/geo/radius",
        params={"latitude": 55.7558, "longitude": 37.6176, "radius_m": 1000},
        headers=API_HEADERS,
    )
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert {item["name"] for item in payload} == {'OOO "Roga i Kopyta"', "AutoShop"}


@pytest.mark.asyncio
async def test_search_organizations_by_bbox_contract(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/organizations/geo/bbox",
        params={"min_lat": 55.5, "max_lat": 56.0, "min_lon": 37.0, "max_lon": 38.0},
        headers=API_HEADERS,
    )
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert {item["name"] for item in payload} == {'OOO "Roga i Kopyta"', "AutoShop"}


@pytest.mark.asyncio
async def test_search_organizations_by_activity_tree_contract(
    client: AsyncClient,
    seeded_directory_data: dict[str, int],
) -> None:
    response = await client.get(
        f"/api/v1/organizations/search/by-activity/{seeded_directory_data['activity_food_id']}",
        headers=API_HEADERS,
    )
    assert response.status_code == 200
    payload = response.json()
    assert {item["name"] for item in payload} == {'OOO "Roga i Kopyta"', "Milk Factory"}


@pytest.mark.asyncio
async def test_list_buildings_contract(client: AsyncClient) -> None:
    response = await client.get("/api/v1/buildings", headers=API_HEADERS)
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) >= 2


@pytest.mark.asyncio
async def test_api_key_is_required(client: AsyncClient) -> None:
    response = await client.get("/api/v1/buildings", headers={})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid API key"}
