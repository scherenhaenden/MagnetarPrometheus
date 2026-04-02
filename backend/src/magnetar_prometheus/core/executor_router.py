from typing import Dict
from magnetar_prometheus.executors.base import BaseExecutor

class ExecutorRouter:
    def __init__(self):
        self._executors: Dict[str, BaseExecutor] = {}

    def register(self, name: str, executor: BaseExecutor):
        self._executors[name] = executor

    def get_executor(self, name: str) -> BaseExecutor:
        if name not in self._executors:
            raise ValueError(f"Executor '{name}' not found.")
        return self._executors[name]
