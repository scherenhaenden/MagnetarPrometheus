import pytest
from unittest.mock import patch, MagicMock
from magnetar_prometheus.bootstrap import check_and_install_dependencies, BootstrapPolicy, BootstrapResult

def test_check_dependencies_all_present():
    deps = [{"module": "sys", "package": "sys"}]
    result = check_and_install_dependencies(deps)
    assert result.success is True
    assert not result.missing
    assert not result.installed
    assert not result.failed

def test_check_dependencies_missing_no_auto():
    deps = [{"module": "non_existent_module_xyz", "package": "pkg_xyz"}]
    policy = BootstrapPolicy(auto_install=False)
    result = check_and_install_dependencies(deps, policy=policy)
    assert result.success is False
    assert result.missing == deps
    assert not result.installed
    assert not result.failed

@patch("subprocess.check_call")
def test_check_dependencies_missing_auto_success(mock_call):
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
    import subprocess
    mock_call.side_effect = subprocess.CalledProcessError(1, "cmd")
    deps = [{"module": "non_existent_module_xyz", "package": "pkg_xyz"}]
    policy = BootstrapPolicy(auto_install=True)
    result = check_and_install_dependencies(deps, policy=policy)
    assert result.success is False
    assert result.missing == deps
    assert not result.installed
    assert result.failed == deps
