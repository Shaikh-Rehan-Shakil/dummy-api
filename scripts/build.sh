#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

if ! command -v pipenv >/dev/null 2>&1; then
  echo "pipenv is required but not installed. Install it via 'pip install pipenv'." >&2
  exit 1
fi

echo "Installing project dependencies with pipenv..."
pipenv install

