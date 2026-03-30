import pytest
import json
import sys
from unittest.mock import patch
from io import StringIO
from pathlib import Path

from magnetar_prometheus.cli import main

def test_cli_default_workflow(capsys):
    # Patch the system arguments to simulate a command line invocation that explicitely requests json format.
    """Test the CLI execution with the default example workflow."""
    with patch("sys.argv", ["cli.py", "--format", "json"]):
        main()

    captured = capsys.readouterr()

    # Verify that standard output contains a fully serialized JSON string.
    # We assert on key elements inside the run state to guarantee execution logic is functional.
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

    # Establish a minimal temporary workflow file content to test correct engine argument parsing behavior
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

    # Invoke the main CLI function with a specifically mocked path to the generated yaml file
    # and explicit json format for easier testing validation structure.
    with patch("sys.argv", ["cli.py", "--workflow", str(workflow_file), "--format", "json"]):
        main()

    captured = capsys.readouterr()
    output = json.loads(captured.out)

    # Validate that the dynamically supplied custom workflow actually successfully fired.
    assert output["run"]["workflow_id"] == "test_workflow"
    assert output["run"]["status"] == "completed"
    assert output["data"]["status"] == "in_review"

def test_cli_format_summary(capsys):
    # Invoke the CLI without format flags to force the default 'summary' flow.
    """Test the CLI defaults to the summary format and prints it correctly."""
    with patch("sys.argv", ["cli.py"]):
        main()

    captured = capsys.readouterr()

    # Assert that the captured output stream contains the exact expected UX summary blocks.
    assert "=== Workflow Execution Summary ===" in captured.out
    assert "Workflow ID: email_triage" in captured.out
    assert "Status: completed" in captured.out
    assert "Steps Completed: 4" in captured.out
    assert "Final Data Keys:" in captured.out
    assert "Final AI Keys:" in captured.out


def test_cli_main_execution():
    """Test the __main__ block behavior."""
    from magnetar_prometheus import cli
    with patch.object(cli, "main") as mock_main:
        with patch.object(cli, "__name__", "__main__"):
            # Normally __name__ == "__main__" triggers main() at module load,
            # but we can't easily trigger the top-level execution block.
            # Instead, we execute the module script using runpy.
            import runpy
            with patch("sys.argv", ["cli.py"]):
                runpy.run_module("magnetar_prometheus.cli", run_name="__main__")
