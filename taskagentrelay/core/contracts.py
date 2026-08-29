from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable

from .models import Capability, ExecutionRequest, ExecutionResult, Implementation, Task


class TaskSource(ABC):
    """Adapter that converts an external source item into a canonical Task."""

    name: str

    @abstractmethod
    def receive(self, payload: dict[str, Any]) -> Task:
        raise NotImplementedError


class Runner(ABC):
    """Execution backend for an implementation."""

    name: str

    @abstractmethod
    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        raise NotImplementedError


class Agent(ABC):
    """Planner/decision layer. v0.1 intentionally supports one implementation."""

    name: str

    @abstractmethod
    def select_capability(self, task: Task, available: Iterable[Capability]) -> Capability:
        raise NotImplementedError

    @abstractmethod
    def select_implementation(
        self,
        task: Task,
        capability: Capability,
        available: Iterable[Implementation],
    ) -> Implementation:
        raise NotImplementedError
