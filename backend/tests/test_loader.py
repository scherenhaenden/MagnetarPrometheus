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
