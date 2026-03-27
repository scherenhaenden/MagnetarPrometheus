from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime

class RunRecord(BaseModel):
    """
    Represents a recorded execution of a workflow.
    """
    run_id: str
    workflow_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    output_summary: Dict[str, Any] = Field(default_factory=dict)
    error_list: List[Dict[str, Any]] = Field(default_factory=list)
