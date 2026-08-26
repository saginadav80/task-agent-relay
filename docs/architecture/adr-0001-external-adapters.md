# ADR-0001: External systems are represented by adapters

- Status: Accepted
- Date: 2026-08-26

## Context

TaskAgentRelay needs to communicate with external systems such as GitHub, n8n, Telegram, Slack, email services, and generic HTTP endpoints.

A single external system can play more than one role. For example, GitHub can provide incoming events that become Tasks, supply data that TaskAgentRelay queries, and receive updates after execution. Modeling these as separate top-level concepts such as `Source`, `Integration`, and `Connector Action` would force users and maintainers to reason about artificial boundaries.

## Decision

Use **Adapter** as the top-level architectural concept for communication with external systems.

An Adapter is the boundary between TaskAgentRelay and one external system or protocol. It may expose one or more behaviors, including:

- inbound task ingestion;
- querying external information;
- publishing execution results or status;
- other protocol-specific communication required by the integration.

The internal TaskAgentRelay pipeline remains explicit:

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
      ↕
External System
```

`Source` remains a useful internal concept for the specific behavior that converts external input into a canonical `Task`. It is not the user-facing packaging concept.

`Integration` is no longer a top-level architectural concept for the project. `Connector Action` and `Connector Operation` are also not architectural concepts.

## Consequences

- Users install or enable one adapter when they want to connect to an external system.
- The same adapter can support inbound and outbound communication without duplicating installation concepts.
- The Core remains independent from external services.
- Adapter-specific behavior stays outside the Core and communicates through stable contracts.
- The v0.1 Source abstraction can remain in place while future external packages move under an `adapters/` structure.

## Examples

```text
adapters/github/
adapters/n8n/
adapters/telegram/
adapters/slack/
adapters/email/
```

A GitHub adapter could provide:

```text
Issue/event → Task
Repository/issue query → external data
Result → comment / label / status update
```

The first implementation does not need to expose every behavior. Adapters should grow only as real use cases justify them.
