# Constraint Audit Report

## Scope

Audited the use-case test suite, `TestingApi`, and the fake model adapter
against these constraints:

- no live API or network calls;
- all gateway dependencies are fake and in-memory;
- tests assert on view models, not UI, console, or HTTP output.

## Findings

### 1. No sneaky live model call found

`FakeModelAdapter.complete` only selects a `ModelResponse` from its in-memory
mapping (`src/transcript_requester/frameworks_drivers/fake_model_adapter.py`).
It imports no network client and performs no socket, subprocess, URL, or model
SDK call. `TestingApi` uses `InMemoryTranscriptRequestGateway` and constructs
`FakeModelAdapter` locally.

The test suite contains no imports of the console view, HTTP server, browser
automation, HTTP client, or live model SDK. The full suite passes without
starting a server or making network requests.

### 2. No UI/console assertions found

Use-case tests call `TestingApi.request_transcript` and assert on the returned
`RequestTranscriptViewModel` (`status_code` and `body`). Presenter tests call
`RequestTranscriptPresenter` directly and assert on its `view_model`.
No test captures stdout, enters console input, selects UI elements, or
asserts on HTTP responses.

### 3. Constraint loophole fixed

The previous `TestingApi` accepted an injectable model adapter. Although its
normal default was fake, that parameter could have been replaced with a live
adapter and violated the test contract.

`TestingApi` now accepts only scripted `ModelResponse` data and always creates
`FakeModelAdapter` itself. This preserves customizable scenarios while making
the no-live-model guarantee structural.

## Verification

`PYTHONPATH=src python -m unittest discover -s tests -v`

Result: 12 tests passed.
