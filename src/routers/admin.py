from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from src.core.database import get_session
from src.services.template_entity_service import TemplateEntityService

admin_router = APIRouter(prefix="/api/v1/admin", tags=["admin-ui"])
templates = Jinja2Templates(directory="src/templates")


def _admin_context(request: Request) -> dict[str, object]:
    return {
        "request": request,
        "entities": [],
    }


@admin_router.get("/ui", include_in_schema=False)
async def admin_dashboard_ui() -> RedirectResponse:
    return RedirectResponse(url="/api/v1/admin/ui/template-entities", status_code=307)


@admin_router.get("/ui/template-entities", include_in_schema=False)
async def admin_template_entities_ui(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    context = _admin_context(request)
    service = TemplateEntityService(session=session)
    context["entities"] = await service.list_entities(limit=500, offset=0)
    return templates.TemplateResponse("admin/template_entities.html", context)
