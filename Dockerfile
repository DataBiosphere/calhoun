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
  curl \
  build-essential \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN R -e 'install.packages(c("rmarkdown", "stringi", "tidyverse", "Seurat", "ggforce"))'

COPY . /work
WORKDIR /work

# Set up python env
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN export PATH="/root/.local/bin:$PATH"
RUN poetry install
# RUN pip install -r requirements-min.txt && pip install gunicorn

EXPOSE 8080

CMD gunicorn -b :8080 main:app
