from typing import Dict, Any
from magnetar_prometheus_sdk.models import StepResult

def start_linear(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    return StepResult(success=True, output={"data": {"status": "started"}})

def process_linear(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    return StepResult(success=True, output={"data": {"status": "processed"}})

def register_linear_steps(registry):
    registry.register("linear.start", start_linear)
    registry.register("linear.process", process_linear)
