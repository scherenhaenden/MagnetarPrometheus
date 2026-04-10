"""Plugin discovery and registration orchestration for backend runtime startup.

Why this file exists in this form:

- The first plugin slice should be generic enough to host bundled modules today and
  package-based plugins later, but small enough to keep failure modes obvious.
- Startup discovery behavior is centralized here so CLI/API entrypoints can share one
  deterministic path and avoid duplicate wiring logic.
- The manager validates plugin contracts early, captures ownership diagnostics for step types,
  and supports optional entry-point loading without making that path mandatory.
"""

from __future__ import annotations

from importlib.metadata import entry_points
from typing import Dict, Iterable, List

from magnetar_prometheus.plugins.models import PluginRuntime
from magnetar_prometheus.registry.step_registry import StepRegistry

PLUGIN_API_VERSION = "1"
PLUGIN_ENTRYPOINT_GROUP = "magnetar_prometheus.plugins"


class PluginManager:
    """Coordinate plugin discovery and registration for the step registry."""

    def __init__(self, required_api_version: str = PLUGIN_API_VERSION):
        self.required_api_version = required_api_version
        self._plugins: Dict[str, PluginRuntime] = {}
        self._step_owners: Dict[str, str] = {}

    def register_plugin(self, plugin: PluginRuntime) -> None:
        """Register a plugin after validating API compatibility and step ownership."""
        manifest = plugin.manifest
        if manifest.api_version != self.required_api_version:
            raise ValueError(
                f"Plugin '{manifest.plugin_id}' uses api_version '{manifest.api_version}' "
                f"but runtime requires '{self.required_api_version}'."
            )

        if manifest.plugin_id in self._plugins:
            raise ValueError(f"Plugin '{manifest.plugin_id}' is already registered.")

        declared_step_types = set(manifest.step_types.keys())
        implemented_step_types = set(plugin.step_handlers.keys())

        missing_handlers = declared_step_types - implemented_step_types
        if missing_handlers:
            missing = ", ".join(sorted(missing_handlers))
            raise ValueError(
                f"Plugin '{manifest.plugin_id}' declares step types without handlers: {missing}."
            )

        undeclared_handlers = implemented_step_types - declared_step_types
        if undeclared_handlers:
            extra = ", ".join(sorted(undeclared_handlers))
            raise ValueError(
                f"Plugin '{manifest.plugin_id}' registers undeclared handlers: {extra}."
            )

        for step_type in declared_step_types:
            if step_type in self._step_owners:
                current_owner = self._step_owners[step_type]
                raise ValueError(
                    f"Step type '{step_type}' is already owned by plugin '{current_owner}'."
                )

        for step_type in declared_step_types:
            self._step_owners[step_type] = manifest.plugin_id

        self._plugins[manifest.plugin_id] = plugin

    def register_many(self, plugins: Iterable[PluginRuntime]) -> None:
        """Register a sequence of plugins in deterministic iteration order."""
        for plugin in plugins:
            self.register_plugin(plugin)

    def discover_entrypoint_plugins(self) -> List[PluginRuntime]:
        """Load plugins exposed via Python package entry points.

        Each entry point must resolve to a zero-arg callable returning ``PluginRuntime``.
        """
        discovered_plugins: List[PluginRuntime] = []
        for ep in entry_points(group=PLUGIN_ENTRYPOINT_GROUP):
            provider = ep.load()
            plugin = provider()
            discovered_plugins.append(plugin)
        return discovered_plugins

    def register_into(self, registry: StepRegistry) -> None:
        """Install every registered plugin step handler into the runtime registry."""
        for plugin in self._plugins.values():
            for step_type, handler in plugin.step_handlers.items():
                registry.register(step_type, handler)

    def list_plugins(self) -> List[str]:
        """Return sorted plugin identifiers for diagnostics and CLI surfaces."""
        return sorted(self._plugins.keys())

    def describe_step_owners(self) -> Dict[str, str]:
        """Return a copy of step-type ownership diagnostics."""
        return dict(self._step_owners)
