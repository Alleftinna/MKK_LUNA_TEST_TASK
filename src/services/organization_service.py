from sqlalchemy.ext.asyncio import AsyncSession

from src.models.organization import Organization
from src.repositories.activity_repository import ActivityRepository
from src.repositories.organization_repository import OrganizationRepository


class OrganizationService:
    def __init__(self, session: AsyncSession) -> None:
        self.organization_repository = OrganizationRepository(session=session)
        self.activity_repository = ActivityRepository(session=session)

    async def get_by_id(self, organization_id: int) -> Organization | None:
        return await self.organization_repository.get_by_id(organization_id)

    async def list_by_building(
        self,
        building_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Organization]:
        return await self.organization_repository.list_by_building(
            building_id=building_id,
            limit=limit,
            offset=offset,
        )

    async def list_by_activity(
        self,
        activity_id: int,
        limit: int = 100,
        offset: int = 0,
        include_descendants: bool = True,
        max_depth: int = 3,
    ) -> list[Organization]:
        if include_descendants:
            activity_ids = await self.activity_repository.get_descendant_ids(
                activity_id=activity_id,
                max_depth=max_depth,
            )
            return await self.organization_repository.list_by_activities(
                activity_ids=activity_ids,
                limit=limit,
                offset=offset,
            )
        return await self.organization_repository.list_by_activity(
            activity_id=activity_id,
            limit=limit,
            offset=offset,
        )

    async def search_by_name(
        self,
        name: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Organization]:
        return await self.organization_repository.search_by_name(
            name=name,
            limit=limit,
            offset=offset,
        )

    async def search_by_radius(
        self,
        latitude: float,
        longitude: float,
        radius_m: float,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Organization]:
        return await self.organization_repository.search_by_radius(
            latitude=latitude,
            longitude=longitude,
            radius_m=radius_m,
            limit=limit,
            offset=offset,
        )

    async def search_by_bbox(
        self,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Organization]:
        return await self.organization_repository.search_by_bbox(
            min_lat=min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon,
            limit=limit,
            offset=offset,
        )
