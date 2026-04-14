import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_template_entities_ui_renders(client: AsyncClient) -> None:
    response = await client.get("/api/v1/admin/ui/template-entities")
    assert response.status_code == 200
    assert "Базовые сущности" in response.text
