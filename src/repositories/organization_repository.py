from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.db_exceptions import handle_db_exceptions
from src.models.activity import Activity
from src.models.building import Building
from src.models.organization import Organization
from src.repositories.base import BaseRepository
from src.utils.geo import build_bounding_box, great_circle_distance_expression


class OrganizationRepository(BaseRepository[Organization]):
    model = Organization

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)

    @staticmethod
    def _relation_load_options():
        return (
            selectinload(Organization.building),
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )

    @handle_db_exceptions
    async def get_by_id(self, entity_id: int) -> Organization | None:
        query = (
            select(Organization)
            .options(*self._relation_load_options())
            .where(Organization.id == entity_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    @handle_db_exceptions
    async def list_organizations(
        self, limit: int = 100, offset: int = 0
    ) -> list[Organization]:
        query = (
            select(Organization)
            .options(*self._relation_load_options())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    @handle_db_exceptions
    async def list_by_building(
        self,
        building_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Organization]:
        query = (
            select(Organization)
            .options(*self._relation_load_options())
            .where(Organization.building_id == building_id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    @handle_db_exceptions
    async def list_by_activity(
        self,
        activity_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Organization]:
        query = (
            select(Organization)
            .options(*self._relation_load_options())
            .where(Organization.activities.any(Activity.id == activity_id))
            .distinct()
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    @handle_db_exceptions
    async def list_by_activities(
        self,
        activity_ids: list[int],
        limit: int = 100,
        offset: int = 0,
    ) -> list[Organization]:
        if not activity_ids:
            return []

        query = (
            select(Organization)
            .join(Organization.activities)
            .options(*self._relation_load_options())
            .where(Activity.id.in_(activity_ids))
            .distinct()
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    @handle_db_exceptions
    async def search_by_name(
        self,
        name: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Organization]:
        query = (
            select(Organization)
            .options(*self._relation_load_options())
            .where(Organization.name.ilike(f"%{name}%"))
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    @handle_db_exceptions
    async def search_by_radius(
        self,
        latitude: float,
        longitude: float,
        radius_m: float,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Organization]:
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
            select(Organization)
            .join(Organization.building)
            .options(*self._relation_load_options())
            .where(Building.latitude >= bounding_box.min_lat)
            .where(Building.latitude <= bounding_box.max_lat)
            .where(Building.longitude >= bounding_box.min_lon)
            .where(Building.longitude <= bounding_box.max_lon)
            .where(distance_expression <= radius_m)
            .order_by(distance_expression.asc(), Organization.id.asc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    @handle_db_exceptions
    async def search_by_bbox(
        self,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Organization]:
        query = (
            select(Organization)
            .join(Organization.building)
            .options(*self._relation_load_options())
            .where(Building.latitude >= min_lat)
            .where(Building.latitude <= max_lat)
            .where(Building.longitude >= min_lon)
            .where(Building.longitude <= max_lon)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())
