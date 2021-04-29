FROM python:3.7-slim-buster

# Install R
RUN apt-get update && apt-get install -y --no-install-recommends \
  r-base \
  r-base-dev \
  pandoc \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN R -e 'install.packages("rmarkdown")'

COPY . /work
WORKDIR /work

# Set up python env
RUN cp config.dev.py config.py \
  && pip install -r requirements-min.txt \
  && pip install gunicorn

EXPOSE 8000

CMD gunicorn -b :8000 main:app