from datetime import datetime, timezone
import unittest

from transcript_requester.entities.transcript_request import TranscriptRequest
from transcript_requester.frameworks_drivers.testing_api import TestingApi
from transcript_requester.use_cases.request_transcript import RequestTranscriptInput


class TestingApiTests(unittest.TestCase):
    def test_seed_replaces_the_use_case_starting_state(self) -> None:
        request = TranscriptRequest(
            id="existing",
            source_url="https://example.com/existing",
            requested_at=datetime(2026, 10, 27, tzinfo=timezone.utc),
        )
        api = TestingApi(initial_requests=[request])

        api.seed([])
        view_model = api.request_transcript(
            RequestTranscriptInput(source_url=" ")
        )

        self.assertEqual(400, view_model.status_code)


if __name__ == "__main__":
    unittest.main()
