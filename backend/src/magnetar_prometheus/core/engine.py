"""
Workflow orchestration engine for MagnetarPrometheus.

:class:`Engine` drives serial workflow execution: it resolves each step,
delegates execution to the appropriate executor, accumulates results into the
run context, and determines the next step until the workflow reaches a terminal
state.
"""

from typing import Dict, Any
from magnetar_prometheus_sdk.models import Workflow, StepResult, ConditionalRouting
from magnetar_prometheus.core.executor_router import ExecutorRouter
from magnetar_prometheus.core.context_manager import ContextManager
from magnetar_prometheus.core.evaluator import ConditionEvaluator

class Engine:
    """Serial workflow execution engine.

    Loads a :class:`~magnetar_prometheus_sdk.models.Workflow`, iterates its
    steps in order, routes each step to the correct executor via
    :class:`ExecutorRouter`, and tracks state through
    :class:`ContextManager`.
    """

    def __init__(self, executor_router: ExecutorRouter, context_manager: ContextManager):
        """Initialise the engine with its routing and context dependencies.

        Args:
            executor_router: Maps executor type names to concrete
                :class:`~magnetar_prometheus.executors.base.BaseExecutor`
                instances.
            context_manager: Responsible for creating and mutating the
                :class:`~magnetar_prometheus_sdk.models.RunContext` during a
                run.
        """
        self.executor_router = executor_router
        self.context_manager = context_manager
        self.evaluator = ConditionEvaluator()

    def run(self, workflow: Workflow, initial_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Executes a workflow from the starting step to completion.
        
        This method initializes the context for the given workflow and iteratively
        processes each step defined in the workflow. It retrieves the appropriate
        executor for each step and handles the execution results, updating the context
        accordingly. If any step fails, the context is marked as failed, and the
        execution halts. The final status of the workflow is returned upon completion.
        
        Args:
            workflow (Workflow): The workflow to be executed.
            initial_context (Dict[str, Any]?): Initial context for the workflow execution.
        """
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
        """Resolve the next step in a workflow based on the provided step definition and
        context.
        
        This function determines the next step to execute in a workflow by first
        checking the `result` for a direct next step. If not found, it evaluates the
        `step_def` for a linear next step or any conditional branching defined in the
        workflow. It handles various types of next values, including strings,
        dictionaries, and `ConditionalRouting` objects, while managing exceptions
        during evaluation.
        
        Args:
            step_def (StepDefinition): The definition of the current workflow step.
            context (Dict[str, Any]): The context in which the workflow is being executed.
            result (StepResult): The result of the previous step execution.
        
        Returns:
            str: The identifier of the next step to execute, or "end" if no valid path is found.
        """
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
        elif isinstance(next_val, ConditionalRouting):
            for condition in next_val.conditions:
                try:
                    if self.evaluator.evaluate(condition.when, context):
                        return condition.go_to
                except Exception:
                    pass

        return "end"
