from __future__ import annotations

from dataclasses import dataclass, field

from .models import Capability, Implementation


@dataclass
class Registry:
    capabilities: dict[str, Capability] = field(default_factory=dict)
    implementations: dict[str, Implementation] = field(default_factory=dict)

    def register_capability(self, capability: Capability) -> None:
        key = capability.id
        if key in self.capabilities:
            raise ValueError(f"Capability already registered: {key}")
        self.capabilities[key] = capability

    def register_implementation(self, implementation: Implementation) -> None:
        key = implementation.id
        if key in self.implementations:
            raise ValueError(f"Implementation already registered: {key}")
        if implementation.capability not in self.capabilities:
            raise ValueError(
                f"Implementation references unknown capability: {implementation.capability}"
            )
        self.implementations[key] = implementation

    def get_capability(self, capability_id: str) -> Capability:
        try:
            return self.capabilities[capability_id]
        except KeyError as exc:
            raise KeyError(f"Unknown capability: {capability_id}") from exc

    def implementations_for(self, capability_id: str) -> list[Implementation]:
        return [
            item for item in self.implementations.values()
            if item.capability == capability_id
        ]
