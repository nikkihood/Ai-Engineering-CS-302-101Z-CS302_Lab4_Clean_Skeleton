from datetime import datetime, timezone
import unittest

from transcript_requester.interface_adapters.presenters.request_transcript_presenter import (
    RequestTranscriptPresenter,
)
from transcript_requester.use_cases.request_transcript import RequestTranscriptOutput


class RequestTranscriptPresenterTests(unittest.TestCase):
    def test_success_output_is_shaped_for_the_application_boundary(self) -> None:
        presenter = RequestTranscriptPresenter()

        presenter.present_success(
            RequestTranscriptOutput(
                id="req-123",
                source_url="https://example.com/video",
                requested_at=datetime(
                    2026, 10, 28, 12, 0, tzinfo=timezone.utc
                ),
                status="requested",
                answer="The requested transcript is ready.",
            )
        )

        self.assertEqual(201, presenter.view_model.status_code)
        self.assertEqual(
            "2026-10-28T12:00:00+00:00",
            presenter.view_model.body["requested_at"],
        )
        self.assertEqual(
            "The requested transcript is ready.",
            presenter.view_model.body["answer"],
        )

    def test_invalid_request_output_contains_a_client_error(self) -> None:
        presenter = RequestTranscriptPresenter()

        presenter.present_invalid_request("source_url is required")

        self.assertEqual(400, presenter.view_model.status_code)
        self.assertEqual(
            {"error": "source_url is required"},
            presenter.view_model.body,
        )

    def test_guardrail_output_requests_human_review(self) -> None:
        presenter = RequestTranscriptPresenter()

        presenter.present_guardrail_failure("restricted_content")

        self.assertEqual(202, presenter.view_model.status_code)
        self.assertEqual("human_review_required", presenter.view_model.body["status"])
        self.assertEqual("human", presenter.view_model.body["next_step"])


if __name__ == "__main__":
    unittest.main()
