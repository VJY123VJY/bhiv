import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.endpoints.bridge_flow import bridge_route, flow_events, issue_auth

app = FastAPI()
app.post("/api/v1/bridge/route")(bridge_route)
app.post("/api/v1/flow/events")(flow_events)
app.post("/auth/issue")(issue_auth)

client = TestClient(app)


def test_bridge_route_contract():
    payload = {
        "event": "test-event",
        "destination": "InsightFlow",
        "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
        "correlation_id": "corr-123",
        "source": "SHAKTI_GC",
        "action": "bridge_route",
        "routed_at": "2026-08-04T00:00:00Z",
    }

    headers = {
        "X-API-Key": "dummy-key",
        "traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
    }

    response = client.post("/api/v1/bridge/route", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ROUTED"
    assert data["routing_ref"].startswith("route-")
    assert data["traceparent"].startswith("00-4bf92f3577b34da6a3ce929d0e0e4736-")
    assert data["traceparent"].endswith("-01")


def test_flow_events_contract():
    payload = {
        "event": "test-event",
        "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
        "correlation_id": "corr-123",
        "source": "SHAKTI_GC",
        "action": "flow_register",
        "registered_at": "2026-08-04T00:00:00Z",
    }

    headers = {
        "X-API-Key": "dummy-key",
        "traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
    }

    response = client.post("/api/v1/flow/events", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "REGISTERED"
    assert data["flow_ref"].startswith("flow-")
    assert data["traceparent"].startswith("00-4bf92f3577b34da6a3ce929d0e0e4736-")
    assert data["traceparent"].endswith("-01")


def test_auth_issue_contract():
    payload = {
        "client_id": "gc-shakti-insightcore-client",
        "client_secret": "gc-shakti-insightcore-secret",
    }
    response = client.post("/auth/issue", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "gc-shakti-insightcore-token"
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 3600
