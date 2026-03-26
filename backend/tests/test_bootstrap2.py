import pytest
from unittest.mock import patch, MagicMock
from magnetar_prometheus.bootstrap import bootstrap_runtime, BootstrapResult, BootstrapPolicy

@patch("magnetar_prometheus.bootstrap.check_and_install_dependencies")
def test_bootstrap_runtime_success(mock_check):
    mock_check.return_value = BootstrapResult(success=True)
    assert bootstrap_runtime(auto_install=True) is True
    mock_check.assert_called_once()

@patch("magnetar_prometheus.bootstrap.check_and_install_dependencies")
def test_bootstrap_runtime_success_installed(mock_check):
    mock_check.return_value = BootstrapResult(success=True, installed=[{"module": "x", "package": "x"}])
    assert bootstrap_runtime(auto_install=True) is True
    mock_check.assert_called_once()

@patch("magnetar_prometheus.bootstrap.check_and_install_dependencies")
def test_bootstrap_runtime_fail_no_auto(mock_check):
    mock_check.return_value = BootstrapResult(success=False, missing=[{"module": "x", "package": "x"}])
    assert bootstrap_runtime(auto_install=False) is False
    mock_check.assert_called_once()

@patch("magnetar_prometheus.bootstrap.check_and_install_dependencies")
def test_bootstrap_runtime_fail_auto_install(mock_check):
    mock_check.return_value = BootstrapResult(success=False, missing=[{"module": "x", "package": "x"}], failed=[{"module": "x", "package": "x"}])
    assert bootstrap_runtime(auto_install=True) is False
    mock_check.assert_called_once()
