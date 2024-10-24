#!/usr/bin/env bash

# Build calhoun and run unit tests
docker image build . -t calhoun-test:0
docker kill t1 || true
docker run --rm --name t1 \
  --entrypoint python \
  calhoun-test:0 \
  unit_test.py -v

# Capture the exit code of the docker run command
exit_code=$?

# Exit the script with the same exit code to trigger a failure in GH
exit $exit_code
