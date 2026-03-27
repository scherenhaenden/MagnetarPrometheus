import json
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from magnetar_prometheus.history.models import RunRecord, RunStatus

def test_run_record_serialization():
    """Test the serialization of a RunRecord to JSON."""
    start = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    end = datetime(2024, 1, 1, 12, 5, 30, tzinfo=timezone.utc)

    record = RunRecord(
        run_id="run-001",
        workflow_id="wf-abc",
        status=RunStatus.RUNNING,
        start_time=start,
        end_time=end,
        output_summary={"progress": 50},
        error_list=[{"msg": "warning 1"}],
    )

    # Dump to JSON
    json_str = record.model_dump_json()
    data = json.loads(json_str)

    # Check fields
    assert data["run_id"] == "run-001"
    assert data["workflow_id"] == "wf-abc"
    assert data["status"] == "running"
    assert "2024-01-01T12:00:00Z" in data["start_time"]
    assert "2024-01-01T12:05:30Z" in data["end_time"]
    assert data["output_summary"] == {"progress": 50}
    assert data["error_list"] == [{"msg": "warning 1"}]

def test_run_record_deserialization():
    """Test the deserialization of a RunRecord from JSON data."""
    json_data = {
        "run_id": "run-002",
        "workflow_id": "wf-def",
        "status": "completed",
        "start_time": "2024-01-02T10:00:00Z",
        "output_summary": {},
        "error_list": [],
    }

    record = RunRecord(**json_data)

    assert record.run_id == "run-002"
    assert record.status == RunStatus.COMPLETED
    assert record.start_time.year == 2024
    assert record.start_time.month == 1
    assert record.end_time is None

def test_run_record_rejects_invalid_status():
    json_data = {
        "run_id": "run-003",
        "workflow_id": "wf-def",
        "status": "unknown",
        "start_time": "2024-01-02T10:00:00Z",
    }

    with pytest.raises(ValidationError, match="status"):
        RunRecord(**json_data)
