# Dependency Rule: Use-case helpers contain application-level parsing policy.

import json


class ModelAnswerParser:
    @staticmethod
    def parse(content: str) -> str:
        try:
            response = json.loads(content)
        except json.JSONDecodeError as error:
            raise ValueError("Model response is not valid JSON") from error

        if not isinstance(response, dict) or not isinstance(
            response.get("answer"), str
        ):
            raise ValueError("Model response must include an answer")

        return response["answer"]
