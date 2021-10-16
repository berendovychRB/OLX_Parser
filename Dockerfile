FROM python:3.8

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry

WORKDIR /usr/src/fastapi

COPY ./app ./app

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction