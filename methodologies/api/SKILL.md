---
name: api-local
description: Bundled API and webhook audit methodology.
license: MIT
---

# API audit

Resolve the shared protocols first, then inspect:

- endpoint inventory
- authentication and authorization
- object-level authorization
- rate limiting
- idempotency
- pagination
- validation and error contracts
- webhook signatures and replay protection
- timeout/retry and debug endpoints

Generate:

`endpoint x auth x authorization x validation x rate-limit x tests`
