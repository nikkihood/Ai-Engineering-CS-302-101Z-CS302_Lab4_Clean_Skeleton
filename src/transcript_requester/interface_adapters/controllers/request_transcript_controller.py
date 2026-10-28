# Dependency Rule: Interface adapters depend inward on use cases and entities, never the reverse.

from typing import Any

from transcript_requester.interface_adapters.presenters.request_transcript_presenter import (
    RequestTranscriptPresenter,
)
from transcript_requester.interface_adapters.view_models.request_transcript_view_model import (
    RequestTranscriptViewModel,
)
from transcript_requester.use_cases.ports.request_transcript_input_boundary import (
    RequestTranscriptInputBoundary,
)
from transcript_requester.use_cases.request_transcript import (
    RequestTranscriptInput,
)


class RequestTranscriptController:
    def __init__(
        self,
        request_transcript: RequestTranscriptInputBoundary,
        presenter: RequestTranscriptPresenter,
    ) -> None:
        self._request_transcript = request_transcript
        self._presenter = presenter

    def handle(
        self,
        body: dict[str, Any],
    ) -> RequestTranscriptViewModel:
        source_url = body.get("source_url")

        if not isinstance(source_url, str):
            return RequestTranscriptViewModel(
                status_code=400,
                body={"error": "source_url must be a string"},
            )

        self._request_transcript.execute(
            RequestTranscriptInput(source_url=source_url)
        )

        view_model = self._presenter.view_model
        if view_model is None:
            return RequestTranscriptViewModel(
                status_code=500,
                body={"error": "No response view model produced"},
            )

        return view_model
