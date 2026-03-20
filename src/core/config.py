from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")

    # Application settings
    APP_NAME: str
    DEBUG: bool = False
    COMPOSE_PROFILES: str = "DEV"
    HOST_PORT: int = 8081

    # DB settings
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_HOST: str = "localhost"
    DB_PORT: int
    DATABASE_ECHO: bool
    DATABASE_URL: str | None = None
    SENTRY_DSN: str | None = None

    # Logging settings
    SQL_LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR
    SQL_LOG_TO_CONSOLE: bool = False  # Отключаем SQL логи в консоли по умолчанию
    SQL_LOG_TO_FILE: bool = True  # Включаем SQL логи в файл по умолчанию

    @property
    def database_echo(self) -> bool:
        """Возвращает флаг SQL echo для SQLAlchemy."""
        return self.DATABASE_ECHO

    @property
    def debug_enabled(self) -> bool:
        """Возвращает флаг debug режима приложения."""
        return self.DEBUG

    @property
    def async_database_url(self) -> str:
        if self.DATABASE_URL:
            return (
                self.DATABASE_URL.replace("+asyncpg", "+psycopg")
                .replace("+psycopg2", "+psycopg")
            )
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def sync_database_url(self) -> str:
        return self.async_database_url


settings = Settings()
