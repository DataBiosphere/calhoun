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
  && python3 -m venv /opt/venv \
  && /opt/venv/bin/pip install -r requirements-min.txt \
  && /opt/venv/bin/pip install gunicorn

# This SHOULD NOT BE USED IN PRODUCTION. It is used here because it disables the need to set up https for testing
ENV FLASK_DEBUG=1

EXPOSE 8000

CMD /opt/venv/bin/gunicorn -b :8000 main:app