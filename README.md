# FastAPI Template Project

Шаблон backend-проекта на FastAPI с готовым каркасом:

- `core` (конфиг, БД, логирование, security),
- `models/schemas/repositories/services/routers`,
- интеграционные и unit тесты,
- Docker, Alembic, CI.

Предметная область удалена, оставлена одна базовая шаблонная сущность `TemplateEntity`, чтобы проект было проще клонировать и развивать под новый домен.

## Что уже есть в шаблоне

- Асинхронный стек: FastAPI + SQLAlchemy + PostgreSQL
- Базовая SQLAlchemy сущность `BaseModel` (`id`, `created_at`, `updated_at`)
- Пример вертикали `TemplateEntity` (model/repository/service/schema/router)
- API-key защита для прикладных ручек
- Seed-скрипт для шаблонных данных
- Тесты:
  - unit (`config`, `db_exceptions`, `base_repository`, `template_entity`)
  - integration (`system`, `template API`, `template repository`)

## Быстрый старт

1) Подготовить окружение:

```bash
cp env_example .env
uv sync --all-groups
```

2) Поднять PostgreSQL:

```bash
docker-compose up db -d
```

3) Применить миграции и заполнить шаблонными данными:

```bash
uv run alembic upgrade head
uv run python -m src.scripts.seed_data
```

4) Запустить приложение:

```bash
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Основные endpoint'ы

- `GET /health/live`
- `GET /health/ready`
- `GET /api/v1/template-entities` (требуется `X-API-Key`)
- `POST /api/v1/template-entities` (требуется `X-API-Key`)
- `DELETE /api/v1/template-entities/{entity_id}` (требуется `X-API-Key`)
- `GET /api/v1/template-entities/{entity_id}` (требуется `X-API-Key`)
- `GET /api/v1/admin/ui/template-entities` (базовая HTML-админка)

## Тесты и качество кода

```bash
uv run pytest
uv run ruff check src tests
uv run mypy src tests
```

## Как развивать шаблон под новый проект

1. Скопировать `TemplateEntity` вертикаль и переименовать под новый домен.
2. Добавить свои поля в модель и схемы.
3. Расширить repository/service новой бизнес-логикой.
4. Добавить роуты и тесты по аналогии с шаблонными.
