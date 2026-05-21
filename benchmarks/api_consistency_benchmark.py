"""API consistency benchmark for GenLayer-style external data relays.

The benchmark can run offline against sample relay responses, or against a live
relay endpoint if RELAY_URL is provided. It measures the property that matters
for GenLayer validators: whether repeated observations converge inside a useful
cache/equivalence window.
"""

from __future__ import annotations

import json
import math
import os
import statistics
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SAMPLE_PATH = Path(__file__).resolve().parents[1] / "examples" / "sample_benchmark_weather_responses.json"


@dataclass(frozen=True)
class MetricSummary:
    count: int
    minimum: float
    average: float
    maximum: float
    stdev: float


def summarize(values: list[float]) -> MetricSummary:
    return MetricSummary(
        count=len(values),
        minimum=min(values),
        average=statistics.fmean(values),
        maximum=max(values),
        stdev=statistics.pstdev(values) if len(values) > 1 else 0.0,
    )


def consistency_score(responses: list[dict[str, Any]], *, temp_tolerance_c: float = 0.5, wind_tolerance_kph: float = 2.0, humidity_tolerance_pct: float = 3.0) -> float:
    """Return 0..1 score for whether relay responses fit one equivalence window."""
    if not responses:
        return 0.0
    data = [r["data"] for r in responses]
    temp = [float(d["temperature_c"]) for d in data]
    wind = [float(d["wind_kph"]) for d in data]
    humidity = [float(d["humidity_pct"]) for d in data]

    checks = [
        (max(temp) - min(temp)) <= temp_tolerance_c,
        (max(wind) - min(wind)) <= wind_tolerance_kph,
        (max(humidity) - min(humidity)) <= humidity_tolerance_pct,
        len({d["condition"] for d in data}) == 1,
    ]
    return sum(checks) / len(checks)


def recommended_cache_window_seconds(responses: list[dict[str, Any]], *, observed_span_seconds: int = 300) -> int:
    score = consistency_score(responses)
    if score >= 1.0:
        return observed_span_seconds
    if score >= 0.75:
        return max(60, observed_span_seconds // 2)
    if score >= 0.50:
        return 60
    return 0


def load_offline_samples() -> tuple[list[dict[str, Any]], list[float]]:
    payload = json.loads(SAMPLE_PATH.read_text())
    return payload["responses"], payload["latencies_ms"]


def fetch_live_samples(relay_url: str, *, count: int = 5, delay_seconds: float = 1.0) -> tuple[list[dict[str, Any]], list[float]]:
    responses: list[dict[str, Any]] = []
    latencies: list[float] = []
    for _ in range(count):
        started = time.perf_counter()
        with urllib.request.urlopen(relay_url, timeout=15) as r:
            responses.append(json.loads(r.read().decode("utf-8")))
        latencies.append((time.perf_counter() - started) * 1000)
        time.sleep(delay_seconds)
    return responses, latencies


def build_report(responses: list[dict[str, Any]], latencies_ms: list[float]) -> dict[str, Any]:
    temps = [float(r["data"]["temperature_c"]) for r in responses]
    winds = [float(r["data"]["wind_kph"]) for r in responses]
    humidity = [float(r["data"]["humidity_pct"]) for r in responses]
    return {
        "sample_count": len(responses),
        "latency_ms": summarize(latencies_ms).__dict__,
        "temperature_c": summarize(temps).__dict__,
        "wind_kph": summarize(winds).__dict__,
        "humidity_pct": summarize(humidity).__dict__,
        "condition_values": sorted({r["data"]["condition"] for r in responses}),
        "consistency_score": consistency_score(responses),
        "recommended_cache_window_seconds": recommended_cache_window_seconds(responses),
    }


def main() -> int:
    relay_url = os.environ.get("RELAY_URL")
    if relay_url:
        responses, latencies = fetch_live_samples(relay_url)
        mode = "live"
    else:
        responses, latencies = load_offline_samples()
        mode = "offline-sample"
    report = {"mode": mode, **build_report(responses, latencies)}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
