from __future__ import annotations

from dataclasses import dataclass

from .approval import ApprovalPolicy, ApprovalRequired
from .contracts import Agent, Runner
from .events import EventRecorder, TaskEvent
from .models import ExecutionResult, Task
from .registry import Registry
from .storage import TaskStore


@dataclass(slots=True)
class TaskEngine:
    registry: Registry
    agent: Agent
    runner: Runner
    store: TaskStore
    approval: ApprovalPolicy
    events: EventRecorder

    def execute(self, task: Task) -> ExecutionResult:
        task.state = "running"
        self.store.save(task)
        self.events.record(TaskEvent(task.id, "task.started"))
        self.store.record_event(self.events.all()[-1])

        try:
            capability = self.agent.select_capability(task, self.registry.capabilities.values())
            implementation = self.agent.select_implementation(
                task, capability, self.registry.implementations_for(capability.id)
            )
            self.approval.check(task, capability)
            result = self.runner.execute(
                __import__("taskagentrelay.core.models", fromlist=["ExecutionRequest"]).ExecutionRequest(
                    task=task, capability=capability, implementation=implementation
                )
            )
        except ApprovalRequired as exc:
            task.state = "awaiting_approval"
            task.error = {"code": "APPROVAL_REQUIRED", "message": str(exc), "retryable": False}
            self.store.save(task)
            event = TaskEvent(task.id, "task.awaiting_approval", {"capability": exc.capability})
            self.events.record(event)
            self.store.record_event(event)
            return ExecutionResult(state="awaiting_approval", error=task.error)
        except Exception as exc:  # noqa: BLE001 - task boundary
            task.state = "failed"
            task.error = {"code": "TASK_ERROR", "message": str(exc), "type": type(exc).__name__, "retryable": False}
            self.store.save(task)
            event = TaskEvent(task.id, "task.failed", task.error)
            self.events.record(event)
            self.store.record_event(event)
            return ExecutionResult(state="failed", error=task.error)

        task.state = result.state
        task.result = result.result
        task.error = result.error
        task.artifacts = list(result.artifacts)
        self.store.save(task)
        event_name = "task.completed" if result.state == "completed" else "task.failed"
        event = TaskEvent(task.id, event_name, {"result": result.result, "error": result.error})
        self.events.record(event)
        self.store.record_event(event)
        return result
