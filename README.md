# TaskAgentRelay

> Agent-powered task execution for tasks ordinary automation cannot complete on its own.

TaskAgentRelay receives tasks from different sources, resolves the required capability and implementation, and executes the work through an appropriate runner.

## v0.1 architecture

```text
Task Source
    ↓
Task
    ↓
Agent
    ↓
Capability
    ↓
Implementation
    ↓
Runner
    ↓
Result / Events
```

GitHub is one possible task source. n8n is an integration/backend, not the system model.

## Current v0.1 slice

The first slice is deliberately small:

- Canonical Task model and lifecycle.
- Webhook and GitHub source adapters.
- Direct Agent implementation.
- Capability and Implementation registry.
- Local Runner with workspace isolation.
- File Management capabilities:
  - `read_file`
  - `write_file`
  - `list_files`
  - `delete_file`
- Approval gate for write/delete operations.
- In-memory state for fast local operation.
- Optional PostgreSQL persistence.
- Event recording.
- CLI and unit/integration test coverage.

## Quick start

Python 3.11+ is required.

```bash
python -m pip install -e '.[test]'
pytest
```

Run diagnostics:

```bash
taskagentrelay doctor
```

List capabilities:

```bash
taskagentrelay capabilities
```

Run the example task in the default workspace:

```bash
taskagentrelay run examples/tasks/write-file.json --approve
```

Use a dedicated workspace:

```bash
taskagentrelay run examples/tasks/write-file.json --workspace /tmp/taskagentrelay-workspace --approve
```

## Safety boundary

Local file operations are restricted to the configured workspace. Paths must be relative and cannot escape that workspace.

Approval is required for write/delete capabilities unless explicitly approved by the caller.

## Roadmap

See `docs/ROADMAP.md` for the planned evolution from v0.1 to v1.0.
