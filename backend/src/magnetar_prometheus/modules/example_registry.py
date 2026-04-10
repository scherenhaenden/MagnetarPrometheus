"""Application-level plugin assembly for bundled example workflow modules.

Why this file exists in this form:

- The repository ships several deterministic example modules used across CLI, API, and tests.
  They should be installable as a coherent default plugin bundle without forcing each module
  to import unrelated siblings.
- This file now exposes those modules as first-class plugin runtimes so startup code can use a
  generic plugin manager instead of hard-coded registration calls.
- The current surface remains intentionally local and explicit: this is the bundled baseline,
  while external package discovery is handled by the plugin manager.
"""

from magnetar_prometheus.modules.email_module.steps import (
    ai_classify,
    create_ticket,
    extract_email_data,
    fetch_emails,
    manual_review,
)
from magnetar_prometheus.modules.error_module.steps import start_error, trigger_error
from magnetar_prometheus.modules.http_module.steps import http_get, json_parse
from magnetar_prometheus.modules.linear_module.steps import process_linear, start_linear
from magnetar_prometheus.modules.math_module.steps import math_add, math_multiply
from magnetar_prometheus.plugins.models import PluginManifest, PluginRuntime
from magnetar_prometheus.registry.step_registry import StepRegistry


def get_builtin_plugins() -> list[PluginRuntime]:
    """Return the default bundled plugin set shipped with the repository."""
    core_manifest = PluginManifest(
        plugin_id="magnetar.core.examples",
        version="1.0.0",
        api_version="1",
        description="Bundled deterministic example steps for local runs and tests.",
        step_types={
            "email.fetch": "python",
            "email.extract": "python",
            "ai.classify": "python",
            "ticket.create": "python",
            "review.queue": "python",
            "linear.start": "python",
            "linear.process": "python",
            "error.start": "python",
            "error.trigger": "python",
            "math.add": "python",
            "math.multiply": "python",
            "http.get": "python",
            "json.parse": "python",
        },
        compatibility={"python": ">=3.11"},
    )

    core_plugin = PluginRuntime(
        manifest=core_manifest,
        step_handlers={
            "email.fetch": fetch_emails,
            "email.extract": extract_email_data,
            "ai.classify": ai_classify,
            "ticket.create": create_ticket,
            "review.queue": manual_review,
            "linear.start": start_linear,
            "linear.process": process_linear,
            "error.start": start_error,
            "error.trigger": trigger_error,
            "math.add": math_add,
            "math.multiply": math_multiply,
            "http.get": http_get,
            "json.parse": json_parse,
        },
    )

    return [core_plugin]


def register_all_example_steps(registry: StepRegistry) -> None:
    """Backward-compatible helper that registers every bundled example step.

    This stays a direct, easy-to-read helper and does not depend on PluginManager.
    """
    for plugin in get_builtin_plugins():
        for step_type, handler in plugin.step_handlers.items():
            registry.register(step_type, handler)
