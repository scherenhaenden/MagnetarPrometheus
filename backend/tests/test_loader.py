from collections import UserDict
from unittest.mock import patch

import pytest

from magnetar_prometheus.core.workflow_loader import WorkflowLoader


def test_load_workflow(tmp_path):
    yaml_content = """
    id: test_id
    name: test name
    version: 1.0.0
    start_step: start
    """
    p = tmp_path / "test.yaml"
    p.write_text(yaml_content)

    loader = WorkflowLoader()
    wf = loader.load_workflow(str(p))

    assert wf.id == "test_id"
    assert wf.name == "test name"
    assert wf.start_step == "start"


@pytest.mark.parametrize(
    "yaml_content",
    [
        "",
        "- item1\n- item2\n",
        "just a scalar\n",
    ],
)
def test_load_workflow_rejects_non_mapping_yaml(tmp_path, yaml_content):
    p = tmp_path / "invalid.yaml"
    p.write_text(yaml_content)

    loader = WorkflowLoader()

    with pytest.raises(ValueError, match=r"invalid\.yaml.*YAML mapping"):
        loader.load_workflow(str(p))


def test_load_workflow_accepts_mapping_subclasses(tmp_path):
    p = tmp_path / "mapping.yaml"
    p.write_text("id: ignored-by-patch\n")

    custom_mapping = UserDict(
        {
            "id": "custom_mapping_workflow",
            "name": "Custom Mapping Workflow",
            "version": "1.0.0",
            "start_step": "start",
        }
    )

    loader = WorkflowLoader()

    with patch(
        "magnetar_prometheus.core.workflow_loader.yaml.safe_load",
        return_value=custom_mapping,
    ):
        wf = loader.load_workflow(str(p))

    assert wf.id == "custom_mapping_workflow"
    assert wf.name == "Custom Mapping Workflow"
    assert wf.start_step == "start"



def test_load_workflow_rejects_empty_mapping_yaml(tmp_path):
    p = tmp_path / "empty_mapping.yaml"
    p.write_text("{}\n")

    loader = WorkflowLoader()

    with pytest.raises(ValueError, match=r"empty_mapping\.yaml.*empty YAML mapping"):
        loader.load_workflow(str(p))
