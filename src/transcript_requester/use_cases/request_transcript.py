# Dependency Rule: Use cases must not depend on interface adapters, frameworks, databases, or transport details.

from dataclasses import dataclass
from datetime import datetime
from typing import Callable

from transcript_requester.entities.transcript_request import (
    create_transcript_request,
)
from transcript_requester.use_cases.ports.request_transcript_input_boundary import (
    RequestTranscriptInputBoundary,
)
from transcript_requester.use_cases.ports.request_transcript_output_boundary import (
    RequestTranscriptOutputBoundary,
)
from transcript_requester.use_cases.ports.transcript_request_gateway import (
    TranscriptRequestGateway,
)


@dataclass(frozen=True, slots=True)
class RequestTranscriptInput:
    source_url: str


@dataclass(frozen=True, slots=True)
class RequestTranscriptOutput:
    id: str
    source_url: str
    requested_at: datetime
    status: str


class RequestTranscript(RequestTranscriptInputBoundary):
    def __init__(
        self,
        gateway: TranscriptRequestGateway,
        output_boundary: RequestTranscriptOutputBoundary,
        create_id: Callable[[], str],
        now: Callable[[], datetime],
    ) -> None:
        self._gateway = gateway
        self._output_boundary = output_boundary
        self._create_id = create_id
        self._now = now

    def execute(
        self,
        input_data: RequestTranscriptInput,
    ) -> None:
        try:
            request = create_transcript_request(
                request_id=self._create_id(),
                source_url=input_data.source_url,
                requested_at=self._now(),
            )
        except ValueError as error:
            self._output_boundary.present_invalid_request(str(error))
            return

        self._gateway.save(request)
        self._output_boundary.present_success(
            RequestTranscriptOutput(
                id=request.id,
                source_url=request.source_url,
                requested_at=request.requested_at,
                status=request.status,
            )
        )
