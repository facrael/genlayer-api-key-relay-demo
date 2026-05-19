"""Core sanitization logic for a GenLayer external API key relay.

The relay keeps API keys offchain and returns only a small, deterministic,
consensus-friendly JSON envelope to Intelligent Contracts.
"""

from __future__ import annotations

import re
from typing import Any

CITY_RE = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ .'-]{1,80}$")
WEATHER_SCHEMA = "weather.v1"


def validate_city(city: str) -> str:
    """Return a safe city string or raise ValueError.

    This intentionally accepts human city names but rejects shell/control/API
    composition characters. The relay should not pass user strings directly
    into upstream URLs without validation.
    """
    city = city.strip()
    if not CITY_RE.fullmatch(city):
        raise ValueError("invalid city")
    return city


def _number(value: Any, *, digits: int = 1) -> float | int:
    if isinstance(value, bool) or value is None:
        raise ValueError("expected number")
    number = float(value)
    rounded = round(number, digits)
    if rounded.is_integer():
        return int(rounded)
    return rounded


def normalize_weather_payload(raw: dict[str, Any]) -> dict[str, Any]:
    """Extract only stable, non-secret weather fields from an upstream payload."""
    location = raw.get("location") or {}
    current = raw.get("current") or {}
    condition = current.get("condition") or {}

    return {
        "city": str(location["name"]),
        "country": str(location["country"]),
        "temperature_c": _number(current["temp_c"], digits=1),
        "humidity_pct": int(current["humidity"]),
        "wind_kph": _number(current["wind_kph"], digits=1),
        "condition": str(condition["text"]),
        "observed_at": str(location["localtime"]),
        "source": "weatherapi.com",
    }


def build_sanitized_response(normalized: dict[str, Any], *, request_id: str) -> dict[str, Any]:
    """Wrap normalized data with schema metadata useful to validators."""
    return {
        "request_id": request_id,
        "data": normalized,
        "integrity": {
            "schema": WEATHER_SCHEMA,
            "fields": sorted(normalized.keys()),
        },
    }
