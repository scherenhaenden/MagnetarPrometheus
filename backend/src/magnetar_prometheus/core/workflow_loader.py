"""
Workflow definition loader for MagnetarPrometheus.

This file is intentionally small, but it owns an important boundary: untrusted YAML from disk
becomes a validated in-memory workflow model here. The loader therefore performs two distinct
jobs instead of delegating everything blindly to the schema layer:

- parse YAML from the filesystem using the repository's standard loader path;
- reject obviously invalid root shapes early with file-specific error messages before handing
  the data to Pydantic for deeper structural validation.

Keeping these responsibilities explicit makes CLI failures easier to understand and keeps review
threads about malformed workflow files localized to one module.
"""

from collections.abc import Mapping

import yaml
from magnetar_prometheus_sdk.models import Workflow


class WorkflowLoader:
    """Load YAML workflow files into validated `Workflow` instances.

    The class remains intentionally lightweight because the repository currently only needs one
    workflow-loading strategy. It still exists as a dedicated type so callers can depend on a
    stable boundary and tests can target loader behavior directly without pulling in the full
    engine stack.
    """

    def load_workflow(self, filepath: str) -> Workflow:
        """Load and validate a workflow definition from a YAML file.

        Args:
            filepath: Absolute or relative path to a YAML workflow definition.

        Returns:
            A validated `Workflow` instance ready for execution by the runtime engine.

        Raises:
            FileNotFoundError: When `filepath` does not exist.
            yaml.YAMLError: When the file contains invalid YAML syntax.
            ValueError: When the parsed YAML root is not a mapping or is an empty mapping.
            pydantic.ValidationError: When the mapping cannot be validated as a `Workflow`.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # Accept mapping-shaped YAML objects, not just plain dict instances, so the loader
        # remains correct even if the YAML parser returns a custom mapping implementation.
        if not isinstance(data, Mapping):
            raise ValueError(
                f"Workflow definition in '{filepath}' must be a YAML mapping."
            )

        # Empty mappings are still invalid workflows. Surfacing that here keeps the caller's
        # error message precise instead of forcing operators to interpret a later schema-level
        # failure that no longer points clearly at the original YAML root-shape mistake.
        if not data:
            raise ValueError(
                f"Workflow definition in '{filepath}' cannot be an empty YAML mapping."
            )

        return Workflow.model_validate(data)
