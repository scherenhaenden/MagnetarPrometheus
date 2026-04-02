from typing import Dict, Any, Callable
from magnetar_prometheus_sdk.models import StepResult

class StepRegistry:
    def __init__(self):
        self._registry: Dict[str, Callable[[Dict[str, Any], Dict[str, Any]], StepResult]] = {}

    def register(self, step_type: str, handler: Callable[[Dict[str, Any], Dict[str, Any]], StepResult]):
        self._registry[step_type] = handler

    def get_handler(self, step_type: str) -> Callable[[Dict[str, Any], Dict[str, Any]], StepResult]:
        if step_type not in self._registry:
            raise ValueError(f"Step type '{step_type}' not registered.")
        return self._registry[step_type]
