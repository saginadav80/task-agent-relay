from __future__ import annotations

from typing import Iterable

from .contracts import Agent, Runner, TaskSource
from .models import Capability, ExecutionRequest, ExecutionResult, Task


class DefaultTaskSource(TaskSource):
    name = "default"

    def receive(self, payload: dict[str, object]) -> Task:
        return Task.from_mapping(payload)


class DirectAgent(Agent):
    name = "direct"

    def select_capability(self, task: Task, available: Iterable[Capability]) -> Capability:
        for capability in available:
            if capability.id == task.capability:
                return capability
        raise ValueError(f"Capability not available: {task.capability}")

    def select_implementation(self, task: Task, capability: Capability, available):
        for implementation in available:
            return implementation
        raise ValueError(f"No implementation available for capability: {capability.id}")


class RejectingRunner(Runner):
    """Safe v0.1 placeholder runner until local execution is implemented."""

    name = "rejecting"

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        return ExecutionResult(
            state="failed",
            error={
                "code": "RUNNER_NOT_IMPLEMENTED",
                "message": f"Runner {self.name!r} cannot execute {request.implementation.id!r}",
                "retryable": False,
            },
        )
