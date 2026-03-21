from typing import Any

from src.core.config import Settings


def build_settings(**overrides: Any) -> Settings:
    base_data = {
        "APP_NAME": "test-app",
        "DEBUG": False,
        "COMPOSE_PROFILES": "test",
        "HOST_PORT": 8000,
        "DB_USER": "user",
        "DB_PASS": "password",
        "DB_NAME": "postgres",
        "DB_HOST": "localhost",
        "DB_PORT": 5432,
        "DATABASE_ECHO": False,
        "DATABASE_URL": None,
        "SENTRY_DSN": None,
    }
    base_data.update(overrides)
    return Settings(**base_data)  # type: ignore[arg-type]


def test_builds_async_database_url_from_parts() -> None:
    settings = build_settings()
    assert (
        settings.async_database_url
        == "postgresql+psycopg://user:password@localhost:5432/postgres"
    )


def test_uses_database_url_when_provided() -> None:
    settings = build_settings(DATABASE_URL="postgresql+asyncpg://a:b@db:5432/test_db")
    assert settings.async_database_url == "postgresql+psycopg://a:b@db:5432/test_db"
    assert settings.sync_database_url == "postgresql+psycopg://a:b@db:5432/test_db"
