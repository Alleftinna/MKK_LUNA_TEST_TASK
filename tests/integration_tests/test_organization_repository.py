import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.activity import Activity
from src.models.building import Building
from src.models.organization import Organization
from src.models.organization_phone import OrganizationPhone
from src.repositories.organization_repository import OrganizationRepository


async def _seed_organization_data(async_session: AsyncSession) -> tuple[Organization, Organization]:
    building_center = Building(address="Center", latitude=55.7558, longitude=37.6176)
    building_remote = Building(address="Remote", latitude=56.3000, longitude=38.4000)

    food = Activity(name="Food", level=1, parent_id=None)
    milk = Activity(name="Milk products", level=2, parent=food)
    cars = Activity(name="Cars", level=1, parent_id=None)

    org_a = Organization(name='OOO "Roga i Kopyta"', building=building_center)
    org_b = Organization(name="AutoShop", building=building_remote)

    org_a.activities.extend([food, milk])
    org_b.activities.append(cars)

    org_a.phones.append(OrganizationPhone(phone="2-222-222", phone_description="Reception"))
    org_b.phones.append(OrganizationPhone(phone="8-923-666-13-13", phone_description="Sales"))

    async_session.add_all([org_a, org_b])
    await async_session.commit()
    return org_a, org_b


@pytest.mark.asyncio
async def test_organization_repository_get_by_id_loads_relations(
    async_session: AsyncSession,
) -> None:
    repository = OrganizationRepository(async_session)
    org_a, _ = await _seed_organization_data(async_session)

    payload = await repository.get_by_id(org_a.id)
    assert payload is not None
    assert payload.building.address == "Center"
    assert len(payload.phones) == 1
    assert len(payload.activities) == 2


@pytest.mark.asyncio
async def test_organization_repository_list_by_building(async_session: AsyncSession) -> None:
    repository = OrganizationRepository(async_session)
    org_a, _ = await _seed_organization_data(async_session)

    payload = await repository.list_by_building(building_id=org_a.building_id)
    assert [item.name for item in payload] == ['OOO "Roga i Kopyta"']


@pytest.mark.asyncio
async def test_organization_repository_list_by_activity(async_session: AsyncSession) -> None:
    repository = OrganizationRepository(async_session)
    org_a, _ = await _seed_organization_data(async_session)
    food_id = next(activity.id for activity in org_a.activities if activity.name == "Food")

    payload = await repository.list_by_activity(activity_id=food_id)
    assert [item.name for item in payload] == ['OOO "Roga i Kopyta"']


@pytest.mark.asyncio
async def test_organization_repository_search_by_name(async_session: AsyncSession) -> None:
    repository = OrganizationRepository(async_session)
    await _seed_organization_data(async_session)

    payload = await repository.search_by_name(name="Roga")
    assert [item.name for item in payload] == ['OOO "Roga i Kopyta"']


@pytest.mark.asyncio
async def test_organization_repository_search_by_radius(async_session: AsyncSession) -> None:
    repository = OrganizationRepository(async_session)
    await _seed_organization_data(async_session)

    payload = await repository.search_by_radius(
        latitude=55.7558,
        longitude=37.6176,
        radius_m=1500,
    )
    assert [item.name for item in payload] == ['OOO "Roga i Kopyta"']


@pytest.mark.asyncio
async def test_organization_repository_search_by_bbox(async_session: AsyncSession) -> None:
    repository = OrganizationRepository(async_session)
    await _seed_organization_data(async_session)

    payload = await repository.search_by_bbox(
        min_lat=55.70,
        max_lat=55.90,
        min_lon=37.50,
        max_lon=37.80,
    )
    assert [item.name for item in payload] == ['OOO "Roga i Kopyta"']
