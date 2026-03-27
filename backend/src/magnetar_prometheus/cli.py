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

    # Add a format argument to determine how the execution context is rendered to the user.
    # We default to "summary" to avoid overwhelming users with raw JSON on their first interaction.
    parser.add_argument(
        "--format",
        choices=["json", "summary"],
        default="summary",
        help="Output format. 'summary' provides a clean terminal overview, 'json' dumps the full execution context."
    )

    args = parser.parse_args()

    # Validate the existence of the provided workflow YAML prior to attempting execution.
    # Exits the application and reports the invalid path to stderr if the file is absent.
    workflow_path = args.workflow
    if not workflow_path.is_file():
        print(f"Error: Workflow file not found at {workflow_path}", file=sys.stderr)
        sys.exit(1)

    # Initialize the WorkflowLoader and load the target workflow model from the file system.
    loader = WorkflowLoader()
    wf = loader.load_workflow(str(workflow_path))

    # Initialize the step registry and populate it with example step implementation handlers.
    registry = StepRegistry()
    register_example_steps(registry)

    # Create the PythonExecutor backend, linking it to the populated registry.
    # Register the Python execution backend with the router for orchestration dispatch.
    executor = PythonExecutor(registry)
    router = ExecutorRouter()
    router.register('python', executor)

    # Instantiate the state context manager and initialize the core orchestrator engine.
    cm = ContextManager()
    engine = Engine(router, cm)

    # Log the active workflow to the user before dispatching it to the engine
    # to maintain a transparent terminal launch experience, unless raw json mode is forced.
    if args.format == "summary":
        print(f"Executing workflow from {workflow_path}...")

    # Execute the workflow synchronously, yielding the final execution JSON context payload.
    result_context = engine.run(wf)

    # Print a high-level summary overview if the format is explicitly summary.
    # The dictionary lookups safely handle edge cases if the execution context structure is malformed
    # or empty in a catastrophic failure. Provides pointers to retrieve full diagnostic payload.
    if args.format == "summary":
        print("=== Workflow Execution Summary ===")
        print(f"Workflow ID: {result_context.get('run', {}).get('workflow_id', 'unknown')}")
        print(f"Status: {result_context.get('run', {}).get('status', 'unknown')}")
        print(f"Steps Completed: {len(result_context.get('history', []))}")
        print(f"Final Data Keys: {list(result_context.get('data', {}).keys())}")
        print(f"Final AI Keys: {list(result_context.get('ai', {}).keys())}")
        print("To see the full technical output, run with --format json")
    else:
        # If the user requested raw JSON output (e.g., for piping or analysis tools),
        # print the fully serialized output state exactly as returned from the engine.
        print(json.dumps(result_context, indent=2))


if __name__ == "__main__":
    main()
