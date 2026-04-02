"""
Minimal local HTTP API surface for MagnetarPrometheus.

Why this file exists in this form:

- The repository currently has a working CLI-driven backend proof of concept, but PR #123
  adds the first long-running service boundary so the engine can be exercised through a
  simple HTTP interface instead of only one-shot command execution.
- This module intentionally uses Python's standard-library ``http.server`` machinery rather
  than introducing a heavier framework such as FastAPI or Flask. The goal of this slice is
  to prove the service boundary and its contracts, not to prematurely commit the project to
  a larger web stack.
- The built-in ``email_triage`` example workflow is used as the server's demonstration
  payload because it is already the canonical runnable workflow elsewhere in the repository.
  Reusing it keeps the API slice aligned with the CLI slice instead of creating a second,
  divergent example path that would have to be maintained separately.
- The server pre-builds and reuses the workflow runtime components rather than reconstructing
  them on every request. That is important even for a minimal server because repeated setup
  would hide avoidable latency in the request path and make the API performance profile look
  worse than necessary.
- Error handling is deliberately conservative. Operational details are logged for developers,
  while clients receive stable, limited error payloads rather than raw exception text that
  could expose internal implementation details.
"""

import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from magnetar_prometheus.core.context_manager import ContextManager
from magnetar_prometheus.core.engine import Engine
from magnetar_prometheus.core.executor_router import ExecutorRouter
from magnetar_prometheus.core.workflow_loader import WorkflowLoader
from magnetar_prometheus.executors.python_executor import PythonExecutor
from magnetar_prometheus.modules.example_registry import register_all_example_steps
from magnetar_prometheus.registry.step_registry import StepRegistry

logger = logging.getLogger(__name__)


def _resolve_example_workflow_path() -> Path:
    """Return the canonical path to the built-in example workflow.

    The API server exists to expose the already-supported example execution path over HTTP.
    Resolving the workflow location in one helper keeps that choice explicit and prevents the
    request handler from scattering filesystem assumptions across multiple branches.
    """
    return Path(__file__).parent.parent / "modules" / "email_module" / "email_triage.yaml"


def _build_example_runtime() -> tuple[Path, object, Engine]:
    """Assemble the reusable runtime objects for the ``/run-example`` endpoint.

    The runtime setup mirrors the CLI's core execution path on purpose: both surfaces should
    load the same workflow definition, register the same example steps, use the same executor
    routing, and execute through the same ``Engine`` abstraction. Building the objects here
    once lets the server reuse them across requests instead of paying setup cost repeatedly.
    """
    workflow_path = _resolve_example_workflow_path()
    if not workflow_path.is_file():
        raise FileNotFoundError("Example workflow file not found.")

    loader = WorkflowLoader()
    workflow = loader.load_workflow(str(workflow_path))

    registry = StepRegistry()
    register_all_example_steps(registry)

    executor = PythonExecutor(registry)
    router = ExecutorRouter()
    router.register("python", executor)

    context_manager = ContextManager()
    engine = Engine(router, context_manager)
    return workflow_path, workflow, engine


class MagnetarAPIServer(HTTPServer):
    """HTTP server that owns the reusable example-workflow runtime.

    The request handler should stay focused on HTTP translation concerns. This server class
    owns the long-lived runtime objects so they can be prepared once when the server starts
    and then reused safely for every ``/run-example`` request. If startup initialization
    fails, the server records a stable client-facing error message while retaining the full
    exception in logs for debugging.
    """

    def __init__(self, server_address, handler_class):
        """Create the HTTP server and eagerly configure the example runtime.

        Startup-time initialization keeps the expensive workflow-loading and engine-assembly
        work out of the hot request path. It also means configuration problems surface as a
        server-state problem instead of being rediscovered on every request.
        """
        super().__init__(server_address, handler_class)
        self.example_workflow_path = None
        self.example_workflow = None
        self.engine = None
        self.runtime_error_message = None
        self._configure_example_runtime()

    def _configure_example_runtime(self) -> None:
        """Prepare the reusable runtime objects or capture a stable startup failure.

        Missing example assets are returned to clients with a specific message because the
        issue is operational and predictable. Unexpected initialization failures are logged
        in full but reduced to a generic client response to avoid leaking internals.
        """
        try:
            workflow_path, workflow, engine = _build_example_runtime()
            self.example_workflow_path = workflow_path
            self.example_workflow = workflow
            self.engine = engine
            self.runtime_error_message = None
        except FileNotFoundError as exc:
            self.runtime_error_message = str(exc)
            logger.warning(
                "Magnetar API example runtime is unavailable because the workflow file is missing: %s",
                exc,
            )
        except Exception:
            self.runtime_error_message = "Internal server error."
            logger.exception("Failed to initialize the reusable example runtime for the API server.")


