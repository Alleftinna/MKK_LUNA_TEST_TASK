import sentry_sdk

from src.core.config import settings


def setup_sentry() -> None:
    """Инициализация Sentry, если задан DSN."""
    if not settings.SENTRY_DSN:
        return
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0 if settings.debug_enabled else 0.1,
        environment=settings.COMPOSE_PROFILES.lower(),
    )
