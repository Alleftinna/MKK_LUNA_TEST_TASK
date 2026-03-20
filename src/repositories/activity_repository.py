from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.activity import Activity
from src.repositories.base import BaseRepository


class ActivityRepository(BaseRepository[Activity]):
    model = Activity

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)

    async def list_tree(self) -> list[Activity]:
        query = select(Activity).order_by(Activity.level.asc(), Activity.name.asc())
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_descendant_ids(
        self, activity_id: int, max_depth: int = 3
    ) -> list[int]:
        if max_depth < 1:
            return []

        discovered_ids: list[int] = [activity_id]
        current_level_ids: list[int] = [activity_id]

        for _ in range(max_depth - 1):
            if not current_level_ids:
                break

            query = select(Activity.id).where(Activity.parent_id.in_(current_level_ids))
            result = await self.session.execute(query)
            next_level_ids = list(result.scalars().all())

            if not next_level_ids:
                break

            discovered_ids.extend(next_level_ids)
            current_level_ids = next_level_ids

        return discovered_ids
