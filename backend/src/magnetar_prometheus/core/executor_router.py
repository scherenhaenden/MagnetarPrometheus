"""
Executor routing for the MagnetarPrometheus workflow engine.

:class:`ExecutorRouter` acts as a registry that maps executor-type names
(e.g. ``"python"``) to concrete
:class:`~magnetar_prometheus.executors.base.BaseExecutor` instances so the
engine can dispatch step execution without depending on a specific executor
implementation.
"""

from typing import Dict
from magnetar_prometheus.executors.base import BaseExecutor

class ExecutorRouter:
    """Maps executor-type names to :class:`~magnetar_prometheus.executors.base.BaseExecutor` instances.

    The engine calls :meth:`get_executor` with the executor-type string found
    in each step definition and receives the corresponding executor back,
    keeping executor selection decoupled from workflow logic.
    """

    def __init__(self):
        """Initialise the router with an empty executor registry."""
        self._executors: Dict[str, BaseExecutor] = {}

    def register(self, name: str, executor: BaseExecutor):
        """Register an executor under the given type name.

        Args:
            name: The executor type string used in workflow YAML definitions
                (e.g. ``"python"``).
            executor: The executor instance that handles steps of that type.
        """
        self._executors[name] = executor

    def get_executor(self, name: str) -> BaseExecutor:
        """Retrieve a registered executor by type name.

        Args:
            name: The executor type string to look up.

        Returns:
            The :class:`~magnetar_prometheus.executors.base.BaseExecutor`
            registered under *name*.

        Raises:
            ValueError: When no executor has been registered for *name*.
        """
        if name not in self._executors:
            raise ValueError(f"Executor '{name}' not found.")
        return self._executors[name]
