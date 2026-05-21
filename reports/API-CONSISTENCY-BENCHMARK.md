# API Consistency Benchmark for GenLayer External Data Relays

Category: Research & Analysis / Benchmarks

## Summary

This benchmark measures whether repeated external-data relay responses stay inside a validator-friendly equivalence window. For GenLayer-style Intelligent Contracts, raw speed is not enough: validators need responses that can converge despite timing, upstream cache, and small numeric drift.

## Offline sample result

Sample: 5 weather.v1 responses for Lisbon.

- Latency average: ~122.9 ms
- Temperature range: 24.1–24.3 C
- Wind range: 13.6–13.9 kph
- Humidity range: 61–62%
- Condition values: Partly cloudy
- Consistency score: 1.0 / 1.0
- Recommended cache window: 300 seconds for this sample

## Recommendation

Relays should cache by `(query, provider, time_window)` and serve the same signed payload to all validators inside the window. A 60–300 second window is a practical starting point for weather-like data. For price data, the window should be shorter and paired with explicit drift tolerance.

## Gotcha

The dangerous failure mode is not high latency. It is low reproducibility: two validators can receive individually valid API responses that disagree just enough to break consensus.
