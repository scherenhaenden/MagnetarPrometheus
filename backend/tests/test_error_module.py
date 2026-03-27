import pytest
from magnetar_prometheus.modules.error_module.steps import (
    start_error, trigger_error, register_error_steps
)
from magnetar_prometheus.registry.step_registry import StepRegistry

def test_start_error():
    res = start_error({}, {})
    assert res.success is True
    assert res.output["data"]["status"] == "started"

def test_trigger_error():
    res = trigger_error({}, {})
    assert res.success is False
    assert res.error_message == "Simulated error occurred"

def test_register_error_steps():
    registry = StepRegistry()
    register_error_steps(registry)
    assert registry.get_handler("error.start") == start_error
    assert registry.get_handler("error.trigger") == trigger_error
