from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

from ..core.contracts import Runner
from ..core.models import ExecutionRequest, ExecutionResult


class LocalRunner(Runner):
    """Runs a declared Python entrypoint in the local process."""

    name = "local"

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace).expanduser().resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        module_name, function_name = request.implementation.entrypoint.split(":", 1)
        try:
            module = importlib.import_module(module_name)
            func = getattr(module, function_name)
            value: Any = func(request.task.parameters, workspace=self.workspace)
            return ExecutionResult(state="completed", result=value)
        except Exception as exc:  # noqa: BLE001 - runner boundary converts failures to results
            return ExecutionResult(
                state="failed",
                error={
                    "code": "EXECUTION_ERROR",
                    "message": str(exc),
                    "type": type(exc).__name__,
                    "retryable": False,
                },
            )
