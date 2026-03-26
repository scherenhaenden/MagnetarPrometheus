#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${VENV_DIR:-${ROOT_DIR}/venv}"
VENV_ACTIVATE="${VENV_DIR}/bin/activate"

echo "Running MagnetarPrometheus backend..."

if [ ! -f "${VENV_ACTIVATE}" ]; then
    echo "Virtual environment missing. Bootstrapping first..."
    bash "${ROOT_DIR}/scripts/bootstrap_python.sh"
fi

source "${VENV_ACTIVATE}"

# The runtime shell wrapper stays intentionally thin.
# The PoC behavior should be reproducible from a clean checkout without
# requiring the caller to manually activate a virtual environment first.
PYTHONPATH="${ROOT_DIR}/sdk/python/src:${ROOT_DIR}/backend/src" python <<PY
from magnetar_prometheus.core.workflow_loader import WorkflowLoader
from magnetar_prometheus.core.executor_router import ExecutorRouter
from magnetar_prometheus.core.context_manager import ContextManager
from magnetar_prometheus.core.engine import Engine
from magnetar_prometheus.registry.step_registry import StepRegistry
from magnetar_prometheus.executors.python_executor import PythonExecutor
from magnetar_prometheus.modules.email_module.steps import register_example_steps
import json

loader = WorkflowLoader()
wf = loader.load_workflow('${ROOT_DIR}/backend/src/magnetar_prometheus/modules/email_module/email_triage.yaml')

registry = StepRegistry()
register_example_steps(registry)

executor = PythonExecutor(registry)
router = ExecutorRouter()
router.register('python', executor)

cm = ContextManager()
engine = Engine(router, cm)

result_context = engine.run(wf)
print(json.dumps(result_context, indent=2))
PY
