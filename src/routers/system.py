"""
Системные роуты приложения
"""

from fastapi import APIRouter, FastAPI, HTTPException, Request, Response, status
from fastapi.openapi.docs import (
    get_swagger_ui_html,
)

from src.core.config import settings
from src.core.database import is_db_healthy
from src.core.templates import Jinja2Templates

# Создаем роутер для системных эндпоинтов
system_router = APIRouter()


jinja_templates = Jinja2Templates(directory="src/templates")


@system_router.get("/", include_in_schema=False)
async def root(request: Request):
    """Главная страница"""
    return jinja_templates.TemplateResponse(
        "index.html",
        {"request": request, "settings": settings},
    )


@system_router.get("/docs#", include_in_schema=False)
async def get_documentation():
    """
    Кастомная страница Swagger UI с правильной настройкой OAuth2 Authorization Code Flow + PKCE
    """
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"Web {settings.APP_NAME} API Documentation",
    )


# Переменная для хранения ссылки на приложение
_app_instance: FastAPI | None = None


def set_app_instance(app: FastAPI) -> None:
    """Устанавливает ссылку на экземпляр приложения для избежания циклических импортов"""
    global _app_instance
    _app_instance = app


@system_router.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    """Получение OpenAPI схемы"""
    from fastapi.openapi.utils import get_openapi

    if _app_instance is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Application instance not set",
        )

    return get_openapi(
        title="Iteach API documentation",
        version="1.0.0",
        routes=_app_instance.routes,
    )


@system_router.get("/robots.txt", include_in_schema=False)
async def robots_txt():
    """Файл robots.txt"""
    content = "User-agent: *\nDisallow: /"
    return Response(content, media_type="text/plain")


@system_router.get("/health/live", include_in_schema=False)
async def liveness_probe() -> dict[str, str]:
    """Liveness probe: сервис запущен."""
    return {"status": "ok"}


@system_router.get("/health/ready", include_in_schema=False)
async def readiness_probe() -> dict[str, str]:
    """Readiness probe: сервис готов принимать трафик."""
    if not await is_db_healthy():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is not ready",
        )
    return {"status": "ready"}


@system_router.get("/sentry-debug", include_in_schema=False)
async def trigger_error():
    """Debug endpoint для тестирования Sentry"""
    if not settings.debug_enabled:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint is available only in debug mode",
        )
    return {"value": 1 / 0}
