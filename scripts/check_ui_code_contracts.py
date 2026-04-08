#!/usr/bin/env python3
"""
UI source contract guard.

This script enforces the minimum conventions requested by project governance for
the Angular TypeScript slice:
1. every app `.ts` file starts with a file-level intent comment (`/** ... */`)
2. class members (properties/methods) use explicit access modifiers
3. declared methods/functions include an explicit return type annotation
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_APP = ROOT / "ui" / "src" / "app"


HEADER_RE = re.compile(r"^\s*/\*\*")
CLASS_RE = re.compile(r"^\s*export\s+(?:abstract\s+)?class\s+\w+")
ACCESS_MODIFIER_RE = re.compile(r"^(public|private|protected)\b")
EXPORTED_FUNCTION_RE = re.compile(r"^export\s+function\b")
EXPORTED_ARROW_RE = re.compile(r"^export\s+const\s+\w+\s*=")
MEMBER_DECLARATION_RE = re.compile(
    r"^(?:(?:public|private|protected)\s+)?"
    r"(?:(?:readonly|static|abstract|override)\s+)*"
    r"(?:get|set\s+)?[A-Za-z_]\w*\s*(?:[(:=]|!\s*:)"
)
METHOD_DECLARATION_RE = re.compile(
    r"^(?:(?:public|private|protected)\s+)"
    r"(?:(?:readonly|static|abstract|override)\s+)*"
    r"(?:async\s+)?(?:get\s+|set\s+)?[A-Za-z_]\w*\s*\("
)
DECORATOR_PREFIX_RE = re.compile(r"^(?:@\w+(?:\([^)]*\))?\s*)+")
MODIFIERLESS_MEMBER_RE = re.compile(
    r"^(?:(?:readonly|static|abstract|override)\s+)*"
    r"(?:async\s+)?(?:get\s+|set\s+)?[A-Za-z_]\w*\s*(?:[(:=]|!\s*:)"
)
RETURN_TYPE_RE = re.compile(r"\)\s*:\s*[^=]+(?:=>|\{)")


def starts_with_intent_header(text: str) -> bool:
    """Return True when the first non-empty line begins with a file intent header."""

    for line in text.splitlines():
        if not line.strip():
            continue
        return bool(HEADER_RE.match(line))
    return False


def strip_strings_and_comments(text: str) -> str:
    """Remove comments and string contents while preserving line structure."""

    result: list[str] = []
    state = "code"
    template_expression_depth = 0
    index = 0
    while index < len(text):
        char = text[index]
        nxt = text[index + 1] if index + 1 < len(text) else ""

        if state == "line_comment":
            if char == "\n":
                state = "code"
                result.append("\n")
            else:
                result.append(" ")
            index += 1
            continue

        if state == "block_comment":
            if char == "*" and nxt == "/":
                result.extend("  ")
                index += 2
                state = "code"
            else:
                result.append("\n" if char == "\n" else " ")
                index += 1
            continue

        if state == "single_quote":
            if char == "\\":
                result.extend("  ")
                index += 2
            elif char == "'":
                result.append(" ")
                index += 1
                state = "code"
            else:
                result.append("\n" if char == "\n" else " ")
                index += 1
            continue

        if state == "double_quote":
            if char == "\\":
                result.extend("  ")
                index += 2
            elif char == '"':
                result.append(" ")
                index += 1
                state = "code"
            else:
                result.append("\n" if char == "\n" else " ")
                index += 1
            continue

        if state == "template":
            if char == "\\":
                result.extend("  ")
                index += 2
            elif char == "`":
                result.append(" ")
                index += 1
                state = "code"
            elif char == "$" and nxt == "{":
                result.extend("${")
                index += 2
                state = "code"
                template_expression_depth = 1
            else:
                result.append("\n" if char == "\n" else " ")
                index += 1
            continue

        if char == "/" and nxt == "/":
            result.extend("  ")
            index += 2
            state = "line_comment"
            continue

        if char == "/" and nxt == "*":
            result.extend("  ")
            index += 2
            state = "block_comment"
            continue

        if char == "'":
            result.append(" ")
            index += 1
            state = "single_quote"
            continue

        if char == '"':
            result.append(" ")
            index += 1
            state = "double_quote"
            continue

        if char == "`":
            result.append(" ")
            index += 1
            state = "template"
            continue

        result.append(char)
        if template_expression_depth:
            if char == "{":
                template_expression_depth += 1
            elif char == "}":
                template_expression_depth -= 1
                if template_expression_depth == 0:
                    state = "template"
        index += 1

    return "".join(result)


def strip_leading_decorators(statement: str) -> str:
    """Remove one-line decorators before analyzing a class member declaration."""

    return DECORATOR_PREFIX_RE.sub("", statement).strip()


def has_explicit_return_type(statement: str) -> bool:
    """Return True when a method/function signature declares a return type."""

    compact = " ".join(statement.split())
    if "constructor(" in compact:
        return True
    return bool(RETURN_TYPE_RE.search(compact))


def statement_needs_access_modifier(statement: str) -> bool:
    """Return True when a top-level class statement declares a member."""

    compact = strip_leading_decorators(" ".join(statement.split()))
    if not compact or compact.startswith("constructor("):
        return False
    return bool(MODIFIERLESS_MEMBER_RE.match(compact))


def statement_is_method(statement: str) -> bool:
    """Return True when a top-level class statement declares a method body."""

    compact = strip_leading_decorators(" ".join(statement.split()))
    if not compact or compact.startswith("constructor("):
        return False
    return bool(METHOD_DECLARATION_RE.match(compact)) and compact.endswith("{")


def statement_is_exported_function(statement: str) -> bool:
    """Return True when a top-level statement is an exported function declaration."""

    compact = " ".join(statement.split())
    return (
        (bool(EXPORTED_FUNCTION_RE.match(compact)) and compact.endswith("{"))
        or (bool(EXPORTED_ARROW_RE.match(compact)) and "=>" in compact)
    )


def process_class_statement(statement: str, rel: Path, lineno: int, errors: list[str]) -> None:
    """Validate one class-level statement after the full declaration is assembled."""

    compact = strip_leading_decorators(" ".join(statement.split()))
    if not compact or compact == "}":
        return
    if statement_needs_access_modifier(compact) and not ACCESS_MODIFIER_RE.match(compact):
        errors.append(f"{rel}:{lineno} class member missing access modifier")
    if statement_is_method(compact) and not has_explicit_return_type(compact):
        errors.append(f"{rel}:{lineno} method missing explicit return type")


def process_top_level_statement(statement: str, rel: Path, lineno: int, errors: list[str]) -> None:
    """Validate one top-level exported function statement."""

    compact = " ".join(statement.split())
    if statement_is_exported_function(compact) and not has_explicit_return_type(compact):
        errors.append(f"{rel}:{lineno} function missing explicit return type")


def is_statement_complete(statement: str) -> bool:
    """Return True once a buffered declaration has enough structure to validate."""

    compact = " ".join(statement.split())
    if not compact:
        return False
    paren_balance = compact.count("(") - compact.count(")")
    bracket_balance = compact.count("[") - compact.count("]")
    brace_balance = compact.count("{") - compact.count("}")
    if compact.endswith("{"):
        return paren_balance == 0 and bracket_balance == 0
    return compact.endswith(";") and paren_balance == 0 and bracket_balance == 0 and brace_balance == 0


def analyze_file(ts_file: Path) -> list[str]:
    """Validate one TypeScript file and return any contract violations."""

    text = ts_file.read_text(encoding="utf-8")
    rel = ts_file.relative_to(ROOT)
    errors: list[str] = []
    if not starts_with_intent_header(text):
        errors.append(f"{rel}: missing top-of-file /** intent header")

    sanitized_lines = strip_strings_and_comments(text).splitlines()
    brace_depth = 0
    class_depth: int | None = None
    pending_class_open = False
    class_statement: list[str] = []
    class_statement_start: int | None = None
    top_level_statement: list[str] = []
    top_level_statement_start: int | None = None

    for lineno, line in enumerate(sanitized_lines, start=1):
        stripped = line.strip()

        if class_depth is None and CLASS_RE.match(line):
            pending_class_open = True

        if class_depth is not None and brace_depth == class_depth and stripped not in {"", "}"}:
            if class_statement_start is None:
                class_statement_start = lineno
            class_statement.append(stripped)
            if is_statement_complete(" ".join(class_statement)):
                process_class_statement(" ".join(class_statement), rel, class_statement_start, errors)
                class_statement = []
                class_statement_start = None

        if class_depth is None and brace_depth == 0 and stripped:
            if top_level_statement or EXPORTED_FUNCTION_RE.match(stripped) or EXPORTED_ARROW_RE.match(stripped):
                if top_level_statement_start is None:
                    top_level_statement_start = lineno
                top_level_statement.append(stripped)
                if is_statement_complete(" ".join(top_level_statement)):
                    process_top_level_statement(" ".join(top_level_statement), rel, top_level_statement_start, errors)
                    top_level_statement = []
                    top_level_statement_start = None

        opens = line.count("{")
        closes = line.count("}")

        if pending_class_open and opens:
            class_depth = brace_depth + 1
            pending_class_open = False

        brace_depth += opens - closes

        if class_depth is not None and brace_depth < class_depth:
            class_depth = None
            class_statement = []
            class_statement_start = None

    return errors


def main() -> int:
    errors: list[str] = []
    for ts_file in sorted(UI_APP.rglob("*.ts")):
        errors.extend(analyze_file(ts_file))

    if errors:
        print("UI code contract check failed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print("UI code contract check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
