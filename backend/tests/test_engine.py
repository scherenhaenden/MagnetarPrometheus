import pytest
from magnetar_prometheus_sdk.models import Workflow, StepDefinition, StepResult
from magnetar_prometheus.core.engine import Engine
from magnetar_prometheus.core.executor_router import ExecutorRouter
from magnetar_prometheus.core.context_manager import ContextManager
from magnetar_prometheus.executors.base import BaseExecutor

class MockExecutor(BaseExecutor):
    def execute(self, step_def, context):
        if step_def.type == "success_step":
            return StepResult(success=True, output={"data": {"val": 1}})
        elif step_def.type == "fail_step":
            return StepResult(success=False, error_message="failed")
        elif step_def.type == "exception_step":
            raise ValueError("exception")
        elif step_def.type == "ai_step":
            return StepResult(success=True, output={"ai": {"decision": "branch_b"}})
        elif step_def.type == "custom_output":
            return StepResult(success=True, output={"other_key": "val"})
        return StepResult(success=True)

@pytest.fixture
def engine():
    router = ExecutorRouter()
    router.register("python", MockExecutor())
    cm = ContextManager()
    return Engine(router, cm)

def test_engine_successful_flow(engine):
    wf = Workflow(
        id="wf_1",
        name="Test",
        version="1.0.0",
        start_step="step1",
        steps={
            "step1": StepDefinition(type="success_step", executor="python", next="end")
        }
    )
    result = engine.run(wf)
    assert result["run"]["status"] == "completed"
    assert result["data"]["val"] == 1

def test_engine_fail_flow(engine):
    wf = Workflow(
        id="wf_2",
        name="Test",
        version="1.0.0",
        start_step="step1",
        steps={
            "step1": StepDefinition(type="fail_step", executor="python", next="end")
        }
    )
    result = engine.run(wf)
    assert result["run"]["status"] == "failed"
    assert len(result["errors"]) == 1

def test_engine_exception_flow(engine):
    wf = Workflow(
        id="wf_3",
        name="Test",
        version="1.0.0",
        start_step="step1",
        steps={
            "step1": StepDefinition(type="exception_step", executor="python", next="end")
        }
    )
    result = engine.run(wf)
    assert result["run"]["status"] == "failed"
    assert result["errors"][0]["error_message"] == "exception"

def test_engine_missing_step(engine):
    wf = Workflow(
        id="wf_4",
        name="Test",
        version="1.0.0",
        start_step="missing",
        steps={}
    )
    with pytest.raises(ValueError, match="Step 'missing' not found in workflow definition."):
        engine.run(wf)

def test_engine_conditional_branching(engine):
    wf = Workflow(
        id="wf_5",
        name="Test",
        version="1.0.0",
        start_step="step1",
        steps={
            "step1": StepDefinition(type="ai_step", executor="python", next={
                "mode": "conditional",
                "conditions": [
                    {"when": "context['ai'].get('decision') == 'branch_a'", "go_to": "step2"},
                    {"when": "context['ai'].get('decision') == 'branch_b'", "go_to": "step3"}
                ]
            }),
            "step2": StepDefinition(type="success_step", executor="python", next="end"),
            "step3": StepDefinition(type="success_step", executor="python", next="end")
        }
    )
    result = engine.run(wf)
    assert result["run"]["status"] == "completed"
    assert result["history"][-1]["step"] == "step3"

def test_engine_custom_output_keys(engine):
    wf = Workflow(
        id="wf_6",
        name="Test",
        version="1.0.0",
        start_step="step1",
        steps={
            "step1": StepDefinition(type="custom_output", executor="python", next="end")
        }
    )
    result = engine.run(wf)
    assert result["run"]["status"] == "completed"
    assert result["data"]["other_key"] == "val"

def test_engine_next_step_from_result(engine):
    class OverrideExecutor(BaseExecutor):
        def execute(self, step_def, context):
            return StepResult(success=True, next_step="end")

    router = ExecutorRouter()
    router.register("override", OverrideExecutor())
    cm = ContextManager()
    eng = Engine(router, cm)

    wf = Workflow(
        id="wf_7",
        name="Test",
        version="1.0.0",
        start_step="step1",
        steps={
            "step1": StepDefinition(type="custom_output", executor="override", next="step2"),
            "step2": StepDefinition(type="custom_output", executor="override", next="end")
        }
    )
    result = eng.run(wf)
    assert result["run"]["status"] == "completed"
    assert len(result["history"]) == 1
    assert result["history"][0]["step"] == "step1"

