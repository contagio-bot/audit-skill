---
name: testing-local
description: Bundled test-strategy and regression-resistance audit methodology.
license: MIT
---

# Testing audit

Resolve the shared protocols first:

- `audit/reference/capability-protocol.md`
- `audit/reference/inventory-protocol.md`
- `audit/reference/coverage-protocol.md`
- `audit/reference/persistence-protocol.md`
- `audit/reference/evidence-protocol.md`
- `audit/reference/finding-schema.md`
- `audit/reference/output-contract.md`

Then inspect:

- unit / integration / contract / e2e layers
- critical-path coverage
- disabled/flaky/assertion-light tests
- fixture fragility
- mock overuse
- migration/concurrency/idempotency/failure-path coverage

## Output

Follow `audit/reference/output-contract.md`.

Output a matrix:

`Risk | Code | Test | Quality | Gap`
