"""
Workflow definition loader for MagnetarPrometheus.

Reads YAML workflow files from disk and deserialises them into validated
:class:`~magnetar_prometheus_sdk.models.Workflow` instances using Pydantic.
"""

from collections.abc import Mapping

import yaml
from magnetar_prometheus_sdk.models import Workflow


class WorkflowLoader:
    """Deserialises YAML workflow files into :class:`~magnetar_prometheus_sdk.models.Workflow` objects."""

    def load_workflow(self, filepath: str) -> Workflow:
        """Load and validate a workflow definition from a YAML file.

        Args:
            filepath: Absolute or relative path to a YAML workflow definition.

        Returns:
            A validated :class:`~magnetar_prometheus_sdk.models.Workflow`
            instance ready for execution by :class:`~magnetar_prometheus.core.engine.Engine`.

        Raises:
            FileNotFoundError: When *filepath* does not exist.
            yaml.YAMLError: When the file contains invalid YAML.
            ValueError: When the YAML root is not a mapping type or is empty.
            pydantic.ValidationError: When the parsed data does not conform to
                the :class:`~magnetar_prometheus_sdk.models.Workflow` schema.
        """
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)

        # Accept mapping-shaped YAML objects, not just plain dict instances, so
        # loader behavior stays correct if the parser returns a custom mapping.
        if not isinstance(data, Mapping):
            raise ValueError(
                f"Workflow definition in '{filepath}' must be a YAML mapping."
            )

        # Empty mappings are still invalid workflows; surface that as a loader-
        # level error instead of a less specific downstream schema failure.
        if not data:
            raise ValueError(
                f"Workflow definition in '{filepath}' cannot be an empty YAML mapping."
            )
        return Workflow.model_validate(data)
