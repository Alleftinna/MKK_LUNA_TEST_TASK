import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.building import Building
from src.models.organization import Organization
from src.models.organization_phone import OrganizationPhone
from src.repositories.organization_phone_repository import OrganizationPhoneRepository


@pytest.mark.asyncio
async def test_organization_phone_repository_list_by_organization(
    async_session: AsyncSession,
) -> None:
    repository = OrganizationPhoneRepository(async_session)
    building = Building(address="B1", latitude=55.75, longitude=37.61)
    organization = Organization(name="Org One", building=building)
    async_session.add(organization)
    await async_session.flush()

    async_session.add_all(
        [
            OrganizationPhone(
                organization_id=organization.id,
                phone="2-222-222",
                phone_description="Reception",
            ),
            OrganizationPhone(
                organization_id=organization.id,
                phone="3-333-333",
                phone_description="Support",
            ),
        ]
    )
    await async_session.commit()

    phones = await repository.list_by_organization(organization_id=organization.id)
    assert [item.phone for item in phones] == ["2-222-222", "3-333-333"]
