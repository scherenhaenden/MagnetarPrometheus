"""Plugin contracts and runtime helpers for MagnetarPrometheus.

Why this package exists in this form:

- The repository already had a module-level step registration path, but it lacked a reusable,
  explicit plugin abstraction that can grow into package-based discovery and policy gating.
- Keeping plugin contracts in their own package prevents the core engine from coupling itself
  to a specific module layout while still allowing today's bundled examples to load unchanged.
- The package starts intentionally small: contract objects, a manager, and discovery hooks.
  This keeps the first slice easy to reason about and test while preserving room for future
  policy, signatures, remote catalogs, and richer capability metadata.
"""

from magnetar_prometheus.plugins.manager import PluginManager
from magnetar_prometheus.plugins.models import PluginManifest, PluginRuntime

__all__ = ["PluginManifest", "PluginRuntime", "PluginManager"]
