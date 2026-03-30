"""
CLI-focused tests for the MagnetarPrometheus proof-of-concept entrypoint.

Why this file exists in this form:

- This file protects the repository's current runnable interface: the lightweight backend
  CLI. The tests are intentionally focused on observable CLI behavior rather than deep
  implementation details of the engine or workflow runtime, which are covered elsewhere.
- The cases are small and direct because this test file needs to verify argument parsing,
  missing-file failure behavior, default execution, custom workflow execution, and the
  `__main__` entrypoint wiring without duplicating broader engine tests.
- The `__main__` execution test is intentionally stricter than a simple "module executes"
  smoke test. Its job is to verify that the entrypoint wiring really calls `main()`, since
  that line is easy to break during refactors while still leaving most runtime behavior
  intact.
- The `__main__` test uses execution tracing together with `runpy.run_path(...)` because
  direct patching of an already imported module does not observe the fresh `__main__`
  module context created by script execution in this repository. This keeps the assertion
  honest while still using the standard library's path-execution helper instead of manual
  source compilation.
- This file should stay biased toward behavior that a CLI user would notice: successful
  JSON output, clear exit behavior on invalid input, and correct startup wiring.
- If the CLI later grows substantially more modes, output formats, or service-launch
  behaviors, this file should probably be split into focused test modules rather than
  continuing to accumulate unrelated entrypoint concerns.
"""

import json
import runpy
import sys
from unittest.mock import patch

import pytest

from magnetar_prometheus.cli import main

def test_cli_default_workflow(capsys):
    """Test that the CLI runs successfully with the default example workflow."""
    with patch("sys.argv", ["cli.py"]):
        main()

    captured = capsys.readouterr()

    # Check that standard output contains JSON output and successful execution status
    output = json.loads(captured.out)
    assert output["run"]["workflow_id"] == "email_triage"
    assert output["run"]["status"] == "completed"
    assert output["data"]["ticket_id"] == "TKT-1234"
    assert output["ai"]["decision"] == "create_ticket"

def test_cli_missing_workflow():
    """Test that the CLI exits gracefully if a provided workflow file doesn't exist."""
    with patch("sys.argv", ["cli.py", "--workflow", "nonexistent_workflow.yaml"]):
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

def test_cli_custom_workflow_argument(capsys, tmp_path):
    """Test providing a custom valid workflow file via the --workflow argument."""

    # Create a temporary minimal workflow to test argument parsing properly
    workflow_content = """
id: test_workflow
name: Test Workflow
version: 1.0.0
start_step: manual_review

steps:
  manual_review:
    type: review.queue
    executor: python
    next: end
    """

    workflow_file = tmp_path / "test_workflow.yaml"
    workflow_file.write_text(workflow_content)

    with patch("sys.argv", ["cli.py", "--workflow", str(workflow_file)]):
        main()

    captured = capsys.readouterr()
    output = json.loads(captured.out)

    assert output["run"]["workflow_id"] == "test_workflow"
    assert output["run"]["status"] == "completed"
    assert output["data"]["status"] == "in_review"

def test_cli_main_execution():
    """Test the __main__ block behavior."""
    from magnetar_prometheus import cli
    main_called = False

    def tracer(frame, event, arg):
        nonlocal main_called
        if (
            event == "call"
            and frame.f_code.co_name == "main"
            and frame.f_globals.get("__name__") == "__main__"
        ):
            main_called = True
        return tracer

    previous_trace = sys.gettrace()
    try:
        sys.settrace(tracer)
        with patch("sys.argv", ["cli.py"]):
            runpy.run_path(cli.__file__, run_name="__main__")
    finally:
        sys.settrace(previous_trace)

    assert main_called
