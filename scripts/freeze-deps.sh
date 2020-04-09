#!/usr/bin/env bash
set -eo pipefail

clean_up() {
  echo 'cleaning up...'
  if [[ -n $VIRTUAL_ENV ]]; then
    deactivate
  fi
  rm -rf env.prod
}
trap clean_up EXIT HUP INT QUIT PIPE TERM 0 20

python3 -m venv env.prod
source env.prod/bin/activate

pip install -r requirements-min.txt
pip freeze -r requirements-min.txt > requirements.txt
