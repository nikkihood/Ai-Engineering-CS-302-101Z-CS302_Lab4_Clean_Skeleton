# Dependency Rule: Interface adapters implement output boundaries and expose a view model to frameworks.

from transcript_requester.interface_adapters.view_models.request_transcript_view_model import (
    RequestTranscriptViewModel,
)
from transcript_requester.use_cases.ports.request_transcript_output_boundary import (
    RequestTranscriptOutputBoundary,
)
from transcript_requester.use_cases.request_transcript import RequestTranscriptOutput


class RequestTranscriptPresenter(RequestTranscriptOutputBoundary):
    def __init__(self) -> None:
        self._view_model: RequestTranscriptViewModel | None = None

    @property
    def view_model(self) -> RequestTranscriptViewModel | None:
        return self._view_model

    def present_success(self, output_data: RequestTranscriptOutput) -> None:
        self._view_model = RequestTranscriptViewModel(
            status_code=201,
            body={
                "id": output_data.id,
                "source_url": output_data.source_url,
                "requested_at": output_data.requested_at.isoformat(),
                "status": output_data.status,
                "answer": output_data.answer,
            },
        )

    def present_invalid_request(self, message: str) -> None:
        self._view_model = RequestTranscriptViewModel(
            status_code=400,
            body={"error": message},
        )

    def present_malformed_model_response(self, message: str) -> None:
        self._view_model = RequestTranscriptViewModel(
            status_code=502,
            body={"error": message},
        )

    def present_guardrail_failure(self, policy_violation: str) -> None:
        self._view_model = RequestTranscriptViewModel(
            status_code=202,
            body={
                "status": "human_review_required",
                "next_step": "human",
                "policy_violation": policy_violation,
            },
        )
