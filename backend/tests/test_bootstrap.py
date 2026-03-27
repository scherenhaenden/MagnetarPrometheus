import pytest
from unittest.mock import patch, MagicMock
from magnetar_prometheus.bootstrap import check_and_install_dependencies, bootstrap_runtime

def test_check_dependencies_all_present():
    deps = [{"module": "sys", "package": "sys"}]
    assert check_and_install_dependencies(deps) is True

def test_check_dependencies_missing_no_auto():
    deps = [{"module": "non_existent_module_xyz", "package": "pkg_xyz"}]
    assert check_and_install_dependencies(deps, auto_install=False) is False

@patch("subprocess.check_call")
def test_check_dependencies_missing_auto_success(mock_call):
    deps = [{"module": "non_existent_module_xyz", "package": "pkg_xyz"}]
    assert check_and_install_dependencies(deps, auto_install=True) is True
    mock_call.assert_called_once()

@patch("subprocess.check_call")
def test_check_dependencies_missing_auto_fail(mock_call):
    import subprocess
    mock_call.side_effect = subprocess.CalledProcessError(1, "cmd")
    deps = [{"module": "non_existent_module_xyz", "package": "pkg_xyz"}]
    assert check_and_install_dependencies(deps, auto_install=True) is False

@patch("magnetar_prometheus.bootstrap.check_and_install_dependencies")
def test_bootstrap_runtime(mock_check):
    mock_check.return_value = True
    assert bootstrap_runtime(auto_install=True) is True
    mock_check.assert_called_once()
