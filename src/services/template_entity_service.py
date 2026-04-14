from sqlalchemy.ext.asyncio import AsyncSession

from src.models.template_entity import TemplateEntity
from src.repositories.template_entity_repository import TemplateEntityRepository
from src.schemas.template_entity import TemplateEntityCreate


class TemplateEntityService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = TemplateEntityRepository(session=session)

    async def get_by_id(self, entity_id: int) -> TemplateEntity | None:
        return await self.repository.get_by_id(entity_id)

    async def list_entities(self, limit: int = 100, offset: int = 0) -> list[TemplateEntity]:
        return await self.repository.list_all(limit=limit, offset=offset)

    async def create_entity(self, payload: TemplateEntityCreate) -> TemplateEntity:
        entity = TemplateEntity(name=payload.name, description=payload.description)
        return await self.repository.add(entity)

    async def delete_entity(self, entity_id: int) -> bool:
        return await self.repository.delete_by_id(entity_id=entity_id)
