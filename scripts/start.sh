#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

export FLASK_APP=app
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-5000}"

echo "Starting Dummy HR API on ${HOST}:${PORT}..."
python -m flask run --host "${HOST}" --port "${PORT}" --reload