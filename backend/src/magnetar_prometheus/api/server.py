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
    Provides /health and /run-example endpoints.
    """

    def _send_json_response(self, status_code: int, payload: dict):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode('utf-8'))

    def do_GET(self):
        if self.path == '/health':
            self._send_json_response(200, {"status": "ok"})
        else:
            self._send_json_response(404, {"error": "Not Found"})

    def do_POST(self):
        if self.path == '/run-example':
            try:
                # Resolve the default workflow path dynamically
                default_workflow_path = (
                    Path(__file__).parent.parent / "modules" / "email_module" / "email_triage.yaml"
                )

                if not default_workflow_path.is_file():
                    self._send_json_response(500, {"error": "Example workflow file not found."})
                    return

                # Reusing core runtime assembly
                loader = WorkflowLoader()
                wf = loader.load_workflow(str(default_workflow_path))

                registry = StepRegistry()
                register_example_steps(registry)

                executor = PythonExecutor(registry)
                router = ExecutorRouter()
                router.register('python', executor)

                cm = ContextManager()
                engine = Engine(router, cm)

                result_context = engine.run(wf)

                self._send_json_response(200, {
                    "status": "success",
                    "result": result_context
                })
            except Exception as e:
                self._send_json_response(500, {"error": str(e)})
        else:
            self._send_json_response(404, {"error": "Not Found"})


def run_server(port: int = 8000):
    """Starts the minimal local API server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MagnetarAPIHandler)
    print(f"Starting Magnetar API on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print("Magnetar API stopped.")
