"""
Python-based step executor for the MagnetarPrometheus workflow engine.

:class:`PythonExecutor` looks up registered Python handler functions via a
:class:`~magnetar_prometheus.registry.step_registry.StepRegistry` and
invokes them with the current run context and step configuration.
"""

from typing import Dict, Any
from magnetar_prometheus_sdk.models import StepDefinition, StepResult
from magnetar_prometheus.executors.base import BaseExecutor
from magnetar_prometheus.registry.step_registry import StepRegistry

class PythonExecutor(BaseExecutor):
    """Executes workflow steps by calling registered Python handler functions.

    Looks up the handler for each step type in the provided
    :class:`~magnetar_prometheus.registry.step_registry.StepRegistry` and
    delegates execution to it, keeping the engine decoupled from specific
    business-logic implementations.
    """

    def __init__(self, registry: StepRegistry):
        """Initialise the executor with a step handler registry.

        Args:
            registry: The registry from which handler callables are retrieved
                at step-execution time.
        """
        self.registry = registry

    def execute(self, step_def: StepDefinition, context: Dict[str, Any]) -> StepResult:
        """Execute a step by dispatching to its registered Python handler.

        Args:
            step_def: The step definition containing the type and configuration
                for this execution.
            context: A snapshot of the current run context.

        Returns:
            The :class:`~magnetar_prometheus_sdk.models.StepResult` produced
            by the handler.
        """
        handler = self.registry.get_handler(step_def.type)
        return handler(context, step_def.config)
