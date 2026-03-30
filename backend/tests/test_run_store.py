import json
from unittest.mock import patch
from datetime import datetime, timezone

import pytest

from magnetar_prometheus.history.models import RunRecord, RunStatus
from magnetar_prometheus.run_store import LocalJSONRunStore


@pytest.fixture
def temp_store_dir(tmp_path):
    """Return the path for storing temporary test run history."""
    return tmp_path / "test_run_history"

@pytest.fixture
def store(temp_store_dir):
    """Create and return a LocalJSONRunStore instance."""
    return LocalJSONRunStore(storage_dir=str(temp_store_dir))

@pytest.fixture
def sample_record():
    """Fixture that provides a sample RunRecord for testing."""
    return RunRecord(
        run_id="run-123",
        workflow_id="wf-abc",
        status=RunStatus.COMPLETED,
        start_time=datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc),
        end_time=datetime(2023, 1, 1, 10, 5, 0, tzinfo=timezone.utc),
        output_summary={"result": "success"},
        error_list=[],
    )

def test_store_initialization(temp_store_dir):
    # Should create directory if it doesn't exist
    """Test the initialization of the LocalJSONRunStore."""
    assert not temp_store_dir.exists()
    LocalJSONRunStore(storage_dir=str(temp_store_dir))
    assert temp_store_dir.exists()
    assert temp_store_dir.is_dir()

def test_save_and_get(store, sample_record):
    # Save
    """Test saving and retrieving a record from the store."""
    store.save(sample_record)

    # Get
    retrieved = store.get("run-123")
    assert retrieved is not None
    assert retrieved.run_id == "run-123"
    assert retrieved.workflow_id == "wf-abc"
    assert retrieved.status == RunStatus.COMPLETED
    assert retrieved.start_time == sample_record.start_time
    assert retrieved.end_time == sample_record.end_time
    assert retrieved.output_summary == {"result": "success"}

def test_get_not_found(store):
    """Test that a non-existent run returns None from the store."""
    assert store.get("non-existent-run") is None

def test_get_invalid_json(store, temp_store_dir):
    # Create invalid JSON file
    """Test retrieval of an invalid JSON file."""
    file_path = temp_store_dir / "bad-run.json"
    with open(file_path, "w") as f:
        f.write("{ invalid json")

    assert store.get("bad-run") is None

def test_list_records(store, sample_record):
    """Test listing records in the store."""
    record2 = RunRecord(
        run_id="run-456",
        workflow_id="wf-xyz",
        status=RunStatus.FAILED,
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
    """Test listing files while ignoring invalid JSON files."""
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
    """Test listing records in a non-existent directory."""
    store = LocalJSONRunStore(storage_dir=str(tmp_path / "missing"))
    # Delete the directory created by init to simulate it being removed
    import shutil
    shutil.rmtree(str(tmp_path / "missing"))

    records = store.list()
    assert len(records) == 0

def test_save_wraps_file_write_errors(store, sample_record):
    """Test that saving a record raises a RuntimeError on file write errors."""
    with patch("builtins.open", side_effect=OSError("disk full")):
        with pytest.raises(RuntimeError, match="Failed to save record"):
            store.save(sample_record)

def test_get_rejects_path_traversal_run_id(store):
    """Test that path traversal is rejected."""
    assert store.get("../escape") is None

def test_list_ignores_invalid_record_shape(store, temp_store_dir):
    """Test that the list method ignores invalid record shapes."""
    invalid_record = temp_store_dir / "invalid-record.json"
    invalid_record.write_text(
        json.dumps(
            {
                "run_id": "run-invalid",
                "workflow_id": "wf-abc",
                "status": "unknown",
                "start_time": "2023-01-01T10:00:00Z",
            }
        ),
        encoding="utf-8",
    )

    assert store.list() == []
