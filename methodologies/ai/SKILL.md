---
name: ai-local
description: Bundled LLM/agent/ML integration risk audit methodology.
license: MIT
---

# AI audit

Resolve the shared protocols first:

- `audit/reference/bootstrap.md`
- `audit/reference/persistence-protocol.md`
- `audit/reference/finding-contract.md`
- `audit/reference/output-contract.md`

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

Follow `audit/reference/output-contract.md`.
