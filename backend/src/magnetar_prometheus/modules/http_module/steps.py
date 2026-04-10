"""Step handlers for the mock HTTP example workflow module.

Why this file exists in this form:
- This module demonstrates how an external system interaction might be modeled.
- The logic is entirely mocked to remain side-effect free and deterministic for tests.
"""

import json
from collections.abc import Mapping
from typing import Dict, Any
from magnetar_prometheus_sdk.models import StepResult


def _get_context_data(context: Dict[str, Any]) -> dict[str, Any]:
    """Return the current context `data` payload if it is mapping-like."""
    data = context.get("data")
    return dict(data) if isinstance(data, Mapping) else {}


def http_get(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Simulates an HTTP GET request to the configured URL."""
    url = config.get("url", "unknown")
    next_data = _get_context_data(context)
    next_data["http_status"] = 200
    next_data["raw_body"] = json.dumps({"url": url, "valid": True})
    return StepResult(success=True, output={"data": next_data})

def json_parse(context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
    """Simulates parsing the raw body string returned by the HTTP GET step."""
    next_data = _get_context_data(context)
    raw_body = next_data.get("raw_body", "{}")
    try:
        parsed = json.loads(raw_body)
        next_data["parsed"] = parsed
        return StepResult(success=True, output={"data": next_data})
    except json.JSONDecodeError:
        return StepResult(success=False, error_message="Failed to parse JSON")

def register_http_steps(registry):
    """Registers the mock HTTP module's steps with the workflow engine."""
    registry.register("http.get", http_get)
    registry.register("json.parse", json_parse)
