import pytest
from magnetar_prometheus.executors.base import BaseExecutor
from magnetar_prometheus_sdk.models import StepDefinition, StepResult

def test_base_executor_abstract():
    """Verify that delegating to the abstract base implementation raises clearly."""
    class TestExecutor(BaseExecutor):
        def execute(self, step_def: StepDefinition, context: dict) -> StepResult:
            return super().execute(step_def, context)

    ex = TestExecutor()
    with pytest.raises(NotImplementedError, match="BaseExecutor\\.execute must be implemented by subclasses\\."):
        ex.execute(StepDefinition(type="test", executor="python"), {})
