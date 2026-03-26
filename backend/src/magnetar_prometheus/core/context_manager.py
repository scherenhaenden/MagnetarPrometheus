from typing import Dict, Any
from magnetar_prometheus_sdk.models import RunContext, StepResult

class ContextManager:
    def create(self, workflow_id: str, initial_context: Dict[str, Any]) -> RunContext:
        ctx = RunContext()
        ctx.run["workflow_id"] = workflow_id
        ctx.run["status"] = "running"
        ctx.input = initial_context
        return ctx

    def apply_step_result(self, context: RunContext, step_name: str, result: StepResult) -> RunContext:
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
