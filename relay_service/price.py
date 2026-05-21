"""Price-feed variant of the external data relay pattern."""

from __future__ import annotations

import re
from typing import Any

SYMBOL_RE = re.compile(r"^[A-Z0-9]{2,12}$")
PRICE_SCHEMA = "price.v1"


def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not SYMBOL_RE.fullmatch(symbol):
        raise ValueError("invalid symbol")
    return symbol


def normalize_price_payload(raw: dict[str, Any], *, source: str = "coingecko") -> dict[str, Any]:
    symbol = validate_symbol(str(raw["symbol"]))
    price = round(float(raw["price_usd"]), 6)
    if price <= 0:
        raise ValueError("invalid price")
    return {
        "symbol": symbol,
        "price_usd": price,
        "observed_at": str(raw["observed_at"]),
        "source": source,
    }


def build_price_response(normalized: dict[str, Any], *, request_id: str) -> dict[str, Any]:
    return {
        "request_id": request_id,
        "data": normalized,
        "integrity": {
            "schema": PRICE_SCHEMA,
            "fields": sorted(normalized.keys()),
        },
    }
