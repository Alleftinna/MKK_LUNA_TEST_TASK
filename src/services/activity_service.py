from sqlalchemy.ext.asyncio import AsyncSession

from src.models.activity import Activity
from src.repositories.activity_repository import ActivityRepository


class ActivityService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = ActivityRepository(session=session)

    async def get_by_id(self, activity_id: int) -> Activity | None:
        return await self.repository.get_by_id(activity_id)

    async def list(self, limit: int = 100, offset: int = 0) -> list[Activity]:
        return await self.repository.list(limit=limit, offset=offset)

    async def list_tree(self) -> list[Activity]:
        return await self.repository.list_tree()

    async def get_descendant_ids(
        self, activity_id: int, max_depth: int = 3
    ) -> list[int]:
        return await self.repository.get_descendant_ids(
            activity_id=activity_id, max_depth=max_depth
        )
