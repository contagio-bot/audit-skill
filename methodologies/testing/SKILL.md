---
name: testing-local
description: Bundled test-strategy and regression-resistance audit methodology.
license: MIT
---

# Testing audit

Resolve the shared protocols first, then inspect:

- unit / integration / contract / e2e layers
- critical-path coverage
- disabled/flaky/assertion-light tests
- fixture fragility
- mock overuse
- migration/concurrency/idempotency/failure-path coverage

Output a matrix:

`Risk | Code | Test | Quality | Gap`
