from __future__ import annotations

from typing import Any, Mapping

from ..core.contracts import TaskSource
from ..core.models import Task


class GitHubSource(TaskSource):
    """Maps a GitHub Issue-like payload into the canonical Task model.

    Network access is intentionally outside this adapter in v0.1. A GitHub
    integration can fetch an issue and pass its JSON payload here.
    """

    name = "github"

    def receive(self, payload: dict[str, Any]) -> Task:
        body = str(payload.get("body") or "")
        labels = [item.get("name") for item in payload.get("labels", []) if isinstance(item, Mapping)]
        capability = str(payload.get("capability") or "")
        if not capability:
            raise ValueError("GitHub task payload must include capability")
        return Task(
            id=f"github:{payload.get('id') or payload.get('number') or 'unknown'}",
            capability=capability,
            parameters=dict(payload.get("parameters") or {}),
            source=self.name,
            metadata={
                "title": payload.get("title"),
                "body": body,
                "html_url": payload.get("html_url"),
                "labels": labels,
                "repository": payload.get("repository"),
            },
        )
