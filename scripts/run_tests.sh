#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${VENV_DIR:-${ROOT_DIR}/venv}"
VENV_ACTIVATE="${VENV_DIR}/bin/activate"

echo "Running tests for MagnetarPrometheus..."

if [ ! -f "${VENV_ACTIVATE}" ]; then
    echo "Virtual environment missing. Bootstrapping first..."
    bash "${ROOT_DIR}/scripts/bootstrap_python.sh"
fi

source "${VENV_ACTIVATE}"

# Coverage is enforced in pytest configuration so this script can stay focused
# on providing a stable, repo-relative execution path.
cd "${ROOT_DIR}/backend"
pytest
