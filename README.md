# GenLayer API Key Relay Demo

A minimal Builder-track artifact for GenLayer Intelligent Contracts: a private API-key relay pattern for external data.

The goal is to show how an Intelligent Contract can use weather data without putting the upstream API key in contract code, calldata, validator prompts, or public examples.

## What this builds

- `relay_service/` — FastAPI relay that owns `WEATHER_API_KEY` server-side.
- `contracts/weather_risk_contract.py` — GenLayer-style Intelligent Contract sketch that calls the relay.
- `tests/` — tests for input validation, response normalization, and secret stripping.
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

## Sanitized response shape

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
    "observed_at": "2026-05-19 12:00",
    "source": "weatherapi.com"
  },
  "integrity": {
    "schema": "weather.v1",
    "fields": ["city", "condition", "country", "humidity_pct", "observed_at", "source", "temperature_c", "wind_kph"]
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
5. document validator disagreement and relay-trust risks.

## Next improvements

- add signed relay responses;
- add multiple upstream providers for cross-source comparison;
- add replay protection and request timestamps;
- add docker-compose for deployment;
- add a GenLayer Studio walkthrough with screenshots/logs.
