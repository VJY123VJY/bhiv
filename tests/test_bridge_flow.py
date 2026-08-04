import pytest

from app.services.trace_service import build_trace_context, issue_insightcore_token


def test_build_trace_context_uses_header_trace_id():
    context = build_trace_context(
        "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
        "4bf92f3577b34da6a3ce929d0e0e4736",
    )

    assert context["trace_id"] == "4bf92f3577b34da6a3ce929d0e0e4736"
    assert context["traceparent"].startswith("00-4bf92f3577b34da6a3ce929d0e0e4736-")
    assert context["traceparent"].endswith("-01")
    assert context["span_id"]


def test_build_trace_context_rejects_missing_header():
    with pytest.raises(ValueError, match="traceparent"):
        build_trace_context(None, "4bf92f3577b34da6a3ce929d0e0e4736")


def test_issue_insightcore_token_for_known_credentials():
    token = issue_insightcore_token(
        "gc-shakti-insightcore-client",
        "gc-shakti-insightcore-secret",
    )

    assert token["token_type"] == "bearer"
    assert token["access_token"]
    assert token["expires_in"] == 3600
