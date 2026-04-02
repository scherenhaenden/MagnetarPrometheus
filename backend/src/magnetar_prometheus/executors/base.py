"""Abstract executor contract for runtime step execution.

Why this file exists in this form:

- The runtime needs a narrow shared contract for executor implementations.
- The base class is intentionally small so executor-specific behavior stays in
  concrete implementations instead of being hidden in framework magic.
- The abstract method still raises ``NotImplementedError`` so tests can verify
  the fallback behavior explicitly when a subclass delegates to ``super()``.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

from magnetar_prometheus_sdk.models import StepDefinition, StepResult


class BaseExecutor(ABC):
    """Define the minimum execution contract for runtime executor backends."""

    @abstractmethod
    def execute(self, step_def: StepDefinition, context: Dict[str, Any]) -> StepResult:
        """Execute one workflow step against the supplied context.

        Concrete executors must override this method. The explicit
        ``NotImplementedError`` is kept even though the method is abstract so
        tests and subclasses that delegate to ``super()`` fail loudly and
        predictably instead of returning ``None`` by accident.
        """
        raise NotImplementedError("BaseExecutor.execute must be implemented by subclasses.")
