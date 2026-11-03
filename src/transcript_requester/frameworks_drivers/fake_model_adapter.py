# Dependency Rule: Frameworks and drivers provide test doubles for inner-layer ports.

from collections.abc import Mapping

from transcript_requester.use_cases.ports.model_gateway import (
    ModelGateway,
    ModelResponse,
)


class FakeModelAdapter(ModelGateway):
    HAPPY_PATH = "happy_path"
    MALFORMED_ANSWER = "malformed_answer"
    GUARDRAIL_TRIPPING_ANSWER = "guardrail_tripping_answer"

    _DEFAULT_RESPONSES: Mapping[str, ModelResponse] = {
        HAPPY_PATH: ModelResponse(
            content='{"answer":"The requested transcript is ready.","status":"complete"}'
        ),
        MALFORMED_ANSWER: ModelResponse(
            content='{"answer":"The requested transcript is ready."'
        ),
        GUARDRAIL_TRIPPING_ANSWER: ModelResponse(
            content="I cannot provide that restricted content.",
            finish_reason="guardrail",
            metadata={
                "policy_violation": "restricted_content",
                "off_ramp": True,
            },
        ),
    }

    def __init__(
        self,
        responses: Mapping[str, ModelResponse] | None = None,
    ) -> None:
        self._responses = dict(self._DEFAULT_RESPONSES)
        if responses is not None:
            self._responses.update(responses)

    def complete(
        self,
        prompt: str,
        *,
        scenario: str | None = None,
    ) -> ModelResponse:
        key = scenario or self._scenario_from_prompt(prompt)
        try:
            return self._responses[key]
        except KeyError as error:
            raise ValueError(f"Unknown fake model scenario: {key}") from error

    @staticmethod
    def _scenario_from_prompt(prompt: str) -> str:
        normalized_prompt = prompt.strip().lower()
        if normalized_prompt in {
            FakeModelAdapter.HAPPY_PATH,
            "happy path",
        }:
            return FakeModelAdapter.HAPPY_PATH
        if normalized_prompt in {
            FakeModelAdapter.MALFORMED_ANSWER,
            "malformed answer",
        }:
            return FakeModelAdapter.MALFORMED_ANSWER
        if normalized_prompt in {
            FakeModelAdapter.GUARDRAIL_TRIPPING_ANSWER,
            "guardrail-tripping answer",
        }:
            return FakeModelAdapter.GUARDRAIL_TRIPPING_ANSWER
        return FakeModelAdapter.HAPPY_PATH
