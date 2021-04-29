#!/usr/bin/env bash

# Build and start calhoun
docker image build . -t calhoun-test:0
docker kill t1 || true
docker run -e FLASK_DEBUG=1 --rm -itd --name t1 -p 8000:8000 calhoun-test:0

# Wait for calhoun to start
sleep 5

# /status test case
status_code=$(curl -sI --write-out %{http_code} -o /dev/null http://127.0.0.1:8000/status)
echo -e "Response from /status: $status_code"

if [ "$status_code" -ne 200 ] ; then
  echo -e "  ** Failure! Expected 200 but was $status_code."
  docker kill t1 || true
  exit 1
fi

if [ "$RUN_AUTHENTICATED_TEST" -eq 1 ] ;
then
  # ipynb test case
  status_code=$(curl -s --write-out %{http_code} -o /dev/null \
    -X POST -H "Content-Type: application/json" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    --data @notebooks/test1.ipynb \
    http://127.0.0.1:8000/api/convert)

  echo -e "Response from /api/convert: $status_code"

  if [ "$status_code" -ne 200 ] ; then
    echo -e "  ** Failure! Expected 200 but was $status_code."
    docker kill t1 || true
    exit 1
  fi

  # rmd test case
  status_code=$(curl -s --write-out %{http_code} -o /dev/null \
    -X POST -H "Content-Type: application/json" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    --data @notebooks/test-rmd.ipynb \
    http://127.0.0.1:8000/api/convert/rmd)

  echo -e "Response from /api/convert/rmd: $status_code"

  if [ "$status_code" -ne 200 ] ; then
    echo -e "  ** Failure! Expected 200 but was $status_code."
    docker kill t1 || true
    exit 1
  fi
else
  echo "Skipping authenticated tests."
fi

echo "All tests passed.\n"
docker kill t1 || true
exit 0