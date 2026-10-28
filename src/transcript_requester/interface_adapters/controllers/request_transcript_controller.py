# Dependency Rule: Interface adapters depend inward on use cases and entities, never the reverse.

from dataclasses import asdict
from typing import Any

from transcript_requester.use_cases.request_transcript import (
    RequestTranscript,
    RequestTranscriptInput,
)


class RequestTranscriptController:
    def __init__(self, request_transcript: RequestTranscript) -> None:
        self._request_transcript = request_transcript

    def handle(
        self,
        body: dict[str, Any],
    ) -> tuple[int, dict[str, Any]]:
        source_url = body.get("source_url")

        if not isinstance(source_url, str) or not source_url.strip():
            return 400, {"error": "source_url must be a non-empty string"}

        try:
            request = self._request_transcript.execute(
                RequestTranscriptInput(source_url=source_url)
            )
        except ValueError as error:
            return 400, {"error": str(error)}

        response = asdict(request)
        response["requested_at"] = request.requested_at.isoformat()

        return 201, response
