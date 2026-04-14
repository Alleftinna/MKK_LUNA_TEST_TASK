import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_template_entities_list_requires_api_key(client: AsyncClient) -> None:
    response = await client.get("/api/v1/template-entities")
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid API key"}


@pytest.mark.asyncio
async def test_template_entities_list_returns_seeded_data(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/template-entities",
        headers={"X-API-Key": "test-api-key"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 2
    assert payload[0]["name"] in {"entity-one", "entity-two"}


@pytest.mark.asyncio
async def test_template_entity_create_and_get_by_id(client: AsyncClient) -> None:
    create_response = await client.post(
        "/api/v1/template-entities",
        headers={"X-API-Key": "test-api-key"},
        json={
            "name": "created-from-api",
            "description": "created in integration test",
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()

    get_response = await client.get(
        f"/api/v1/template-entities/{created['id']}",
        headers={"X-API-Key": "test-api-key"},
    )
    assert get_response.status_code == 200
    fetched = get_response.json()
    assert fetched["name"] == "created-from-api"


@pytest.mark.asyncio
async def test_template_entity_delete(client: AsyncClient) -> None:
    create_response = await client.post(
        "/api/v1/template-entities",
        headers={"X-API-Key": "test-api-key"},
        json={
            "name": "to-delete",
            "description": "will be deleted",
        },
    )
    created = create_response.json()

    delete_response = await client.delete(
        f"/api/v1/template-entities/{created['id']}",
        headers={"X-API-Key": "test-api-key"},
    )
    assert delete_response.status_code == 204

    get_response = await client.get(
        f"/api/v1/template-entities/{created['id']}",
        headers={"X-API-Key": "test-api-key"},
    )
    assert get_response.status_code == 404
