from sqlalchemy.ext.asyncio import AsyncSession

from src.models.building import Building
from src.repositories.building_repository import BuildingRepository


class BuildingService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = BuildingRepository(session=session)

    async def get_by_id(self, building_id: int) -> Building | None:
        return await self.repository.get_by_id(building_id)

    async def list(self, limit: int = 100, offset: int = 0) -> list[Building]:
        return await self.repository.list(limit=limit, offset=offset)

    async def list_within_bbox(
        self,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float,
    ) -> list[Building]:
        return await self.repository.list_within_bbox(
            min_lat=min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon,
        )

    async def list_within_radius(
        self,
        latitude: float,
        longitude: float,
        radius_m: float,
    ) -> list[Building]:
        return await self.repository.list_within_radius(
            latitude=latitude,
            longitude=longitude,
            radius_m=radius_m,
        )
