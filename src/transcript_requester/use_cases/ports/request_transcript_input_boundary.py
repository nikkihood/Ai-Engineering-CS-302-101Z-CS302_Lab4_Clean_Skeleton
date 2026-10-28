# Dependency Rule: Use cases define input boundaries as abstractions for outer layers to call inward.

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from transcript_requester.use_cases.request_transcript import RequestTranscriptInput


class RequestTranscriptInputBoundary(Protocol):
    def execute(self, input_data: "RequestTranscriptInput") -> None:
        ...
