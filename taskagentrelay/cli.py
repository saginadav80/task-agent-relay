from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core.approval import ApprovalPolicy
from .core.bootstrap import build_registry, default_workspace
from .core.defaults import DirectAgent
from .core.engine import TaskEngine
from .core.events import EventRecorder
from .core.models import Task
from .core.storage import InMemoryTaskStore
from .runners.local import LocalRunner


def build_engine(workspace: str | None, approve: bool = False) -> TaskEngine:
    root = Path(workspace).expanduser() if workspace else default_workspace()
    return TaskEngine(
        registry=build_registry(),
        agent=DirectAgent(),
        runner=LocalRunner(root),
        store=InMemoryTaskStore(),
        approval=ApprovalPolicy(auto_approve=approve),
        events=EventRecorder(),
    )


def cmd_doctor(_: argparse.Namespace) -> int:
    workspace = default_workspace()
    workspace.mkdir(parents=True, exist_ok=True)
    registry = build_registry()
    print("TaskAgentRelay Doctor")
    print("Core: OK")
    print(f"Capabilities: {len(registry.capabilities)}")
    print("Local runner: OK")
    print(f"Workspace: {workspace}")
    return 0


def cmd_list_capabilities(_: argparse.Namespace) -> int:
    for capability in build_registry().capabilities.values():
        approval = "approval" if capability.requires_approval else "no-approval"
        print(f"{capability.id}\t{capability.version}\t{approval}\t{capability.description}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    payload = json.loads(Path(args.file).read_text(encoding="utf-8"))
    task = Task.from_mapping(payload)
    engine = build_engine(args.workspace, approve=args.approve)
    result = engine.execute(task)
    print(json.dumps({"task": task, "result": result}, default=lambda value: value.__dict__, indent=2, ensure_ascii=False))
    return 0 if result.state in {"completed", "awaiting_approval"} else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="taskagentrelay")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Run local health checks")
    doctor.set_defaults(func=cmd_doctor)

    caps = sub.add_parser("capabilities", help="List available capabilities")
    caps.set_defaults(func=cmd_list_capabilities)

    run = sub.add_parser("run", help="Run a Task JSON file")
    run.add_argument("file")
    run.add_argument("--workspace")
    run.add_argument("--approve", action="store_true", help="Approve capabilities that require human approval")
    run.set_defaults(func=cmd_run)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
