# Dependency Rule: Use cases may depend on entities and abstractions, but not adapters or frameworks.

from typing import Protocol

from transcript_requester.entities.transcript_request import TranscriptRequest


class TranscriptRequestGateway(Protocol):
    def save(self, request: TranscriptRequest) -> None:
        ...

    def find_by_id(self, request_id: str) -> TranscriptRequest | None:
        ...
