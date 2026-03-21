from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.core.config import settings
from src.core.db_exceptions import handle_db_exceptions


class DummyRepository:
    def __init__(self) -> None:
        self.session = AsyncMock()

    @handle_db_exceptions
    async def ok(self) -> str:
        return "ok"

    @handle_db_exceptions
    async def raises_http(self) -> None:
        raise HTTPException(status_code=418, detail="teapot")

    @handle_db_exceptions
    async def raises_integrity(self) -> None:
        raise IntegrityError("insert", {"id": 1}, Exception("duplicate key"))

    @handle_db_exceptions
    async def raises_sqlalchemy(self) -> None:
        raise SQLAlchemyError("db unavailable")

    @handle_db_exceptions
    async def raises_unexpected(self) -> None:
        raise RuntimeError("unexpected")


@pytest.mark.asyncio
async def test_decorator_returns_original_result() -> None:
    repository = DummyRepository()
    payload = await repository.ok()
    assert payload == "ok"
    repository.session.rollback.assert_not_awaited()


@pytest.mark.asyncio
async def test_decorator_passthrough_http_exception() -> None:
    repository = DummyRepository()
    with pytest.raises(HTTPException) as error:
        await repository.raises_http()
    assert error.value.status_code == 418
    assert error.value.detail == "teapot"
    repository.session.rollback.assert_not_awaited()


@pytest.mark.asyncio
async def test_decorator_handles_integrity_error_with_rollback() -> None:
    repository = DummyRepository()
    with pytest.raises(HTTPException) as error:
        await repository.raises_integrity()
    assert error.value.status_code == 400
    assert "Integrity error occurred" in error.value.detail
    repository.session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_decorator_hides_internal_error_details_when_not_debug() -> None:
    repository = DummyRepository()
    original_debug = settings.DEBUG
    settings.DEBUG = False
    try:
        with pytest.raises(HTTPException) as error:
            await repository.raises_sqlalchemy()
        assert error.value.status_code == 500
        assert error.value.detail == "Database error occurred"
    finally:
        settings.DEBUG = original_debug


@pytest.mark.asyncio
async def test_decorator_shows_internal_error_details_in_debug() -> None:
    repository = DummyRepository()
    original_debug = settings.DEBUG
    settings.DEBUG = True
    try:
        with pytest.raises(HTTPException) as error:
            await repository.raises_unexpected()
        assert error.value.status_code == 500
        assert "An unexpected error occurred" in error.value.detail
        assert "unexpected" in error.value.detail
    finally:
        settings.DEBUG = original_debug
