from datetime import datetime, timezone

import pytest

from magnetar_prometheus_sdk.models import (
    Workflow,
    StepDefinition,
    StepResult,
    RunContext,
    Condition,
    ConditionalRouting,
    RunStatus,
    RunSubmissionRequest,
    RunResponse,
    RunListingItem,
    RunSummary,
)


def test_step_definition_defaults():
    step = StepDefinition(type="test.step", executor="python")
    assert step.type == "test.step"
    assert step.executor == "python"
    assert step.description is None
    assert step.config == {}
    assert step.next is None
    assert step.ui_metadata == {}


def test_workflow_defaults():
    wf = Workflow(id="test_wf", name="Test Workflow", version="1.0.0", start_step="start")
    assert wf.id == "test_wf"
    assert wf.name == "Test Workflow"
    assert wf.version == "1.0.0"
    assert wf.description is None
    assert wf.start_step == "start"
    assert wf.settings == {}
    assert wf.steps == {}
    assert wf.ui_metadata == {}


def test_condition_and_routing():
    cond = Condition(when="a == b", go_to="next_step")
    assert cond.when == "a == b"
    assert cond.go_to == "next_step"

    route = ConditionalRouting(conditions=[cond])
    assert route.mode == "conditional"
    assert len(route.conditions) == 1
    assert route.conditions[0].when == "a == b"

    step = StepDefinition(type="test.branch", executor="python", next=route)
    assert step.next.mode == "conditional"
    assert len(step.next.conditions) == 1
    assert step.next.conditions[0].go_to == "next_step"


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


def test_run_status_serialization():
    assert RunStatus.PENDING == "pending"
    assert RunStatus.RUNNING == "running"
    assert RunStatus.COMPLETED == "completed"
    assert RunStatus.FAILED == "failed"
    assert RunStatus.CANCELLED == "cancelled"


def test_run_submission_request_defaults():
    req = RunSubmissionRequest(workflow_id="wf_123")
    assert req.workflow_id == "wf_123"
    assert req.workflow_version is None
    assert req.input_data == {}
    assert req.tags == []


def test_run_response_defaults():
    resp = RunResponse(
        run_id="run_1",
        workflow_id="wf_123",
        status=RunStatus.PENDING,
        created_at="2023-01-01T00:00:00Z",
    )
    assert resp.run_id == "run_1"
    assert resp.workflow_id == "wf_123"
    assert resp.status == RunStatus.PENDING
    assert resp.created_at == datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert resp.message is None


def test_run_listing_item_defaults():
    item = RunListingItem(
        run_id="run_1",
        workflow_id="wf_123",
        status=RunStatus.COMPLETED,
        created_at="2023-01-01T00:00:00Z",
    )
    assert item.run_id == "run_1"
    assert item.workflow_id == "wf_123"
    assert item.status == RunStatus.COMPLETED
    assert item.created_at == datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert item.completed_at is None
    assert item.tags == []


def test_run_summary_defaults():
    summary = RunSummary(
        run_id="run_1",
        workflow_id="wf_123",
        status=RunStatus.FAILED,
        created_at="2023-01-01T00:00:00Z",
    )
    assert summary.run_id == "run_1"
    assert summary.workflow_id == "wf_123"
    assert summary.status == RunStatus.FAILED
    assert summary.created_at == datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert summary.completed_at is None
    assert summary.tags == []
    assert summary.final_context is None
    assert summary.error_message is None
