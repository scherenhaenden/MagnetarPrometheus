from typing import Dict, Any
from magnetar_prometheus_sdk.models import StepResult

def start_linear(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """
    Executes the first step of the linear workflow.

    This function simply returns a successful StepResult and updates the context
    with a 'started' status, simulating the initialization phase of a linear process.

    Args:
        context (Dict[str, Any]): The current state of the workflow context.
        config (Dict[str, Any]): Configuration parameters for this specific step.

    Returns:
        StepResult: An object indicating successful execution and the updated data.
    """
    return StepResult(success=True, output={"data": {"status": "started"}})

def process_linear(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """
    Executes the final processing step of the linear workflow.

    This function simulates processing data and returns a successful StepResult,
    updating the context status to 'processed'.

    Args:
        context (Dict[str, Any]): The current state of the workflow context, which may
                                  contain data from previous steps.
        config (Dict[str, Any]): Configuration parameters for this step.

    Returns:
        StepResult: An object indicating successful execution and the final processing state.
    """
    return StepResult(success=True, output={"data": {"status": "processed"}})

def register_linear_steps(registry):
    """
    Registers the linear module's steps with the workflow engine.

    This function maps the string identifiers used in the workflow YAML definitions
    to the actual Python functions that execute the logic.

    Args:
        registry (StepRegistry): The central registry used by the workflow engine
                                 to route step execution.
    """
    registry.register("linear.start", start_linear)
    registry.register("linear.process", process_linear)
