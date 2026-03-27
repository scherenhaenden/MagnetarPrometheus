#!/usr/bin/env bash
# MagnetarPrometheus Backend Script
# This shell script serves as a localized entry point for running the python
# workflow engine. It ensures the environment exists and isolates python
# path complexities from the caller.

set -euo pipefail

# Calculate absolute paths for the repository root and virtual environment
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${VENV_DIR:-${ROOT_DIR}/venv}"
VENV_ACTIVATE="${VENV_DIR}/bin/activate"

# Verify if the virtual environment exists by checking its activation script.
# If absent, seamlessly trigger the python bootstrap process, suppressing
# stdout to maintain a clean terminal UX, leaving stderr for failure tracing.
if [ ! -f "${VENV_ACTIVATE}" ]; then
    echo "Virtual environment missing. Bootstrapping first..."
    bash "${ROOT_DIR}/scripts/bootstrap_python.sh" > /dev/null
fi

# Activate the local virtual environment to guarantee that python and
# dependency paths are correctly sourced before module execution.
source "${VENV_ACTIVATE}"

# The runtime shell wrapper stays intentionally thin.
# The PoC behavior should be reproducible from a clean checkout without
# requiring the caller to manually activate a virtual environment first.
# Here, PYTHONPATH is explicitly extended to include the python SDK and Backend
# sources, ensuring internal imports resolve successfully. Finally, any CLI
# parameters provided to this script are forwarded to the Python cli execution.
PYTHONPATH="${ROOT_DIR}/sdk/python/src:${ROOT_DIR}/backend/src" python -m magnetar_prometheus.cli "$@"
