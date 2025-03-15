FROM python:3.13.2-slim-bookworm AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.13.2 \
    UV_PROJECT_ENVIRONMENT=/app

COPY --from=ghcr.io/astral-sh/uv:0.6.3 /uv /uvx /bin/
RUN useradd --create-home app

FROM base AS builder

RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev libpq-dev wget

RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync \
        --locked \
        --no-install-project

COPY . /src
WORKDIR /src
RUN --mount=type=cache,target=/root/.cache \
    uv sync \
        --locked \
        --no-editable

FROM base

ENV PATH=/app/bin:$PATH

RUN apt-get update \
    && apt-get install -y --no-install-recommends git libpq5 \
    && apt-get -y autoremove \
    && apt-get clean autoclean \
    && rm -fr /var/lib/apt/lists/{apt,dpkg,cache,log} /tmp/* /var/tmp/*

COPY --from=builder --chown=app:app /app /app

COPY ./compose/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

COPY . /code
RUN chown app:app /code
WORKDIR /code

RUN mkdir /celery
RUN chown app /celery

USER app

ENTRYPOINT ["/entrypoint"]
