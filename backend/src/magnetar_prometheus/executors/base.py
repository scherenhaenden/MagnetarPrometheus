from abc import ABC, abstractmethod
from typing import Dict, Any
from magnetar_prometheus_sdk.models import StepDefinition, StepResult

class BaseExecutor(ABC):
    @abstractmethod
    def execute(self, step_def: StepDefinition, context: Dict[str, Any]) -> StepResult:
        pass
