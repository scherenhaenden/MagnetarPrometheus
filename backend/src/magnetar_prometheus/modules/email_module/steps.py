from typing import Dict, Any
from magnetar_prometheus_sdk.models import StepResult
from magnetar_prometheus.modules.linear_module.steps import register_linear_steps
from magnetar_prometheus.modules.error_module.steps import register_error_steps

def fetch_emails(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    return StepResult(success=True, output={"data": {"emails": [{"subject": "Urgent problem", "body": "My account is locked."}]}})

def extract_email_data(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    emails = context.get("data", {}).get("emails", [])
    if not emails:
        return StepResult(success=False, error_message="No emails found.")
    return StepResult(success=True, output={"data": {"extracted": emails[0]["subject"]}})

def ai_classify(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    extracted = context.get("data", {}).get("extracted", "")
    decision = "create_ticket" if "urgent" in extracted.lower() else "manual_review"
    return StepResult(success=True, output={"ai": {"decision": decision}})

def create_ticket(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    return StepResult(success=True, output={"data": {"ticket_id": "TKT-1234"}})

def manual_review(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    return StepResult(success=True, output={"data": {"status": "in_review"}})

def register_example_steps(registry):
    registry.register("email.fetch", fetch_emails)
    registry.register("email.extract", extract_email_data)
    registry.register("ai.classify", ai_classify)
    registry.register("ticket.create", create_ticket)
    registry.register("review.queue", manual_review)

    register_linear_steps(registry)
    register_error_steps(registry)
