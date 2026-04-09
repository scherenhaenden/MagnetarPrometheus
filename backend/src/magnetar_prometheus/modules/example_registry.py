"""Application-level registration for bundled example workflow modules.

Why this file exists in this form:

- The repository currently ships a handful of small example workflow modules that are useful
  together in the CLI and API demonstration surfaces, but those modules should not import one
  another just to become runnable.
- Earlier branch work temporarily registered ``linear_module`` and ``error_module`` from
  inside ``email_module`` because the application entrypoints only had one obvious seed
  function. That worked operationally, but it created the wrong dependency direction by making
  one example module responsible for wiring unrelated examples.
- This file is the narrow application-level fix for that problem. The individual modules stay
  responsible for their own handlers, while the CLI and API can import one explicit helper
  when they want the full bundled example surface.
- The helper stays intentionally small. It is not a general plugin system or dynamic module
  discovery layer yet; it is only the central registration point for the example modules that
  the repository currently uses for demonstration and testing.
"""

from magnetar_prometheus.modules.email_module.steps import register_example_steps
from magnetar_prometheus.modules.error_module.steps import register_error_steps
from magnetar_prometheus.modules.linear_module.steps import register_linear_steps
from magnetar_prometheus.modules.math_module.steps import register_math_steps
from magnetar_prometheus.modules.http_module.steps import register_http_steps


def register_all_example_steps(registry) -> None:
    """Register every bundled example module into the provided step registry."""
    register_example_steps(registry)
    register_linear_steps(registry)
    register_error_steps(registry)
    register_math_steps(registry)
    register_http_steps(registry)
