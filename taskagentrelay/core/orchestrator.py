from __future__ import annotations

from dataclasses import dataclass

from .contracts import Agent, Runner
from .models import ExecutionRequest, ExecutionResult, Task
from .registry import Registry


@dataclass
class Orchestrator:
    registry: Registry
    agent: Agent
    runner: Runner

    def run(self, task: Task) -> ExecutionResult:
        capability = self.agent.select_capability(task, self.registry.capabilities.values())
        if capability.id != task.capability:
            raise ValueError(
                f"Agent selected capability {capability.id!r} for task requiring {task.capability!r}"
            )
        implementations = self.registry.implementations_for(capability.id)
        implementation = self.agent.select_implementation(task, capability, implementations)
        request = ExecutionRequest(task=task, capability=capability, implementation=implementation)
        return self.runner.execute(request)
