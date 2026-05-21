import pytest

from relay_service.price import build_price_response, normalize_price_payload, validate_symbol


def test_validate_symbol_normalizes_safe_symbols():
    assert validate_symbol("eth") == "ETH"
    assert validate_symbol("BTC") == "BTC"


def test_validate_symbol_rejects_injection():
    with pytest.raises(ValueError, match="invalid symbol"):
        validate_symbol("ETH;curl")


def test_normalize_price_payload_returns_schema_safe_fields():
    normalized = normalize_price_payload({"symbol": "eth", "price_usd": "3812.1234567", "observed_at": "2026-05-21T09:30:00Z", "api_key": "secret"})
    assert normalized == {"symbol": "ETH", "price_usd": 3812.123457, "observed_at": "2026-05-21T09:30:00Z", "source": "coingecko"}
    response = build_price_response(normalized, request_id="price_1")
    assert response["integrity"]["schema"] == "price.v1"
    assert "api_key" not in str(response).lower()
