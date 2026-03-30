import pytest
import json
import sys
from unittest.mock import patch
from io import StringIO
from pathlib import Path

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
    with patch.object(cli, "main") as mock_main:
        with patch.object(cli, "__name__", "__main__"):
            # Normally __name__ == "__main__" triggers main() at module load,
            # but we can't easily trigger the top-level execution block.
            # Instead, we execute the module script using runpy.
            import runpy
            with patch("sys.argv", ["cli.py"]):
                runpy.run_module("magnetar_prometheus.cli", run_name="__main__")
