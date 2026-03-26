#!/usr/bin/env bash
set -euo pipefail

echo "Bootstrapping MagnetarPrometheus Python runtime..."

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing SDK..."
pip install -e sdk/python

echo "Installing Backend..."
pip install -e backend

echo "Installing testing dependencies..."
pip install pytest pytest-cov

echo "Running startup check (which may trigger automatic dependency installation if missing)..."
python -c "from magnetar_prometheus.bootstrap import bootstrap_runtime; bootstrap_runtime(auto_install=True)"

echo "Bootstrap complete."

