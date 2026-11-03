from datetime import datetime, timezone
import unittest

from transcript_requester.frameworks_drivers.fake_model_adapter import (
    FakeModelAdapter,
)
from transcript_requester.frameworks_drivers.testing_api import TestingApi
from transcript_requester.use_cases.request_transcript import RequestTranscriptInput


class RequestTranscriptUseCaseTests(unittest.TestCase):
    def _api(self) -> TestingApi:
        return TestingApi(
            create_id=lambda: "req-123",
            now=lambda: datetime(2026, 10, 28, 12, 0, tzinfo=timezone.utc),
        )

    def test_valid_source_url_produces_a_completed_transcript_request(self) -> None:
        view_model = self._api().request_transcript(
            RequestTranscriptInput(source_url="https://example.com/video")
        )

        self.assertEqual(201, view_model.status_code)
        self.assertEqual("req-123", view_model.body["id"])
        self.assertEqual(
            "The requested transcript is ready.",
            view_model.body["answer"],
        )
        self.assertEqual("requested", view_model.body["status"])

    def test_blank_source_url_is_rejected_before_model_processing(self) -> None:
        view_model = self._api().request_transcript(
            RequestTranscriptInput(source_url=" ")
        )

        self.assertEqual(400, view_model.status_code)
        self.assertEqual("source_url is required", view_model.body["error"])

    def test_malformed_model_answer_is_rejected_as_an_upstream_error(self) -> None:
        view_model = self._api().request_transcript(
            RequestTranscriptInput(
                source_url="https://example.com/video",
                model_scenario=FakeModelAdapter.MALFORMED_ANSWER,
            )
        )

        self.assertEqual(502, view_model.status_code)
        self.assertEqual(
            "Model response is not valid JSON",
            view_model.body["error"],
        )

    def test_guardrail_failure_off_ramps_request_to_human_review(self) -> None:
        view_model = self._api().request_transcript(
            RequestTranscriptInput(
                source_url="https://example.com/video",
                model_scenario=FakeModelAdapter.GUARDRAIL_TRIPPING_ANSWER,
            )
        )

        self.assertEqual(202, view_model.status_code)
        self.assertEqual("human_review_required", view_model.body["status"])
        self.assertEqual("human", view_model.body["next_step"])
        self.assertEqual(
            "restricted_content",
            view_model.body["policy_violation"],
        )


if __name__ == "__main__":
    unittest.main()
