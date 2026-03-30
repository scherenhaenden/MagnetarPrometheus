#!/usr/bin/env bash
# MagnetarPrometheus Launcher
# This script orchestrates the local bootstrapping and execution
# of the workflow engine. It presents a clean, user-friendly
# terminal experience without dumping verbose installation logs.

set -euo pipefail

# Determine the absolute path to the repository root directory
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define paths to necessary backend scripts
BOOTSTRAP_SCRIPT="${ROOT_DIR}/scripts/bootstrap_python.sh"
RUN_SCRIPT="${ROOT_DIR}/scripts/run_backend.sh"

# Display a clear, distinct visual boundary indicating the application is starting
echo "=== MagnetarPrometheus Launcher ==="
echo "--- Bootstrapping Environment ---"

# Verify that the bootstrap script is executable
if [ ! -x "${BOOTSTRAP_SCRIPT}" ]; then
    echo "Bootstrap script not found at ${BOOTSTRAP_SCRIPT}."
    exit 1
fi

# Verify that the backend run script is executable
if [ ! -x "${RUN_SCRIPT}" ]; then
    echo "Backend run script not found at ${RUN_SCRIPT}."
    exit 1
fi

# Inform the user that the bootstrap process is running, as it may take
# several seconds if a virtual environment needs to be constructed.
echo "Bootstrapping (this may take a minute)..."

# Execute the bootstrap script and suppress standard output to keep
# the terminal clean. Standard error is intentionally preserved
# so critical pip or installation failures remain visible to the user.
bash "${BOOTSTRAP_SCRIPT}" > /dev/null
echo

# Announce the transition from the bootstrap phase to the execution phase.
echo "--- Executing Workflow Engine ---"

# Launch the backend engine script, passing along any arguments (e.g., --workflow path)
# provided by the user on the command line.
bash "${RUN_SCRIPT}" "$@"
