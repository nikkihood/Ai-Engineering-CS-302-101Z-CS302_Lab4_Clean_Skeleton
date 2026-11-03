# Dependency Rule: Use cases depend on model abstractions, not concrete providers.

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class ModelResponse:
    content: str
    finish_reason: str = "stop"
    metadata: dict[str, Any] = field(default_factory=dict)


class ModelGateway(Protocol):
    def complete(
        self,
        prompt: str,
        *,
        scenario: str | None = None,
    ) -> ModelResponse:
        ...
