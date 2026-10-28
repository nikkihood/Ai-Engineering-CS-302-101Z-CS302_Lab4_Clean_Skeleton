# Dependency Rule: Interface adapters shape use-case output into a view model for frameworks to display.

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RequestTranscriptViewModel:
    status_code: int
    body: dict[str, Any]
