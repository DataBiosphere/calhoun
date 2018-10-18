FROM gcr.io/google-appengine/nodejs
RUN apt-get update && \
  apt-get install -y python3-pip && \
  python3 -m pip install jupyter
COPY . /app/
