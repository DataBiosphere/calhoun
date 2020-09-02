#!/usr/bin/env bash
set -eo pipefail

cp config.$TERRA_ENV.py config.py
gcloud app deploy --project=terra-calhoun-$TERRA_ENV $*
