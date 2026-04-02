"""Tests for the focused failure-path example workflow handlers.

Why this file exists in this form:

- The error example module exists to make failure semantics explicit, so its tests must verify
  the exact failure result shape rather than only checking that something went wrong.
- This file also protects the branch's logging addition so the example failure path leaves a
  traceable signal without relying on broader engine logging behavior.
- Registration checks remain here because the example modules are intentionally small and the
  repository benefits from keeping each module's local contract tests close to its behavior.
"""

import pytest
from magnetar_prometheus.modules.error_module.steps import (
    start_error, trigger_error, register_error_steps
)
from magnetar_prometheus.registry.step_registry import StepRegistry

def test_start_error():
    """
    Tests the initial step of the error workflow.

    Verifies that the initial step executes successfully, simulating
    a normal start to a workflow prior to an error condition.
    """
    res = start_error({}, {})
    assert res.success is True
    assert res.output["data"]["status"] == "started"

def test_trigger_error():
    """
    Tests the step designed to trigger an error.

    Verifies that the step intentionally fails by checking the returned
    StepResult success flag and ensuring the proper simulated error
    message is provided.
    """
    res = trigger_error({}, {})
    assert res.success is False
    assert res.error_message == "Simulated error occurred"
    assert res.output == {}

def test_trigger_error_logs_failure(caplog):
    """
    Tests that the simulated failure path emits an error log for traceability.
    """
    with caplog.at_level("ERROR"):
        trigger_error({}, {})

    assert "Error triggered in example workflow" in caplog.text

def test_register_error_steps():
    """
    Tests the registration of the error workflow steps.

    Ensures that the string identifiers ('error.start', 'error.trigger')
    are correctly mapped to their respective Python function handlers
    within the workflow engine's registry.
    """
    registry = StepRegistry()
    register_error_steps(registry)
    assert registry.get_handler("error.start") == start_error
    assert registry.get_handler("error.trigger") == trigger_error
