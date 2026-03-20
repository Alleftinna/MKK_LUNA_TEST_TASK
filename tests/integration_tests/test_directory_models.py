import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.activity import Activity
from src.models.building import Building
from src.models.organization import Organization
from src.models.organization_phone import OrganizationPhone


@pytest.mark.asyncio
async def test_directory_models_persist_relations(async_session: AsyncSession) -> None:
    building = Building(
        address="Moscow, Lenina 1, office 3",
        latitude=55.7558,
        longitude=37.6176,
    )
    root_activity = Activity(name="Food", level=1, parent_id=None)
    nested_activity = Activity(name="Milk products", level=2, parent=root_activity)
    organization = Organization(name='OOO "Roga i Kopyta"', building=building)
    organization.phones.extend(
        [
            OrganizationPhone(phone="2-222-222", phone_description="Reception"),
            OrganizationPhone(phone="3-333-333", phone_description="Support"),
        ]
    )
    organization.activities.extend([root_activity, nested_activity])

    async_session.add(organization)
    await async_session.commit()

    query = (
        select(Organization)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
        .where(Organization.name == 'OOO "Roga i Kopyta"')
    )
    result = await async_session.execute(query)
    saved_organization = result.scalar_one()

    assert saved_organization.building.address == "Moscow, Lenina 1, office 3"
    assert len(saved_organization.phones) == 2
    assert {item.phone_description for item in saved_organization.phones} == {
        "Reception",
        "Support",
    }
    assert {item.name for item in saved_organization.activities} == {
        "Food",
        "Milk products",
    }
