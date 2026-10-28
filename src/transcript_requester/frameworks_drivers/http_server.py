# Dependency Rule: Frameworks and drivers contain transport-specific code and depend inward on application policies.

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from transcript_requester.frameworks_drivers.composition_root import (
    request_transcript_controller,
)


class TranscriptRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        if self.path != "/transcript-requests":
            self._send_json(404, {"error": "Not found"})
            return

        try:
            body = self._read_json_body()
        except ValueError as error:
            self._send_json(400, {"error": str(error)})
            return

        view_model = request_transcript_controller.handle(body)
        self._send_json(view_model.status_code, view_model.body)

    def _read_json_body(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)

        try:
            body = json.loads(raw_body)
        except json.JSONDecodeError as error:
            raise ValueError("Invalid JSON body") from error

        if not isinstance(body, dict):
            raise ValueError("JSON body must be an object")

        return body

    def _send_json(self, status_code: int, body: dict[str, Any]) -> None:
        encoded_body = json.dumps(body).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded_body)))
        self.end_headers()
        self.wfile.write(encoded_body)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    server = HTTPServer(("localhost", 8000), TranscriptRequestHandler)
    print("Transcript requester listening on http://localhost:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
