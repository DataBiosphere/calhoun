#!/usr/bin/env bash

# Build and start calhoun
docker image build . -t calhoun-test:0
docker kill t1 || true
docker run --rm -itd --name t1 -p 8000:8000 calhoun-test:0

# Wait for calhoun to start
sleep 5

echo -e "\nResponse from /status:\n"
curl -I -X GET http://127.0.0.1:8000/status


# If the status code of the previous call is 0 (successful)
if [ $? -eq 0 ] ;
then
  echo -e "\nSmoke test succeeded."
else
  echo -e "\nSmoke test failed."
  docker kill t1 || true
  exit 1;
fi

docker kill t1 || true

