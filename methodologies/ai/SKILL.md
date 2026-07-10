---
name: ai-local
description: Bundled LLM/agent/ML integration risk audit methodology.
license: MIT
---

# AI audit

Resolve the shared protocols first, then inspect:

- prompt injection exposure
- tool permissions and sandboxing
- data leakage and PII to providers
- output validation
- fallback and eval traces
- prompt/version traceability
- retrieval poisoning trust boundaries
- cost/token/human-approval limits
- provider and model supply-chain risk
