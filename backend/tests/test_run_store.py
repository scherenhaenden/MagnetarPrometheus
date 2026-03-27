import json
import pytest
from datetime import datetime, timezone
from pathlib import Path

from magnetar_prometheus.history.models import RunRecord
from magnetar_prometheus.run_store import LocalJSONRunStore


@pytest.fixture
def temp_store_dir(tmp_path):
    return tmp_path / "test_run_history"

@pytest.fixture
def store(temp_store_dir):
    return LocalJSONRunStore(storage_dir=str(temp_store_dir))

@pytest.fixture
def sample_record():
    return RunRecord(
        run_id="run-123",
        workflow_id="wf-abc",
        status="completed",
        start_time=datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc),
        end_time=datetime(2023, 1, 1, 10, 5, 0, tzinfo=timezone.utc),
        output_summary={"result": "success"},
        error_list=[]
    )

def test_store_initialization(temp_store_dir):
    # Should create directory if it doesn't exist
    assert not temp_store_dir.exists()
    LocalJSONRunStore(storage_dir=str(temp_store_dir))
    assert temp_store_dir.exists()
    assert temp_store_dir.is_dir()

def test_save_and_get(store, sample_record):
    # Save
    store.save(sample_record)

    # Get
    retrieved = store.get("run-123")
    assert retrieved is not None
    assert retrieved.run_id == "run-123"
    assert retrieved.workflow_id == "wf-abc"
    assert retrieved.status == "completed"
    assert retrieved.start_time == sample_record.start_time
    assert retrieved.end_time == sample_record.end_time
    assert retrieved.output_summary == {"result": "success"}

def test_get_not_found(store):
    assert store.get("non-existent-run") is None

def test_get_invalid_json(store, temp_store_dir):
    # Create invalid JSON file
    file_path = temp_store_dir / "bad-run.json"
    with open(file_path, "w") as f:
        f.write("{ invalid json")

    assert store.get("bad-run") is None

def test_list_records(store, sample_record):
    record2 = RunRecord(
        run_id="run-456",
        workflow_id="wf-xyz",
        status="failed",
        start_time=datetime(2023, 1, 2, 10, 0, 0, tzinfo=timezone.utc),
    )

    store.save(sample_record)
    store.save(record2)

    records = store.list()
    assert len(records) == 2

    # Check default sorting (start_time descending)
    assert records[0].run_id == "run-456"  # Later date
    assert records[1].run_id == "run-123"

def test_list_with_invalid_files(store, sample_record, temp_store_dir):
    store.save(sample_record)

    # Create an invalid JSON file
    file_path = temp_store_dir / "bad-run.json"
    with open(file_path, "w") as f:
        f.write("not json")

    # List should ignore the invalid file
    records = store.list()
    assert len(records) == 1
    assert records[0].run_id == "run-123"

def test_list_non_existent_dir(tmp_path):
    store = LocalJSONRunStore(storage_dir=str(tmp_path / "missing"))
    # Delete the directory created by init to simulate it being removed
    import shutil
    shutil.rmtree(str(tmp_path / "missing"))

    records = store.list()
    assert len(records) == 0