class MagnetarAPIHandler(BaseHTTPRequestHandler):
    """Translate HTTP requests into minimal workflow-engine interactions.

    The handler intentionally exposes only two endpoints in this product slice:
    - ``GET /health`` for lightweight process liveness checks
    - ``POST /run-example`` for exercising the existing email-triage workflow over HTTP

    The class assumes it is attached to ``MagnetarAPIServer``, which supplies the reusable
    engine/workflow objects needed by the ``/run-example`` path.
    """

    def log_message(self, format: str, *args) -> None:
        """Route the base handler's access logs through the standard logging system.

        ``BaseHTTPRequestHandler`` writes directly to stderr by default. Using the logging
        module instead gives the repository one consistent path for API observability.
        """
        logger.info("API request: %s - %s", self.address_string(), format % args)

    def _send_json_response(self, status_code: int, payload: dict) -> None:
        """Serialize and send a JSON response payload.

        Keeping response construction in one helper ensures both the health and workflow
        endpoints emit the same content type and encoding behavior.
        """
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_GET(self) -> None:
        """Handle the server's read-only endpoints.

        This slice intentionally keeps GET support minimal. ``/health`` exists so operators
        and tests can verify that the process is reachable without invoking workflow logic.
        """
        if self.path == "/health":
            self._send_json_response(200, {"status": "ok"})
        else:
            self._send_json_response(404, {"error": "Not Found"})

    def do_POST(self) -> None:
        """Handle write-style endpoints for the minimal API slice.

        ``/run-example`` is the first service-style execution path in the repository. The
        handler delegates to the reusable engine stack prepared by ``MagnetarAPIServer`` so
        request-time work is limited to execution and response serialization.
        """
        if self.path != "/run-example":
            self._send_json_response(404, {"error": "Not Found"})
            return

        if self.server.runtime_error_message is not None:
            # If startup could not prepare the reusable runtime, there is no safe request-time
            # recovery path here. Return the stable captured message instead of retrying the
            # full initialization sequence on every request.
            self._send_json_response(500, {"error": self.server.runtime_error_message})
            return

        try:
            result_context = self.server.engine.run(self.server.example_workflow)
            self._send_json_response(200, {"status": "success", "result": result_context})
        except Exception:
            logger.exception("Unexpected error while executing the /run-example workflow.")
            self._send_json_response(500, {"error": "Internal server error."})


def run_server(port: int = 8000, host: str = "127.0.0.1") -> None:
    """Start the minimal local MagnetarPrometheus API server.

    Why the default host is ``127.0.0.1`` and not ``""`` (all interfaces):

    - The unauthenticated ``/run-example`` endpoint must not be exposed on every network
      interface by default. Binding to the loopback address keeps the server genuinely
      local unless the caller explicitly opts into a broader binding by passing a different
      ``host`` value. This makes broader exposure an intentional operator decision rather
      than the inadvertent default.
    - The ``host`` parameter is therefore the supported escape hatch for cases where the
      caller genuinely wants to bind on all interfaces (e.g., ``host="0.0.0.0"`` in a
      controlled containerised environment). The decision stays explicit at the call site
      instead of being buried in module-level logic.
    - The log line includes both ``host`` and ``port`` so operators can verify the actual
      binding at a glance rather than having to infer it from port alone.
    - Shutdown handling is explicit so ``Ctrl+C`` releases the socket cleanly and the test
      suite can assert the server lifecycle behavior without leaking OS resources.

    Args:
        port: TCP port to listen on.  Defaults to ``8000``.
        host: Network interface to bind to.  Defaults to ``"127.0.0.1"`` (loopback only).
              Pass ``"0.0.0.0"`` to bind on all interfaces.
    """
    # Build the (host, port) tuple that Python's HTTPServer expects.  Using the loopback
    # address by default keeps the unauthenticated endpoint off the network without any
    # operator action.
    server_address = (host, port)
    httpd = MagnetarAPIServer(server_address, MagnetarAPIHandler)
    # Log the full address so the operator can confirm the binding at a glance.
    logger.info("Starting Magnetar API on %s:%s", host, port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received; shutting down Magnetar API.")
    finally:
        httpd.server_close()
        logger.info("Magnetar API stopped.")
