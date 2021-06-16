FROM us.gcr.io/broad-dsp-gcr-public/base/python:debian

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
RUN pip install -r requirements-min.txt && pip install gunicorn

EXPOSE 8080

CMD gunicorn -b :8080 main:app
