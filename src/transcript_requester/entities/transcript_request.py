# Dependency Rule: Entities are the innermost layer and must not depend on outer layers.

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


TranscriptRequestStatus = Literal["requested"]


@dataclass(frozen=True, slots=True)
class TranscriptRequest:
    id: str
    source_url: str
    requested_at: datetime
    status: TranscriptRequestStatus = "requested"


def create_transcript_request(
    request_id: str,
    source_url: str,
    requested_at: datetime,
) -> TranscriptRequest:
    if not source_url.strip():
        raise ValueError("source_url is required")

    return TranscriptRequest(
        id=request_id,
        source_url=source_url,
        requested_at=requested_at,
    )
