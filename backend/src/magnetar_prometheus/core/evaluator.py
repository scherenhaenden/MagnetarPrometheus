"""
Condition evaluator for MagnetarPrometheus workflow branching.

:class:`ConditionEvaluator` inspects string expressions produced by workflow
YAML definitions and resolves them against the live run context without
resorting to ``eval()``.
"""

from typing import Dict, Any, Optional

class ConditionEvaluator:
    """
    Evaluates conditional expressions safely without using eval().
    """

    def evaluate(self, expression: str, context: Dict[str, Any]) -> bool:
        """Evaluate a simple equality expression against the run context.

        Supports the form ``<context_path> == '<string_literal>'``.  Returns
        ``False`` for any expression that does not match a supported pattern or
        whose left-hand-side path cannot be resolved.

        Args:
            expression: The condition string from the workflow definition.
            context: The current run context dictionary.

        Returns:
            ``True`` when the expression resolves to a truthy equality match,
            ``False`` otherwise.
        """
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
        """Extracts the string value from quotes.
        
        This function checks if the provided string `value` is enclosed in single or
        double quotes. If it is, the function returns the substring without the
        surrounding quotes. If the string is not properly quoted, it returns None.
        """
        if value.startswith("'") and value.endswith("'"):
            return value[1:-1]
        elif value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        return None

    def _resolve_context_path(self, path: str, context: Dict[str, Any]) -> Any:
        # minimal safe evaluator for the PoC
        """Resolve the context path to retrieve a value from the context.
        
        This function evaluates a given path string to extract a key for accessing a
        value from the 'context' dictionary. It specifically handles paths that
        reference the 'ai' key in various formats, ensuring safe evaluation by checking
        the structure of the path string before attempting to retrieve the
        corresponding value.
        
        Args:
            path (str): The path string used to locate the value in the context.
            context (Dict[str, Any]): The dictionary containing context values.
        """
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
