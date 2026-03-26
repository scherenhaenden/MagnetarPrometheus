import pytest
from magnetar_prometheus_sdk.models import Workflow, StepDefinition, StepResult, RunContext

def test_step_definition_defaults():
    step = StepDefinition(type="test.step", executor="python")
    assert step.type == "test.step"
    assert step.executor == "python"
    assert step.config == {}
    assert step.next is None

def test_workflow_defaults():
    wf = Workflow(
        id="test_wf",
        name="Test Workflow",
        version="1.0.0",
        start_step="start"
    )
    assert wf.id == "test_wf"
    assert wf.name == "Test Workflow"
    assert wf.version == "1.0.0"
    assert wf.start_step == "start"
    assert wf.settings == {}
    assert wf.steps == {}

def test_step_result_defaults():
    res = StepResult(success=True)
    assert res.success is True
    assert res.output == {}
    assert res.next_step is None
    assert res.warnings == []
    assert res.error_code is None
    assert res.error_message is None

def test_run_context_defaults():
    ctx = RunContext()
    assert ctx.run == {}
    assert ctx.input == {}
    assert ctx.data == {}
    assert ctx.ai == {}
    assert ctx.history == []
    assert ctx.errors == []
