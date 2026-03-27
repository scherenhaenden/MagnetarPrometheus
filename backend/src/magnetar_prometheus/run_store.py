import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

from magnetar_prometheus.history.models import RunRecord

class RunStore(ABC):
    """
    Abstract interface for persisting and retrieving workflow run records.
    """

    @abstractmethod
    def save(self, record: RunRecord) -> None:
        """Saves a run record to the store."""

    @abstractmethod
    def get(self, run_id: str) -> Optional[RunRecord]:
        """Retrieves a run record by its run ID. Returns None if not found."""

    @abstractmethod
    def list(self) -> List[RunRecord]:
        """Retrieves all run records in the store."""


class LocalJSONRunStore(RunStore):
    """
    A simple file-based JSON implementation of RunStore.
    """

    def __init__(self, storage_dir: str = ".run_history"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, run_id: str) -> Path:
        return self.storage_dir / f"{run_id}.json"

    def save(self, record: RunRecord) -> None:
        file_path = self._get_file_path(record.run_id)
        with open(file_path, "w", encoding="utf-8") as f:
            # model_dump_json handles datetime serialization
            f.write(record.model_dump_json(indent=2))

    def get(self, run_id: str) -> Optional[RunRecord]:
        file_path = self._get_file_path(run_id)
        if not file_path.is_file():
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return RunRecord(**data)
        except (json.JSONDecodeError, Exception):
            return None

    def list(self) -> List[RunRecord]:
        records = []
        if not self.storage_dir.is_dir():
            return records

        for file_path in self.storage_dir.glob("*.json"):
            if file_path.is_file():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    records.append(RunRecord(**data))
                except (json.JSONDecodeError, Exception):
                    continue

        # Sort by start_time descending by default
        records.sort(key=lambda r: r.start_time, reverse=True)
        return records
