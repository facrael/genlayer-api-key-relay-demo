"""GenLayer-style sketch consuming normalized price.v1 relay data."""

from __future__ import annotations


class PriceVolatilityGuardContract:
    """Example decision: reject trade execution when price drift is too large."""

    def __init__(self, max_drift_bps: int = 100):
        self.max_drift_bps = max_drift_bps

    def decide_execution(self, reference_price: float, relay_price_response: dict) -> str:
        if relay_price_response["integrity"]["schema"] != "price.v1":
            return "reject_unknown_schema"
        price = float(relay_price_response["data"]["price_usd"])
        drift_bps = abs(price - reference_price) / reference_price * 10_000
        if drift_bps > self.max_drift_bps:
            return "reject_price_drift"
        return "allow_execution"
