"""Plugin bootstrap helpers for runtime entrypoints.

Why this file exists in this form:
- CLI and API server entrypoints need a unified way to configure the plugin system.
- Centralizing the startup wiring allows discovery and registration policies to evolve
  in one place without duplicating boilerplate across the repository.
"""

from __future__ import annotations

from magnetar_prometheus.modules.example_registry import get_builtin_plugins
from magnetar_prometheus.plugins.manager import PluginManager
from magnetar_prometheus.registry.step_registry import StepRegistry


def build_plugin_manager(registry: StepRegistry) -> PluginManager:
    """
    Configure and register all builtin plugins into the given registry.

    Centralizing this startup wiring allows API and CLI entrypoints to
    share the same plugin initialization behavior.
    """
    plugin_manager = PluginManager()
    plugin_manager.register_many(get_builtin_plugins())
    plugin_manager.register_into(registry)
    return plugin_manager
