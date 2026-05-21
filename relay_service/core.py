"""Core sanitization logic for a GenLayer external API key relay.

The relay keeps API keys offchain and returns only a small, deterministic,
consensus-friendly JSON envelope to Intelligent Contracts.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import time
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


SIGNATURE_ALGORITHM = "hmac-sha256"
DEFAULT_MAX_SIGNATURE_AGE_SECONDS = 300


def canonical_json(value: dict[str, Any]) -> str:
    """Return deterministic JSON bytes-as-text for signing and verification.

    Validator-facing signatures must not depend on Python dict insertion order or
    whitespace. This format is compact, sorted, and UTF-8 safe.
    """
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sign_payload(payload: dict[str, Any], *, secret: str) -> str:
    """Sign a canonical payload with the relay signing secret."""
    if not secret:
        raise ValueError("missing signing secret")
    return hmac.new(secret.encode("utf-8"), canonical_json(payload).encode("utf-8"), hashlib.sha256).hexdigest()


def build_signed_response(
    response: dict[str, Any],
    *,
    secret: str,
    issued_at: int | None = None,
    expires_in: int = DEFAULT_MAX_SIGNATURE_AGE_SECONDS,
    nonce: str,
) -> dict[str, Any]:
    """Attach timestamp, expiry, nonce, and signature metadata to a relay response."""
    issued = int(time.time()) if issued_at is None else int(issued_at)
    signed = {
        **response,
        "integrity": {
            **response["integrity"],
            "issued_at": issued,
            "expires_at": issued + int(expires_in),
            "nonce": nonce,
            "algorithm": SIGNATURE_ALGORITHM,
        },
    }
    signed["integrity"]["signature"] = sign_payload(_signature_payload(signed), secret=secret)
    return signed


def verify_signed_response(
    signed: dict[str, Any],
    *,
    secret: str,
    now: int | None = None,
    seen_nonces: set[str] | None = None,
) -> bool:
    """Verify signature, expiry, and optional replay nonce.

    A real validator/client can keep `seen_nonces` for the consensus window to
    reject replayed relay responses.
    """
    integrity = signed.get("integrity") or {}
    signature = integrity.get("signature")
    if not isinstance(signature, str) or not signature:
        raise ValueError("missing signature")
    if integrity.get("algorithm") != SIGNATURE_ALGORITHM:
        raise ValueError("unsupported signature algorithm")

    current_time = int(time.time()) if now is None else int(now)
    issued_at = int(integrity["issued_at"])
    expires_at = int(integrity["expires_at"])
    if issued_at > current_time + 30:
        raise ValueError("signature issued in the future")
    if expires_at < current_time:
        raise ValueError("signature expired")

    nonce = integrity.get("nonce")
    if not isinstance(nonce, str) or not nonce:
        raise ValueError("missing nonce")
    if seen_nonces is not None:
        if nonce in seen_nonces:
            raise ValueError("replayed nonce")
        seen_nonces.add(nonce)

    expected = sign_payload(_signature_payload(signed), secret=secret)
    if not hmac.compare_digest(expected, signature):
        raise ValueError("invalid signature")
    return True


def _signature_payload(signed: dict[str, Any]) -> dict[str, Any]:
    """Return the signed material with the signature field removed."""
    integrity = dict(signed["integrity"])
    integrity.pop("signature", None)
    return {**signed, "integrity": integrity}
