import logging
import logging.config
from pathlib import Path

from src.core.config import settings


def configure_sql_logging() -> None:
    """
    Дополнительная настройка логирования для SQLAlchemy.
    Устанавливает правильные уровни в зависимости от окружения.
    """
    # В продакшене отключаем SQL логи полностью
    if settings.COMPOSE_PROFILES.upper() == "PROD":
        sql_level = logging.WARNING
    elif settings.debug_enabled:
        sql_level = logging.INFO
    else:
        sql_level = logging.WARNING

    # Настраиваем SQLAlchemy логгеры
    sqlalchemy_loggers = [
        "sqlalchemy.engine",
        "sqlalchemy.dialects",
        "sqlalchemy.pool",
        "sqlalchemy.orm",
    ]

    for logger_name in sqlalchemy_loggers:
        sql_logger = logging.getLogger(logger_name)
        sql_logger.setLevel(sql_level)
        # Отключаем propagation, чтобы SQL логи не попадали в root logger
        sql_logger.propagate = False


def setup_logging():
    """
    Настраивает логирование для приложения.

    Использует конфигурацию из logging.ini и создает директорию для логов.
    Также настраивает отправку логов в Elasticsearch, если доступен.
    """
    # Создаем директорию для логов, если она не существует
    log_dir = Path("logs")
    if not log_dir.exists():
        log_dir.mkdir(parents=True)

    # Загружаем конфигурацию логирования из файла
    logging_ini_path = Path("logging.ini")
    if logging_ini_path.exists():
        logging.config.fileConfig(logging_ini_path, disable_existing_loggers=False)
        logging.info("Logging configured from logging.ini")
    else:
        # Базовая конфигурация, если файл не найден
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_dir / settings.APP_NAME),
            ],
        )
        logging.warning("logging.ini not found, using basic configuration")

    # Дополнительная настройка SQL логирования
    configure_sql_logging()

    app_logger = logging.getLogger(settings.APP_NAME)

    # Устанавливаем уровень логирования в зависимости от окружения
    if settings.debug_enabled:
        app_logger.setLevel(logging.DEBUG)
        logging.info("Debug logging enabled")
    else:
        app_logger.setLevel(logging.INFO)

    return app_logger


# Создаем логгер для использования в других модулях
logger = setup_logging()


def shutdown_logging():
    """
    Функция для корректного завершения работы логгера при завершении приложения.
    Должна быть вызвана при завершении приложения.
    """
    # Останавливаем асинхронный обработчик логов, если он был создан
    if hasattr(logger, "listener") and logger.listener:
        try:
            logger.listener.stop()
            logger.info("Elasticsearch logging stopped")
        except Exception:
            # Игнорируем ошибки при завершении работы логгера
            pass
