from typing import Dict, Any
from magnetar_prometheus_sdk.models import StepResult

def start_linear(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Executes the first step of the linear workflow.

    This function simply returns a successful StepResult and updates the context
    with a 'started' status, simulating the initialization phase of a linear process.
    """
    return StepResult(success=True, output={"data": {"status": "started"}})

def process_linear(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Executes the final processing step of the linear workflow.

    This function simulates processing data and returns a successful StepResult,
    updating the context status to 'processed'.
    """
    return StepResult(success=True, output={"data": {"status": "processed"}})

def register_linear_steps(registry):
    """Registers the linear module's steps with the workflow engine.

    This function maps the string identifiers used in the workflow YAML definitions
    to the actual Python functions that execute the logic.
    """
    registry.register("linear.start", start_linear)
    registry.register("linear.process", process_linear)
