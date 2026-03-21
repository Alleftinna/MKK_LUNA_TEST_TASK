from math import cos, radians

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_exceptions import handle_db_exceptions
from src.models.building import Building
from src.repositories.base import BaseRepository


class BuildingRepository(BaseRepository[Building]):
    model = Building

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)

    @handle_db_exceptions
    async def list_within_bbox(
        self,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float,
    ) -> list[Building]:
        query = select(Building).where(
            Building.latitude >= min_lat,
            Building.latitude <= max_lat,
            Building.longitude >= min_lon,
            Building.longitude <= max_lon,
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    @handle_db_exceptions
    async def list_within_radius(
        self,
        latitude: float,
        longitude: float,
        radius_m: float,
    ) -> list[Building]:
        lat_delta = radius_m / 111_320
        cos_lat = max(0.0001, abs(cos(radians(latitude))))
        lon_delta = radius_m / (111_320 * cos_lat)

        return await self.list_within_bbox(
            min_lat=latitude - lat_delta,
            max_lat=latitude + lat_delta,
            min_lon=longitude - lon_delta,
            max_lon=longitude + lon_delta,
        )
