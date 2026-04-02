"""Bundled example step handlers for the default email-triage workflow.

Why this file exists in this form:

- The repository still ships a simple email example as the most approachable
  workflow for CLI/runtime demonstrations.
- The handlers intentionally stay deterministic and side-effect free so they
  are safe for tests, docs, and first-run contributor flows.
- Even though the example is small, it still needs to fail in a controlled way
  when input shape assumptions are violated. Example code becomes de facto
  reference code in a young repository, so defensive behavior matters here too.
"""

from typing import Any, Dict

from magnetar_prometheus_sdk.models import StepResult


def fetch_emails(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Return a deterministic mock inbox payload for the bundled example flow."""
    return StepResult(
        success=True,
        output={"data": {"emails": [{"subject": "Urgent problem", "body": "My account is locked."}]}},
    )


def extract_email_data(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Extract the first email subject while failing cleanly on malformed input.

    The example flow still needs to demonstrate controlled failure behavior.
    Returning a structured ``StepResult`` failure here is preferable to letting
    ``KeyError`` or shape surprises escape from reference example code.
    """
    emails = context.get("data", {}).get("emails", [])
    if not isinstance(emails, list):
        return StepResult(success=False, error_message="Email payload is malformed.")

    if not emails:
        return StepResult(success=False, error_message="No emails found.")

    first_email = emails[0]
    if not isinstance(first_email, dict):
        return StepResult(success=False, error_message="Email payload is malformed.")

    subject = first_email.get("subject")
    if not subject:
        return StepResult(success=False, error_message="Email subject is missing.")

    return StepResult(success=True, output={"data": {"extracted": subject}})


def ai_classify(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Route urgent-looking extracted text into a simple example decision."""
    extracted = context.get("data", {}).get("extracted", "")
    decision = "create_ticket" if "urgent" in extracted.lower() else "manual_review"
    return StepResult(success=True, output={"ai": {"decision": decision}})


def create_ticket(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Return a stable synthetic ticket identifier for the example path."""
    return StepResult(success=True, output={"data": {"ticket_id": "TKT-1234"}})


def manual_review(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Return a stable manual-review status for the example path."""
    return StepResult(success=True, output={"data": {"status": "in_review"}})


def register_example_steps(registry):
    """Register the bundled email example handlers on the provided registry."""
    registry.register("email.fetch", fetch_emails)
    registry.register("email.extract", extract_email_data)
    registry.register("ai.classify", ai_classify)
    registry.register("ticket.create", create_ticket)
    registry.register("review.queue", manual_review)
