from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

from .events import TaskEvent
from .models import Task


class TaskStore(ABC):
    """Persistence boundary for TaskAgentRelay state."""

    @abstractmethod
    def save(self, task: Task) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, task_id: str) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    def record_event(self, event: TaskEvent) -> None:
        raise NotImplementedError


class InMemoryTaskStore(TaskStore):
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}
        self._events: list[TaskEvent] = []

    def save(self, task: Task) -> None:
        self._tasks[task.id] = task

    def get(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def record_event(self, event: TaskEvent) -> None:
        self._events.append(event)

    def events_for(self, task_id: str) -> list[TaskEvent]:
        return [event for event in self._events if event.task_id == task_id]
