#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${VENV_DIR:-${ROOT_DIR}/venv}"
VENV_ACTIVATE="${VENV_DIR}/bin/activate"

echo "Running MagnetarPrometheus backend..."

if [ ! -f "${VENV_ACTIVATE}" ]; then
    echo "Virtual environment missing. Bootstrapping first..."
    bash "${ROOT_DIR}/scripts/bootstrap_python.sh"
fi

source "${VENV_ACTIVATE}"

PYTHONPATH="${ROOT_DIR}/sdk/python/src:${ROOT_DIR}/backend/src" python -m magnetar_prometheus.cli "$@"
