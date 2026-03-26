import pytest
from magnetar_prometheus.example_module import (
    fetch_emails, extract_email_data, ai_classify, create_ticket, manual_review, register_example_steps
)
from magnetar_prometheus.registry.step_registry import StepRegistry

def test_fetch_emails():
    res = fetch_emails({}, {})
    assert res.success is True
    assert "emails" in res.output["data"]

def test_extract_email_data():
    res1 = extract_email_data({}, {})
    assert res1.success is False

    ctx = {"data": {"emails": [{"subject": "Test"}]}}
    res2 = extract_email_data(ctx, {})
    assert res2.success is True
    assert res2.output["data"]["extracted"] == "Test"

def test_ai_classify():
    ctx1 = {"data": {"extracted": "urgent issue"}}
    res1 = ai_classify(ctx1, {})
    assert res1.success is True
    assert res1.output["ai"]["decision"] == "create_ticket"

    ctx2 = {"data": {"extracted": "other issue"}}
    res2 = ai_classify(ctx2, {})
    assert res2.success is True
    assert res2.output["ai"]["decision"] == "manual_review"

def test_create_ticket():
    res = create_ticket({}, {})
    assert res.success is True
    assert "ticket_id" in res.output["data"]

def test_manual_review():
    res = manual_review({}, {})
    assert res.success is True
    assert "status" in res.output["data"]

def test_register_example_steps():
    registry = StepRegistry()
    register_example_steps(registry)
    assert registry.get_handler("email.fetch") == fetch_emails
