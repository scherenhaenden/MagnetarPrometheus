import pytest
from magnetar_prometheus.core.evaluator import ConditionEvaluator

@pytest.fixture
def evaluator():
    return ConditionEvaluator()

def test_evaluate_successful_matches(evaluator):
    ctx = {"ai": {"decision": "x", "other": "y"}}

    assert evaluator.evaluate('context["ai"]["decision"] == "x"', ctx) is True
    assert evaluator.evaluate("context['ai']['decision'] == 'x'", ctx) is True
    assert evaluator.evaluate('context["ai"].get("decision") == "x"', ctx) is True
    assert evaluator.evaluate("context['ai']['other'] == 'y'", ctx) is True

def test_evaluate_unsupported_conditions(evaluator):
    ctx = {"ai": {"decision": "x", "other": "y"}}

    assert evaluator.evaluate("context['ai']['other'] == 'z'", ctx) is False
    assert evaluator.evaluate("foo == 'bar'", ctx) is False
    assert evaluator.evaluate("context['ai']['other'] == y", ctx) is False
    assert evaluator.evaluate("context['ai']['other'] == ", ctx) is False
    assert evaluator.evaluate("not an equal equal statement", ctx) is False

def test_evaluate_missing_context_keys(evaluator):
    ctx = {"ai": {"decision": "x"}}

    assert evaluator.evaluate("context['ai']['other'] == 'y'", ctx) is False
    assert evaluator.evaluate("context['other_dict']['other'] == 'y'", ctx) is False
