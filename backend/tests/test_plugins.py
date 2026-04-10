"""Contract tests for the backend plugin manager and bundled plugin metadata.

Why this file exists in this form:

- The repository now supports a generic plugin registration path for step handlers, so this
  test module protects the contract that keeps plugin discovery deterministic and safe.
- The tests verify both happy-path registration and failure-path validation (API mismatches,
  duplicate step ownership, and inconsistent manifest/handler declarations).
- A focused check against the bundled example plugin ensures the default CLI/API runtime keeps
  exposing the expected step capabilities while being routed through the new plugin layer.
"""

import pytest

from magnetar_prometheus.modules.example_registry import get_builtin_plugins
from magnetar_prometheus.plugins.manager import PluginManager
from magnetar_prometheus.plugins.models import PluginManifest, PluginRuntime
from magnetar_prometheus.registry.step_registry import StepRegistry


def _make_test_plugin(plugin_id: str, step_type: str) -> PluginRuntime:
    """Create a tiny valid plugin used across multiple manager tests."""

    def _handler(context, config):  # pragma: no cover - handler body not relevant to contract checks
        return context, config

    manifest = PluginManifest(
        plugin_id=plugin_id,
        version="1.0.0",
        api_version="1",
        description="test plugin",
        step_types={step_type: "python"},
    )
    return PluginRuntime(manifest=manifest, step_handlers={step_type: _handler})


def test_plugin_manager_registers_bundled_plugins_into_step_registry():
    """Verify that bundled plugin handlers are installed into the runtime step registry."""
    manager = PluginManager()
    manager.register_many(get_builtin_plugins())

    registry = StepRegistry()
    manager.register_into(registry)

    assert registry.get_handler("email.fetch") is not None
    assert registry.get_handler("json.parse") is not None
    assert "magnetar.core.examples" in manager.list_plugins()


def test_plugin_manager_rejects_api_version_mismatch():
    """Verify plugin registration fails when API versions are incompatible."""
    manager = PluginManager(required_api_version="1")
    plugin = PluginRuntime(
        manifest=PluginManifest(
            plugin_id="plugin.bad.version",
            version="1.0.0",
            api_version="2",
            description="bad",
            step_types={"x.step": "python"},
        ),
        step_handlers={"x.step": lambda _context, _config: None},
    )

    with pytest.raises(ValueError, match="runtime requires '1'"):
        manager.register_plugin(plugin)


def test_plugin_manager_rejects_duplicate_step_ownership():
    """Verify two plugins cannot claim the same step type."""
    manager = PluginManager()
    manager.register_plugin(_make_test_plugin("plugin.one", "dup.step"))

    with pytest.raises(ValueError, match="already owned"):
        manager.register_plugin(_make_test_plugin("plugin.two", "dup.step"))


def test_plugin_manager_rejects_manifest_handler_mismatch():
    """Verify registration fails when declarations and handlers diverge."""
    manager = PluginManager()

    missing_handler_plugin = PluginRuntime(
        manifest=PluginManifest(
            plugin_id="plugin.missing.handler",
            version="1.0.0",
            api_version="1",
            description="missing",
            step_types={"declared.step": "python"},
        ),
        step_handlers={},
    )
    with pytest.raises(ValueError, match="without handlers"):
        manager.register_plugin(missing_handler_plugin)

    extra_handler_plugin = PluginRuntime(
        manifest=PluginManifest(
            plugin_id="plugin.extra.handler",
            version="1.0.0",
            api_version="1",
            description="extra",
            step_types={},
        ),
        step_handlers={"not.declared": lambda _context, _config: None},
    )
    with pytest.raises(ValueError, match="undeclared handlers"):
        manager.register_plugin(extra_handler_plugin)


def test_plugin_manager_rejects_duplicate_plugin_id_registration():
    """Verify that a plugin ID can only be registered once."""
    manager = PluginManager()
    plugin = _make_test_plugin("plugin.duplicate", "step.one")
    manager.register_plugin(plugin)

    with pytest.raises(ValueError, match="already registered"):
        manager.register_plugin(plugin)


def test_plugin_manager_discovers_entrypoint_plugins(monkeypatch):
    """Verify that plugins can be discovered via entry points."""
    mock_plugin = _make_test_plugin("plugin.discovered", "step.discovered")

    class MockEntryPoint:
        def load(self):
            return lambda: mock_plugin

    def mock_entry_points(group=None):
        if group == "magnetar_prometheus.plugins":
            return [MockEntryPoint()]
        return []

    monkeypatch.setattr("magnetar_prometheus.plugins.manager.entry_points", mock_entry_points)

    manager = PluginManager()
    discovered = manager.discover_entrypoint_plugins()

    assert len(discovered) == 1
    assert discovered[0].manifest.plugin_id == "plugin.discovered"


def test_plugin_manager_provides_step_ownership_diagnostics():
    """Verify that the manager can report step-type ownership."""
    manager = PluginManager()
    manager.register_plugin(_make_test_plugin("plugin.owner", "step.owned"))

    owners = manager.describe_step_owners()
    assert owners == {"step.owned": "plugin.owner"}
