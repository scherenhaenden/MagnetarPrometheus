#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOTSTRAP_SCRIPT="${ROOT_DIR}/scripts/bootstrap_python.sh"
RUN_SCRIPT="${ROOT_DIR}/scripts/run_backend.sh"

echo "=== MagnetarPrometheus Launcher ==="
echo "--- Bootstrapping Environment ---"

if [ ! -x "${BOOTSTRAP_SCRIPT}" ]; then
    echo "Bootstrap script not found at ${BOOTSTRAP_SCRIPT}."
    exit 1
fi

if [ ! -x "${RUN_SCRIPT}" ]; then
    echo "Backend run script not found at ${RUN_SCRIPT}."
    exit 1
fi

# Print an explicit message so the user knows what's happening
echo "Bootstrapping (this may take a minute)..."
bash "${BOOTSTRAP_SCRIPT}" > /dev/null
echo
echo "--- Executing Workflow Engine ---"
bash "${RUN_SCRIPT}" "$@"
