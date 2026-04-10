"""Tests for the math example workflow module."""
from magnetar_prometheus.modules.math_module.steps import math_add, math_multiply, register_math_steps
from magnetar_prometheus.registry.step_registry import StepRegistry


def test_math_add():
    """Test the math_add step."""
    result = math_add({}, {"a": 5, "b": 10})
    assert result.success is True
    assert result.output["data"]["sum"] == 15

    # test missing config
    result = math_add({}, {})
    assert result.success is True
    assert result.output["data"]["sum"] == 0


def test_math_add_preserves_existing_context_data():
    """Test the math_add step preserves existing data fields."""
    result = math_add({"data": {"workflow_id": "math-demo"}}, {"a": 2, "b": 3})
    assert result.success is True
    assert result.output["data"]["workflow_id"] == "math-demo"
    assert result.output["data"]["sum"] == 5


def test_math_multiply():
    """Test the math_multiply step."""
    result = math_multiply({"data": {"sum": 15}}, {"factor": 2})
    assert result.success is True
    assert result.output["data"]["result"] == 30

    # test missing data and factor
    result = math_multiply({}, {})
    assert result.success is True
    assert result.output["data"]["result"] == 0


def test_math_multiply_handles_non_mapping_context_data():
    """Test the math_multiply step treats invalid context data as empty."""
    result = math_multiply({"data": None}, {"factor": 2})
    assert result.success is True
    assert result.output["data"]["result"] == 0


def test_math_multiply_preserves_existing_context_data():
    """Test the math_multiply step preserves fields already present in context data."""
    result = math_multiply({"data": {"sum": 15, "workflow_id": "math-demo"}}, {"factor": 2})
    assert result.success is True
    assert result.output["data"]["workflow_id"] == "math-demo"
    assert result.output["data"]["sum"] == 15
    assert result.output["data"]["result"] == 30


def test_register_math_steps():
    """Test registration of math steps."""
    registry = StepRegistry()
    register_math_steps(registry)
    assert callable(registry.get_handler("math.add"))
    assert callable(registry.get_handler("math.multiply"))
