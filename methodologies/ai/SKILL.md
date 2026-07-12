---
name: ai-local
description: Bundled LLM/agent/ML integration risk audit methodology.
license: MIT
---

# AI audit

Resolve the shared protocols first:

- `audit/reference/bootstrap-lite.md`

Load conditionally: `audit/reference/persistence-protocol.md` only for
`--persist`/writes beyond the report; `audit/reference/finding-contract.md`
+ `audit/reference/formal-delta.md` + `audit/reference/output-contract.md`
only when the run is formal.

Then inspect:

- prompt injection exposure
- tool permissions and sandboxing
- data leakage and PII to providers
- output validation
- fallback and eval traces
- prompt/version traceability
- retrieval poisoning trust boundaries
- cost/token/human-approval limits
- provider and model supply-chain risk

## Output

Standard mode: per `bootstrap-lite.md`'s 4-section format. Formal mode: follow `audit/reference/output-contract.md`.
