# Dependency Rule: Frameworks and drivers compose concrete implementations around inner-layer policies.

from datetime import datetime, timezone
from uuid import uuid4

from transcript_requester.frameworks_drivers.persistence.in_memory_transcript_request_gateway import (
    InMemoryTranscriptRequestGateway,
)
from transcript_requester.interface_adapters.controllers.request_transcript_controller import (
    RequestTranscriptController,
)
from transcript_requester.interface_adapters.presenters.request_transcript_presenter import (
    RequestTranscriptPresenter,
)
from transcript_requester.use_cases.request_transcript import RequestTranscript


gateway = InMemoryTranscriptRequestGateway()
request_transcript_presenter = RequestTranscriptPresenter()

request_transcript = RequestTranscript(
    gateway=gateway,
    output_boundary=request_transcript_presenter,
    create_id=lambda: str(uuid4()),
    now=lambda: datetime.now(timezone.utc),
)

request_transcript_controller = RequestTranscriptController(
    request_transcript=request_transcript,
    presenter=request_transcript_presenter,
)
