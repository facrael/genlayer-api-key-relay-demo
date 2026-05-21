"""FastAPI relay that keeps the upstream API key private.

Run:
  WEATHER_API_KEY=... uvicorn relay_service.app:app --reload

The Intelligent Contract should call this relay, not the upstream API.
The relay validates inputs, fetches upstream data with the private key,
normalizes the response, and returns only a small deterministic JSON object.
"""

from __future__ import annotations

import os
import uuid

import httpx
from fastapi import FastAPI, HTTPException

from .core import build_sanitized_response, build_signed_response, normalize_weather_payload, validate_city

WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"

app = FastAPI(title="GenLayer API Key Relay Demo", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/weather")
async def weather(city: str) -> dict:
    try:
        safe_city = validate_city(city)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    api_key = os.environ.get("WEATHER_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="WEATHER_API_KEY is not configured")

    async with httpx.AsyncClient(timeout=10) as client:
        upstream = await client.get(
            WEATHER_API_URL,
            params={"key": api_key, "q": safe_city, "aqi": "no"},
        )

    if upstream.status_code != 200:
        raise HTTPException(status_code=502, detail="upstream weather API failed")

    normalized = normalize_weather_payload(upstream.json())
    response = build_sanitized_response(normalized, request_id=f"weather_{uuid.uuid4().hex[:12]}")

    signing_secret = os.environ.get("RELAY_SIGNING_SECRET")
    if signing_secret:
        return build_signed_response(
            response,
            secret=signing_secret,
            nonce=f"nonce_{uuid.uuid4().hex[:16]}",
        )
    return response
