"""Step handlers for the simple math example workflow module.

Why this file exists in this form:
- This module demonstrates a simple numeric calculation workflow.
- It allows operators to see how state is accumulated and passed between steps.
"""

from typing import Dict, Any
from magnetar_prometheus_sdk.models import StepResult

def math_add(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Executes the addition step, returning the sum of 'a' and 'b'."""
    a = config.get("a", 0)
    b = config.get("b", 0)
    return StepResult(success=True, output={"data": {"sum": a + b}})

def math_multiply(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Executes the multiplication step, multiplying 'factor' by the previously computed sum."""
    factor = config.get("factor", 1)
    previous_sum = context.get("data", {}).get("sum", 0)
    return StepResult(success=True, output={"data": {"result": previous_sum * factor}})

def register_math_steps(registry):
    """Registers the math module's steps with the workflow engine."""
    registry.register("math.add", math_add)
    registry.register("math.multiply", math_multiply)
