import os
from collections.abc import AsyncIterator
from typing import Any, cast

import psycopg
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from psycopg import sql
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import settings
from src.core.database import get_session
from src.models import Base
from src.models.template_entity import TemplateEntity
from src.routers.admin import admin_router
from src.routers.system import set_app_instance, system_router
from src.routers.template import template_router

DB_NAME_TEST = os.getenv("TEST_DB_NAME", "test_db")


def build_test_database_url() -> str:
    explicit_url = os.getenv("TEST_DATABASE_URL")
    if explicit_url:
        return explicit_url

    user = os.getenv("TEST_DB_USER", os.getenv("DB_USER", "user"))
    password = os.getenv("TEST_DB_PASS", os.getenv("DB_PASS", "password"))
    host = os.getenv("TEST_DB_HOST", os.getenv("DB_HOST", "localhost"))
    port = os.getenv("TEST_DB_PORT", os.getenv("DB_PORT", "5432"))
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{DB_NAME_TEST}"


def _build_admin_connection_kwargs() -> dict[str, object]:
    host = os.getenv("TEST_DB_HOST", os.getenv("DB_HOST", "localhost"))
    return {
        "dbname": "postgres",
        "user": os.getenv("TEST_DB_USER", os.getenv("DB_USER", "user")),
        "password": os.getenv("TEST_DB_PASS", os.getenv("DB_PASS", "password")),
        "host": host,
        "port": int(os.getenv("TEST_DB_PORT", os.getenv("DB_PORT", "5432"))),
    }


def create_db() -> None:
    connection = psycopg.connect(
        **cast(dict[str, Any], _build_admin_connection_kwargs())
    )
    connection.autocommit = True
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (DB_NAME_TEST,),
            )
            if cursor.fetchone() is None:
                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME_TEST))
                )
    finally:
        connection.close()


def drop_db() -> None:
    connection = psycopg.connect(
        **cast(dict[str, Any], _build_admin_connection_kwargs())
    )
    connection.autocommit = True
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = %s AND pid <> pg_backend_pid()
                """,
                (DB_NAME_TEST,),
            )
            cursor.execute(
                sql.SQL("DROP DATABASE IF EXISTS {}").format(
                    sql.Identifier(DB_NAME_TEST)
                )
            )
    finally:
        connection.close()


def truncate_db() -> None:
    connection = psycopg.connect(build_test_database_url().replace("+psycopg", ""))
    connection.autocommit = True
    try:
        with connection.cursor() as cursor:
            cursor.execute("SET session_replication_role = 'replica';")
            cursor.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
            )
            tables = cursor.fetchall()
            for (table_name,) in tables:
                cursor.execute(
                    sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY CASCADE").format(
                        sql.Identifier(table_name)
                    )
                )
            cursor.execute("SET session_replication_role = 'origin';")
    finally:
        connection.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db() -> AsyncIterator[None]:
    create_db()
    yield
    drop_db()


@pytest_asyncio.fixture(scope="function")
async def async_engine(setup_test_db) -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(
        build_test_database_url(),
        echo=False,
        poolclass=NullPool,
    )

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()
    truncate_db()


@pytest_asyncio.fixture
async def async_session(async_engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def seeded_template_data(
    async_session: AsyncSession,
) -> AsyncIterator[dict[str, int]]:
    first_entity = TemplateEntity(
        name="entity-one",
        description="primary fixture entity",
    )
    second_entity = TemplateEntity(
        name="entity-two",
        description="secondary fixture entity",
    )

    async_session.add_all([first_entity, second_entity])
    await async_session.commit()

    yield {
        "first_entity_id": first_entity.id,
        "second_entity_id": second_entity.id,
    }


@pytest_asyncio.fixture
async def client(
    async_engine: AsyncEngine,
    seeded_template_data: dict[str, int],
) -> AsyncIterator[AsyncClient]:
    original_api_key = settings.API_KEY
    settings.API_KEY = "test-api-key"

    session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False)

    async def override_get_session():
        async with session_factory() as session:
            yield session

    test_app = FastAPI()
    test_app.include_router(system_router)
    test_app.include_router(template_router)
    test_app.include_router(admin_router)
    set_app_instance(test_app)
    test_app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=test_app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as test_client:
        yield test_client

    test_app.dependency_overrides.clear()
    settings.API_KEY = original_api_key
