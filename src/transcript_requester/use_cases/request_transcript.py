# Dependency Rule: Use cases must not depend on interface adapters, frameworks, databases, or transport details.

from dataclasses import dataclass
from datetime import datetime
import json
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
from transcript_requester.use_cases.ports.model_gateway import ModelGateway
from transcript_requester.use_cases.ports.transcript_request_gateway import (
    TranscriptRequestGateway,
)


@dataclass(frozen=True, slots=True)
class RequestTranscriptInput:
    source_url: str
    model_scenario: str | None = None


@dataclass(frozen=True, slots=True)
class RequestTranscriptOutput:
    id: str
    source_url: str
    requested_at: datetime
    status: str
    answer: str


class RequestTranscript(RequestTranscriptInputBoundary):
    def __init__(
        self,
        gateway: TranscriptRequestGateway,
        model_gateway: ModelGateway,
        output_boundary: RequestTranscriptOutputBoundary,
        create_id: Callable[[], str],
        now: Callable[[], datetime],
    ) -> None:
        self._gateway = gateway
        self._model_gateway = model_gateway
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

        model_response = self._model_gateway.complete(
            input_data.source_url,
            scenario=input_data.model_scenario,
        )
        if model_response.finish_reason == "guardrail":
            self._output_boundary.present_guardrail_failure(
                str(
                    model_response.metadata.get(
                        "policy_violation",
                        "model safety policy",
                    )
                )
            )
            return

        try:
            answer = self._parse_model_answer(model_response.content)
        except ValueError as error:
            self._output_boundary.present_malformed_model_response(str(error))
            return

        self._gateway.save(request)
        self._output_boundary.present_success(
            RequestTranscriptOutput(
                id=request.id,
                source_url=request.source_url,
                requested_at=request.requested_at,
                status=request.status,
                answer=answer,
            )
        )

    @staticmethod
    def _parse_model_answer(content: str) -> str:
        try:
            response = json.loads(content)
        except json.JSONDecodeError as error:
            raise ValueError("Model response is not valid JSON") from error

        if not isinstance(response, dict) or not isinstance(
            response.get("answer"), str
        ):
            raise ValueError("Model response must include an answer")

        return response["answer"]
