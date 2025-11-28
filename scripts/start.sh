#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

if ! command -v pipenv >/dev/null 2>&1; then
  echo "pipenv is required but not installed. Install it via 'pip install pipenv'." >&2
  exit 1
fi

export FLASK_APP=app
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-5000}"

echo "Starting Dummy HR API on ${HOST}:${PORT}..."
pipenv run flask run --host "${HOST}" --port "${PORT}" --reload

