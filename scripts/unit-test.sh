#!/usr/bin/env bash

# Build calhoun and run unit tests
docker image build . -t calhoun-test:0
docker kill t1 || true > /dev/null 2>&1
docker run --rm --name t1 \
  --entrypoint python \
  calhoun-test:0 \
  test_convert.py