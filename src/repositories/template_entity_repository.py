from sqlalchemy.ext.asyncio import AsyncSession

from src.models.template_entity import TemplateEntity
from src.repositories.base import BaseRepository


class TemplateEntityRepository(BaseRepository[TemplateEntity]):
    model = TemplateEntity

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
