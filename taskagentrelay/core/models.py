from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping


TASK_STATES = {
    "received",
    "running",
    "awaiting_approval",
    "completed",
    "failed",
    "cancelled",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(slots=True)
class Task:
    id: str
    capability: str
    parameters: dict[str, Any] = field(default_factory=dict)
    source: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    state: str = "received"
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    result: Any = None
    error: dict[str, Any] | None = None
    artifacts: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Task id must not be empty")
        if not self.capability.strip():
            raise ValueError("Task capability must not be empty")
        if self.state not in TASK_STATES:
            raise ValueError(f"Unsupported task state: {self.state}")
        self.updated_at = utc_now()

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "Task":
        return cls(
            id=str(data["id"]),
            capability=str(data["capability"]),
            parameters=dict(data.get("parameters") or {}),
            source=str(data["source"]) if data.get("source") is not None else None,
            metadata=dict(data.get("metadata") or {}),
            state=str(data.get("state", "received")),
            created_at=str(data.get("created_at") or utc_now()),
            updated_at=str(data.get("updated_at") or utc_now()),
            result=data.get("result"),
            error=dict(data["error"]) if isinstance(data.get("error"), Mapping) else None,
            artifacts=list(data.get("artifacts") or []),
        )

    def to_mapping(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "capability": self.capability,
            "parameters": self.parameters,
            "source": self.source,
            "metadata": self.metadata,
            "state": self.state,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "result": self.result,
            "error": self.error,
            "artifacts": self.artifacts,
        }


@dataclass(frozen=True, slots=True)
class Capability:
    id: str
    version: str
    description: str
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    permissions: tuple[str, ...] = ()
    requires_approval: bool = False


@dataclass(frozen=True, slots=True)
class Implementation:
    id: str
    capability: str
    version: str
    runner: str
    entrypoint: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ExecutionRequest:
    task: Task
    capability: Capability
    implementation: Implementation


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    state: str
    result: Any = None
    error: dict[str, Any] | None = None
    artifacts: tuple[dict[str, Any], ...] = ()

    def __post_init__(self) -> None:
        if self.state not in TASK_STATES:
            raise ValueError(f"Unsupported execution state: {self.state}")
