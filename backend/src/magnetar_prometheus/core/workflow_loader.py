import yaml
from magnetar_prometheus_sdk.models import Workflow

class WorkflowLoader:
    def load_workflow(self, filepath: str) -> Workflow:
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
        return Workflow(**data)
