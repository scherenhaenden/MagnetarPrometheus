#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${VENV_DIR:-${ROOT_DIR}/venv}"
VENV_ACTIVATE="${VENV_DIR}/bin/activate"

TIER="${1:-all}"

echo "Running tests for MagnetarPrometheus..."
echo "Target test tier: ${TIER}"

if [ ! -f "${VENV_ACTIVATE}" ]; then
    echo "Virtual environment missing. Bootstrapping first..."
    bash "${ROOT_DIR}/scripts/bootstrap_python.sh"
fi

source "${VENV_ACTIVATE}"

run_backend_tests() {
    echo "--- Running Backend & SDK Tests ---"
    # Coverage is enforced in pytest configuration so this script can stay focused
    # on providing a stable, repo-relative execution path.
    (cd "${ROOT_DIR}/backend" && pytest)
    # ensure failure of pytest fails the script immediately
    if [ $? -ne 0 ]; then exit 1; fi
}

run_api_tests() {
    echo "--- Running API Tests ---"
    echo "[Stub] Future API integration tests slot."
    echo "This slot will validate the HTTP service boundary once implemented."
}

run_ui_tests() {
    echo "--- Running UI Tests ---"
    echo "[Stub] Future UI end-to-end tests slot."
    echo "This slot will validate the visual product surface once implemented."
}

case "${TIER}" in
    backend) run_backend_tests ;;
    api) run_api_tests ;;
    ui) run_ui_tests ;;
    all)
        run_backend_tests
        run_api_tests
        run_ui_tests
        ;;
    *)
        echo "Error: Unknown test tier '${TIER}'. Valid options are: backend, api, ui, all."
        exit 1
        ;;
esac
