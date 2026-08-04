from fastapi import APIRouter, Header, HTTPException, Request
from typing import Optional

from app.services.trace_service import build_trace_context, issue_insightcore_token

router = APIRouter(prefix="", tags=["BridgeFlow"])


@router.post("/bridge/route")
async def bridge_route(
    payload: dict,
    request: Request,
    x_api_key: Optional[str] = Header(default=None, alias="X-API-Key"),
    traceparent: Optional[str] = Header(default=None),
):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")

    try:
        trace_context = build_trace_context(traceparent, payload.get("trace_id"))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "status": "ROUTED",
        "routing_ref": f"route-{trace_context['trace_id'][:8]}",
        "routed_at": payload.get("routed_at") or payload.get("registered_at") or "now",
        "traceparent": trace_context["traceparent"],
    }


@router.post("/flow/events")
async def flow_events(
    payload: dict,
    request: Request,
    x_api_key: Optional[str] = Header(default=None, alias="X-API-Key"),
    traceparent: Optional[str] = Header(default=None),
):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")

    try:
        trace_context = build_trace_context(traceparent, payload.get("trace_id"))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "status": "REGISTERED",
        "flow_ref": f"flow-{trace_context['trace_id'][:8]}",
        "registered_at": payload.get("registered_at") or payload.get("routed_at") or "now",
        "traceparent": trace_context["traceparent"],
    }


@router.post("/auth/issue")
async def issue_auth(payload: dict):
    client_id = payload.get("client_id")
    client_secret = payload.get("client_secret")
    if not client_id or not client_secret:
        raise HTTPException(status_code=400, detail="client_id and client_secret are required")

    try:
        return issue_insightcore_token(client_id, client_secret)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
