import os

import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.models import Base


def build_test_database_url() -> str:
    explicit_url = os.getenv("TEST_DATABASE_URL")
    if explicit_url:
        return explicit_url

    user = os.getenv("TEST_DB_USER", os.getenv("DB_USER", "user"))
    password = os.getenv("TEST_DB_PASS", os.getenv("DB_PASS", "password"))
    host = os.getenv("TEST_DB_HOST", os.getenv("DB_HOST", "127.0.0.1"))
    if host == "localhost":
        host = "127.0.0.1"
    port = os.getenv("TEST_DB_PORT", os.getenv("DB_PORT", "5432"))
    db_name = os.getenv("TEST_DB_NAME", os.getenv("DB_NAME", "postgres"))
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db_name}"


@pytest_asyncio.fixture
async def async_engine() -> AsyncEngine:
    engine = create_async_engine(build_test_database_url(), echo=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def async_session(async_engine: AsyncEngine) -> AsyncSession:
    session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
