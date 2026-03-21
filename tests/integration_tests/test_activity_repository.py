import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.activity import Activity
from src.repositories.activity_repository import ActivityRepository


@pytest.mark.asyncio
async def test_activity_repository_list_tree(async_session: AsyncSession) -> None:
    repository = ActivityRepository(async_session)
    cars = Activity(name="Cars", level=1, parent_id=None)
    food = Activity(name="Food", level=1, parent_id=None)
    async_session.add_all([cars, food])
    await async_session.flush()

    async_session.add_all(
        [
            Activity(name="Milk products", level=2, parent_id=food.id),
            Activity(name="Truck", level=2, parent_id=cars.id),
        ]
    )
    await async_session.commit()

    activities = await repository.list_tree()
    assert [item.name for item in activities] == ["Cars", "Food", "Milk products", "Truck"]


@pytest.mark.asyncio
async def test_activity_repository_get_descendant_ids(async_session: AsyncSession) -> None:
    repository = ActivityRepository(async_session)
    root = Activity(name="Food", level=1, parent_id=None)
    async_session.add(root)
    await async_session.flush()

    level_2 = Activity(name="Meat products", level=2, parent_id=root.id)
    async_session.add(level_2)
    await async_session.flush()

    level_3 = Activity(name="Sausages", level=3, parent_id=level_2.id)
    async_session.add(level_3)
    await async_session.commit()

    ids = await repository.get_descendant_ids(activity_id=root.id, max_depth=3)
    assert set(ids) == {root.id, level_2.id, level_3.id}
