# Signed Relay Responses for GenLayer Intelligent Contracts

I extended the private API-key relay with signed responses. The relay still keeps `WEATHER_API_KEY` server-side and returns a normalized `weather.v1` payload, but now it can also attach timestamp, expiry, nonce, algorithm, and signature metadata when `RELAY_SIGNING_SECRET` is configured.

Technically, the signing layer canonicalizes the JSON response, removes the `signature` field from the signed material, and signs the remaining payload with HMAC-SHA256. The repo includes a verification helper, a sample signed payload, a GenLayer-style contract sketch that rejects unsigned or tampered data, and tests for valid signatures, tampered payloads, expired signatures, and replayed nonces.

The main gotcha is that a signature proves relay-origin and payload integrity, not truth. A signed relay can still sign wrong data, omit unfavorable data, or query at a bad time. For GenLayer builders, signatures are useful because they narrow the failure mode: validators can separate “payload was modified or stale” from “the trusted relay produced a bad answer.”

The next technical milestone is to replace shared-secret HMAC with public-key signatures and add cache windows by `(city, time_window)`, so independent validators can verify the same signed response without needing relay secrets.
