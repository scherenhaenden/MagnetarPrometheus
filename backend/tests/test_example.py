"""Tests for the repository's bundled example registration and email example handlers.

Why this file exists in this form:

- These tests protect the original email example workflow logic because that workflow remains
  the default runnable slice for the CLI and the reference happy-path example for contributors.
- The file now also verifies the distinction between module-local registration and
  application-level bundled example registration so the branch's decoupling work does not
  regress silently.
- The assertions stay intentionally direct and deterministic because this file is meant to
  guard example-surface behavior, not explore deep engine semantics already covered elsewhere.
"""

import pytest
from magnetar_prometheus.modules.example_registry import register_all_example_steps
from magnetar_prometheus.modules.email_module.steps import (
    fetch_emails, extract_email_data, ai_classify, create_ticket, manual_review, register_example_steps
)
from magnetar_prometheus.registry.step_registry import StepRegistry

def test_fetch_emails():
    """Verify that the email example returns a deterministic mock email payload."""
    res = fetch_emails({}, {})
    assert res.success is True
    assert "emails" in res.output["data"]

def test_extract_email_data():
    """Verify that extraction fails without emails and succeeds with the first subject."""
    res1 = extract_email_data({}, {})
    assert res1.success is False

    ctx = {"data": {"emails": [{"subject": "Test"}]}}
    res2 = extract_email_data(ctx, {})
    assert res2.success is True
    assert res2.output["data"]["extracted"] == "Test"

def test_ai_classify():
    """Verify that the example classifier routes urgent text differently from other text."""
    ctx1 = {"data": {"extracted": "urgent issue"}}
    res1 = ai_classify(ctx1, {})
    assert res1.success is True
    assert res1.output["ai"]["decision"] == "create_ticket"

    ctx2 = {"data": {"extracted": "other issue"}}
    res2 = ai_classify(ctx2, {})
    assert res2.success is True
    assert res2.output["ai"]["decision"] == "manual_review"

def test_create_ticket():
    """Verify that the example ticket step returns a stable synthetic ticket id."""
    res = create_ticket({}, {})
    assert res.success is True
    assert "ticket_id" in res.output["data"]

def test_manual_review():
    """Verify that the manual-review example step reports an in-review status."""
    res = manual_review({}, {})
    assert res.success is True
    assert "status" in res.output["data"]

def test_register_example_steps():
    """Verify that email-only registration stays local to the email example module."""
    registry = StepRegistry()
    register_example_steps(registry)
    assert registry.get_handler("email.fetch") == fetch_emails
    with pytest.raises(ValueError, match="linear.start"):
        registry.get_handler("linear.start")
    with pytest.raises(ValueError, match="error.trigger"):
        registry.get_handler("error.trigger")


def test_register_all_example_steps():
    """Verify that application-level example registration exposes every bundled example."""
    registry = StepRegistry()
    register_all_example_steps(registry)
    assert registry.get_handler("email.fetch") == fetch_emails
    assert registry.get_handler("linear.start") is not None
    assert registry.get_handler("error.trigger") is not None
