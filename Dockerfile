FROM python:3.13.7-slim

RUN apt-get update \
 && apt-get -y --no-install-recommends upgrade \
 && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV FASTAPI_ENV=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY pyproject.toml uv.lock README.md ./
COPY src/fastapi_solid/__init__.py ./src/fastapi_solid/__init__.py

RUN uv sync --frozen --no-dev

RUN useradd -m appuser && chown -R appuser /code
USER appuser

COPY --chown=appuser:appuser . .
EXPOSE 8000