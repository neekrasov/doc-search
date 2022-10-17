FROM python:3.11-rc-bullseye

ENV HOME = /usr/src/doc-search

WORKDIR $HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip
RUN pip install poetry 
RUN poetry config virtualenvs.create false
RUN poetry install --without dev --no-root

COPY . $HOME

WORKDIR $HOME/app
