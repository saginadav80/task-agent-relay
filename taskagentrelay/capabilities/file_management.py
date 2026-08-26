from __future__ import annotations

from pathlib import Path
from typing import Any


class FileCapabilityError(ValueError):
    pass


def _safe_path(path: str, workspace: Path) -> Path:
    if not path or Path(path).is_absolute():
        raise FileCapabilityError("path must be a non-empty relative path")
    candidate = (workspace / path).resolve()
    try:
        candidate.relative_to(workspace)
    except ValueError as exc:
        raise FileCapabilityError("path escapes the configured workspace") from exc
    return candidate


def read_file(parameters: dict[str, Any], *, workspace: Path) -> dict[str, Any]:
    path = _safe_path(str(parameters.get("path", "")), workspace)
    if not path.is_file():
        raise FileCapabilityError(f"file does not exist: {parameters.get('path')}")
    content = path.read_text(encoding="utf-8")
    return {"path": str(path.relative_to(workspace)), "content": content, "size_bytes": len(content.encode('utf-8'))}


def write_file(parameters: dict[str, Any], *, workspace: Path) -> dict[str, Any]:
    path_value = str(parameters.get("path", ""))
    path = _safe_path(path_value, workspace)
    content = str(parameters.get("content", ""))
    mode = str(parameters.get("mode", "create"))
    if mode not in {"create", "overwrite", "upsert"}:
        raise FileCapabilityError(f"unsupported write mode: {mode}")
    if mode == "create" and path.exists():
        raise FileCapabilityError(f"file already exists: {path_value}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return {"path": str(path.relative_to(workspace)), "size_bytes": len(content.encode('utf-8')), "mode": mode}


def list_files(parameters: dict[str, Any], *, workspace: Path) -> dict[str, Any]:
    relative = str(parameters.get("path", ""))
    directory = workspace if not relative else _safe_path(relative, workspace)
    if not directory.is_dir():
        raise FileCapabilityError(f"directory does not exist: {relative}")
    recursive = bool(parameters.get("recursive", False))
    entries = directory.rglob("*") if recursive else directory.iterdir()
    files = sorted(str(item.relative_to(workspace)) for item in entries if item.is_file())
    return {"path": relative, "files": files}


def delete_file(parameters: dict[str, Any], *, workspace: Path) -> dict[str, Any]:
    path_value = str(parameters.get("path", ""))
    path = _safe_path(path_value, workspace)
    if not path.is_file():
        raise FileCapabilityError(f"file does not exist: {path_value}")
    path.unlink()
    return {"path": path_value, "deleted": True}
