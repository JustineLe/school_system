FROM python:3.9.7-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY pyproject.toml entrypoint.sh ./
RUN chmod +x /code/entrypoint.sh

RUN apt-get update && \
    apt-get install --no-install-recommends --yes && \
    pip install poetry

RUN poetry config virtualenvs.in-project false && poetry env use python
RUN poetry install --no-root
