"""
Workflow definition loader for MagnetarPrometheus.

Reads YAML workflow files from disk and deserialises them into validated
:class:`~magnetar_prometheus_sdk.models.Workflow` instances using Pydantic.
"""

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
            ValueError: When the YAML root is not a mapping.
            pydantic.ValidationError: When the parsed data does not conform to
                the :class:`~magnetar_prometheus_sdk.models.Workflow` schema.
        """
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise ValueError(
                f"Workflow definition in '{filepath}' must be a YAML mapping."
            )
        return Workflow.model_validate(data)
