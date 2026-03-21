from unittest.mock import AsyncMock, Mock

import pytest

from src.models.building import Building
from src.repositories.base import BaseRepository


class BuildingRepositoryForTest(BaseRepository[Building]):
    model = Building


def build_session_double() -> Mock:
    session = Mock()
    session.execute = AsyncMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    session.rollback = AsyncMock()
    return session


@pytest.mark.asyncio
async def test_base_repository_get_by_id_returns_scalar_result() -> None:
    session = build_session_double()
    repository = BuildingRepositoryForTest(session=session)

    model_payload = Building(
        id=1,
        address="Moscow, Lenina 1",
        latitude=55.7558,
        longitude=37.6176,
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
    repository = BuildingRepositoryForTest(session=session)

    first_item = Building(
        id=1,
        address="Moscow, Lenina 1",
        latitude=55.7558,
        longitude=37.6176,
    )
    second_item = Building(
        id=2,
        address="Moscow, Lenina 2",
        latitude=55.7658,
        longitude=37.6276,
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
    repository = BuildingRepositoryForTest(session=session)

    instance = Building(
        id=1,
        address="Moscow, Lenina 1",
        latitude=55.7558,
        longitude=37.6176,
    )
    payload = await repository.add(instance)
    assert payload is instance

    session.add.assert_called_once_with(instance)
    session.flush.assert_awaited_once()
    session.refresh.assert_awaited_once_with(instance)
