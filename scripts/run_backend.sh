#!/usr/bin/env bash
set -euo pipefail

echo "Running MagnetarPrometheus backend..."

source venv/bin/activate

python -c "
import sys
from magnetar_prometheus.core.workflow_loader import WorkflowLoader
from magnetar_prometheus.core.executor_router import ExecutorRouter
from magnetar_prometheus.core.context_manager import ContextManager
from magnetar_prometheus.core.engine import Engine
from magnetar_prometheus.registry.step_registry import StepRegistry
from magnetar_prometheus.executors.python_executor import PythonExecutor
from magnetar_prometheus.example_module import register_example_steps
import json

loader = WorkflowLoader()
wf = loader.load_workflow('backend/src/magnetar_prometheus/example_workflow.yaml')

registry = StepRegistry()
register_example_steps(registry)

executor = PythonExecutor(registry)
router = ExecutorRouter()
router.register('python', executor)

cm = ContextManager()
engine = Engine(router, cm)

result_context = engine.run(wf)
print(json.dumps(result_context, indent=2))
"

