---
name: operability-local
description: Bundled production operability and resilience audit methodology.
license: MIT
---

# Operability audit

Resolve the shared protocols first, then inspect:

- health/readiness/liveness
- metrics, logging, tracing
- alerting / SLI / SLO evidence
- graceful shutdown
- retries, backoff, circuit breaking
- dead-letter/recovery patterns
- rollback/runbook/incident-response evidence
- diagnostic affordances
