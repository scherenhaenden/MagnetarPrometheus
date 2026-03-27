import json
import threading
import urllib.request
import urllib.error
import time
from http.server import HTTPServer
from unittest.mock import patch, MagicMock

import pytest

from magnetar_prometheus.api.server import MagnetarAPIHandler, run_server


class TestAPIHandler:

    @pytest.fixture(scope="class")
    def server(self):
        """Starts the server in a background thread for tests."""
        # Find a free port by binding to 0
        httpd = HTTPServer(('localhost', 0), MagnetarAPIHandler)
        port = httpd.server_port

        thread = threading.Thread(target=httpd.serve_forever)
        thread.daemon = True
        thread.start()

        # Give the server a moment to start
        time.sleep(0.1)

        yield f"http://localhost:{port}"

        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=1)

    def test_health_endpoint(self, server):
        url = f"{server}/health"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            data = json.loads(response.read().decode('utf-8'))
            assert data == {"status": "ok"}

    def test_not_found_get(self, server):
        url = f"{server}/unknown"
        req = urllib.request.Request(url, method="GET")
        try:
            urllib.request.urlopen(req)
            assert False, "Should have raised HTTPError 404"
        except urllib.error.HTTPError as e:
            assert e.code == 404
            data = json.loads(e.read().decode('utf-8'))
            assert data == {"error": "Not Found"}

    def test_run_example_endpoint(self, server):
        url = f"{server}/run-example"
        req = urllib.request.Request(url, method="POST")
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            data = json.loads(response.read().decode('utf-8'))
            assert data["status"] == "success"
            assert "result" in data

    def test_not_found_post(self, server):
        url = f"{server}/unknown-post"
        req = urllib.request.Request(url, method="POST")
        try:
            urllib.request.urlopen(req)
            assert False, "Should have raised HTTPError 404"
        except urllib.error.HTTPError as e:
            assert e.code == 404
            data = json.loads(e.read().decode('utf-8'))
            assert data == {"error": "Not Found"}

    @patch("magnetar_prometheus.api.server.Engine.run")
    def test_run_example_internal_error(self, mock_engine_run, server):
        # Mock the engine to throw an exception
        mock_engine_run.side_effect = Exception("Test engine error")

        url = f"{server}/run-example"
        req = urllib.request.Request(url, method="POST")
        try:
            urllib.request.urlopen(req)
            assert False, "Should have raised HTTPError 500"
        except urllib.error.HTTPError as e:
            assert e.code == 500
            data = json.loads(e.read().decode('utf-8'))
            assert data == {"error": "Test engine error"}

    @patch("magnetar_prometheus.api.server.Path.is_file")
    def test_run_example_missing_file(self, mock_is_file, server):
        # Mock the file check to return False
        mock_is_file.return_value = False

        url = f"{server}/run-example"
        req = urllib.request.Request(url, method="POST")
        try:
            urllib.request.urlopen(req)
            assert False, "Should have raised HTTPError 500"
        except urllib.error.HTTPError as e:
            assert e.code == 500
            data = json.loads(e.read().decode('utf-8'))
            assert data == {"error": "Example workflow file not found."}


def test_run_server_keyboard_interrupt():
    """Test that the server shuts down gracefully on KeyboardInterrupt."""
    with patch("magnetar_prometheus.api.server.HTTPServer") as mock_server_class:
        mock_server = MagicMock()
        mock_server.serve_forever.side_effect = KeyboardInterrupt
        mock_server_class.return_value = mock_server

        run_server(port=8080)

        mock_server_class.assert_called_once()
        mock_server.serve_forever.assert_called_once()
        mock_server.server_close.assert_called_once()
