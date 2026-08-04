import os
import secrets
import re
from typing import Dict, Any

_TRACEPARENT_PATTERN = re.compile(r"^00-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})$")


def build_trace_context(traceparent_header: str | None, provided_trace_id: str | None) -> Dict[str, Any]:
    if not traceparent_header:
        raise ValueError("traceparent header is required")

    match = _TRACEPARENT_PATTERN.match(traceparent_header)
    if not match:
        raise ValueError("traceparent header must follow W3C format")

    incoming_trace_id = match.group(1)
    if provided_trace_id and provided_trace_id != incoming_trace_id:
        raise ValueError("trace_id mismatch between payload and traceparent")

    span_id = secrets.token_hex(8)
    outgoing_traceparent = f"00-{incoming_trace_id}-{span_id}-01"
    return {
        "trace_id": incoming_trace_id,
        "span_id": span_id,
        "traceparent": outgoing_traceparent,
    }


def issue_insightcore_token(client_id: str, client_secret: str) -> Dict[str, Any]:
    if client_id == "gc-shakti-insightcore-client" and client_secret == "gc-shakti-insightcore-secret":
        return {
            "access_token": "gc-shakti-insightcore-token",
            "token_type": "bearer",
            "expires_in": 3600,
        }

    raise ValueError("invalid InsightCore credentials")
