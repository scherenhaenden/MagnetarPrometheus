from typing import Dict, Any, Optional

class ConditionEvaluator:
    """
    Evaluates conditional expressions safely without using eval().
    """

    def evaluate(self, expression: str, context: Dict[str, Any]) -> bool:
        expr = expression.strip()

        if "==" in expr:
            left, right = [part.strip() for part in expr.split("==", 1)]

            right_val = self._extract_string_value(right)
            if right_val is None:
                return False

            left_val = self._resolve_context_path(left, context)

            return left_val == right_val

        return False

    def _extract_string_value(self, value: str) -> Optional[str]:
        if value.startswith("'") and value.endswith("'"):
            return value[1:-1]
        elif value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        return None

    def _resolve_context_path(self, path: str, context: Dict[str, Any]) -> Any:
        # minimal safe evaluator for the PoC
        if path.startswith("context['ai'].get('") and path.endswith("')"):
            key = path.replace("context['ai'].get('", "").replace("')", "")
            return context.get("ai", {}).get(key)
        elif path.startswith('context["ai"].get("') and path.endswith('")'):
            key = path.replace('context["ai"].get("', "").replace('")', "")
            return context.get("ai", {}).get(key)
        elif path.startswith("context['ai']['") and path.endswith("']"):
            key = path.replace("context['ai']['", "").replace("']", "")
            return context.get("ai", {}).get(key)
        elif path.startswith('context["ai"]["') and path.endswith('"]'):
            key = path.replace('context["ai"]["', "").replace('"]', "")
            return context.get("ai", {}).get(key)

        return None
