"""Tests for the mock HTTP workflow module."""
from magnetar_prometheus.modules.http_module.steps import http_get, json_parse, register_http_steps
from magnetar_prometheus.registry.step_registry import StepRegistry

def test_http_get():
    """Test the http_get step."""
    result = http_get({}, {"url": "https://api.test.com"})
    assert result.success is True
    assert result.output["data"]["http_status"] == 200
    assert "https://api.test.com" in result.output["data"]["raw_body"]

    result = http_get({}, {})
    assert result.success is True
    assert result.output["data"]["http_status"] == 200
    assert "unknown" in result.output["data"]["raw_body"]

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

def test_register_http_steps():
    """Test registration of http steps."""
    registry = StepRegistry()
    register_http_steps(registry)
    assert callable(registry.get_handler("http.get"))
    assert callable(registry.get_handler("json.parse"))
