FROM python:3.9.9-slim AS base

ARG DJANGO_ENV

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gettext \
    curl \
    && rm -rf /var/lib/apt/lists/* 

ENV POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Installing `poetry` package manager:
# https://github.com/python-poetry/poetry
RUN curl -sSL 'https://install.python-poetry.org' | python3 -

ENV PATH="$PATH:$POETRY_HOME/bin"

RUN poetry --version

FROM base AS builder

WORKDIR /app

# Copy only requirements, to cache them in docker layer
COPY ./poetry.lock ./pyproject.toml .

# Install deps:
RUN poetry run pip install -U pip \
    && poetry install \
        $(if [ "$DJANGO_ENV" = 'production' ]; then echo '--only main'; fi) \
        --no-interaction --no-ansi

# This is a special case. We need to run this script as an entry point:
COPY ./docker/django/entrypoint.sh /docker-entrypoint.sh

# Setting up proper permissions:
RUN chmod +x '/docker-entrypoint.sh' \
    # Replacing line separator CRLF with LF for Windows users:
    && sed -i 's/\r$//g' '/docker-entrypoint.sh'

ENTRYPOINT ["/docker-entrypoint.sh"]

FROM builder AS development

FROM development AS staging

FROM staging AS production