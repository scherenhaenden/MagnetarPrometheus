#!/usr/bin/env bash
set -euo pipefail

echo "Running tests for MagnetarPrometheus..."

source venv/bin/activate

# We enforce 100% coverage on the combined sdk and backend packages.
# --cov-fail-under=100 ensures the process exits with an error if it misses the target.
PYTHONPATH=sdk/python/src:backend/src pytest --cov=magnetar_prometheus_sdk --cov=magnetar_prometheus --cov-report=term-missing --cov-fail-under=100 sdk/python/tests/ backend/tests/
