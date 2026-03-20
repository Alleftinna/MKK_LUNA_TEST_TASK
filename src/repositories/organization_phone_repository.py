from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.organization_phone import OrganizationPhone
from src.repositories.base import BaseRepository


class OrganizationPhoneRepository(BaseRepository[OrganizationPhone]):
    model = OrganizationPhone

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)

    async def list_by_organization(
        self, organization_id: int
    ) -> list[OrganizationPhone]:
        query = (
            select(OrganizationPhone)
            .where(OrganizationPhone.organization_id == organization_id)
            .order_by(OrganizationPhone.id.asc())
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())
