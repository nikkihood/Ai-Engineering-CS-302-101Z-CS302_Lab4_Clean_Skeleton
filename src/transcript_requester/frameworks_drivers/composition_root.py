# Dependency Rule: Frameworks and drivers compose concrete implementations around inner-layer policies.

from datetime import datetime, timezone
from uuid import uuid4

from transcript_requester.frameworks_drivers.persistence.in_memory_transcript_request_gateway import (
    InMemoryTranscriptRequestGateway,
)
from transcript_requester.interface_adapters.controllers.request_transcript_controller import (
    RequestTranscriptController,
)
from transcript_requester.use_cases.request_transcript import RequestTranscript


gateway = InMemoryTranscriptRequestGateway()

request_transcript = RequestTranscript(
    gateway=gateway,
    create_id=lambda: str(uuid4()),
    now=lambda: datetime.now(timezone.utc),
)

request_transcript_controller = RequestTranscriptController(
    request_transcript=request_transcript,
)
