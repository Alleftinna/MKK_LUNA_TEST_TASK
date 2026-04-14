from unittest.mock import AsyncMock, Mock

import pytest

from src.models.template_entity import TemplateEntity
from src.schemas.template_entity import TemplateEntityCreate
from src.services.template_entity_service import TemplateEntityService


@pytest.mark.asyncio
async def test_list_entities_proxies_repository_call(monkeypatch) -> None:
    session = Mock()
    service = TemplateEntityService(session=session)
    first_entity = TemplateEntity(name="first", description="first")
    second_entity = TemplateEntity(name="second", description="second")

    list_mock = AsyncMock(return_value=[first_entity, second_entity])
    monkeypatch.setattr(service.repository, "list_all", list_mock)

    payload = await service.list_entities(limit=2, offset=0)
    assert payload == [first_entity, second_entity]
    list_mock.assert_awaited_once_with(limit=2, offset=0)


@pytest.mark.asyncio
async def test_create_entity_builds_model_and_delegates(monkeypatch) -> None:
    session = Mock()
    service = TemplateEntityService(session=session)
    created = TemplateEntity(id=1, name="first", description="first")

    add_mock = AsyncMock(return_value=created)
    monkeypatch.setattr(service.repository, "add", add_mock)

    payload = await service.create_entity(
        payload=TemplateEntityCreate(name="first", description="first")
    )
    assert payload is created
    add_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_entity_delegates_to_repository(monkeypatch) -> None:
    session = Mock()
    service = TemplateEntityService(session=session)

    delete_mock = AsyncMock(return_value=True)
    monkeypatch.setattr(service.repository, "delete_by_id", delete_mock)

    payload = await service.delete_entity(entity_id=1)
    assert payload is True
    delete_mock.assert_awaited_once_with(entity_id=1)
