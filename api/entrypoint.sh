#!/bin/bash

sleep 10

set -e

poetry run python manage.py makemigrations
poetry run python manage.py migrate --noinput

server_env=$1

if [[ "$server_env" = "prod" ]]
then
    poetry run python manage.py collectstatic --noinput
    uvicorn new_app.asgi:application --reload \
        --host 0.0.0.0 \
        --port 8000
else
    poetry run python manage.py runserver --insecure 0.0.0.0:8000
fi