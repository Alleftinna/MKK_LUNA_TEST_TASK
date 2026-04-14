from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.config import settings
from src.core.database import close_db, init_db
from src.core.logger import logger, shutdown_logging
from src.core.scheduler import set_jobs, stop_scheduler
from src.integrations import setup_sentry
from src.routers.admin import admin_router
from src.routers.system import set_app_instance, system_router
from src.routers.template import template_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Контекст жизненного цикла приложения"""
    # Инициализируем подключение к БД
    logger.info("Initializing database connection...")
    setup_sentry()
    await init_db()
    await set_jobs()

    logger.info("Application startup complete")
    yield

    # Shutdown
    logger.info("Shutting down application...")
    await close_db()
    await stop_scheduler()
    # Корректно завершаем работу логгера
    shutdown_logging()
    logger.info("Application shutdown complete")


app = FastAPI(
    lifespan=lifespan,
    title=f"Web {settings.APP_NAME} API Documentation",
    description=f"{settings.APP_NAME} api",
    version="1.0.0",
)

app.include_router(system_router)
app.include_router(template_router)
app.include_router(admin_router)

set_app_instance(app)
