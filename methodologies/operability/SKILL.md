---
name: operability-local
description: Bundled production operability and resilience audit methodology.
license: MIT
---

# Operability audit

Resolve the shared protocols first:

- `audit/reference/bootstrap-lite.md`

Load conditionally: `audit/reference/persistence-protocol.md` only for
`--persist`/writes beyond the report; `audit/reference/finding-contract.md`
+ `audit/reference/formal-delta.md` + `audit/reference/output-contract.md`
only when the run is formal.

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

Standard mode: per `bootstrap-lite.md`'s 4-section format. Formal mode: follow `audit/reference/output-contract.md`.
