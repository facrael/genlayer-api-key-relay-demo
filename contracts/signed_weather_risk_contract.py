"""GenLayer-style sketch for consuming signed relay responses.

This is intentionally a sketch: real GenLayer code would call the relay through
GenLayer web access APIs and then verify the response before using the data.
"""

from __future__ import annotations

from relay_service.core import verify_signed_response


class SignedWeatherRiskContract:
    """Example contract decision that rejects unsigned or tampered weather data."""

    def __init__(self, relay_signing_secret: str):
        self.relay_signing_secret = relay_signing_secret

    def decide_weather_risk(self, signed_weather_response: dict, *, now: int) -> str:
        verify_signed_response(
            signed_weather_response,
            secret=self.relay_signing_secret,
            now=now,
        )
        data = signed_weather_response["data"]

        if data["wind_kph"] >= 60 or data["temperature_c"] >= 38:
            return "high_weather_risk"
        return "normal_weather_risk"
