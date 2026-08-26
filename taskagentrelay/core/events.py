from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class TaskEvent:
    task_id: str
    event: str
    timestamp: str = field(default_factory=utc_now)
    data: dict[str, Any] = field(default_factory=dict)


class EventRecorder:
    """Small in-memory event recorder used by v0.1 and tests."""

    def __init__(self) -> None:
        self._events: list[TaskEvent] = []

    def record(self, event: TaskEvent) -> None:
        self._events.append(event)

    def for_task(self, task_id: str) -> list[TaskEvent]:
        return [event for event in self._events if event.task_id == task_id]

    def all(self) -> list[TaskEvent]:
        return list(self._events)
