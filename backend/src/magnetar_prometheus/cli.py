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
        "--format",
        choices=["json", "summary"],
        default="summary",
        help="Output format."
    )

    args = parser.parse_args()

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

    if args.format == "summary":
        print(f"Executing workflow from {workflow_path}...")

    result_context = engine.run(wf)

    if args.format == "summary":
        print("=== Workflow Execution Summary ===")
        print(f"Workflow ID: {result_context.get('run', {}).get('workflow_id', 'unknown')}")
        print(f"Status: {result_context.get('run', {}).get('status', 'unknown')}")
        print(f"Steps Completed: {len(result_context.get('history', []))}")
        print(f"Final Data Keys: {list(result_context.get('data', {}).keys())}")
        print(f"Final AI Keys: {list(result_context.get('ai', {}).keys())}")
        print("To see the full technical output, run with --format json")
    else:
        print(json.dumps(result_context, indent=2))


if __name__ == "__main__":
    main()
