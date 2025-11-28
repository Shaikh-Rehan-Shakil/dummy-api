#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT}"

export PIPENV_VENV_IN_PROJECT=1

if ! command -v pipenv >/dev/null 2>&1; then
  echo "[build] Installing pipenv..."
  python3 -m pip install --upgrade pip pipenv
fi

echo "[build] Installing dependencies..."
pipenv install --deploy --ignore-pipfile

echo "[build] Ready."

