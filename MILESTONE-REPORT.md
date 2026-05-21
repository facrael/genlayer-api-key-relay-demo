# MVP Milestone Report: GenLayer External Data Relay Kit

Category: Projects & Milestones

## What exists now

This repo has grown from a single private API-key relay into a small GenLayer external-data relay kit.

Implemented artifacts:

1. Private API-key relay for weather data.
2. Signed relay responses with timestamp, expiry, nonce, and tamper/replay tests.
3. API consistency benchmark for validator-friendly cache windows.
4. External-data attack surface report.
5. Price feed relay variant with price.v1 schema.
6. Studio debugging UX spec for subjective execution.

## Verification

- Unit tests cover weather validation, secret stripping, signed response verification, replay/expiry rejection, price normalization, and benchmark report generation.
- Offline benchmark sample demonstrates stable weather responses inside a 300-second cache window.

## Known limitations

- HMAC signatures are useful for demos but public-key signatures are better for third-party validator verification.
- Offline benchmark samples are deterministic; live provider measurements should be collected over longer windows.
- Relay trust is explicit but not decentralized. Multiple providers and response hashes are still needed.

## Next milestone

Split this kit into specialized repos: public-key signed relay, multi-provider consistency benchmark, external-data security corpus, price-feed adapter, and Studio run-report prototype.
