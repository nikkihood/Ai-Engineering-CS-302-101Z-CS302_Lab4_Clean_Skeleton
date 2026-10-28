from datetime import datetime, timezone
import unittest

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


class RequestTranscriptRoundTripTests(unittest.TestCase):
    def _build_controller(self) -> tuple[
        RequestTranscriptController,
        InMemoryTranscriptRequestGateway,
    ]:
        gateway = InMemoryTranscriptRequestGateway()
        presenter = RequestTranscriptPresenter()
        interactor = RequestTranscript(
            gateway=gateway,
            output_boundary=presenter,
            create_id=lambda: "req-123",
            now=lambda: datetime(2026, 10, 28, 12, 0, tzinfo=timezone.utc),
        )
        return (
            RequestTranscriptController(
                request_transcript=interactor,
                presenter=presenter,
            ),
            gateway,
        )

    def test_full_round_trip_to_view_model(self) -> None:
        controller, gateway = self._build_controller()

        view_model = controller.handle(
            {"source_url": "https://example.com/video"}
        )

        self.assertEqual(201, view_model.status_code)
        self.assertEqual("req-123", view_model.body["id"])
        self.assertEqual(
            "https://example.com/video",
            view_model.body["source_url"],
        )
        self.assertEqual("requested", view_model.body["status"])
        self.assertEqual(
            "2026-10-28T12:00:00+00:00",
            view_model.body["requested_at"],
        )
        self.assertIsNotNone(gateway.find_by_id("req-123"))

    def test_validation_behavior(self) -> None:
        controller, gateway = self._build_controller()

        type_error_view_model = controller.handle({"source_url": 123})
        empty_error_view_model = controller.handle({"source_url": " "})

        self.assertEqual(400, type_error_view_model.status_code)
        self.assertEqual(
            "source_url must be a string",
            type_error_view_model.body["error"],
        )
        self.assertEqual(400, empty_error_view_model.status_code)
        self.assertEqual(
            "source_url is required",
            empty_error_view_model.body["error"],
        )
        self.assertIsNone(gateway.find_by_id("req-123"))


if __name__ == "__main__":
    unittest.main()
