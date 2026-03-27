from typing import Dict, Any
from magnetar_prometheus_sdk.models import StepResult

def start_error(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    return StepResult(success=True, output={"data": {"status": "started"}})

def trigger_error(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    return StepResult(success=False, error_message="Simulated error occurred")

def register_error_steps(registry):
    registry.register("error.start", start_error)
    registry.register("error.trigger", trigger_error)
