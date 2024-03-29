FROM us.gcr.io/broad-dsp-gcr-public/base/python:debian

# Install R
RUN apt-get update && apt-get install -y --no-install-recommends \
  r-base \
  r-base-dev \
  pandoc \
  && apt update \
  && apt install -yq --no-install-recommends \
  libcurl4-openssl-dev \
  libssl-dev \
  libgeos-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN R -e 'install.packages(c("rmarkdown", "stringi", "tidyverse", "Seurat", "ggforce"))'

COPY . /work
WORKDIR /work

# Set up python env
RUN pip install "poetry==1.4.0"
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

EXPOSE 8080

CMD gunicorn -b :8080 main:app
