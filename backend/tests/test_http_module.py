"""Tests for the mock HTTP workflow module."""
import json

from magnetar_prometheus.modules.http_module.steps import http_get, json_parse, register_http_steps
from magnetar_prometheus.registry.step_registry import StepRegistry


def test_http_get():
    """Test the http_get step."""
    result = http_get({}, {"url": "https://api.test.com"})
    assert result.success is True
    assert result.output["data"]["http_status"] == 200
    assert json.loads(result.output["data"]["raw_body"]) == {"url": "https://api.test.com", "valid": True}

    result = http_get({}, {})
    assert result.success is True
    assert result.output["data"]["http_status"] == 200
    assert json.loads(result.output["data"]["raw_body"]) == {"url": "unknown", "valid": True}


def test_http_get_escapes_special_characters_in_url_and_preserves_context_data():
    """Test the http_get step serializes safely and keeps existing data fields."""
    result = http_get({"data": {"workflow_id": "http-demo"}}, {"url": 'https://api.test.com?q="quoted"'})
    assert result.success is True
    assert result.output["data"]["workflow_id"] == "http-demo"
    assert json.loads(result.output["data"]["raw_body"]) == {
        "url": 'https://api.test.com?q="quoted"',
        "valid": True,
    }

def test_json_parse():
    """Test the json_parse step."""
    result = json_parse({"data": {"raw_body": '{"key": "value"}'}}, {})
    assert result.success is True
    assert result.output["data"]["parsed"]["key"] == "value"

    result = json_parse({"data": {"raw_body": 'invalid'}}, {})
    assert result.success is False
    assert result.error_message == "Failed to parse JSON"

    result = json_parse({}, {})
    assert result.success is True
    assert result.output["data"]["parsed"] == {}


def test_json_parse_preserves_existing_context_data():
    """Test the json_parse step extends existing context data instead of overwriting it."""
    result = json_parse({"data": {"raw_body": '{"key": "value"}', "http_status": 200}}, {})
    assert result.success is True
    assert result.output["data"]["http_status"] == 200
    assert result.output["data"]["parsed"] == {"key": "value"}


def test_json_parse_handles_non_mapping_context_data():
    """Test the json_parse step treats invalid context data as empty."""
    result = json_parse({"data": []}, {})
    assert result.success is True
    assert result.output["data"]["parsed"] == {}


def test_register_http_steps():
    """Test registration of http steps."""
    registry = StepRegistry()
    register_http_steps(registry)
    assert callable(registry.get_handler("http.get"))
    assert callable(registry.get_handler("json.parse"))
