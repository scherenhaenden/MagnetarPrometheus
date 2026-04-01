"""
CLI-focused tests for the MagnetarPrometheus proof-of-concept entrypoint.

Why this file exists in this form:

- This file protects the repository's current runnable interface: the lightweight backend
  CLI. The tests are intentionally focused on observable CLI behavior rather than deep
  implementation details of the engine or workflow runtime, which are covered elsewhere.
- The cases are small and direct because this test file needs to verify argument parsing,
  missing-file failure behavior, invalid-workflow failure behavior, custom workflow
  execution, summary-mode output, JSON-mode output, and the `__main__` entrypoint wiring
  without duplicating broader engine tests.
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
  JSON output, clear exit behavior on invalid input, readable summary output, and correct
  startup wiring.
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
    """Test the CLI execution with the default example workflow as JSON."""
    with patch("sys.argv", ["cli.py", "--format", "json"]):
        main()

    captured = capsys.readouterr()
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


def test_cli_invalid_workflow_definition(capsys, tmp_path):
    """Test CLI behavior with an invalid workflow file."""
    workflow_file = tmp_path / "invalid_workflow.yaml"
    workflow_file.write_text("- not-a-mapping\n")

    with patch("sys.argv", ["cli.py", "--workflow", str(workflow_file)]):
        with pytest.raises(SystemExit) as exc_info:
            main()

    captured = capsys.readouterr()

    assert exc_info.value.code == 1
    assert "Error loading workflow from" in captured.err
    assert str(workflow_file) in captured.err


def test_cli_custom_workflow_argument(capsys, tmp_path):
    """Test the CLI with a custom valid workflow file via the --workflow argument."""
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

    with patch("sys.argv", ["cli.py", "--workflow", str(workflow_file), "--format", "json"]):
        main()

    captured = capsys.readouterr()
    output = json.loads(captured.out)

    assert output["run"]["workflow_id"] == "test_workflow"
    assert output["run"]["status"] == "completed"
    assert output["data"]["status"] == "in_review"


def test_cli_format_summary(capsys):
    """Test the CLI defaults to the summary format and prints it correctly."""
    with patch("sys.argv", ["cli.py"]):
        main()

    captured = capsys.readouterr()

    assert "Executing workflow from" in captured.out
    assert "=== Workflow Execution Summary ===" in captured.out
    assert "Workflow ID: email_triage" in captured.out
    assert "Status: completed" in captured.out
    assert "Steps Executed: 4" in captured.out
    assert "Final Data Keys:" in captured.out
    assert "Final AI Keys:" in captured.out


def test_cli_failed_workflow_exits_non_zero(capsys):
    """Test the CLI returns exit code 1 when workflow execution fails."""
    failed_context = {
        "run": {"workflow_id": "email_triage", "status": "failed"},
        "input": {},
        "data": {},
        "ai": {},
        "history": [],
        "errors": [{"message": "boom"}],
    }

    with patch("magnetar_prometheus.cli.Engine.run", return_value=failed_context):
        with patch("sys.argv", ["cli.py", "--format", "json"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

    captured = capsys.readouterr()

    assert exc_info.value.code == 1
    assert json.loads(captured.out)["run"]["status"] == "failed"


def test_cli_summary_tolerates_partial_context(capsys):
    """Test the CLI summary path degrades gracefully on partial engine output."""
    partial_context = {"run": {"status": "failed"}}

    with patch("magnetar_prometheus.cli.Engine.run", return_value=partial_context):
        with patch("sys.argv", ["cli.py"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

    captured = capsys.readouterr()

    assert exc_info.value.code == 1
    assert "Workflow ID: unknown" in captured.out
    assert "Status: failed" in captured.out
    assert "Steps Executed: 0" in captured.out
    assert "Final Data Keys:" in captured.out
    assert "Final AI Keys:" in captured.out


def test_cli_main_execution():
    """Test that executing the CLI module as ``__main__`` still reaches ``main()``.

    This protects the tiny top-level entrypoint wrapper in ``cli.py``. The wrapper is easy
    to break accidentally during refactors because it only exists for direct script/module
    execution, not for the ordinary imported test path. The test therefore executes the file
    as a fresh ``__main__`` module instead of merely calling ``main()`` directly.
    """
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
        # This traces the freshly executed __main__ module rather than the already-imported
        # test module object, which is the only reliable way to prove the entrypoint wrapper
        # still invokes main() after refactors. A simple patch on cli.main would not observe
        # the new module namespace created by runpy.run_path(..., run_name="__main__").
        sys.settrace(tracer)
        with patch("sys.argv", ["cli.py"]):
            runpy.run_path(cli.__file__, run_name="__main__")
    finally:
        sys.settrace(previous_trace)

    assert main_called


@patch("magnetar_prometheus.cli.run_server")
def test_cli_api_flag(mock_run_server):
    """Test that ``--api`` switches the CLI into long-running server mode.

    The normal CLI path is a one-shot workflow execution. This branch adds an alternate mode
    where operators can start the minimal HTTP server instead. The test asserts that the CLI
    does not continue into workflow-loading/execution code when ``--api`` is present, and
    instead delegates immediately to ``run_server`` with the requested port.
    """
    # The API mode is the distinguishing behavior of this branch: the CLI should short-circuit
    # one-shot workflow execution and delegate to the long-running HTTP server entrypoint with
    # the operator-supplied port. This assertion protects that intercept path directly.
    with patch("sys.argv", ["cli.py", "--api", "--port", "9000"]):
        main()

    mock_run_server.assert_called_once_with(port=9000)
