import unittest

from transcript_requester.frameworks_drivers.fake_model_adapter import (
    FakeModelAdapter,
)
from transcript_requester.use_cases.ports.model_gateway import ModelResponse


class FakeModelAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = FakeModelAdapter()

    def test_happy_path_returns_valid_success_response(self) -> None:
        response = self.adapter.complete(
            "unused prompt",
            scenario=FakeModelAdapter.HAPPY_PATH,
        )

        self.assertEqual("stop", response.finish_reason)
        self.assertEqual(
            '{"answer":"The requested transcript is ready.","status":"complete"}',
            response.content,
        )
        self.assertEqual({}, response.metadata)

    def test_malformed_answer_returns_invalid_format(self) -> None:
        response = self.adapter.complete("malformed answer")

        self.assertIn('"answer"', response.content)
        self.assertFalse(response.content.endswith("}"))
        self.assertEqual("stop", response.finish_reason)

    def test_guardrail_answer_contains_off_ramp_metadata(self) -> None:
        response = self.adapter.complete(
            "unused prompt",
            scenario=FakeModelAdapter.GUARDRAIL_TRIPPING_ANSWER,
        )

        self.assertEqual("guardrail", response.finish_reason)
        self.assertTrue(response.metadata["off_ramp"])
        self.assertEqual(
            "restricted_content",
            response.metadata["policy_violation"],
        )

    def test_custom_scripted_response_is_in_memory(self) -> None:
        adapter = FakeModelAdapter(
            responses={
                "custom": ModelResponse(
                    content='{"answer":"scripted"}',
                    metadata={"scripted": True},
                )
            }
        )
        response = adapter.complete("custom", scenario="custom")

        self.assertEqual({"scripted": True}, response.metadata)


if __name__ == "__main__":
    unittest.main()
