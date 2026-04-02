"""Application-level registration for bundled example workflow modules.

This helper keeps cross-module wiring out of the example modules themselves. The individual
module packages remain responsible for registering their own handlers, while the CLI/API
entrypoints can import one central function when they want the whole demonstration surface.
"""

from magnetar_prometheus.modules.email_module.steps import register_example_steps
from magnetar_prometheus.modules.error_module.steps import register_error_steps
from magnetar_prometheus.modules.linear_module.steps import register_linear_steps


def register_all_example_steps(registry) -> None:
    """Register every bundled example module into the provided step registry."""
    register_example_steps(registry)
    register_linear_steps(registry)
    register_error_steps(registry)
