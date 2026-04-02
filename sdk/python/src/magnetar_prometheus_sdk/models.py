from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Literal

from pydantic import BaseModel, Field


class Condition(BaseModel):
    when: str
    go_to: str


class ConditionalRouting(BaseModel):
    mode: Literal["conditional"] = "conditional"
    conditions: List[Condition] = Field(default_factory=list)


class StepDefinition(BaseModel):
    type: str
    executor: str
    description: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)
    next: Union[str, ConditionalRouting, Dict[str, Any], None] = None
    ui_metadata: Dict[str, Any] = Field(default_factory=dict)


class Workflow(BaseModel):
    id: str
    name: str
    version: str
    description: Optional[str] = None
    start_step: str
    settings: Dict[str, Any] = Field(default_factory=dict)
    steps: Dict[str, StepDefinition] = Field(default_factory=dict)
    ui_metadata: Dict[str, Any] = Field(default_factory=dict)


class StepResult(BaseModel):
    success: bool
    output: Dict[str, Any] = Field(default_factory=dict)
    next_step: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
    error_code: Optional[str] = None
    error_message: Optional[str] = None


class RunContext(BaseModel):
    run: Dict[str, Any] = Field(default_factory=dict)
    input: Dict[str, Any] = Field(default_factory=dict)
    data: Dict[str, Any] = Field(default_factory=dict)
    ai: Dict[str, Any] = Field(default_factory=dict)
    history: List[Dict[str, Any]] = Field(default_factory=list)
    errors: List[Dict[str, Any]] = Field(default_factory=list)


class RunStatus(str, Enum):
    """
    An enumeration of lifecycle states a workflow run can inhabit.

    Attributes:
        PENDING: The run is queued but execution has not started.
        RUNNING: The run is currently actively executing steps.
        COMPLETED: The run has successfully finished all steps.
        FAILED: The run encountered an unrecoverable error during execution.
        CANCELLED: The run was aborted manually or by an external trigger.
    """

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RunSubmissionRequest(BaseModel):
    """
    The payload required to request the start of a workflow execution.

    Attributes:
        workflow_id (str): The unique ID of the workflow to be executed.
        workflow_version (Optional[str]): A specific version of the workflow to run. If None, it assumes the latest available.
        input_data (Dict[str, Any]): The dynamic input variables needed by the workflow context. Defaults to an empty dict.
        tags (List[str]): Categorization labels for searching and filtering runs later. Defaults to an empty list.
    """

    workflow_id: str = Field(description="The unique ID of the workflow to execute")
    workflow_version: Optional[str] = Field(
        default=None,
        description="Optional specific version to execute; defaults to latest if omitted",
    )
    input_data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Dictionary of input arguments required by the workflow",
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Optional list of tags for searching and categorizing the run",
    )


class RunResponse(BaseModel):
    """
    The immediate acknowledgment returned after successfully submitting a run.

    Attributes:
        run_id (str): A unique identifier for this specific execution attempt.
        workflow_id (str): The ID of the workflow that was scheduled to run.
        status (RunStatus): The initial status of the execution (usually pending or running).
        created_at (datetime): The submission timestamp as a validated datetime object.
        message (Optional[str]): An optional message offering additional details on the submission.
    """

    run_id: str = Field(
        description="The unique identifier generated for this specific execution"
    )
    workflow_id: str = Field(description="The ID of the workflow being executed")
    status: RunStatus = Field(
        description="The initial status of the run (usually 'pending' or 'running')"
    )
    # Keep timestamp fields typed as datetime so the SDK boundary validates and normalizes
    # API payloads instead of leaving timestamp parsing to every downstream caller.
    created_at: datetime = Field(description="Timestamp when the run was requested")
    message: Optional[str] = Field(
        default=None,
        description="Optional descriptive message regarding the submission",
    )


class RunListingItem(BaseModel):
    """
    A lightweight representation of a run suitable for dashboard lists and CLI tables.

    Attributes:
        run_id (str): The unique execution identifier.
        workflow_id (str): The ID of the workflow.
        status (RunStatus): The current execution state of this run.
        created_at (datetime): The validated creation timestamp.
        completed_at (Optional[datetime]): The validated completion timestamp, or None if still active.
        tags (List[str]): User-defined categorizations assigned during submission.
    """

    run_id: str = Field(
        description="The unique identifier generated for this specific execution"
    )
    workflow_id: str = Field(description="The ID of the workflow being executed")
    status: RunStatus = Field(description="The current status of the run")
    created_at: datetime = Field(description="Timestamp when the run was requested")
    completed_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the run reached a terminal state; null if active",
    )
    tags: List[str] = Field(
        default_factory=list,
        description="List of tags for searching and categorizing the run",
    )


class RunSummary(RunListingItem):
    """
    A detailed view of a single run containing its final state and context results.

    This model intentionally extends `RunListingItem` instead of re-declaring the shared
    listing fields. That keeps the SDK contract honest about the relationship between the
    lightweight list view and the detailed inspect view: the summary is the listing shape plus
    deeper completion/error data.

    Attributes:
        final_context (Optional[RunContext]): The aggregated state context generated throughout the workflow execution.
        error_message (Optional[str]): Any global or top-level error messages encountered during failure.
    """

    final_context: Optional[RunContext] = Field(
        default=None,
        description="The aggregated state of the workflow upon completion.",
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Top-level error message if the run failed",
    )
