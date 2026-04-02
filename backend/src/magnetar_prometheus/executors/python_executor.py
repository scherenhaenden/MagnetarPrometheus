from typing import Dict, Any
from magnetar_prometheus_sdk.models import StepDefinition, StepResult
from magnetar_prometheus.executors.base import BaseExecutor
from magnetar_prometheus.registry.step_registry import StepRegistry

class PythonExecutor(BaseExecutor):
    def __init__(self, registry: StepRegistry):
        self.registry = registry

    def execute(self, step_def: StepDefinition, context: Dict[str, Any]) -> StepResult:
        handler = self.registry.get_handler(step_def.type)
        return handler(context, step_def.config)
