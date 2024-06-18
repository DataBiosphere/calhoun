FROM us.gcr.io/broad-dsp-gcr-public/base/python:debian

ENV R_BASE_VERSION 4.4.0

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

## Switch to use Debian unstable - neccessary to install 4.4.0 since it was just released 4/24/24
RUN echo "deb http://http.debian.net/debian sid main" > /etc/apt/sources.list.d/debian-unstable.list \
        && echo 'APT::Default-Release "testing";' > /etc/apt/apt.conf.d/default \
        && echo 'APT::Install-Recommends "false";' > /etc/apt/apt.conf.d/90local-no-recommends

# Install R
RUN apt-get update && apt-get install -y -t unstable --no-install-recommends \
  r-base=${R_BASE_VERSION}-* \
  r-base-dev=${R_BASE_VERSION}-*

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
