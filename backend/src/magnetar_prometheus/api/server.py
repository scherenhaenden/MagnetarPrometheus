import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from magnetar_prometheus.core.workflow_loader import WorkflowLoader
from magnetar_prometheus.core.executor_router import ExecutorRouter
from magnetar_prometheus.core.context_manager import ContextManager
from magnetar_prometheus.core.engine import Engine
from magnetar_prometheus.registry.step_registry import StepRegistry
from magnetar_prometheus.executors.python_executor import PythonExecutor
from magnetar_prometheus.modules.email_module.steps import register_example_steps


class MagnetarAPIHandler(BaseHTTPRequestHandler):
    """
    A minimal HTTP handler for the MagnetarPrometheus API.
    Provides a simple surface to interact with the workflow engine over HTTP.

    This handler avoids introducing complex web frameworks (like FastAPI or Flask)
    at this early stage, keeping the runtime footprint small and focused on testing
    the core engine's integration as a service boundary.

    Endpoints:
    - GET /health: Returns a simple 200 OK status to verify the server is running.
    - POST /run-example: Loads the default email_triage example workflow, executes it
      using the core engine, and returns the resulting RunContext as a JSON response.
    """

    def _send_json_response(self, status_code: int, payload: dict):
        """
        Helper method to construct and send a standard JSON HTTP response.

        Args:
            status_code (int): The HTTP status code (e.g., 200 for success, 404 for not found).
            payload (dict): The dictionary containing the response data, which will be serialized to JSON.
        """
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode('utf-8'))

    def do_GET(self):
        """
        Handles incoming HTTP GET requests.

        Currently supports:
        - /health: A lightweight endpoint to confirm the server is responsive.

        Any other path will result in a 404 Not Found response.
        """
        if self.path == '/health':
            self._send_json_response(200, {"status": "ok"})
        else:
            self._send_json_response(404, {"error": "Not Found"})

    def do_POST(self):
        """
        Handles incoming HTTP POST requests.

        Currently supports:
        - /run-example: Executes the built-in email_triage workflow and returns its result.
          This demonstrates how the backend engine can be wrapped in an API surface
          and integrated with an external trigger, advancing the project past CLI-only execution.

        Any other path will result in a 404 Not Found response.
        """
        if self.path == '/run-example':
            try:
                # Resolve the default workflow path dynamically relative to the API server module
                default_workflow_path = (
                    Path(__file__).parent.parent / "modules" / "email_module" / "email_triage.yaml"
                )

                if not default_workflow_path.is_file():
                    self._send_json_response(500, {"error": "Example workflow file not found."})
                    return

                # Reusing core runtime assembly
                # This explicitly mimics the setup logic in `cli.py` to ensure consistent execution behavior.
                loader = WorkflowLoader()
                wf = loader.load_workflow(str(default_workflow_path))

                # Register the steps specifically required by the email triage example
                registry = StepRegistry()
                register_example_steps(registry)

                # Initialize the python executor and bind it to the step registry
                executor = PythonExecutor(registry)
                router = ExecutorRouter()
                router.register('python', executor)

                # Initialize context management and the main workflow engine
                cm = ContextManager()
                engine = Engine(router, cm)

                # Execute the workflow. This call blocks until the workflow completes.
                result_context = engine.run(wf)

                # Send back the serialized result context to the caller
                self._send_json_response(200, {
                    "status": "success",
                    "result": result_context
                })
            except Exception as e:
                # Catch any unexpected runtime errors during workflow execution and return a 500
                self._send_json_response(500, {"error": str(e)})
        else:
            self._send_json_response(404, {"error": "Not Found"})


def run_server(port: int = 8000):
    """
    Starts the minimal local API server.

    Binds the MagnetarAPIHandler to the specified port (default 8000) on all available interfaces ('').
    The server runs in an infinite loop until interrupted (e.g., via Ctrl+C).

    Args:
        port (int): The port number to listen on.
    """
    server_address = ('', port)
    httpd = HTTPServer(server_address, MagnetarAPIHandler)
    print(f"Starting Magnetar API on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        # Allow the server to shut down cleanly upon receiving a termination signal from the user
        pass
    finally:
        # Ensure the socket is properly released and the server is fully closed
        httpd.server_close()
        print("Magnetar API stopped.")
