"""Step handlers for the focused failure-path example workflow module.

Why this file exists in this form:

- This module demonstrates the engine's behavior when a step returns a failed `StepResult`
  intentionally instead of succeeding or raising a lower-level exception.
- The implementation is deliberately deterministic. The startup step always succeeds, and the
  trigger step always fails with the same message so tests and example runs stay stable.
- The explicit error log in `trigger_error` is not meant to be production-grade observability;
  it exists to leave a traceable signal when the example failure path is exercised.
- Registration remains local to this module's own step types so the example can stay
  self-contained while application-level bundling happens elsewhere.
"""

import logging
from typing import Dict, Any
from magnetar_prometheus_sdk.models import StepResult

logger = logging.getLogger(__name__)

def start_error(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Executes the initial step of the error workflow.

    This function sets up the context for the workflow before the simulated
    failure occurs, proving that the engine executes normally until the error.
    """
    return StepResult(success=True, output={"data": {"status": "started"}})

def trigger_error(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Executes a step designed to intentionally fail the workflow.

    This function returns a StepResult indicating failure, providing an error
    message to simulate a real-world problem during execution. It demonstrates
    the engine's error handling and halting capabilities.
    """
    logger.error("Error triggered in example workflow: Simulated error occurred")
    return StepResult(
        success=False,
        error_message="Simulated error occurred",
        output={},
    )

def register_error_steps(registry):
    """Registers the error module's steps with the workflow engine.

    This function maps the string identifiers from the workflow YAML to the
    Python functions that simulate normal execution and intentional failure.
    """
    registry.register("error.start", start_error)
    registry.register("error.trigger", trigger_error)
