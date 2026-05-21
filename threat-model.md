# Threat Model: Private API Key Relay for GenLayer Intelligent Contracts

## Assets

- Upstream API key, e.g. `WEATHER_API_KEY`.
- Integrity of normalized external data returned to the Intelligent Contract.
- Availability of the relay during contract execution.
- Consistency of responses observed by validators.

## Trust boundary

The Intelligent Contract does not call the upstream API directly. It calls a relay controlled by the builder. The relay stores API keys server-side and returns sanitized JSON.

This improves key privacy but introduces a new trust assumption: the relay can fail, censor, or lie.

## Attack vectors

### 1. API key leakage

Risk: API key appears in contract code, logs, returned JSON, validator prompts, or public examples.

Mitigation in this demo:
- key is read only from `WEATHER_API_KEY` environment variable;
- tests assert secret-like fields are not returned;
- normalized response uses an allowlist of fields.

### 2. Input injection

Risk: user-provided city names are passed into upstream URLs or logs without validation.

Mitigation:
- `validate_city()` rejects shell/control/API composition characters;
- relay passes city as an HTTP query parameter, not string-concatenated URL text.

### 3. Upstream schema drift

Risk: upstream API changes field names or adds ambiguous fields.

Mitigation:
- relay extracts only required fields;
- response includes `integrity.schema = weather.v1`;
- validators and clients can reject unknown schema versions.

### 4. Relay lies or tampers with data

Risk: the relay fabricates safe weather when conditions are unsafe.

Mitigations implemented in Day 2:
- sign relay responses when `RELAY_SIGNING_SECRET` is configured;
- sign canonical JSON so field order and whitespace cannot change verification;
- reject tampered payloads in tests.

Still-needed mitigations:
- query multiple providers;
- include timestamped raw-response hash;
- publish relay code and deployment metadata.

### 5. Validator disagreement

Risk: validators query at different times and receive different weather.

Mitigations:
- response includes `observed_at`;
- signed envelopes include `issued_at`, `expires_at`, and `nonce`;
- verification can reject expired payloads and replayed nonces;
- future version should add relay-side caching by `(city, time_window)`;
- contracts should use tolerance windows instead of exact equality for live data.

### 6. Availability failure

Risk: relay or upstream API is down.

Mitigations:
- return explicit 502 for upstream failure;
- future version should add fallback providers and cached last-known-good values.

## Open specification questions for GenLayer builders

1. Should relays use public-key signatures so validators can verify without shared secrets?
2. What cache window is acceptable for subjective external data?
3. Should contracts store raw response hashes for later audit?
4. How should validators treat disagreement caused by live API timing?
5. When is a relay pattern acceptable versus a decentralized oracle network?
