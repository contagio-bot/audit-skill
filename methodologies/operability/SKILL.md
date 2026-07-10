---
name: operability-local
description: Bundled production operability and resilience audit methodology.
license: MIT
---

# Operability audit

Resolve the shared protocols first:

- `audit/reference/capability-protocol.md`
- `audit/reference/inventory-protocol.md`
- `audit/reference/coverage-protocol.md`
- `audit/reference/persistence-protocol.md`
- `audit/reference/evidence-protocol.md`
- `audit/reference/finding-schema.md`
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
