"""Typed plugin contracts for the MagnetarPrometheus backend runtime.

Why this file exists in this form:

- The codebase needs a formal plugin boundary so new capabilities can be added without editing
  core orchestration code whenever a new module or executor type is introduced.
- These models keep plugin metadata explicit and machine-validated, which makes startup
  diagnostics and future compatibility checks far easier than ad-hoc dictionaries.
- The contract is deliberately conservative in v1: it captures identity, compatibility, and
  high-value capability metadata while leaving room for future extensibility.
"""

from dataclasses import dataclass, field
from typing import Callable, Mapping

from magnetar_prometheus_sdk.models import StepResult

StepHandler = Callable[[dict, dict], StepResult]


@dataclass(frozen=True)
class PluginManifest:
    """Describe one loadable plugin package for the runtime registry.

    Attributes:
        plugin_id: Stable unique identifier for the plugin.
        version: Plugin package version.
        api_version: Plugin API compatibility version expected by the runtime.
        description: Human-readable short plugin summary.
        step_types: Mapping of declared step type names to executor identifiers.
        ui_metadata: Optional plugin-scoped UI metadata for future surfaces.
        compatibility: Free-form compatibility metadata (e.g., python/backend constraints).
    """

    plugin_id: str
    version: str
    api_version: str
    description: str
    step_types: Mapping[str, str] = field(default_factory=dict)
    ui_metadata: Mapping[str, object] = field(default_factory=dict)
    compatibility: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class PluginRuntime:
    """Runtime-ready plugin bundle with manifest and step handlers.

    Attributes:
        manifest: Immutable plugin metadata used for diagnostics and policy checks.
        step_handlers: Mapping of step type to Python callables used by the executor.
    """

    manifest: PluginManifest
    step_handlers: Mapping[str, StepHandler] = field(default_factory=dict)
