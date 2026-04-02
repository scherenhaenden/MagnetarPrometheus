#!/usr/bin/env bash
#
# run_tests.sh
#
# Main entrypoint for validating MagnetarPrometheus.
# This script orchestrates the different testing "tiers" required to validate the entire
# product suite. As the product expands from a backend engine into an API and UI,
# this script ensures that CI and local environments have a unified interface for testing.
#
# Usage: bash scripts/run_tests.sh [tier]
# Options for tier:
#   all     - (Default) Runs all registered test tiers sequentially.
#   backend - Runs the internal Python engine, SDK tests, and enforces 100% coverage.
#   api     - Validates the HTTP boundary (Stubbed for future use).
#   ui      - Validates the visual application (Stubbed for future use).

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${VENV_DIR:-${ROOT_DIR}/venv}"
VENV_ACTIVATE="${VENV_DIR}/bin/activate"

# Determine the target testing tier. If no argument is provided, default to "all".
TIER="${1:-all}"

echo "Running tests for MagnetarPrometheus..."
echo "Target test tier: ${TIER}"

# Ensure the Python environment is bootstrapped and ready before invoking any Python-based validation
if [ ! -f "${VENV_ACTIVATE}" ]; then
    echo "Virtual environment missing. Bootstrapping first..."
    bash "${ROOT_DIR}/scripts/bootstrap_python.sh"
fi

source "${VENV_ACTIVATE}"

# -----------------------------------------------------------------------------
# Tier 1: Backend & SDK Tests
# This tier focuses on engine internals, model validation, routing, and shared schemas.
# It enforces a strict 100% code coverage threshold.
# -----------------------------------------------------------------------------
run_backend_tests() {
    echo "--- Running Backend & SDK Tests ---"
    # Execute pytest from within the backend directory inside a subshell.
    # The subshell `(...)` ensures we do not permanently change the working directory
    # for the subsequent test functions that might rely on being at the repo root.
    # Code coverage enforcement rules are centralized in backend/pyproject.toml
    (cd "${ROOT_DIR}/backend" && pytest)

    # If the subshell commands fail (e.g. coverage < 100%), explicitly exit with an error.
    if [ $? -ne 0 ]; then exit 1; fi
}

# -----------------------------------------------------------------------------
# Tier 2: API Tests
# This tier will focus on the HTTP service boundary, ensuring that API endpoints
# properly expose engine functionality and respect authorization/routing rules.
# -----------------------------------------------------------------------------
run_api_tests() {
    echo "--- Running API Tests ---"
    echo "[Stub] Future API integration tests slot."
    echo "This slot will validate the HTTP service boundary once implemented."
    # Future implementation e.g.: (cd "${ROOT_DIR}/api" && run_api_tests.sh)
}

# -----------------------------------------------------------------------------
# Tier 3: UI Tests
# This tier will run end-to-end browser automation tests (e.g. Playwright/Cypress)
# to ensure the visual workflow editor and drag-and-drop operations behave correctly.
# -----------------------------------------------------------------------------
run_ui_tests() {
    echo "--- Running UI Tests ---"
    echo "[Stub] Future UI end-to-end tests slot."
    echo "This slot will validate the visual product surface once implemented."
    # Future implementation e.g.: (cd "${ROOT_DIR}/ui" && npm run test:e2e)
}

# -----------------------------------------------------------------------------
# Execution Routing
# -----------------------------------------------------------------------------
case "${TIER}" in
    backend) run_backend_tests ;;
    api) run_api_tests ;;
    ui) run_ui_tests ;;
    all)
        # Run all tiers sequentially. If `run_backend_tests` fails, the `set -e`
        # and explicit `exit 1` ensures that the script halts immediately.
        run_backend_tests
        run_api_tests
        run_ui_tests
        ;;
    *)
        echo "Error: Unknown test tier '${TIER}'. Valid options are: backend, api, ui, all."
        exit 1
        ;;
esac
