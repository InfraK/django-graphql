#!/usr/bin/env bash

set -x
set -e

export PIPENV_VENV_IN_PROJECT="enabled"

if ! command -v pipenv &>/dev/null; then
  pip install pipenv
fi

LOCK_FILE=Pipfile.lock
if exists -f "$LOCK_FILE"; then
  pipenv sync
else
  pipenv install
fi
