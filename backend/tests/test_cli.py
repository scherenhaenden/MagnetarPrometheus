"""
CLI-focused tests for the MagnetarPrometheus proof-of-concept entrypoint.

Why this file exists in this form:

- This file protects the repository's current runnable interface: the lightweight backend
  CLI. The tests are intentionally focused on observable CLI behavior rather than deep
  implementation details of the engine or workflow runtime, which are covered elsewhere.
- The cases are small and direct because this test file needs to verify argument parsing,
  missing-file failure behavior, invalid-workflow failure behavior, custom workflow
  execution, summary-mode output, JSON-mode output, API-mode short-circuiting, and the
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
  JSON output, clear exit behavior on invalid input, readable summary output, correct API
  startup delegation, and correct startup wiring.
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
    """Test that executing the CLI module as `__main__` still reaches `main()`."""
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
        # Trace the freshly executed `__main__` module rather than the already-imported test
        # module object. That is the only reliable way to prove the tiny entrypoint wrapper
        # still invokes `main()` after refactors.
        sys.settrace(tracer)
        with patch("sys.argv", ["cli.py"]):
            runpy.run_path(cli.__file__, run_name="__main__")
    finally:
        sys.settrace(previous_trace)

    assert main_called


def test_cli_api_startup_failure(capsys):
    """Test that API startup failures are normalized to stderr plus exit code 1.

    The CLI deliberately treats server bind/startup problems like other operator-facing CLI
    errors: the user should receive a concise stderr message and a non-zero exit code rather
    than a raw traceback from the lower-level HTTP server implementation.
    """
    with patch("magnetar_prometheus.cli.run_server", side_effect=OSError("port busy")):
        with patch("sys.argv", ["cli.py", "--api", "--port", "9000"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

    captured = capsys.readouterr()

    assert exc_info.value.code == 1
    assert "Error starting API server on port 9000" in captured.err
    assert "port busy" in captured.err


@patch("magnetar_prometheus.cli.WorkflowLoader.load_workflow")
@patch("magnetar_prometheus.cli.run_server")
def test_cli_api_flag(mock_run_server, mock_load_workflow):
    """Test that `--api` switches the CLI into long-running server mode.

    This test deliberately protects multiple policy boundaries at once:

    - the CLI must delegate to `run_server` when `--api` is present
    - the safe loopback default must be forwarded explicitly at the call boundary
    - the normal workflow-loading path must not run at all in API mode

    The docstring stays long on purpose because this is exactly the kind of test that looks
    "too wordy" to a cleanup pass and then quietly loses the context for why the extra
    assertions are there. The branch is protecting a mode boundary, not just a mock call.
    """
    with patch("sys.argv", ["cli.py", "--api", "--port", "9000"]):
        main()

    mock_run_server.assert_called_once_with(port=9000, host="127.0.0.1")
    mock_load_workflow.assert_not_called()


@patch("magnetar_prometheus.cli.run_server")
def test_cli_api_flag_custom_host(mock_run_server):
    """Test that ``--host`` is forwarded to ``run_server`` when provided explicitly.

    The default loopback path is already covered by ``test_cli_api_flag``. This companion case
    protects the opposite boundary: users are allowed to opt into a broader bind, but only
    when they request it explicitly.

    This should remain documented in detail because it is easy for a future simplification to
    preserve the default-host path while accidentally dropping the explicit-host forwarding
    behavior and thereby collapsing operator intent back to the default.
    """
    with patch("sys.argv", ["cli.py", "--api", "--port", "9000", "--host", "0.0.0.0"]):
        main()

    mock_run_server.assert_called_once_with(port=9000, host="0.0.0.0")
