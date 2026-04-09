"""Step handlers for the mock HTTP example workflow module.

Why this file exists in this form:
- This module demonstrates how an external system interaction might be modeled.
- The logic is entirely mocked to remain side-effect free and deterministic for tests.
"""

from typing import Dict, Any
from magnetar_prometheus_sdk.models import StepResult

def http_get(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Simulates an HTTP GET request to the configured URL."""
    url = config.get("url", "unknown")
    return StepResult(success=True, output={"data": {"http_status": 200, "raw_body": f'{{"url": "{url}", "valid": true}}'}})

def json_parse(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Simulates parsing the raw body string returned by the HTTP GET step."""
    import json
    raw_body = context.get("data", {}).get("raw_body", "{}")
    try:
        parsed = json.loads(raw_body)
        return StepResult(success=True, output={"data": {"parsed": parsed}})
    except json.JSONDecodeError:
        return StepResult(success=False, error_message="Failed to parse JSON")

def register_http_steps(registry):
    """Registers the mock HTTP module's steps with the workflow engine."""
    registry.register("http.get", http_get)
    registry.register("json.parse", json_parse)
