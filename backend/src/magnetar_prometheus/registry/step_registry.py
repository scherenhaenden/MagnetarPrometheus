"""
Step handler registry for the MagnetarPrometheus workflow engine.

:class:`StepRegistry` stores the mapping from workflow step-type strings to
the Python callables that implement them, allowing the engine to resolve and
invoke handlers without any direct import dependency on specific step
implementations.
"""

from typing import Dict, Any, Callable
from magnetar_prometheus_sdk.models import StepResult

class StepRegistry:
    """Maps step-type strings to Python handler callables.

    Handler callables must accept ``(context: Dict[str, Any], config:
    Dict[str, Any])`` and return a
    :class:`~magnetar_prometheus_sdk.models.StepResult`.
    """

    def __init__(self):
        """Initialise the registry with an empty handler mapping."""
        self._registry: Dict[str, Callable[[Dict[str, Any], Dict[str, Any]], StepResult]] = {}

    def register(self, step_type: str, handler: Callable[[Dict[str, Any], Dict[str, Any]], StepResult]):
        """Register a handler callable for a step type.

        Args:
            step_type: The step type string used in workflow YAML definitions
                (e.g. ``"email.fetch"``).
            handler: A callable that implements the step logic.
        """
        self._registry[step_type] = handler

    def get_handler(self, step_type: str) -> Callable[[Dict[str, Any], Dict[str, Any]], StepResult]:
        """Retrieve the handler registered for a step type.

        Args:
            step_type: The step type string to look up.

        Returns:
            The registered handler callable.

        Raises:
            ValueError: When no handler has been registered for *step_type*.
        """
        if step_type not in self._registry:
            raise ValueError(f"Step type '{step_type}' not registered.")
        return self._registry[step_type]
