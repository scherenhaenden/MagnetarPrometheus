"""
Step handler implementations for the email-triage example module.

Each function in this module is a deterministic, in-memory stub that
demonstrates how step handlers interact with the run context and produce
:class:`~magnetar_prometheus_sdk.models.StepResult` objects.  The data
returned is intentionally hard-coded so the example workflow always produces
predictable output without requiring external services.
"""

from typing import Dict, Any
from magnetar_prometheus_sdk.models import StepResult

def fetch_emails(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Return a stubbed list of unread emails from the configured mailbox.

    Args:
        context: Current run context (unused in this stub).
        config: Step configuration from the workflow YAML (unused in this stub).

    Returns:
        A successful :class:`~magnetar_prometheus_sdk.models.StepResult`
        containing one hard-coded email in ``data.emails``.
    """
    return StepResult(success=True, output={"data": {"emails": [{"subject": "Urgent problem", "body": "My account is locked."}]}})

def extract_email_data(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Extract the subject from the first email in the context.

    Args:
        context: Current run context; expects ``data.emails`` to be populated
            by a preceding ``email.fetch`` step.
        config: Step configuration from the workflow YAML (unused in this stub).

    Returns:
        A successful result with ``data.extracted`` set to the first email's
        subject, or a failure result when no emails are present.
    """
    emails = context.get("data", {}).get("emails", [])
    if not emails:
        return StepResult(success=False, error_message="No emails found.")
    return StepResult(success=True, output={"data": {"extracted": emails[0]["subject"]}})

def ai_classify(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Classify the extracted email subject and produce a routing decision.

    Checks whether the extracted subject contains the word ``"urgent"``
    (case-insensitive) and emits either ``"create_ticket"`` or
    ``"manual_review"`` as the AI decision.

    Args:
        context: Current run context; expects ``data.extracted`` to be set.
        config: Step configuration from the workflow YAML (unused in this stub).

    Returns:
        A successful result with ``ai.decision`` set to the classification
        outcome.
    """
    extracted = context.get("data", {}).get("extracted", "")
    decision = "create_ticket" if "urgent" in extracted.lower() else "manual_review"
    return StepResult(success=True, output={"ai": {"decision": decision}})

def create_ticket(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Simulate creating a support ticket and return a stub ticket ID.

    Args:
        context: Current run context (unused in this stub).
        config: Step configuration from the workflow YAML (unused in this stub).

    Returns:
        A successful result with ``data.ticket_id`` set to a hard-coded
        ticket reference.
    """
    return StepResult(success=True, output={"data": {"ticket_id": "TKT-1234"}})

def manual_review(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Simulate queuing an email for manual review.

    Args:
        context: Current run context (unused in this stub).
        config: Step configuration from the workflow YAML (unused in this stub).

    Returns:
        A successful result with ``data.status`` set to ``"in_review"``.
    """
    return StepResult(success=True, output={"data": {"status": "in_review"}})

def register_example_steps(registry) -> None:
    """Register all email-triage step handlers with the given step registry.

    Maps each workflow step type string used in ``email_triage.yaml`` to its
    corresponding Python handler function.

    Args:
        registry: A :class:`~magnetar_prometheus.registry.step_registry.StepRegistry`
            instance to register the handlers into.
    """
    registry.register("email.fetch", fetch_emails)
    registry.register("email.extract", extract_email_data)
    registry.register("ai.classify", ai_classify)
    registry.register("ticket.create", create_ticket)
    registry.register("review.queue", manual_review)
