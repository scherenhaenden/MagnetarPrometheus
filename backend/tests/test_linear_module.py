import pytest
from magnetar_prometheus.modules.linear_module.steps import (
    start_linear, process_linear, register_linear_steps
)
from magnetar_prometheus.registry.step_registry import StepRegistry

def test_start_linear():
    """
    Tests the initial step of the linear workflow.

    Verifies that the step executes successfully and correctly updates
    the output data status to 'started'.
    """
    res = start_linear({}, {})
    assert res.success is True
    assert res.output["data"]["status"] == "started"

def test_start_linear_rejects_invalid_inputs():
    """Tests that the first linear step rejects malformed context/config values."""
    res = start_linear([], {})
    assert res.success is False
    assert res.error_message == "Invalid context or config"

def test_process_linear():
    """
    Tests the final processing step of the linear workflow.

    Verifies that the simulated processing step completes successfully
    and updates the output data status to 'processed'.
    """
    res = process_linear({}, {})
    assert res.success is True
    assert res.output["data"]["status"] == "processed"

def test_process_linear_rejects_invalid_inputs():
    """Tests that the processing step rejects malformed context/config values."""
    res = process_linear({}, [])
    assert res.success is False
    assert res.error_message == "Invalid context or config"

def test_register_linear_steps():
    """
    Tests the registration of the linear workflow steps.

    Ensures that the string identifiers ('linear.start', 'linear.process')
    are correctly mapped to their respective Python function handlers
    within the workflow engine's registry.
    """
    registry = StepRegistry()
    register_linear_steps(registry)
    assert registry.get_handler("linear.start") == start_linear
    assert registry.get_handler("linear.process") == process_linear
