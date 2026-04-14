import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.template_entity import TemplateEntity
from src.repositories.template_entity_repository import TemplateEntityRepository


@pytest.mark.asyncio
async def test_template_entity_repository_list_all_returns_seeded_rows(
    async_session: AsyncSession,
    seeded_template_data: dict[str, int],
) -> None:
    repository = TemplateEntityRepository(session=async_session)
    payload = await repository.list_all(limit=10, offset=0)
    assert len(payload) == 2
    assert payload[0].name in {"entity-one", "entity-two"}


@pytest.mark.asyncio
async def test_template_entity_repository_add_persists_row(
    async_session: AsyncSession,
) -> None:
    repository = TemplateEntityRepository(session=async_session)
    entity = TemplateEntity(name="new-entity", description="new description")
    created = await repository.add(entity)
    await async_session.commit()

    payload = await repository.get_by_id(created.id)
    assert payload is not None
    assert payload.name == "new-entity"
