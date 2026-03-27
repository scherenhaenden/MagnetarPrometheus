from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class RunRecord(BaseModel):
    """
    Represents a recorded execution of a workflow.
    """

    run_id: str
    workflow_id: str
    status: RunStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    output_summary: Dict[str, Any] = Field(default_factory=dict)
    error_list: List[Dict[str, Any]] = Field(default_factory=list)
