FROM python:3.12

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY /event_manager/ /usr/src/app/
COPY ./pyproject.toml /usr/src/app/
COPY ./uv.lock /usr/src/app/

WORKDIR /usr/src/app

RUN uv sync --locked

ENV PATH="/usr/src/app/.venv/bin:$PATH"

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
