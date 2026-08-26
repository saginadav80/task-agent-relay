from __future__ import annotations

from pathlib import Path

from .models import Capability, Implementation
from .registry import Registry


FILE_IMPLEMENTATIONS = {
    "read_file": "taskagentrelay.capabilities.file_management:read_file",
    "write_file": "taskagentrelay.capabilities.file_management:write_file",
    "list_files": "taskagentrelay.capabilities.file_management:list_files",
    "delete_file": "taskagentrelay.capabilities.file_management:delete_file",
}


def build_registry() -> Registry:
    registry = Registry()
    for capability_id, approval in (
        ("read_file", False),
        ("write_file", True),
        ("list_files", False),
        ("delete_file", True),
    ):
        registry.register_capability(
            Capability(
                id=capability_id,
                version="1.0.0",
                description=f"Local file capability: {capability_id}",
                permissions=("filesystem.read" if capability_id in {"read_file", "list_files"} else "filesystem.write",),
                requires_approval=approval,
            )
        )
        registry.register_implementation(
            Implementation(
                id=f"{capability_id}/local/v1",
                capability=capability_id,
                version="1.0.0",
                runner="local",
                entrypoint=FILE_IMPLEMENTATIONS[capability_id],
            )
        )
    return registry


def default_workspace() -> Path:
    return (Path.home() / ".taskagentrelay" / "workspace").resolve()
