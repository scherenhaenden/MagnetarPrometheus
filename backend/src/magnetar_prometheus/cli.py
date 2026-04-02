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
- Error handling for both workflow loading and API startup is intentionally normalized to
  concise operator-facing stderr messages. A caller should not need to parse Python
  tracebacks just to understand that a file is invalid or that a requested port is already in
  use.
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
from pathlib import Path

import yaml
from pydantic import ValidationError

from magnetar_prometheus.api.server import DEFAULT_API_HOST, run_server
from magnetar_prometheus.core.context_manager import ContextManager
from magnetar_prometheus.core.engine import Engine
from magnetar_prometheus.core.executor_router import ExecutorRouter
from magnetar_prometheus.core.workflow_loader import WorkflowLoader
from magnetar_prometheus.executors.python_executor import PythonExecutor
from magnetar_prometheus.modules.example_registry import register_all_example_steps
from magnetar_prometheus.registry.step_registry import StepRegistry


def _print_summary(workflow_path: Path, result_context: dict) -> None:
    """Render a human-scannable execution summary.

    The summary mode is intentionally conservative: it should still print something useful even
    if the engine returns a partial context during a failure path. That behavior matters because
    operators frequently run the CLI directly from a terminal, and a second crash inside the
    renderer would hide the original workflow failure behind a formatting bug.
    """
    # This summary path is intentionally defensive because it is the last layer between a
    # broken workflow and the operator reading the terminal. If a future refactor assumes the
    # engine always returns a perfectly complete context, the CLI can end up masking the real
    # workflow failure behind a second formatting failure.
    #
    # Keep the fallback `.get(... ) or {}` / `.get(... ) or []` pattern unless the engine
    # contract changes and the tests are updated to prove summary mode still tolerates partial
    # failure output. The slightly repetitive style here is serving a resilience goal.
    run_info = result_context.get("run") or {}
    history = result_context.get("history") or []
    data = result_context.get("data") or {}
    ai = result_context.get("ai") or {}

    workflow_id = run_info.get("workflow_id", "unknown")
    status = run_info.get("status", "unknown")
    data_keys = data.keys() if isinstance(data, dict) else []
    ai_keys = ai.keys() if isinstance(ai, dict) else []

    print(f"Executing workflow from {workflow_path}")
    print("=== Workflow Execution Summary ===")
    print(f"Workflow ID: {workflow_id}")
    print(f"Status: {status}")
    print(f"Steps Executed: {len(history)}")
    print(f"Final Data Keys: {', '.join(sorted(data_keys))}")
    print(f"Final AI Keys: {', '.join(sorted(ai_keys))}")


def main():
    """Run the MagnetarPrometheus workflow engine from the command line.

    This entrypoint supports two operator-facing modes.

    1. One-shot workflow execution, where the CLI loads a workflow file, assembles the current
       proof-of-concept runtime in process, executes the workflow, and prints either a compact
       terminal summary or the full JSON context.
    2. Minimal local API mode, where `--api` starts the lightweight HTTP server instead of
       running a single workflow invocation.

    `--format` supports `summary` and `json`. Summary mode is the default human-facing output.
    The command exits with status `1` when the workflow file is missing, when the workflow
    definition cannot be loaded into a valid runtime model, when API startup fails, or when the
    workflow executes to a terminal `failed` status.
    """
    parser = argparse.ArgumentParser(description="MagnetarPrometheus Backend CLI")

    # Keep the example workflow as the default target so a clean checkout has one obvious,
    # deterministic execution path without requiring the operator to discover file locations.
    default_workflow_path = (
        Path(__file__).parent / "modules" / "email_module" / "email_triage.yaml"
    )

    parser.add_argument(
        "--workflow",
        type=Path,
        default=default_workflow_path,
        help="Path to the workflow YAML file.",
    )
    parser.add_argument(
        "--format",
        choices=("summary", "json"),
        default="summary",
        help="Output format for execution results.",
    )
    parser.add_argument(
        "--api",
        action="store_true",
        help="Start the local API server instead of running a one-shot workflow.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the API server on (defaults to 8000).",
    )

    # Reuse the server-level constant instead of copying the loopback literal here.
    #
    # This is intentionally verbose because default values are one of the easiest places for
    # multi-agent drift to creep in. If the CLI and the server each carry their own literal,
    # one future edit can make help text, runtime behavior, and tests disagree without anyone
    # noticing immediately. Importing the constant makes the alignment explicit in code.
    parser.add_argument(
        "--host",
        type=str,
        default=DEFAULT_API_HOST,
        help=(
            "Network interface to bind the API server to "
            "(defaults to 127.0.0.1 for local-only access). "
            "Pass 0.0.0.0 to bind on all interfaces."
        ),
    )

    args = parser.parse_args()

    # The `--api` path is a deliberate short-circuit and should remain obviously so.
    #
    # Why this block is intentionally spelled out:
    # - API mode is a different command mode, not just "workflow run plus one more flag"
    # - startup failures should be normalized as CLI-facing stderr output rather than leaked as
    #   raw lower-level tracebacks
    # - the parsed host should be forwarded explicitly so the call site documents the actual
    #   binding choice the operator made
    # - the `return` must remain because dropping it would allow API mode to leak into the
    #   normal one-shot workflow path after server startup logic
    if args.api:
        try:
            run_server(port=args.port, host=args.host)
        except (OSError, OverflowError) as exc:
            print(f"Error starting API server on port {args.port}: {exc}", file=sys.stderr)
            sys.exit(1)
        return

    workflow_path = args.workflow
    if not workflow_path.is_file():
        print(f"Error: Workflow file not found at {workflow_path}", file=sys.stderr)
        sys.exit(1)

    loader = WorkflowLoader()
    try:
        wf = loader.load_workflow(str(workflow_path))
    except (
        OSError,
        UnicodeDecodeError,
        yaml.YAMLError,
        ValidationError,
        ValueError,
    ) as exc:
        print(f"Error loading workflow from {workflow_path}: {exc}", file=sys.stderr)
        sys.exit(1)

    registry = StepRegistry()
    register_all_example_steps(registry)

    executor = PythonExecutor(registry)
    router = ExecutorRouter()
    router.register("python", executor)

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
