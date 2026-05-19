import pytest

from relay_service.core import normalize_weather_payload, build_sanitized_response, validate_city


def test_validate_city_accepts_safe_city_names():
    assert validate_city("Lisbon") == "Lisbon"
    assert validate_city("New York") == "New York"
    assert validate_city("São Paulo") == "São Paulo"


def test_validate_city_rejects_injection_like_input():
    with pytest.raises(ValueError, match="invalid city"):
        validate_city("London; curl attacker")


def test_normalize_weather_payload_keeps_only_consensus_safe_fields():
    raw = {
        "location": {"name": "Lisbon", "country": "Portugal", "localtime": "2026-05-19 12:00"},
        "current": {
            "temp_c": 24.2,
            "humidity": 61,
            "wind_kph": 13.7,
            "condition": {"text": "Partly cloudy", "icon": "//cdn.example/icon.png"},
            "last_updated_epoch": 1770000000,
            "debug": "do not expose",
        },
        "api_key": "should-never-leak",
    }

    result = normalize_weather_payload(raw)

    assert result == {
        "city": "Lisbon",
        "country": "Portugal",
        "temperature_c": 24.2,
        "humidity_pct": 61,
        "wind_kph": 13.7,
        "condition": "Partly cloudy",
        "observed_at": "2026-05-19 12:00",
        "source": "weatherapi.com",
    }
    assert "api_key" not in result
    assert "icon" not in str(result)


def test_build_sanitized_response_wraps_metadata_without_secret_material():
    normalized = {
        "city": "Lisbon",
        "country": "Portugal",
        "temperature_c": 24.2,
        "humidity_pct": 61,
        "wind_kph": 13.7,
        "condition": "Partly cloudy",
        "observed_at": "2026-05-19 12:00",
        "source": "weatherapi.com",
    }

    response = build_sanitized_response(normalized, request_id="req_123")

    assert response["request_id"] == "req_123"
    assert response["data"] == normalized
    assert response["integrity"]["schema"] == "weather.v1"
    assert response["integrity"]["fields"] == sorted(normalized.keys())
    assert "api_key" not in str(response).lower()