def test_engine_conditional_branching_eval_error(engine):
    # This test verifies that if safe_evaluate throws an exception, it is caught
    class BuggyEngine(Engine):
        def _safe_evaluate(self, expr, ctx):
            raise Exception("Unexpected eval error")

    router = ExecutorRouter()
    router.register("python", MockExecutor())
    cm = ContextManager()
    buggy_eng = BuggyEngine(router, cm)

    wf = Workflow(
        id="wf_8",
        name="Test",
        version="1.0.0",
        start_step="step1",
        steps={
            "step1": StepDefinition(type="success_step", executor="python", next={
                "mode": "conditional",
                "conditions": [
                    {"when": "something", "go_to": "step2"}
                ]
            }),
            "step2": StepDefinition(type="success_step", executor="python", next="end")
        }
    )
    result = buggy_eng.run(wf)
    assert result["run"]["status"] == "completed"
    assert len(result["history"]) == 1
    assert result["history"][0]["step"] == "step1"

def test_engine_safe_evaluate_paths(engine):
    ctx = {"ai": {"decision": "x", "other": "y"}}

    assert engine._safe_evaluate('context["ai"]["decision"] == "x"', ctx) == True
    assert engine._safe_evaluate("context['ai']['decision'] == 'x'", ctx) == True
    assert engine._safe_evaluate('context["ai"].get("decision") == "x"', ctx) == True
    assert engine._safe_evaluate("context['ai']['other'] == 'y'", ctx) == True
    assert engine._safe_evaluate("context['ai']['other'] == 'z'", ctx) == False

    # unsupported evaluation pattern falls back safely to False
    assert engine._safe_evaluate("foo == 'bar'", ctx) == False
    assert engine._safe_evaluate("context['ai']['other'] == y", ctx) == False
    assert engine._safe_evaluate("context['ai']['other'] == ", ctx) == False
    assert engine._safe_evaluate("not an equal equal statement", ctx) == False

def test_engine_conditional_branching_dict_compatibility(engine):
    # Tests the backward compatibility logic where next is a dict
    wf = Workflow(
        id="wf_dict",
        name="Test",
        version="1.0.0",
        start_step="step1",
        steps={
            "step1": StepDefinition(type="ai_step", executor="python", next={
                "mode": "conditional",
                "conditions": [
                    {"when": "context['ai'].get('decision') == 'branch_a'", "go_to": "step2"},
                    {"when": "context['ai'].get('decision') == 'branch_b'", "go_to": "step3"}
                ]
            }),
            "step2": StepDefinition(type="success_step", executor="python", next="end"),
            "step3": StepDefinition(type="success_step", executor="python", next="end")
        }
    )
    # the dict is converted to dict internally by pydantic because of Union[str, ConditionalRouting, Dict[str, Any], None]
    # Actually wait, Union will try to parse it into ConditionalRouting if it matches the schema.
    # To test the dict branch explicitly, we need to bypass Pydantic model validation
    # or ensure it doesn't match ConditionalRouting (e.g. invalid mode).
    # If it parses to ConditionalRouting, the dict branch is never hit.
    # Let's write a mock object that mimics dict but is a dict to force the branch,
    # or just mock the step_def.next directly.
    step1 = StepDefinition(type="ai_step", executor="python")
    step1.next = {
        "mode": "conditional",
        "conditions": [
            {"when": "context['ai'].get('decision') == 'branch_a'", "go_to": "step2"},
            {"when": "context['ai'].get('decision') == 'branch_b'", "go_to": "step3"}
        ]
    }
    wf.steps["step1"] = step1
    result = engine.run(wf)
    assert result["run"]["status"] == "completed"
    assert result["history"][-1]["step"] == "step3"

def test_engine_conditional_branching_dict_eval_error(engine):
    # Covers the exception block in the dict compatibility branch
    class BuggyEngineDict(Engine):
        def _safe_evaluate(self, expr, ctx):
            raise Exception("Unexpected eval error")

    from magnetar_prometheus.core.executor_router import ExecutorRouter
    from magnetar_prometheus.core.context_manager import ContextManager
    from magnetar_prometheus.executors.base import BaseExecutor

    class MockExecutor2(BaseExecutor):
        def execute(self, step_def, context):
            return StepResult(success=True)

    router = ExecutorRouter()
    router.register("python", MockExecutor2())
    cm = ContextManager()
    buggy_eng = BuggyEngineDict(router, cm)

    wf = Workflow(
        id="wf_dict_err",
        name="Test",
        version="1.0.0",
        start_step="step1",
        steps={
            "step1": StepDefinition(type="success_step", executor="python"),
            "step2": StepDefinition(type="success_step", executor="python", next="end")
        }
    )
    step1 = wf.steps["step1"]
    step1.next = {
        "mode": "conditional",
        "conditions": [
            {"when": "something", "go_to": "step2"}
        ]
    }
    result = buggy_eng.run(wf)
    assert result["run"]["status"] == "completed"
    assert len(result["history"]) == 1
    assert result["history"][0]["step"] == "step1"
