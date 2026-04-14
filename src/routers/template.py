from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.security import verify_api_key
from src.schemas.template_entity import TemplateEntityCreate, TemplateEntityRead
from src.services.template_entity_service import TemplateEntityService

template_router = APIRouter(
    prefix="/api/v1/template-entities",
    tags=["template-entities"],
    dependencies=[Depends(verify_api_key)],
)


@template_router.get("", response_model=list[TemplateEntityRead])
async def list_template_entities(
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> list[TemplateEntityRead]:
    service = TemplateEntityService(session=session)
    payload = await service.list_entities(limit=limit, offset=offset)
    return [TemplateEntityRead.model_validate(item) for item in payload]


@template_router.post("", response_model=TemplateEntityRead, status_code=status.HTTP_201_CREATED)
async def create_template_entity(
    body: TemplateEntityCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TemplateEntityRead:
    service = TemplateEntityService(session=session)
    payload = await service.create_entity(payload=body)
    await session.commit()
    return TemplateEntityRead.model_validate(payload)


@template_router.get("/{entity_id}", response_model=TemplateEntityRead)
async def get_template_entity(
    entity_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TemplateEntityRead:
    service = TemplateEntityService(session=session)
    payload = await service.get_by_id(entity_id=entity_id)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template entity not found",
        )
    return TemplateEntityRead.model_validate(payload)


@template_router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template_entity(
    entity_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> None:
    service = TemplateEntityService(session=session)
    deleted = await service.delete_entity(entity_id=entity_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template entity not found",
        )
    await session.commit()
