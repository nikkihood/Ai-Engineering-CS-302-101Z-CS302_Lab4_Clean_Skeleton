# Dependency Rule: Frameworks and drivers may depend on every inner layer, but inner layers never depend on them.

from transcript_requester.entities.transcript_request import TranscriptRequest


class InMemoryTranscriptRequestGateway:
    def __init__(self) -> None:
        self._requests: dict[str, TranscriptRequest] = {}

    def save(self, request: TranscriptRequest) -> None:
        self._requests[request.id] = request

    def find_by_id(self, request_id: str) -> TranscriptRequest | None:
        return self._requests.get(request_id)
