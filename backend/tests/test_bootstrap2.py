import pytest
from unittest.mock import patch, MagicMock
from magnetar_prometheus.bootstrap import bootstrap_runtime

@patch("magnetar_prometheus.bootstrap.check_and_install_dependencies")
def test_bootstrap_runtime(mock_check):
    mock_check.return_value = True
    assert bootstrap_runtime(auto_install=True) is True
    mock_check.assert_called_once()
