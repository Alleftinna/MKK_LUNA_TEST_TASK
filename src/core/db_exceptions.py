from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.logger import logger


def _looks_like_async_session(candidate: Any) -> bool:
    rollback = getattr(candidate, "rollback", None)
    return callable(rollback)


def _extract_session(args: tuple[Any, ...], kwargs: dict[str, Any]) -> AsyncSession | Any | None:
    session_from_kwargs = kwargs.get("session")
    if _looks_like_async_session(session_from_kwargs):
        return session_from_kwargs

    for arg in args:
        if _looks_like_async_session(arg):
            return arg
        maybe_session = getattr(arg, "session", None)
        if _looks_like_async_session(maybe_session):
            return maybe_session
    return None


async def _safe_rollback(session: AsyncSession | Any | None) -> None:
    if session is None:
        return
    try:
        await session.rollback()
    except Exception:
        logger.exception("Failed to rollback session after DB error")


def _error_detail(default_detail: str, error: Exception) -> str:
    if settings.debug_enabled:
        return f"{default_detail}: {error}"
    return default_detail


def handle_db_exceptions(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    """Декоратор для обработки и нормализации ошибок при работе с БД."""

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        session = _extract_session(args=args, kwargs=kwargs)
        try:
            return await func(*args, **kwargs)
        except HTTPException as http_exc:
            logger.warning("HTTP exception in %s: %s", func.__name__, http_exc.detail)
            raise
        except IntegrityError as error:
            await _safe_rollback(session)
            logger.exception("Integrity error in %s", func.__name__)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=_error_detail("Integrity error occurred", error),
            ) from error
        except SQLAlchemyError as error:
            await _safe_rollback(session)
            logger.exception("Database error in %s", func.__name__)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=_error_detail("Database error occurred", error),
            ) from error
        except Exception as error:
            await _safe_rollback(session)
            logger.exception("Unexpected error in %s", func.__name__)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=_error_detail("An unexpected error occurred", error),
            ) from error

    return wrapper
