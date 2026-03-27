from typing import Dict, Any
from magnetar_prometheus_sdk.models import StepResult

def start_error(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """
    Executes the initial step of the error workflow.

    This function sets up the context for the workflow before the simulated
    failure occurs, proving that the engine executes normally until the error.

    Args:
        context (Dict[str, Any]): The current state of the workflow context.
        config (Dict[str, Any]): Configuration parameters for this step.

    Returns:
        StepResult: An object indicating successful execution and the initial state.
    """
    return StepResult(success=True, output={"data": {"status": "started"}})

def trigger_error(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """
    Executes a step designed to intentionally fail the workflow.

    This function returns a StepResult indicating failure, providing an error
    message to simulate a real-world problem during execution. It demonstrates
    the engine's error handling and halting capabilities.

    Args:
        context (Dict[str, Any]): The current state of the workflow context.
        config (Dict[str, Any]): Configuration parameters for this step.

    Returns:
        StepResult: An object indicating failed execution with an associated error message.
    """
    return StepResult(success=False, error_message="Simulated error occurred")

def register_error_steps(registry):
    """
    Registers the error module's steps with the workflow engine.

    This function maps the string identifiers from the workflow YAML to the
    Python functions that simulate normal execution and intentional failure.

    Args:
        registry (StepRegistry): The central registry used by the workflow engine
                                 to route step execution.
    """
    registry.register("error.start", start_error)
    registry.register("error.trigger", trigger_error)
