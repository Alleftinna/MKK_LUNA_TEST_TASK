FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT=/usr/local

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl libpq5 \
    && pip install uv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ARG INSTALL_DEV=false

COPY pyproject.toml uv.lock ./
RUN if [ "$INSTALL_DEV" = "true" ]; then uv sync --frozen --all-groups; else uv sync --frozen --no-dev; fi

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

