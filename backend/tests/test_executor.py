import re

import pytest
from magnetar_prometheus.core.executor_router import ExecutorRouter
from magnetar_prometheus.executors.base import BaseExecutor
from magnetar_prometheus.executors.python_executor import PythonExecutor
from magnetar_prometheus.registry.step_registry import StepRegistry
from magnetar_prometheus_sdk.models import StepDefinition, StepResult

class DummyExecutor(BaseExecutor):
    def execute(self, step_def, context):
        return StepResult(success=True)

def test_executor_router():
    router = ExecutorRouter()
    executor = DummyExecutor()
    router.register("dummy", executor)

    assert router.get_executor("dummy") is executor

    with pytest.raises(ValueError, match=re.escape("Executor 'not_found' not found.")):
        router.get_executor("not_found")

def test_step_registry():
    registry = StepRegistry()
    def dummy_step(context, config):
        return StepResult(success=True)

    registry.register("dummy", dummy_step)
    handler = registry.get_handler("dummy")
    assert handler({}, {}).success is True

    with pytest.raises(ValueError, match=re.escape("Step type 'not_found' not registered.")):
        registry.get_handler("not_found")

def test_python_executor():
    registry = StepRegistry()
    def dummy_step(context, config):
        return StepResult(success=True, output={"data": {"test": config.get("val")}})

    registry.register("dummy", dummy_step)
    executor = PythonExecutor(registry)

    step_def = StepDefinition(type="dummy", executor="python", config={"val": 123})
    result = executor.execute(step_def, {})

    assert result.success is True
    assert result.output["data"]["test"] == 123
