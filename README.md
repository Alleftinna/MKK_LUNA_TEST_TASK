## Приложение доступно по адресу: http://31.128.33.148:8001

# Directory API (FastAPI)

REST API приложения для справочника:
- организаций
- зданий
- деятельностей (с вложенностью до 3 уровней)

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
- **API key авторизация**


## 📁 Структура проекта

```
MKK_LUNA_TEST_TASK/
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
│   ├── scripts/        # Скрипты (например, seed данных)
│   └── main.py         # Точка входа
├── data/              # Данные БД (для Docker)
├── logs/              # Логи приложения
├── docker-compose.yml # Docker Compose конфигурация
├── Dockerfile         # Docker образ
├── pyproject.toml     # Зависимости и настройки uv
└── env_example        # Пример переменных окружения
```

## 🛠 Установка и запуск

### Предварительные требования

- Python 3.14
- Docker и Docker Compose
- uv

### 1. Клонирование и настройка

```bash
git clone https://github.com/Alleftinna/MKK_LUNA_TEST_TASK
cd MKK_LUNA_TEST_TASK
```

### 2. Настройка переменных окружения

```bash
cp env_example .env
```

Отредактируйте `.env` файл под ваши нужды:

```env
APP_NAME=your_app_name
API_KEY=test-api-key
HOST_PORT=8899
DB_NAME=postgres
DB_USER=your_user
DB_HOST=your_db_host
DB_PORT=5432
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

# Запуск PostgreSQL
docker-compose up db -d

# Применение миграций (если есть)
uv run alembic upgrade head

# Заполнение БД тестовыми русскоязычными данными
uv run python -m src.scripts.seed_data

# Запуск приложения
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Запуск проекта с Docker (полный цикл)

```bash
# Поднять приложение + БД
docker-compose up -d --build

# Применить миграции внутри app-контейнера
docker-compose exec app uv run alembic upgrade head

# Заполнить БД тестовыми данными
docker-compose exec app uv run python -m src.scripts.seed_data
```

### 6. Проверки качества кода

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

### Авторизация

Для ручек справочника (`/api/v1/*`) требуется заголовок:

```http
X-API-Key: <API_KEY из .env>
```

## 🗄 База данных

### Миграции

```bash
# Создание новой миграции
uv run alembic revision --autogenerate -m "Description"

# Применение миграций
uv run alembic upgrade head

# Откат миграции
uv run alembic downgrade -1

# Проверка, что Alembic скрипты корректно видят текущие head-ревизии
uv run alembic heads
```

### Заполнение БД тестовыми данными

Используется скрипт `src/scripts/seed_data.py`.

```bash
# Очистить текущие данные справочника и заполнить заново
uv run python -m src.scripts.seed_data

# Заполнить без предварительной очистки
uv run python -m src.scripts.seed_data --no-reset
```

Скрипт добавляет:
- здания с координатами
- дерево деятельностей (до 3 уровней)
- организации с телефонами и описаниями телефонов

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

# Только unit-тесты
uv run pytest tests/unit_tests

# Только integration-тесты
uv run pytest tests/integration_tests

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

## 🔧 Основные ручки API

- `GET /api/v1/buildings`
- `GET /api/v1/organizations/{organization_id}`
- `GET /api/v1/organizations/by-building/{building_id}`
- `GET /api/v1/organizations/by-activity/{activity_id}`
- `GET /api/v1/organizations/search/by-activity/{activity_id}` (с учетом вложенных деятельностей)
- `GET /api/v1/organizations/search?name=...`
- `GET /api/v1/organizations/geo/radius?latitude=...&longitude=...&radius_m=...`
- `GET /api/v1/organizations/geo/bbox?min_lat=...&max_lat=...&min_lon=...&max_lon=...`

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
