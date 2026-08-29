# Contributing to TaskAgentRelay

Thank you for contributing.

TaskAgentRelay is intentionally small in its early versions. Contributions are welcome, but preserving clear architecture and keeping the core understandable is more important than adding features quickly.

## Where to send things

- **Bug:** open a Bug Report issue.
- **Feature idea:** open a Feature Request issue before starting large implementation work.
- **Question or design discussion:** open a Discussion/Question issue.
- **Code contribution:** submit a pull request.
- **Security vulnerability:** follow `SECURITY.md`; do not disclose security-sensitive details in a public issue.

## Before opening a pull request

1. Explain the problem the change solves.
2. Keep the change focused.
3. Preserve the separation between Sources, Tasks, Capabilities, Implementations, Runners, and Integrations.
4. Add or update tests for behavior that changed.
5. Update documentation when the public behavior or architecture changes.
6. Do not add a new framework, service, or abstraction unless the change has a clear v0.x use case.

## Architecture rule

A useful contribution should fit this flow without coupling unrelated layers:

```text
Source → Task → Agent → Capability → Implementation → Runner → Result
```

## Pull requests

Pull requests are reviewed for correctness, scope, architecture, and maintainability. A technically good change may still be declined if it is outside the current roadmap or creates unnecessary complexity.

Please do not assume that opening a pull request means the feature will be merged.

## Development

The project targets Python 3.11+.

```bash
python -m pip install -e '.[test]'
pytest
```

Run the local diagnostics with:

```bash
taskagentrelay doctor
```
