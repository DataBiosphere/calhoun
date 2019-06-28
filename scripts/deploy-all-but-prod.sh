#!/usr/bin/env bash
set -eo pipefail

for env in dev alpha perf staging ; do
    TERRA_ENV=$env
    cp config.$TERRA_ENV.py config.py
    gcloud app deploy --project=terra-calhoun-$TERRA_ENV
done
