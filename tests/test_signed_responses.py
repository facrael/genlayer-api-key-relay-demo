import pytest

from relay_service.core import (
    build_sanitized_response,
    build_signed_response,
    verify_signed_response,
)


def _base_response():
    normalized = {
        "city": "Lisbon",
        "country": "Portugal",
        "temperature_c": 24.2,
        "humidity_pct": 61,
        "wind_kph": 13.7,
        "condition": "Partly cloudy",
        "observed_at": "2026-05-20 12:00",
        "source": "weatherapi.com",
    }
    return build_sanitized_response(normalized, request_id="weather_test")


def test_signed_response_verifies_with_timestamp_and_nonce():
    signed = build_signed_response(
        _base_response(),
        secret="test-secret",
        issued_at=1_779_278_400,
        expires_in=300,
        nonce="nonce_abc",
    )

    assert signed["integrity"]["algorithm"] == "hmac-sha256"
    assert signed["integrity"]["issued_at"] == 1_779_278_400
    assert signed["integrity"]["expires_at"] == 1_779_278_700
    assert signed["integrity"]["nonce"] == "nonce_abc"
    assert verify_signed_response(signed, secret="test-secret", now=1_779_278_401) is True


def test_tampered_payload_is_rejected():
    signed = build_signed_response(
        _base_response(),
        secret="test-secret",
        issued_at=1_779_278_400,
        expires_in=300,
        nonce="nonce_abc",
    )
    signed["data"]["temperature_c"] = 99.9

    with pytest.raises(ValueError, match="invalid signature"):
        verify_signed_response(signed, secret="test-secret", now=1_779_278_401)


def test_expired_signature_is_rejected():
    signed = build_signed_response(
        _base_response(),
        secret="test-secret",
        issued_at=1_779_278_400,
        expires_in=10,
        nonce="nonce_abc",
    )

    with pytest.raises(ValueError, match="signature expired"):
        verify_signed_response(signed, secret="test-secret", now=1_779_278_411)


def test_replayed_nonce_is_rejected():
    signed = build_signed_response(
        _base_response(),
        secret="test-secret",
        issued_at=1_779_278_400,
        expires_in=300,
        nonce="nonce_abc",
    )
    seen = set()

    assert verify_signed_response(signed, secret="test-secret", now=1_779_278_401, seen_nonces=seen) is True
    with pytest.raises(ValueError, match="replayed nonce"):
        verify_signed_response(signed, secret="test-secret", now=1_779_278_402, seen_nonces=seen)
