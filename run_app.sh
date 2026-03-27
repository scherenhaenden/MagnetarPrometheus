#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOTSTRAP_SCRIPT="${ROOT_DIR}/scripts/bootstrap_python.sh"
RUN_SCRIPT="${ROOT_DIR}/scripts/run_backend.sh"

echo "Starting MagnetarPrometheus..."

if [ ! -x "${BOOTSTRAP_SCRIPT}" ]; then
    echo "Bootstrap script not found at ${BOOTSTRAP_SCRIPT}."
    exit 1
fi

if [ ! -x "${RUN_SCRIPT}" ]; then
    echo "Backend run script not found at ${RUN_SCRIPT}."
    exit 1
fi

bash "${BOOTSTRAP_SCRIPT}"
echo
echo "Launching example workflow..."
bash "${RUN_SCRIPT}" "$@"
