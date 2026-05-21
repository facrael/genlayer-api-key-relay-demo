# GenLayer API Key Relay Demo

A minimal Builder-track artifact for GenLayer Intelligent Contracts: a private API-key relay pattern for external data.

The goal is to show how an Intelligent Contract can use weather data without putting the upstream API key in contract code, calldata, validator prompts, or public examples.

## What this builds

- `relay_service/` — FastAPI relay that owns `WEATHER_API_KEY` server-side.
- `contracts/weather_risk_contract.py` — GenLayer-style Intelligent Contract sketch that calls the relay.
- `tests/` — tests for input validation, response normalization, secret stripping, signed responses, expiry, and replay rejection.
- `examples/verify_signed_response.py` — minimal verification example for a signed relay payload.
- `examples/sample_signed_weather_response.json` — deterministic sample signed payload.
- `threat-model.md` — attack surface and mitigations for the relay pattern.

## Why this matters for GenLayer

External APIs are one of the most useful Intelligent Contract patterns, but most APIs require private keys. A contract should not expose those keys. The relay pattern keeps secrets offchain and returns a small, normalized, schema-tagged JSON response that validators can reason about.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
export WEATHER_API_KEY=your_weatherapi_key
uvicorn relay_service.app:app --reload
```

Call the relay:

```bash
curl 'http://127.0.0.1:8000/weather?city=Lisbon'
```

Run tests:

```bash
python -m pytest -q
```

## Sanitized and signed response shape

```json
{
  "request_id": "weather_abc123",
  "data": {
    "city": "Lisbon",
    "country": "Portugal",
    "temperature_c": 24.2,
    "humidity_pct": 61,
    "wind_kph": 13.7,
    "condition": "Partly cloudy",
    "observed_at": "2026-05-21 09:30",
    "source": "weatherapi.com"
  },
  "integrity": {
    "schema": "weather.v1",
    "fields": ["city", "condition", "country", "humidity_pct", "observed_at", "source", "temperature_c", "wind_kph"],
    "issued_at": 1779356000,
    "expires_at": 1810892000,
    "nonce": "nonce_demo_001",
    "algorithm": "hmac-sha256",
    "signature": "..."
  }
}
```

## Builder-track submission angle

Category: Tools & Infrastructure

Claim: this is a reusable relay pattern for Intelligent Contracts that need external APIs while keeping API keys private.

The technical contribution is not the weather API itself. It is the boundary:

1. validate inputs before upstream calls;
2. keep secrets only in relay environment variables;
3. strip upstream metadata and unstable fields;
4. return schema-tagged normalized JSON;
5. document validator disagreement and relay-trust risks;
6. optionally sign responses with timestamp, expiry, and nonce metadata.

## Signed response extension

Day 2 extends the relay with tamper-evident response envelopes. If `RELAY_SIGNING_SECRET` is configured, `/weather` returns the normal sanitized payload plus:

- `issued_at` and `expires_at` for a short validity window;
- `nonce` so clients can keep a replay cache;
- `algorithm = hmac-sha256`;
- `signature` over canonical JSON with the signature field removed.

Verify a saved signed response:

```bash
python examples/verify_signed_response.py examples/sample_signed_weather_response.json demo-secret
```

This is not a full decentralized oracle design. It is a practical integrity layer: validators or downstream services can detect tampering, stale payloads, and replay within a chosen time window.

## Next improvements

- add public-key signatures instead of shared-secret HMAC for third-party verification;
- add multiple upstream providers for cross-source comparison;
- add docker-compose for deployment;
- add a GenLayer Studio walkthrough with screenshots/logs.
