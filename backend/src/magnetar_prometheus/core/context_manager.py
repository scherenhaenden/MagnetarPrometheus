"""
Runtime context management for the MagnetarPrometheus workflow engine.

:class:`ContextManager` is responsible for creating fresh
:class:`~magnetar_prometheus_sdk.models.RunContext` instances and for
applying each step's result back into the live context as execution progresses.
"""

from typing import Dict, Any
from magnetar_prometheus_sdk.models import RunContext, StepResult

class ContextManager:
    """Creates and mutates :class:`~magnetar_prometheus_sdk.models.RunContext` objects.

    Keeps context-mutation logic out of the engine core so both can be tested
    in isolation.
    """

    def create(self, workflow_id: str, initial_context: Dict[str, Any]) -> RunContext:
        """Create a RunContext with the specified workflow ID and initial context."""
        ctx = RunContext()
        ctx.run["workflow_id"] = workflow_id
        ctx.run["status"] = "running"
        ctx.input = initial_context
        return ctx

    def apply_step_result(self, context: RunContext, step_name: str, result: StepResult) -> RunContext:
        """Apply the result of a step to the given context.
        
        This function updates the context's history with the step's name and result
        details. If the step was successful, it updates the context's AI and data
        attributes based on the output. In case of failure, it appends the error
        information to the context's errors list. The function ultimately returns the
        modified context.
        
        Args:
            context (RunContext): The current run context to be updated.
            step_name (str): The name of the step being applied.
            result (StepResult): The result of the step containing success status and output.
        """
        context.history.append({
            "step": step_name,
            "success": result.success,
            "output": result.output,
            "error_code": result.error_code,
            "error_message": result.error_message
        })

        if result.success:
            if "ai" in result.output:
                context.ai.update(result.output["ai"])
            if "data" in result.output:
                context.data.update(result.output["data"])

            for k, v in result.output.items():
                if k not in ["ai", "data"]:
                    context.data[k] = v
        else:
            context.errors.append({
                "step": step_name,
                "error_code": result.error_code,
                "error_message": result.error_message
            })

        return context
