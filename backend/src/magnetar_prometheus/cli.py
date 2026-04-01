"""
MagnetarPrometheus CLI entrypoint.

Why this file exists in this form:

- This module is the shortest executable path from repository checkout to a real workflow
  run. The project still centers on a backend proof of concept, so this file is intentionally
  direct and avoids introducing a heavier application bootstrap layer before the product has
  earned one.
- The wiring is kept explicit in one place on purpose. Loader, registry, executor router,
  context manager, and engine are assembled inline so a contributor can read one file and
  understand the runnable slice without chasing multiple abstractions.
- The default workflow path points at the example email workflow because the repository
  needs one deterministic, low-friction demonstration path that works from a clean checkout.
  That example is part of the current product slice, not merely test scaffolding.
- Error handling for the workflow path is user-facing and intentionally minimal. The CLI
  should fail fast with a clear message when the provided file path is invalid instead of
  surfacing a confusing lower-level traceback for a basic operator mistake.
- The actual `if __name__ == "__main__"` wrapper is tiny by design. All meaningful behavior
  lives in `main()`, while the wrapper exists only to support direct module execution. That
  is why the wrapper line is excluded from coverage and the real entrypoint behavior is
  asserted in tests instead.
- If this file later starts accumulating environment setup, richer output modes, service
  bootstrapping, or dependency injection concerns, that is likely the point where the CLI
  should be split into a more formal application layer rather than extended indefinitely.
"""

import argparse
import json
import sys

import yaml
from pydantic import ValidationError
from pathlib import Path

from magnetar_prometheus.core.workflow_loader import WorkflowLoader
from magnetar_prometheus.core.executor_router import ExecutorRouter
from magnetar_prometheus.core.context_manager import ContextManager
from magnetar_prometheus.core.engine import Engine
from magnetar_prometheus.registry.step_registry import StepRegistry
from magnetar_prometheus.executors.python_executor import PythonExecutor
from magnetar_prometheus.modules.email_module.steps import register_example_steps


def _print_summary(workflow_path: Path, result_context: dict) -> None:
    """Render a human-scannable execution summary."""
    print(f"Executing workflow from {workflow_path}")
    print("=== Workflow Execution Summary ===")
    print(f"Workflow ID: {result_context['run']['workflow_id']}")
    print(f"Status: {result_context['run']['status']}")
    print(f"Steps Executed: {len(result_context['history'])}")
    print(f"Final Data Keys: {', '.join(sorted(result_context['data'].keys()))}")
    print(f"Final AI Keys: {', '.join(sorted(result_context['ai'].keys()))}")


def main():
    """Run the MagnetarPrometheus workflow engine from the command line.

    Parses ``--workflow`` and ``--format``, assembles the current proof-of-
    concept runtime components inline, executes the workflow, and renders either
    a human-scannable terminal summary or the full JSON execution context.

    ``--format`` supports ``summary`` and ``json``. Summary mode is the default
    operator-facing output and reports the workflow path, workflow id, final
    status, completed-step count, and the top-level data and AI keys. JSON mode
    prints the full execution context returned by the engine.

    The command exits with status ``1`` when the workflow file does not exist or
    when the workflow definition cannot be loaded into a valid runtime model.
    Argument-parsing failures continue to use argparse's default exit behavior.
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
    parser.add_argument(
        "--format",
        choices=("summary", "json"),
        default="summary",
        help="Output format for execution results."
    )

    args = parser.parse_args()

    workflow_path = args.workflow
    if not workflow_path.is_file():
        print(f"Error: Workflow file not found at {workflow_path}", file=sys.stderr)
        sys.exit(1)

    loader = WorkflowLoader()
    try:
        wf = loader.load_workflow(str(workflow_path))
    except (OSError, UnicodeDecodeError, yaml.YAMLError, ValidationError) as exc:
        print(f"Error loading workflow from {workflow_path}: {exc}", file=sys.stderr)
        sys.exit(1)

    registry = StepRegistry()
    register_example_steps(registry)

    executor = PythonExecutor(registry)
    router = ExecutorRouter()
    router.register('python', executor)

    cm = ContextManager()
    engine = Engine(router, cm)

    result_context = engine.run(wf)
    if args.format == "json":
        print(json.dumps(result_context, indent=2))
    else:
        _print_summary(workflow_path, result_context)

    if result_context.get("run", {}).get("status") == "failed":
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover - entrypoint wrapper is asserted indirectly in tests
    main()
