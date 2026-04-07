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
#   all     - (Default) Runs all implemented test tiers and reports placeholder tiers as skipped.
#   backend - Runs the internal Python engine, SDK tests, and enforces 100% coverage.
#   api     - Validates the HTTP boundary (Not implemented yet; exits non-zero).
#   ui      - Validates Angular build, test, and documentation guard checks.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${VENV_DIR:-${ROOT_DIR}/venv}"
VENV_ACTIVATE="${VENV_DIR}/bin/activate"

# Determine the target testing tier. If no argument is provided, default to "all".
TIER="${1:-all}"

echo "Running tests for MagnetarPrometheus..."
echo "Target test tier: ${TIER}"

ensure_python_environment() {
    if [ ! -f "${VENV_ACTIVATE}" ]; then
        echo "Virtual environment missing. Bootstrapping first..."
        bash "${ROOT_DIR}/scripts/bootstrap_python.sh"
    fi

    # shellcheck disable=SC1090
    source "${VENV_ACTIVATE}"
}

report_unimplemented_tier() {
    local tier_name="$1"

    echo "Error: tier '${tier_name}' is not implemented yet." >&2
    return 2
}

# -----------------------------------------------------------------------------
# Tier 1: Backend & SDK Tests
# This tier focuses on engine internals, model validation, routing, and shared schemas.
# It enforces a strict 100% code coverage threshold.
# -----------------------------------------------------------------------------
run_backend_tests() {
    echo "--- Running Backend & SDK Tests ---"
    ensure_python_environment
    (cd "${ROOT_DIR}/backend" && pytest)
}

# -----------------------------------------------------------------------------
# Tier 2: API Tests
# This tier will focus on the HTTP service boundary, ensuring that API endpoints
# properly expose engine functionality and respect authorization/routing rules.
# -----------------------------------------------------------------------------
run_api_tests() {
    echo "--- Running API Tests ---"
    echo "This tier is reserved for future HTTP service-boundary validation."
    report_unimplemented_tier "api"
}

# -----------------------------------------------------------------------------
# Tier 3: UI Tests
# This tier will run end-to-end browser automation tests (e.g. Playwright/Cypress)
# to ensure the visual workflow editor and drag-and-drop operations behave correctly.
# -----------------------------------------------------------------------------
run_ui_tests() {
    echo "--- Running UI Tests ---"
    python3 "${ROOT_DIR}/scripts/check_ui_code_contracts.py"
    (cd "${ROOT_DIR}/ui" && npm run build && npm run test:ci)
    bash "${ROOT_DIR}/scripts/check_ui_docs.sh"
}

# -----------------------------------------------------------------------------
# Execution Routing
# -----------------------------------------------------------------------------
case "${TIER}" in
    backend) run_backend_tests ;;
    api) run_api_tests ;;
    ui) run_ui_tests ;;
    all)
        # Run every currently implemented tier. Placeholder tiers are reported explicitly as
        # skipped here so the default validation path for the current backend proof-of-concept
        # remains usable without incorrectly implying that API/UI tests executed successfully.
        run_backend_tests
        run_ui_tests
        echo "--- Skipped Placeholder Tiers ---"
        echo "api: not implemented yet"
        ;;
    *)
        echo "Error: Unknown test tier '${TIER}'. Valid options are: backend, api, ui, all."
        exit 1
        ;;
esac
