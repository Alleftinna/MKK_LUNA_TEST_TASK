from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.organization_phone import OrganizationPhone
from src.repositories.organization_phone_repository import OrganizationPhoneRepository


class OrganizationPhoneService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = OrganizationPhoneRepository(session=session)

    async def get_by_id(self, phone_id: int) -> OrganizationPhone | None:
        return await self.repository.get_by_id(phone_id)

    async def list_phones(
        self, limit: int = 100, offset: int = 0
    ) -> list[OrganizationPhone]:
        return await self.repository.list_all(limit=limit, offset=offset)

    async def list_by_organization(
        self, organization_id: int
    ) -> list[OrganizationPhone]:
        return await self.repository.list_by_organization(
            organization_id=organization_id
        )
