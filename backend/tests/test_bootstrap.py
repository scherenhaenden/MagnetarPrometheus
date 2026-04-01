"""
Tests for the bootstrap module.

Each test targets a distinct behaviour of ``check_and_install_dependencies``
or ``bootstrap_runtime`` so that failures are easy to diagnose in CI.

Coverage requirements (enforced by pytest-cov --cov-fail-under=100):
- All branches in the detection phase must be exercised.
- All branches in the installation phase must be exercised, including the
  newly-fixed path where multiple dependencies fail without an early return.
"""

import subprocess
from unittest.mock import call, patch

import pytest

from magnetar_prometheus.bootstrap import (
    BootstrapPolicy,
    BootstrapResult,
    bootstrap_runtime,
    check_and_install_dependencies,
)


def test_check_dependencies_all_present():
    """All requested modules are importable — no missing, installed, or failed entries expected.

    Uses ``sys`` which is guaranteed to be present in any Python interpreter,
    so no pip subprocess is ever invoked.
    """
    deps = [{"module": "sys", "package": "sys"}]
    result = check_and_install_dependencies(deps)
    assert result.success is True
    assert not result.missing
    assert not result.installed
    assert not result.failed


def test_check_dependencies_missing_no_auto():
    """A missing module with auto_install=False must be reported but NOT installed.

    The function must return immediately after detection when the policy
    prohibits automatic installation, leaving ``installed`` and ``failed`` empty.
    """
    deps = [{"module": "non_existent_module_xyz", "package": "pkg_xyz"}]
    policy = BootstrapPolicy(auto_install=False)
    result = check_and_install_dependencies(deps, policy=policy)
    assert result.success is False
    assert result.missing == deps
    assert not result.installed
    assert not result.failed


@patch("subprocess.check_call")
def test_check_dependencies_missing_auto_success(mock_call):
    """A single missing dependency that pip installs successfully.

    After a successful ``pip install`` the dependency must appear in
    ``result.installed`` and ``result.success`` must be True.
    """
    deps = [{"module": "non_existent_module_xyz", "package": "pkg_xyz"}]
    policy = BootstrapPolicy(auto_install=True)
    result = check_and_install_dependencies(deps, policy=policy)
    assert result.success is True
    assert result.missing == deps
    assert result.installed == deps
    assert not result.failed
    mock_call.assert_called_once()


@patch("subprocess.check_call")
def test_check_dependencies_missing_auto_fail(mock_call):
    """A single missing dependency whose pip installation fails.

    ``result.failed`` must contain the dependency and ``success`` must be False.
    """
    mock_call.side_effect = subprocess.CalledProcessError(1, "cmd")
    deps = [{"module": "non_existent_module_xyz", "package": "pkg_xyz"}]
    policy = BootstrapPolicy(auto_install=True)
    result = check_and_install_dependencies(deps, policy=policy)
    assert result.success is False
    assert result.missing == deps
    assert not result.installed
    assert result.failed == deps


@patch("subprocess.check_call")
def test_check_dependencies_multiple_failures_all_collected(mock_call):
    """All failing dependencies are collected when multiple pip installs fail.

    This test is the direct regression guard for the bug described in GitHub
    issue #94: the installation loop previously returned on the first failure,
    meaning only the first broken package was reported.  After the fix, every
    dependency that pip cannot install must appear in ``result.failed`` and
    ``result.success`` must be False.

    The mock raises ``CalledProcessError`` for every call, simulating an
    environment where pip is completely unable to reach a package index.
    """
    mock_call.side_effect = subprocess.CalledProcessError(1, "cmd")

    # Three distinct missing packages — all expected to fail.
    dep_a = {"module": "non_existent_module_aaa", "package": "pkg_aaa"}
    dep_b = {"module": "non_existent_module_bbb", "package": "pkg_bbb"}
    dep_c = {"module": "non_existent_module_ccc", "package": "pkg_ccc"}
    deps = [dep_a, dep_b, dep_c]

    policy = BootstrapPolicy(auto_install=True)
    result = check_and_install_dependencies(deps, policy=policy)

    # The loop must NOT have stopped at dep_a — all three must be in ``failed``.
    assert result.success is False
    assert result.missing == deps
    assert not result.installed
    assert result.failed == deps

    # Verify that pip was called exactly once per dependency, proving the loop
    # iterated over every entry instead of stopping at the first exception.
    assert mock_call.call_count == 3
    expected_calls = [
        call([__import__("sys").executable, "-m", "pip", "install", dep["package"]])
        for dep in deps
    ]
    mock_call.assert_has_calls(expected_calls, any_order=False)


@patch("magnetar_prometheus.bootstrap.check_and_install_dependencies")
def test_bootstrap_runtime_success(mock_check):
    """bootstrap_runtime returns True when check_and_install_dependencies reports success."""
    mock_check.return_value = BootstrapResult(success=True)
    assert bootstrap_runtime(auto_install=True) is True
    mock_check.assert_called_once()


@patch("magnetar_prometheus.bootstrap.check_and_install_dependencies")
def test_bootstrap_runtime_success_with_installed_printed(mock_check, capsys):
    """bootstrap_runtime prints a confirmation message when dependencies were installed.

    This covers the ``if result.installed`` branch inside the ``if result.success``
    block of ``bootstrap_runtime``.  The print should only happen when some packages
    were newly installed, not merely when all packages were already present.
    """
    installed_dep = {"module": "non_existent_module_xyz", "package": "pkg_xyz"}
    mock_check.return_value = BootstrapResult(success=True, installed=[installed_dep])
    assert bootstrap_runtime(auto_install=True) is True
    captured = capsys.readouterr()
    assert "Successfully installed missing dependencies." in captured.out


@patch("magnetar_prometheus.bootstrap.check_and_install_dependencies")
def test_bootstrap_runtime_failure_no_auto(mock_check, capsys):
    """bootstrap_runtime prints a manual-install message when auto_install is False.

    This covers the ``if not policy.auto_install`` branch of ``bootstrap_runtime``.
    The output must list every missing package so the operator knows exactly
    what to install without having to inspect internal state.
    """
    missing_dep = {"module": "non_existent_module_xyz", "package": "pkg_xyz"}
    mock_check.return_value = BootstrapResult(success=False, missing=[missing_dep])
    assert bootstrap_runtime(auto_install=False) is False
    captured = capsys.readouterr()
    assert "Missing required dependencies:" in captured.out
    assert "pkg_xyz" in captured.out
    assert "Please install them manually using pip." in captured.out


@patch("magnetar_prometheus.bootstrap.check_and_install_dependencies")
def test_bootstrap_runtime_failure_auto_install(mock_check, capsys):
    """bootstrap_runtime prints a failure message for every failed package when auto_install is True.

    This covers the ``else`` branch of the ``if not policy.auto_install`` block in
    ``bootstrap_runtime``.  The message must be printed for *each* failed dependency,
    which is the user-visible complement to the fix in ``check_and_install_dependencies``
    that now collects all failures rather than stopping at the first one.
    """
    failed_dep = {"module": "non_existent_module_xyz", "package": "pkg_xyz"}
    mock_check.return_value = BootstrapResult(success=False, failed=[failed_dep])
    assert bootstrap_runtime(auto_install=True) is False
    captured = capsys.readouterr()
    assert "Failed to install pkg_xyz." in captured.out
