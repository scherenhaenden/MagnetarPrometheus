from typing import Dict, Any
from magnetar_prometheus_sdk.models import Workflow, StepResult
from magnetar_prometheus.core.executor_router import ExecutorRouter
from magnetar_prometheus.core.context_manager import ContextManager
from magnetar_prometheus.core.evaluator import ConditionEvaluator

class Engine:
    def __init__(self, executor_router: ExecutorRouter, context_manager: ContextManager):
        self.executor_router = executor_router
        self.context_manager = context_manager
        self.evaluator = ConditionEvaluator()

    def run(self, workflow: Workflow, initial_context: Dict[str, Any] = None) -> Dict[str, Any]:
        context = self.context_manager.create(workflow.id, initial_context or {})
        current_step_name = workflow.start_step

        while current_step_name and current_step_name != "end":
            if current_step_name not in workflow.steps:
                raise ValueError(f"Step '{current_step_name}' not found in workflow definition.")

            step_def = workflow.steps[current_step_name]
            executor = self.executor_router.get_executor(step_def.executor)

            try:
                result = executor.execute(step_def, context.model_dump())
            except Exception as e:
                result = StepResult(success=False, error_message=str(e))
                self.context_manager.apply_step_result(context, current_step_name, result)
                context.run["status"] = "failed"
                return context.model_dump()

            context = self.context_manager.apply_step_result(context, current_step_name, result)

            if not result.success:
                context.run["status"] = "failed"
                return context.model_dump()

            current_step_name = self._resolve_next_step(step_def, context.model_dump(), result)

        context.run["status"] = "completed"
        return context.model_dump()

    def _resolve_next_step(self, step_def, context: Dict[str, Any], result: StepResult) -> str:
        # Priority 1: Direct next_step from the step result.
        if result.next_step:
            return result.next_step

        next_val = step_def.next

        # Priority 2: Direct linear next from the workflow step definition
        if isinstance(next_val, str):
            return next_val

        # Priority 3: Conditional next branching from the workflow step definition
        if isinstance(next_val, dict):
            mode = next_val.get("mode")
            if mode == "conditional":
                for condition in next_val.get("conditions", []):
                    when_expr = condition.get("when")
                    try:
                        if self.evaluator.evaluate(when_expr, context):
                            return condition.get("go_to")
                    except Exception:
                        pass

        # Priority 4: Terminal completion if no valid path is found or all conditions fail.
        return "end"
