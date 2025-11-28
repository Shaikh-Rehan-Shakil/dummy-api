#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT}"

export PIPENV_VENV_IN_PROJECT=1

if ! command -v pipenv >/dev/null 2>&1; then
  echo "[start] Installing pipenv..."
  python3 -m pip install --upgrade pip pipenv
fi

export FLASK_APP=app
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-5000}"

echo "[start] Starting Dummy HR API on ${HOST}:${PORT}..."
pipenv run flask run --host "${HOST}" --port "${PORT}" --reload