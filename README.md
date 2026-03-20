# FastAPI Template Project

Базовый шаблон для создания веб-приложений на FastAPI с современной архитектурой и лучшими практиками.

## 🚀 Особенности

- **FastAPI** - современный веб-фреймворк для Python
- **PostgreSQL** - основная база данных
- **SQLAlchemy 2.0** - ORM с асинхронной поддержкой
- **Alembic** - миграции базы данных
- **Pydantic** - валидация данных и сериализация
- **Docker & Docker Compose** - контейнеризация
- **uv** - управление зависимостями и lock-файлом
- **Структурированное логирование**
- **Конфигурация через переменные окружения**
- **Готовые шаблоны для масштабируемой архитектуры**

## 📁 Структура проекта

```
FASTAPI_TEMPLATE-PROJECT/
├── src/
│   ├── core/           # Основные компоненты
│   │   ├── config.py   # Конфигурация приложения
│   │   ├── database.py # Настройки БД
│   │   ├── logger.py   # Логирование
│   │   └── templates.py # Шаблоны
│   ├── models/         # SQLAlchemy модели
│   ├── schemas/        # Pydantic схемы
│   ├── services/       # Бизнес-логика
│   ├── routers/        # API роутеры
│   ├── integrations/   # Внешние интеграции
│   ├── utils/          # Утилиты
│   └── main.py         # Точка входа
├── templates/          # HTML шаблоны
├── data/              # Данные БД (для Docker)
├── logs/              # Логи приложения
├── docker-compose.yml # Docker Compose конфигурация
├── Dockerfile         # Docker образ
├── pyproject.toml     # Зависимости и настройки Poetry
└── env_example        # Пример переменных окружения
```

## 🛠 Установка и запуск

### Предварительные требования

- Python 3.14
- Docker и Docker Compose
- uv

### 1. Клонирование и настройка

```bash
git clone <repository-url>
cd FASTAPI_TEMPLATE-PROJECT
```

### 2. Настройка переменных окружения

```bash
cp env_example .env
```

Отредактируйте `.env` файл под ваши нужды:

```env
APP_NAME=your_app_name
HOST_PORT=8899
DB_NAME=postgres
DB_USER=your_user
DB_PORT=5435
DB_PASS=your_password
DATABASE_ECHO=1
DEBUG=1
```

### 3. Запуск с Docker (рекомендуется)

```bash
# DEV: сборка и запуск
docker-compose up --build

# DEV: запуск в фоновом режиме
docker-compose up -d --build

# PROD-профиль (без --reload и без bind-mount)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

### 4. Локальная разработка

```bash
# Установка зависимостей
uv sync --all-groups

# Запуск PostgreSQL через Docker
docker-compose up db -d

# Запуск приложения
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Проверки качества кода

```bash
# Линтинг
uv run ruff check src tests

# Статическая типизация
uv run mypy src tests

# Установка pre-commit хуков
uv run pre-commit install

# Прогон хуков вручную
uv run pre-commit run --all-files
```

## 📚 API Документация

После запуска приложения документация доступна по адресам:

- **Swagger UI**: `http://localhost:8899/docs`
- **ReDoc**: `http://localhost:8899/redoc`
- **OpenAPI JSON**: `http://localhost:8899/openapi.json`

## 🗄 База данных

### Миграции

```bash
# Создание новой миграции
alembic revision --autogenerate -m "Description"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1

# Проверка, что Alembic скрипты корректно видят текущие head-ревизии
alembic heads
```

### Подключение к БД

```bash
# Через Docker
docker exec -it your_app_name_db psql -U your_user -d postgres

# Локально (если PostgreSQL установлен)
psql -h localhost -p 5435 -U your_user -d postgres
```

## 🧪 Тестирование

```bash
# Запуск тестов
uv run pytest

# Запуск с покрытием
uv run pytest --cov=src

# Запуск конкретного теста
uv run pytest tests/test_specific.py::test_function
```

## ✅ CI

В проект добавлен workflow `.github/workflows/ci.yml`, который запускает:

- `ruff check`
- `mypy`
- `pytest --cov=src`
- `alembic heads`

## 📝 Логирование

Логи сохраняются в директории `logs/` и настраиваются в `src/core/logger.py`.

## 🔧 Разработка

### Добавление новых роутеров

1. Создайте файл в `src/routers/`
2. Определите роутер с помощью `APIRouter`
3. Подключите в `src/main.py`

```python
# src/routers/example.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["example"])

@router.get("/items")
async def get_items():
    return {"items": []}
```

### Добавление моделей

1. Создайте модель в `src/models/`
2. Создайте схему в `src/schemas/`
3. Добавьте сервис в `src/services/`

### Конфигурация

Основные настройки находятся в `src/core/config.py` и загружаются из переменных окружения.

## 🐳 Docker

### Сборка образа

```bash
docker build -t your-app-name .
```

### Запуск контейнера

```bash
docker run -p 8899:8000 --env-file .env your-app-name
```

### Health endpoints

- `GET /health/live` — liveness probe
- `GET /health/ready` — readiness probe (проверяет подключение к БД)

## 📦 Зависимости

Основные зависимости:

- **FastAPI** - веб-фреймворк
- **Uvicorn** - ASGI сервер
- **SQLAlchemy** - ORM
- **Alembic** - миграции
- **Pydantic** - валидация данных
- **Psycopg (v3)** - драйвер PostgreSQL (sync + async)
- **Jinja2** - шаблонизатор
- **APScheduler** - планировщик задач
- **Boto3** - AWS SDK
- **Elasticsearch** - поисковый движок
- **Sentry** - мониторинг ошибок

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT.

## 🆘 Поддержка

При возникновении проблем:

1. Проверьте логи в директории `logs/`
2. Убедитесь, что все переменные окружения настроены
3. Проверьте, что PostgreSQL запущен и доступен
4. Создайте Issue в репозитории

---

**Удачной разработки! 🚀** 