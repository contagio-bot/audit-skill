---
name: operability-local
description: Bundled production operability and resilience audit methodology.
license: MIT
---

# Operability audit

Resolve the shared protocols first:

- `audit/reference/bootstrap.md`
- `audit/reference/persistence-protocol.md`
- `audit/reference/finding-contract.md`
- `audit/reference/output-contract.md`

Then inspect:

- health/readiness/liveness
- metrics, logging, tracing
- alerting / SLI / SLO evidence
- graceful shutdown
- retries, backoff, circuit breaking
- dead-letter/recovery patterns
- rollback/runbook/incident-response evidence
- diagnostic affordances

## Output

Follow `audit/reference/output-contract.md`.
