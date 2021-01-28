FROM python:3.7-slim-buster

COPY . /work
WORKDIR /work

RUN cp config.dev.py config.py

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install -r requirements-min.txt
RUN /opt/venv/bin/pip install gunicorn

# This SHOULD NOT BE USED IN PRODUCTION. It is used here because it disables the need to set up https for testing
ENV FLASK_DEBUG=1

EXPOSE 8000

CMD /opt/venv/bin/gunicorn -b :8000 main:app