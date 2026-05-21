# GenLayer Studio Debugging UX Spec

Category: Tools & Infrastructure / Improve Studio and UX

## Problem

Subjective execution is hard to debug because a builder needs to inspect contract code, external requests, validator observations, prompts, model outputs, equivalence checks, and final state transition in one place.

## Proposed panels

### 1. Execution trace panel

Timeline with method call, deterministic operations, nondeterministic block, external request, validator vote, equivalence result, and state write.

### 2. External request log

For each request: URL host, normalized params, status code, response hash, schema version, timestamp, cache key, and redacted sensitive fields.

### 3. Validator disagreement view

Side-by-side leader/validator outputs with highlighted diffs, tolerance rule, and whether disagreement is numeric drift, schema mismatch, stale data, or model output variance.

### 4. Prompt/input snapshot export

One-click export of prompts, web inputs, normalized relay payloads, model metadata, and equivalence function version for reproducible bug reports.

### 5. Run report format

A JSON/Markdown bundle that builders can attach to Portal submissions or GitHub issues.

## Reusable gotcha

Without a validator disagreement view, builders may mistake a contract logic bug for an external-data consistency bug. Studio should make that distinction visible.
