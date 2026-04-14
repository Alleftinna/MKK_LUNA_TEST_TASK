from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_exceptions import handle_db_exceptions
from src.models.building import Building
from src.repositories.base import BaseRepository
from src.utils.geo import build_bounding_box, great_circle_distance_expression


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
        bounding_box = build_bounding_box(
            latitude=latitude,
            longitude=longitude,
            radius_m=radius_m,
        )
        distance_expression = great_circle_distance_expression(
            latitude=latitude,
            longitude=longitude,
            latitude_column=Building.latitude,
            longitude_column=Building.longitude,
        )
        query = (
            select(Building)
            .where(Building.latitude >= bounding_box.min_lat)
            .where(Building.latitude <= bounding_box.max_lat)
            .where(Building.longitude >= bounding_box.min_lon)
            .where(Building.longitude <= bounding_box.max_lon)
            .where(distance_expression <= radius_m)
            .order_by(distance_expression.asc(), Building.id.asc())
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())
