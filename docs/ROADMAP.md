# TaskAgentRelay Roadmap

## v0.1 — usable core

- Canonical Task model and lifecycle.
- Source adapters for Webhook and GitHub-shaped payloads.
- One direct Agent implementation.
- Capability and Implementation registries.
- Local Runner with workspace isolation.
- File capabilities: read/write/list/delete.
- Approval gate for write/delete.
- In-memory store plus optional PostgreSQL store.
- Event recording.
- CLI: `doctor`, `capabilities`, `run`.
- Unit/integration tests.
- Clean-install documentation.

## v0.2 — extensibility

- Formal package manifests and installation lifecycle.
- Capability discovery and versioning.
- Public `adapters/` model for external-system packages.
- Safer upgrade/uninstall handling.
- Additional practical capabilities and a scheduler source.

## v0.3 — execution targets

- Docker runner.
- SSH runner.
- Remote execution abstraction.
- Timeouts, cancellation, and bounded retries.
- Artifact handling.

## v0.4 — external adapters

- GitHub adapter with real event ingestion and result publishing.
- n8n adapter.
- Email adapter.
- Local task-file adapter.
- Generic REST/webhook adapter.
- Chat adapters where useful.

## v0.5 — agent improvements

- Better capability discovery and selection.
- Structured execution plans.
- Better failure interpretation.
- Human approval from multiple interfaces.

Multi-agent orchestration is intentionally deferred until a real use case requires it.

## v0.6+ — hardening and ecosystem

- Permission and sandboxing improvements.
- Secrets/credential isolation.
- SDK for third-party capabilities and adapters.
- Public package registry only after the local package model proves stable.
- Observability, backups, recovery, and production hardening.
