---
name: testing-local
description: Bundled test-strategy and regression-resistance audit methodology.
license: MIT
---

# Testing audit

Resolve the shared protocols first:

- `audit/reference/bootstrap-lite.md`

Load conditionally: `audit/reference/persistence-protocol.md` only for
`--persist`/writes beyond the report; `audit/reference/finding-contract.md`
+ `audit/reference/formal-delta.md` + `audit/reference/output-contract.md`
only when the run is formal.

Then inspect:

- unit / integration / contract / e2e layers
- critical-path coverage
- disabled/flaky/assertion-light tests
- fixture fragility
- mock overuse
- migration/concurrency/idempotency/failure-path coverage

## Output

Standard mode: per `bootstrap-lite.md`'s 4-section format. Formal mode: follow `audit/reference/output-contract.md`.

Output a matrix:

`Risk | Code | Test | Quality | Gap`
