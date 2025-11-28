#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT}"

export PIPENV_VENV_IN_PROJECT=1

echo "[build] Ensuring pipenv is installed..."
python3 -m pip install --upgrade pip pipenv

echo "[build] Installing dependencies from Pipfile..."
python3 -m pipenv install --deploy --ignore-pipfile

echo "[build] Ready."

