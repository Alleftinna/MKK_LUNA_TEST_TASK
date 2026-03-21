from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.security import verify_api_key
from src.schemas.building import BuildingRead
from src.schemas.organization import (
    OrganizationRead,
    OrganizationSearchByBbox,
    OrganizationSearchByName,
    OrganizationSearchByRadius,
)
from src.services.building_service import BuildingService
from src.services.organization_service import OrganizationService

directory_router = APIRouter(
    prefix="/api/v1",
    tags=["directory"],
    dependencies=[Depends(verify_api_key)],
)


@directory_router.get("/buildings", response_model=list[BuildingRead])
async def list_buildings(
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> list[BuildingRead]:
    service = BuildingService(session=session)
    payload = await service.list(limit=limit, offset=offset)
    return [BuildingRead.model_validate(item) for item in payload]


@directory_router.get(
    "/organizations/by-building/{building_id}", response_model=list[OrganizationRead]
)
async def list_organizations_by_building(
    building_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> list[OrganizationRead]:
    service = OrganizationService(session=session)
    payload = await service.list_by_building(
        building_id=building_id, limit=limit, offset=offset
    )
    return [OrganizationRead.model_validate(item) for item in payload]


@directory_router.get(
    "/organizations/by-activity/{activity_id}", response_model=list[OrganizationRead]
)
async def list_organizations_by_activity(
    activity_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> list[OrganizationRead]:
    service = OrganizationService(session=session)
    payload = await service.list_by_activity(
        activity_id=activity_id,
        include_descendants=False,
        limit=limit,
        offset=offset,
    )
    return [OrganizationRead.model_validate(item) for item in payload]


@directory_router.get(
    "/organizations/search/by-activity/{activity_id}",
    response_model=list[OrganizationRead],
)
async def search_organizations_by_activity_tree(
    activity_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> list[OrganizationRead]:
    service = OrganizationService(session=session)
    payload = await service.list_by_activity(
        activity_id=activity_id,
        include_descendants=True,
        max_depth=3,
        limit=limit,
        offset=offset,
    )
    return [OrganizationRead.model_validate(item) for item in payload]


@directory_router.get("/organizations/search", response_model=list[OrganizationRead])
async def search_organizations_by_name(
    session: Annotated[AsyncSession, Depends(get_session)],
    name: str = Query(..., min_length=1),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> list[OrganizationRead]:
    query_payload = OrganizationSearchByName(name=name)
    service = OrganizationService(session=session)
    payload = await service.search_by_name(
        name=query_payload.name,
        limit=limit,
        offset=offset,
    )
    return [OrganizationRead.model_validate(item) for item in payload]


@directory_router.get(
    "/organizations/geo/radius", response_model=list[OrganizationRead]
)
async def search_organizations_by_radius(
    session: Annotated[AsyncSession, Depends(get_session)],
    latitude: float,
    longitude: float,
    radius_m: float = Query(..., gt=0),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> list[OrganizationRead]:
    query_payload = OrganizationSearchByRadius(
        latitude=latitude,
        longitude=longitude,
        radius_m=radius_m,
    )
    service = OrganizationService(session=session)
    payload = await service.search_by_radius(
        latitude=query_payload.latitude,
        longitude=query_payload.longitude,
        radius_m=query_payload.radius_m,
        limit=limit,
        offset=offset,
    )
    return [OrganizationRead.model_validate(item) for item in payload]


@directory_router.get("/organizations/geo/bbox", response_model=list[OrganizationRead])
async def search_organizations_by_bbox(
    session: Annotated[AsyncSession, Depends(get_session)],
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> list[OrganizationRead]:
    query_payload = OrganizationSearchByBbox(
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
    )
    service = OrganizationService(session=session)
    payload = await service.search_by_bbox(
        min_lat=query_payload.min_lat,
        max_lat=query_payload.max_lat,
        min_lon=query_payload.min_lon,
        max_lon=query_payload.max_lon,
        limit=limit,
        offset=offset,
    )
    return [OrganizationRead.model_validate(item) for item in payload]


@directory_router.get(
    "/organizations/{organization_id}", response_model=OrganizationRead
)
async def get_organization_by_id(
    organization_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> OrganizationRead:
    service = OrganizationService(session=session)
    payload = await service.get_by_id(organization_id)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )
    return OrganizationRead.model_validate(payload)
