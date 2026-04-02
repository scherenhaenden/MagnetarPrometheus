"""
Documentation-contract tests for high-context operational files.

Why this file exists in this form:

- Docstring coverage alone is not enough to preserve the repository's documentation standard.
  A file can have 100 percent coverage and still lose the long-form rationale that tells the
  next agent why the code is shaped this way and which parts are policy rather than accident.
- The CLI/API loopback branch already demonstrated that failure mode: a cleanup pass shortened
  comments that the user explicitly wanted to stay heavy and explanatory. This file exists so
  that the same regression becomes test-visible instead of only review-visible.
- The assertions here are intentionally narrow. They do not try to judge all prose quality in
  the repository. They enforce a documentation contract only for the touched API/CLI surface
  where the policy rationale is important and easy to erode.
"""

from __future__ import annotations

import ast
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_PATH = REPO_ROOT / "backend" / "src" / "magnetar_prometheus" / "cli.py"
API_SERVER_PATH = REPO_ROOT / "backend" / "src" / "magnetar_prometheus" / "api" / "server.py"
CLI_TEST_PATH = REPO_ROOT / "backend" / "tests" / "test_cli.py"


def _read_module_docstring(path: Path) -> str:
    """Return the top-level module docstring for a Python file."""
    module = ast.parse(path.read_text(encoding="utf-8"))
    return ast.get_docstring(module) or ""


def _read_function_docstring(path: Path, function_name: str) -> str:
    """Return the docstring for a named top-level function."""
    module = ast.parse(path.read_text(encoding="utf-8"))
    for node in module.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return ast.get_docstring(node) or ""
    return ""


def test_cli_module_docstring_stays_high_context() -> None:
    """Ensure the CLI module keeps a long-form intent header."""
    docstring = _read_module_docstring(CLI_PATH)

    assert len([line for line in docstring.splitlines() if line.strip()]) >= 12
    assert "Why this file exists in this form:" in docstring
    assert "shortest executable path" in docstring
    assert "application bootstrap layer" in docstring


def test_api_server_module_docstring_stays_high_context() -> None:
    """Ensure the API server module keeps the long-form rationale for the local HTTP slice."""
    docstring = _read_module_docstring(API_SERVER_PATH)

    assert len([line for line in docstring.splitlines() if line.strip()]) >= 12
    assert "Why this file exists in this form:" in docstring
    assert "standard-library ``http.server`` machinery" in docstring
    assert "Error handling is deliberately conservative" in docstring


def test_run_server_docstring_preserves_binding_policy() -> None:
    """Ensure the bind-policy explanation remains explicit in ``run_server``."""
    docstring = _read_function_docstring(API_SERVER_PATH, "run_server")

    assert len([line for line in docstring.splitlines() if line.strip()]) >= 10
    assert "loopback interface" in docstring
    assert "operator" in docstring
    assert "security" in docstring or "policy" in docstring


def test_default_api_host_comment_preserves_policy_context() -> None:
    """Ensure the DEFAULT_API_HOST comment keeps the bind-policy rationale stable."""
    source_text = API_SERVER_PATH.read_text(encoding="utf-8")

    assert "DEFAULT_API_HOST" in source_text
    assert "Keep the loopback default in one constant" in source_text
    assert "unauthenticated `/run-example` endpoint stays local by default" in source_text


def test_cli_api_mode_tests_keep_policy_explanation() -> None:
    """Ensure the CLI API-mode tests keep their long-form policy narrative."""
    api_default_doc = _read_function_docstring(CLI_TEST_PATH, "test_cli_api_flag")
    api_custom_host_doc = _read_function_docstring(
        CLI_TEST_PATH, "test_cli_api_flag_custom_host"
    )

    assert "This test deliberately protects multiple policy boundaries at once" in api_default_doc
    assert "safe loopback default" in api_default_doc
    assert "users are allowed to opt into a broader bind" in api_custom_host_doc
