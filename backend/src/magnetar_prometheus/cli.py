"""
MagnetarPrometheus CLI entrypoint.

Why this file is structured this way:

- This CLI is the current user-facing entrypoint for the backend proof of concept.
  The repository does not yet expose a persistent API server, dashboard, or UI, so
  this file intentionally provides the shortest path from shell command to a real,
  observable workflow run.
- The code performs orchestration wiring directly in one place on purpose:
  loader, registry, executor, router, context manager, and engine are assembled
  inline so a contributor can understand the runnable product slice without
  chasing multiple bootstrap layers. For the current PoC, explicit wiring is
  easier to audit than a more abstract dependency-injection structure.
- The default output mode is "summary" rather than raw JSON because the project
  docs explicitly describe the need for user-incremental delivery and visible
  operator-facing progress. A terminal summary is easier for a human to scan,
  while `--format json` remains available for diagnostics, piping, and tests.
- Workflow-path validation happens before loading so file-not-found failures are
  reported clearly to the user instead of surfacing as lower-level exceptions.
- Workflow loading is wrapped in a user-facing error path because malformed YAML
  or invalid workflow structures are expected operator errors in a CLI product
  surface. This file converts those failures into a concise stderr message and
  exit code `1` rather than exposing an unhandled traceback as the default UX.
- The summary block extracts nested dictionaries from `result_context` into local
  variables to keep the reporting code readable and to make future changes to the
  displayed fields more obvious during review.

If this file later starts to look "too manual", that is probably the point where
MagnetarPrometheus has gained a more formal application bootstrap layer or a
persistent service boundary. Until then, this module is intentionally direct.
"""

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
    """Run the MagnetarPrometheus Backend CLI workflow.
    
    This function sets up the command-line interface for the MagnetarPrometheus
    backend, allowing users to specify a workflow YAML file and output format. It
    validates the existence of the specified workflow file, loads it using the
    WorkflowLoader, and initializes the execution environment with a step registry
    and an executor. The workflow is then executed, and the results are displayed
    in the requested format, either as a summary or raw JSON.
    """
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
    try:
        wf = loader.load_workflow(str(workflow_path))
    except (TypeError, ValueError) as exc:
        print(
            f"Error loading workflow from {workflow_path}: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)

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
        run_info = result_context.get("run", {})
        history = result_context.get("history", [])
        data = result_context.get("data", {})
        ai = result_context.get("ai", {})
        print(f"Workflow ID: {run_info.get('workflow_id', 'unknown')}")
        print(f"Status: {run_info.get('status', 'unknown')}")
        print(f"Steps Completed: {len(history)}")
        print(f"Final Data Keys: {list(data.keys())}")
        print(f"Final AI Keys: {list(ai.keys())}")
        print("To see the full technical output, run with --format json")
    else:
        # If the user requested raw JSON output (e.g., for piping or analysis tools),
        # print the fully serialized output state exactly as returned from the engine.
        print(json.dumps(result_context, indent=2))


if __name__ == "__main__":
    main()
