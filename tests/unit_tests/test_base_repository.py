from unittest.mock import AsyncMock, Mock

import pytest

from src.models.template_entity import TemplateEntity
from src.repositories.base import BaseRepository


class TemplateEntityRepositoryForTest(BaseRepository[TemplateEntity]):
    model = TemplateEntity


def build_session_double() -> Mock:
    session = Mock()
    session.execute = AsyncMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    session.rollback = AsyncMock()
    return session


@pytest.mark.asyncio
async def test_base_repository_get_by_id_returns_scalar_result() -> None:
    session = build_session_double()
    repository = TemplateEntityRepositoryForTest(session=session)

    model_payload = TemplateEntity(
        id=1,
        name="alpha",
        description="first entity",
    )

    scalar_result = Mock()
    scalar_result.scalar_one_or_none.return_value = model_payload
    session.execute.return_value = scalar_result

    payload = await repository.get_by_id(1)
    assert payload is model_payload
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_base_repository_list_returns_scalars_as_list() -> None:
    session = build_session_double()
    repository = TemplateEntityRepositoryForTest(session=session)

    first_item = TemplateEntity(
        id=1,
        name="alpha",
        description="first entity",
    )
    second_item = TemplateEntity(
        id=2,
        name="beta",
        description="second entity",
    )

    scalars_result = Mock()
    scalars_result.all.return_value = [first_item, second_item]

    execute_result = Mock()
    execute_result.scalars.return_value = scalars_result
    session.execute.return_value = execute_result

    payload = await repository.list_all(limit=10, offset=5)
    assert payload == [first_item, second_item]
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_base_repository_add_calls_flush_and_refresh() -> None:
    session = build_session_double()
    repository = TemplateEntityRepositoryForTest(session=session)

    instance = TemplateEntity(
        id=1,
        name="alpha",
        description="first entity",
    )
    payload = await repository.add(instance)
    assert payload is instance

    session.add.assert_called_once_with(instance)
    session.flush.assert_awaited_once()
    session.refresh.assert_awaited_once_with(instance)


@pytest.mark.asyncio
async def test_base_repository_delete_by_id_deletes_existing_entity() -> None:
    session = build_session_double()
    repository = TemplateEntityRepositoryForTest(session=session)

    instance = TemplateEntity(id=1, name="alpha", description="first entity")

    scalar_result = Mock()
    scalar_result.scalar_one_or_none.return_value = instance
    session.execute.return_value = scalar_result

    payload = await repository.delete_by_id(entity_id=1)
    assert payload is True
    session.delete.assert_awaited_once_with(instance)
    session.flush.assert_awaited_once()
