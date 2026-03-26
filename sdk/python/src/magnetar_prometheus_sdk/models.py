from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class StepDefinition(BaseModel):
    type: str
    executor: str
    config: Dict[str, Any] = Field(default_factory=dict)
    next: Any = None

class Workflow(BaseModel):
    id: str
    name: str
    version: str
    start_step: str
    settings: Dict[str, Any] = Field(default_factory=dict)
    steps: Dict[str, StepDefinition] = Field(default_factory=dict)

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
