#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${VENV_DIR:-${ROOT_DIR}/venv}"
VENV_ACTIVATE="${VENV_DIR}/bin/activate"

if [ ! -f "${VENV_ACTIVATE}" ]; then
    echo "Virtual environment missing. Bootstrapping first..."
    bash "${ROOT_DIR}/scripts/bootstrap_python.sh" > /dev/null
fi

source "${VENV_ACTIVATE}"

# The runtime shell wrapper stays intentionally thin.
# The PoC behavior should be reproducible from a clean checkout without
# requiring the caller to manually activate a virtual environment first.
PYTHONPATH="${ROOT_DIR}/sdk/python/src:${ROOT_DIR}/backend/src" python -m magnetar_prometheus.cli "$@"
