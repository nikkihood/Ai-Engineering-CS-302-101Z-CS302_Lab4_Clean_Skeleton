# Dependency Rule: Use cases define output boundaries as abstractions implemented by interface adapters.

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from transcript_requester.use_cases.request_transcript import RequestTranscriptOutput


class RequestTranscriptOutputBoundary(Protocol):
    def present_success(self, output_data: "RequestTranscriptOutput") -> None:
        ...

    def present_invalid_request(self, message: str) -> None:
        ...
