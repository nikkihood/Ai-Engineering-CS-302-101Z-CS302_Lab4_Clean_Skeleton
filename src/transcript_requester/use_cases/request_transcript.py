# Dependency Rule: Use cases must not depend on interface adapters, frameworks, databases, or transport details.

from dataclasses import dataclass
from datetime import datetime
from typing import Callable

from transcript_requester.entities.transcript_request import (
    TranscriptRequest,
    create_transcript_request,
)
from transcript_requester.use_cases.ports.transcript_request_gateway import (
    TranscriptRequestGateway,
)


@dataclass(frozen=True, slots=True)
class RequestTranscriptInput:
    source_url: str


class RequestTranscript:
    def __init__(
        self,
        gateway: TranscriptRequestGateway,
        create_id: Callable[[], str],
        now: Callable[[], datetime],
    ) -> None:
        self._gateway = gateway
        self._create_id = create_id
        self._now = now

    def execute(
        self,
        input_data: RequestTranscriptInput,
    ) -> TranscriptRequest:
        request = create_transcript_request(
            request_id=self._create_id(),
            source_url=input_data.source_url,
            requested_at=self._now(),
        )

        self._gateway.save(request)

        return request
