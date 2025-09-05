#!/bin/sh

uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py collectstatic --no-input --clear

exec "$@"