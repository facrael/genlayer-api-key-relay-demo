# GenLayer Builder Submission — Signed Relay Responses

Topic: Tools & Infrastructure / Security

Title: Signed Relay Responses for GenLayer Intelligent Contracts

Notes / Description:

I extended the private API-key relay demo with signed responses for GenLayer Intelligent Contracts. The relay still keeps the upstream API key server-side and returns a normalized `weather.v1` response, but it can now attach timestamp, expiry, nonce, algorithm, and signature metadata.

The implementation signs canonical JSON with HMAC-SHA256 when `RELAY_SIGNING_SECRET` is configured. The repo includes a verification helper, a deterministic sample signed response, a GenLayer-style contract sketch, and tests that reject tampered payloads, expired signatures, and replayed nonces.

The main technical gotcha is that signatures prove relay-origin and payload integrity, not truth. A trusted relay can still sign wrong or selectively stale data. This contribution makes that trust boundary explicit and gives builders a reusable pattern for separating payload tampering from relay trust.

Next milestone: move from shared-secret HMAC to public-key signatures and add relay-side cache windows so validators can verify the same signed payload independently.

Evidence Description: GitHub repository / signed response implementation

URL: https://github.com/ragatar/orangemd/tree/main/04%20Content/GenLayer/Builder%20Artifacts/genlayer-api-key-relay-demo
