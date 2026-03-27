import argparse
import json
import sys
from pathlib import Path

from magnetar_prometheus.core.workflow_loader import WorkflowLoader
from magnetar_prometheus.core.executor_router import ExecutorRouter
from magnetar_prometheus.core.context_manager import ContextManager
from magnetar_prometheus.core.engine import Engine
from magnetar_prometheus.registry.step_registry import StepRegistry
from magnetar_prometheus.executors.python_executor import PythonExecutor
from magnetar_prometheus.modules.email_module.steps import register_example_steps
from magnetar_prometheus.api.server import run_server


def main():
    parser = argparse.ArgumentParser(description="MagnetarPrometheus Backend CLI")

    # default path to the example workflow relative to the file location
    default_workflow_path = (
        Path(__file__).parent / "modules" / "email_module" / "email_triage.yaml"
    )

    parser.add_argument(
        "--workflow",
        type=Path,
        default=default_workflow_path,
        help="Path to the workflow YAML file."
    )

    parser.add_argument(
        "--api",
        action="store_true",
        help="Start the local API server instead of running a one-shot workflow."
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the API server on (defaults to 8000)."
    )

    args = parser.parse_args()

    if args.api:
        run_server(port=args.port)
        return

    workflow_path = args.workflow
    if not workflow_path.is_file():
        print(f"Error: Workflow file not found at {workflow_path}", file=sys.stderr)
        sys.exit(1)

    loader = WorkflowLoader()
    wf = loader.load_workflow(str(workflow_path))

    registry = StepRegistry()
    register_example_steps(registry)

    executor = PythonExecutor(registry)
    router = ExecutorRouter()
    router.register('python', executor)

    cm = ContextManager()
    engine = Engine(router, cm)

    result_context = engine.run(wf)
    print(json.dumps(result_context, indent=2))


if __name__ == "__main__":
    main()
