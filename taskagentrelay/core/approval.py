from __future__ import annotations

from dataclasses import dataclass

from .models import Capability, Task


class ApprovalRequired(RuntimeError):
    def __init__(self, task_id: str, capability: str) -> None:
        super().__init__(f"Approval required for task {task_id!r} using capability {capability!r}")
        self.task_id = task_id
        self.capability = capability


@dataclass(slots=True)
class ApprovalPolicy:
    auto_approve: bool = False

    def check(self, task: Task, capability: Capability) -> None:
        if capability.requires_approval and not self.auto_approve:
            raise ApprovalRequired(task.id, capability.id)
