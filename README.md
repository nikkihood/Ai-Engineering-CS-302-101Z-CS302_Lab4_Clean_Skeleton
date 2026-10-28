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

## Optional HTTP entry point

```bash
python -m transcript_requester.frameworks_drivers.http_server
```
