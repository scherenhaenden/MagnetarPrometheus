import pytest
from magnetar_prometheus.modules.linear_module.steps import (
    start_linear, process_linear, register_linear_steps
)
from magnetar_prometheus.registry.step_registry import StepRegistry

def test_start_linear():
    res = start_linear({}, {})
    assert res.success is True
    assert res.output["data"]["status"] == "started"

def test_process_linear():
    res = process_linear({}, {})
    assert res.success is True
    assert res.output["data"]["status"] == "processed"

def test_register_linear_steps():
    registry = StepRegistry()
    register_linear_steps(registry)
    assert registry.get_handler("linear.start") == start_linear
    assert registry.get_handler("linear.process") == process_linear
