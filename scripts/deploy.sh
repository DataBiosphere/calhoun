#!/usr/bin/env bash
set -eo pipefail
cp config.$TERRA_ENV.json config.json
npm install
npm run lint
npm run generate-docs
gcloud app deploy --project=terra-calhoun-$TERRA_ENV
