from __future__ import annotations

from typing import Any

from ..core.contracts import TaskSource
from ..core.models import Task


class WebhookSource(TaskSource):
    name = "webhook"

    def receive(self, payload: dict[str, Any]) -> Task:
        return Task.from_mapping({**payload, "source": payload.get("source", self.name)})
