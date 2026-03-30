"""
Abstract base class for step executors in MagnetarPrometheus.

All concrete executor implementations must inherit from :class:`BaseExecutor`
and implement :meth:`execute` so the engine can dispatch step execution
through a stable, type-checked interface regardless of the execution backend.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from magnetar_prometheus_sdk.models import StepDefinition, StepResult

class BaseExecutor(ABC):
    """Abstract contract for all step executor implementations.

    Concrete subclasses (e.g.
    :class:`~magnetar_prometheus.executors.python_executor.PythonExecutor`)
    implement :meth:`execute` to carry out the actual work for a given step
    type.
    """

    @abstractmethod
    def execute(self, step_def: StepDefinition, context: Dict[str, Any]) -> StepResult:
        """Execute a single workflow step and return its result.

        Args:
            step_def: The step definition from the workflow YAML, including
                type, executor, and configuration parameters.
            context: A snapshot of the current run context passed as a plain
                dictionary.

        Returns:
            A :class:`~magnetar_prometheus_sdk.models.StepResult` describing
            the outcome of the step.
        """
