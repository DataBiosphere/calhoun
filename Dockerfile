FROM us.gcr.io/broad-dsp-gcr-public/base/python:debian

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
  curl \
  pandoc \
  && apt update && apt install -yq --no-install-recommends \
  libcurl4-openssl-dev \
  libssl-dev \
  libgeos-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install R
RUN apt-get update && apt-get install -y --no-install-recommends \
  r-base \
  r-base-dev

RUN R -e 'install.packages(c("rmarkdown", "stringi", "tidyverse", "Seurat", "ggforce"))'

COPY . /work
WORKDIR /work

# Install Poetry and dependencies
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.8.2

ENV PATH="$PATH:$POETRY_HOME/bin"

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

EXPOSE 8080

CMD gunicorn -b :8080 main:app
