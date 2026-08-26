# TaskAgentRelay

> Agent-powered task execution for tasks ordinary automation cannot complete on its own.

TaskAgentRelay receives tasks from different sources, resolves the required capability and implementation, and executes the work through an appropriate runner.

## v0.1 architecture

```text
External System
      ↕
   Adapter
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
   Result
      ↕
   Adapter
```

An Adapter is the boundary between TaskAgentRelay and an external system. A single Adapter may ingest Tasks, query external information, and publish results or status. GitHub is one possible Adapter; n8n can be another. Neither is part of the Core model.

## Current v0.1 slice

The first slice is deliberately small:

- Canonical Task model and lifecycle.
- Webhook and GitHub source adapters.
- Direct Agent implementation.
- Capability and Implementation registry.
- Local Runner with workspace isolation.
- File Management capabilities: `read_file`, `write_file`, `list_files`, `delete_file`.
- Approval gate for write/delete operations.
- In-memory state plus optional PostgreSQL persistence.
- Event recording.
- CLI: `doctor`, `capabilities`, `run`.
- Unit/integration test coverage.

## Quick start

Python 3.11+ is required.

```bash
python -m pip install -e '.[test]'
pytest
```

Diagnostics:

```bash
taskagentrelay doctor
```

Capabilities:

```bash
taskagentrelay capabilities
```

Run a task in the default workspace:

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

## Project structure

```text
core/            task lifecycle, orchestration, registries, storage
sources/         internal adapters that turn external inputs into Tasks (legacy v0.1 location)
adapters/        external-system boundaries planned as the public modular integration surface
capabilities/    things TaskAgentRelay can do
runners/         execution backends
packages/        distributable capability packages
contracts/       machine-readable contracts
cli/             user-facing administration and execution
```

The `sources/` directory is retained for the v0.1 implementation. New external-system packaging should use the `adapters/` model defined in `docs/architecture/adr-0001-external-adapters.md`.

## Roadmap

See `docs/ROADMAP.md` for the evolution from v0.1 to v1.0.
