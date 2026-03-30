import yaml
from magnetar_prometheus_sdk.models import Workflow

class WorkflowLoader:
    def load_workflow(self, filepath: str) -> Workflow:
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise ValueError(
                f"Workflow definition in '{filepath}' must be a YAML mapping."
            )
        return Workflow(**data)
