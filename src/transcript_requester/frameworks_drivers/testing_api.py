# Dependency Rule: Test drivers compose concrete adapters around application policies.

from collections.abc import Iterable
from datetime import datetime, timezone
from typing import Callable
from uuid import uuid4

from transcript_requester.entities.transcript_request import TranscriptRequest
from transcript_requester.frameworks_drivers.fake_model_adapter import (
    FakeModelAdapter,
)
from transcript_requester.frameworks_drivers.persistence.in_memory_transcript_request_gateway import (
    InMemoryTranscriptRequestGateway,
)
from transcript_requester.interface_adapters.presenters.request_transcript_presenter import (
    RequestTranscriptPresenter,
)
from transcript_requester.interface_adapters.view_models.request_transcript_view_model import (
    RequestTranscriptViewModel,
)
from transcript_requester.use_cases.request_transcript import (
    RequestTranscript,
    RequestTranscriptInput,
)


class TestingApi:
    """Drive use cases directly without a transport, view, or framework."""

    def __init__(
        self,
        *,
        create_id: Callable[[], str] = lambda: str(uuid4()),
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
        initial_requests: Iterable[TranscriptRequest] = (),
        model_adapter: FakeModelAdapter | None = None,
    ) -> None:
        self._gateway = InMemoryTranscriptRequestGateway()
        self._presenter = RequestTranscriptPresenter()
        self._model_adapter = model_adapter or FakeModelAdapter()
        self._request_transcript = RequestTranscript(
            gateway=self._gateway,
            model_gateway=self._model_adapter,
            output_boundary=self._presenter,
            create_id=create_id,
            now=now,
        )
        self.seed(initial_requests)

    def seed(self, requests: Iterable[TranscriptRequest]) -> None:
        """Replace the in-memory starting state used by subsequent calls."""
        self._gateway.seed(requests)

    def request_transcript(
        self,
        input_data: RequestTranscriptInput,
    ) -> RequestTranscriptViewModel:
        self._request_transcript.execute(input_data)

        view_model = self._presenter.view_model
        if view_model is None:
            raise RuntimeError("No response view model produced")
        return view_model
