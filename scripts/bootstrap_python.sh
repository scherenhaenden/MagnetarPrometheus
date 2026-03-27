#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${VENV_DIR:-${ROOT_DIR}/venv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_PYTHON="${VENV_DIR}/bin/python"
VENV_PIP="${VENV_DIR}/bin/pip"

echo "Bootstrapping MagnetarPrometheus Python runtime..."
if [ ! -d "${VENV_DIR}" ]; then
    echo "Creating virtual environment..."
    "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

if [ ! -x "${VENV_PYTHON}" ]; then
    echo "Virtual environment python not found at ${VENV_PYTHON}."
    exit 1
fi

# Keep bootstrap simple and deterministic for the PoC:
# 1. prepare an isolated virtual environment
# 2. install the runtime and test dependencies from the canonical package declarations
# 3. execute the Python-side startup check so missing imports are surfaced early
echo "Installing runtime and testing dependencies..."
"${VENV_PIP}" install setuptools wheel
"${VENV_PIP}" install --no-build-isolation -e "${ROOT_DIR}/sdk/python[dev]" -e "${ROOT_DIR}/backend[dev]"

echo "Running startup check (which may trigger automatic dependency installation if missing)..."
PYTHONPATH="${ROOT_DIR}/sdk/python/src:${ROOT_DIR}/backend/src" \
    "${VENV_PYTHON}" -c "from magnetar_prometheus.bootstrap import bootstrap_runtime; raise SystemExit(0 if bootstrap_runtime(auto_install=True) else 1)"

echo "Bootstrap complete."
