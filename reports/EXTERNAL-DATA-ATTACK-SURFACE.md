# External Data Attack Surface for GenLayer Intelligent Contracts

Category: Research & Analysis / Security audits

## Scope

This report reviews risks introduced when an Intelligent Contract depends on external HTTP/API data through a relay.

## Vulnerable pattern

A contract or relay accepts arbitrary user input, calls a live API directly for every validator, compares raw JSON fields exactly, and treats the upstream response as truth.

## Patched pattern

A safer relay validates inputs, normalizes data into a small versioned schema, signs the response, adds expiry and nonce metadata, caches within a time window, and documents the relay trust boundary.

## Attack vectors

1. Input injection: user strings become upstream URL fragments or prompt/context text.
2. Schema drift: upstream API changes fields or units without warning.
3. Stale data: a cached response looks valid but no longer describes the world.
4. Validator disagreement: validators query at different moments and receive different values.
5. Malicious HTML/API content: external content includes prompt injection or irrelevant instructions.
6. Retry manipulation: attacker times failures so some validators retry into a different data window.
7. Relay tampering: a centralized relay signs or returns selective data.

## Builder recommendation

Treat external data as part of the contract attack surface. Every external-data contract should define schema, tolerance, freshness, replay policy, and failure behavior before deployment.
