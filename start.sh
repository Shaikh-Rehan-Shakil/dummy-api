#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT}"

export PIPENV_VENV_IN_PROJECT=1

export FLASK_APP=app
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-5000}"

echo "[start] Starting Dummy HR API on ${HOST}:${PORT}..."
python3 -m pipenv run flask run --host "${HOST}" --port "${PORT}" --reload