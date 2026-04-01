"""Integration-style tests for the minimal local API server.

Why this file exists in this form:

- The API server is intentionally lightweight and standard-library based, so the most useful
  tests exercise it through real HTTP requests instead of only mocking the handler methods.
- The fixture spins up a live local server because that is the clearest way to verify the
  health endpoint, the example-workflow execution endpoint, the not-found behavior, and the
  shutdown lifecycle in one place.
- These tests also protect the branch's main user-visible addition: the project now exposes
  a minimal long-running HTTP boundary in addition to the one-shot CLI execution path.
"""

import json
import threading
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

import pytest

from magnetar_prometheus.api.server import (
    MagnetarAPIHandler,
    MagnetarAPIServer,
    _build_example_runtime,
    run_server,
)


@contextmanager
def serve_temporarily(httpd: MagnetarAPIServer):
    """Run a prepared HTTP server in a background thread for the duration of a test.

    The helper centralizes the thread lifecycle so both the shared fixture and the one-off
    failure-path tests can start and stop a real server consistently.
    """
    port = httpd.server_port
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

    # Give the background thread a brief moment to begin accepting connections before the
    # test issues its first request. This keeps the HTTP assertions focused on server logic
    # instead of racing the thread scheduler.
    time.sleep(0.1)

    try:
        yield f"http://localhost:{port}"
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=1)


class TestAPIHandler:
    """Exercise the minimal API server through real HTTP requests."""

    @pytest.fixture(scope="class")
    def server(self):
        """Start the standard API server once for the class's happy-path checks.

        The server binds to port ``0`` so the operating system selects a free ephemeral port,
        which prevents collisions with other local services or parallel test runs.
        """
        httpd = MagnetarAPIServer(("localhost", 0), MagnetarAPIHandler)
        with serve_temporarily(httpd) as base_url:
            yield base_url

    def test_health_endpoint(self, server):
        """Verify that ``GET /health`` returns the server liveness payload."""
        url = f"{server}/health"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            data = json.loads(response.read().decode("utf-8"))
            assert data == {"status": "ok"}

    def test_not_found_get(self, server):
        """Verify that unknown GET paths return the canonical 404 JSON error."""
        url = f"{server}/unknown"
        req = urllib.request.Request(url, method="GET")
        with pytest.raises(urllib.error.HTTPError) as exc_info:
            urllib.request.urlopen(req)

        assert exc_info.value.code == 404
        data = json.loads(exc_info.value.read().decode("utf-8"))
        assert data == {"error": "Not Found"}

    def test_run_example_endpoint(self, server):
        """Verify that ``POST /run-example`` executes the example workflow successfully."""
        url = f"{server}/run-example"
        req = urllib.request.Request(url, method="POST")
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            data = json.loads(response.read().decode("utf-8"))
            assert data["status"] == "success"
            assert "result" in data

    def test_not_found_post(self, server):
        """Verify that unknown POST paths return the canonical 404 JSON error."""
        url = f"{server}/unknown-post"
        req = urllib.request.Request(url, method="POST")
        with pytest.raises(urllib.error.HTTPError) as exc_info:
            urllib.request.urlopen(req)

        assert exc_info.value.code == 404
        data = json.loads(exc_info.value.read().decode("utf-8"))
        assert data == {"error": "Not Found"}

    @patch("magnetar_prometheus.api.server.Engine.run")
    def test_run_example_internal_error(self, mock_engine_run, server):
        """Verify that workflow execution failures are logged but not leaked to clients.

        The API should return a stable generic 500 payload for unexpected runtime failures
        rather than serializing the raw exception text into the response body.
        """
        mock_engine_run.side_effect = Exception("Test engine error")

        url = f"{server}/run-example"
        req = urllib.request.Request(url, method="POST")
        with pytest.raises(urllib.error.HTTPError) as exc_info:
            urllib.request.urlopen(req)

        assert exc_info.value.code == 500
        data = json.loads(exc_info.value.read().decode("utf-8"))
        assert data == {"error": "Internal server error."}

    def test_run_example_missing_file(self):
        """Verify that startup-time example-workflow failures surface as stable 500s.

        Because the server now prepares its reusable runtime once at startup, missing assets
        have to be simulated while the server object is being created rather than during the
        request itself.
        """
        with patch(
            "magnetar_prometheus.api.server._build_example_runtime",
            side_effect=FileNotFoundError("Example workflow file not found."),
        ):
            httpd = MagnetarAPIServer(("localhost", 0), MagnetarAPIHandler)

        with serve_temporarily(httpd) as server:
            url = f"{server}/run-example"
            req = urllib.request.Request(url, method="POST")
            with pytest.raises(urllib.error.HTTPError) as exc_info:
                urllib.request.urlopen(req)

            assert exc_info.value.code == 500
            data = json.loads(exc_info.value.read().decode("utf-8"))
            assert data == {"error": "Example workflow file not found."}


def test_build_example_runtime_rejects_missing_workflow_file():
    """Verify that runtime construction fails clearly when the example file is absent.

    This targets the explicit filesystem guard inside ``_build_example_runtime()`` so the
    startup path keeps a domain-specific missing-file failure instead of falling through to a
    less helpful downstream loader error.
    """
    with patch(
        "magnetar_prometheus.api.server.Path.is_file",
        return_value=False,
    ):
        with pytest.raises(FileNotFoundError, match="Example workflow file not found"):
            _build_example_runtime()


def test_api_server_records_generic_startup_failure_message():
    """Verify that unexpected startup failures become generic client-facing errors.

    The server should log the full initialization exception internally, but the public
    response state stored on the server object must stay generic to avoid leaking details
    through later HTTP responses.
    """
    with patch(
        "magnetar_prometheus.api.server._build_example_runtime",
        side_effect=RuntimeError("boom"),
    ):
        httpd = MagnetarAPIServer(("localhost", 0), MagnetarAPIHandler)

    try:
        assert httpd.runtime_error_message == "Internal server error."
        assert httpd.engine is None
        assert httpd.example_workflow is None
    finally:
        httpd.server_close()


def test_run_server_keyboard_interrupt():
    """Verify that ``run_server`` shuts down cleanly on ``KeyboardInterrupt``."""
    with patch("magnetar_prometheus.api.server.MagnetarAPIServer") as mock_server_class:
        mock_server = MagicMock()
        mock_server.serve_forever.side_effect = KeyboardInterrupt
        mock_server_class.return_value = mock_server

        run_server(port=8080)

        mock_server_class.assert_called_once()
        mock_server.serve_forever.assert_called_once()
        mock_server.server_close.assert_called_once()
