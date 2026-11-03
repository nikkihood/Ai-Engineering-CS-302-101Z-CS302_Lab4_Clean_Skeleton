# Ai-Engineering-CS-302-101Z-CS302_Lab4_Clean_Skeleton
Clean Architecture Python scaffold for requesting a transcript. Ai Engineering (CS-302-101Z), CS302 Lab 4.

## Requirements

- Python 3.11+

## Run the console round trip demo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m transcript_requester.frameworks_drivers.console_view
```

Enter a URL when prompted. The console view prints the presenter-produced view model.

## Testing API

`transcript_requester.frameworks_drivers.testing_api.TestingApi` is a test
driver at the outer edge of the architecture. It composes the in-memory
gateway, presenter, and use case, invokes the use case through its input
boundary, and returns the presenter-produced view model. It does not depend
on the console, a view, or an HTTP/framework type.

Tests can force a starting state with `initial_requests` or `seed`:

```python
from transcript_requester.frameworks_drivers.testing_api import TestingApi
from transcript_requester.use_cases.request_transcript import RequestTranscriptInput

api = TestingApi(initial_requests=[])
view_model = api.request_transcript(
    RequestTranscriptInput(source_url="https://example.com/video")
)
```

## Optional HTTP entry point

```bash
python -m transcript_requester.frameworks_drivers.http_server
```
