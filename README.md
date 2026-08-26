# TaskAgentRelay

> Agent-powered task execution for tasks that ordinary automation cannot complete on its own.

TaskAgentRelay receives tasks from external sources, resolves the required capability and implementation, and executes that work through an appropriate runner.

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
Result
```

GitHub is one possible task source. n8n is an integration/backend, not the system model.

## Current status

This branch contains the first Core MVP skeleton:

- Canonical Task model.
- Source contract.
- Agent contract.
- Capability and Implementation contracts.
- Runner contract.
- Capability/Implementation registry.
- Minimal orchestrator.
- Safe placeholder runner.
- Core smoke tests.

The first real capability will be local file management.
