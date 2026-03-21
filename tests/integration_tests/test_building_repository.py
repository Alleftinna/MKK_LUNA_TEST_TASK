import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.building import Building
from src.repositories.building_repository import BuildingRepository


@pytest.mark.asyncio
async def test_building_repository_list_within_bbox(
    async_session: AsyncSession,
) -> None:
    repository = BuildingRepository(async_session)
    async_session.add_all(
        [
            Building(address="A1", latitude=55.75, longitude=37.61),
            Building(address="A2", latitude=55.80, longitude=37.62),
            Building(address="A3", latitude=56.30, longitude=38.40),
        ]
    )
    await async_session.commit()

    buildings = await repository.list_within_bbox(
        min_lat=55.70,
        max_lat=56.00,
        min_lon=37.50,
        max_lon=37.70,
    )

    assert {item.address for item in buildings} == {"A1", "A2"}


@pytest.mark.asyncio
async def test_building_repository_list_within_radius(
    async_session: AsyncSession,
) -> None:
    repository = BuildingRepository(async_session)
    async_session.add_all(
        [
            Building(address="Center", latitude=55.7558, longitude=37.6176),
            Building(address="Near", latitude=55.7590, longitude=37.6200),
            Building(address="Far", latitude=56.2000, longitude=38.1000),
        ]
    )
    await async_session.commit()

    buildings = await repository.list_within_radius(
        latitude=55.7558,
        longitude=37.6176,
        radius_m=1000,
    )

    assert {item.address for item in buildings} == {"Center", "Near"}
