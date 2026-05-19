"""Example GenLayer-style Intelligent Contract using a private API-key relay.

This is intentionally written as a compact contract sketch. The important
pattern is that the contract asks a relay for sanitized public data; the
upstream API key never appears in contract code, calldata, or validator prompts.
"""

from genlayer import gl
from genlayer.gl import Contract


class WeatherRiskContract(Contract):
    relay_url: str
    city: str
    max_safe_wind_kph: int

    def __init__(self, relay_url: str, city: str, max_safe_wind_kph: int = 45):
        self.relay_url = relay_url.rstrip("/")
        self.city = city
        self.max_safe_wind_kph = max_safe_wind_kph

    @gl.public.write
    def evaluate_weather_risk(self) -> dict:
        """Fetch normalized weather data and return a structured risk decision."""
        response = gl.get_webpage(f"{self.relay_url}/weather?city={self.city}")
        weather = response["data"]

        wind_kph = weather["wind_kph"]
        condition = weather["condition"].lower()
        risky_condition = "storm" in condition or "thunder" in condition
        risky_wind = wind_kph >= self.max_safe_wind_kph

        decision = "unsafe" if risky_condition or risky_wind else "safe"
        return {
            "decision": decision,
            "city": weather["city"],
            "condition": weather["condition"],
            "wind_kph": wind_kph,
            "reason": "weather relay returned normalized weather.v1 data",
            "relay_schema": response["integrity"]["schema"],
        }
