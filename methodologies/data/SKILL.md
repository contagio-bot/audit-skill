---
name: data-local
description: Bundled data modeling, lifecycle, and protection audit methodology.
license: MIT
---

# Data audit

Resolve the shared protocols first:

- `audit/reference/bootstrap-lite.md`

Load conditionally: `audit/reference/persistence-protocol.md` only for
`--persist`/writes beyond the report; `audit/reference/finding-contract.md`
+ `audit/reference/formal-delta.md` + `audit/reference/output-contract.md`
only when the run is formal.

Then inspect:

- schema and constraints
- ownership and multi-tenant isolation
- PII/data classification clues
- retention/deletion signals
- encryption and secrets around data stores
- migrations, compatibility, backup/recovery evidence
- data in logs and non-production environments

## Output

Standard mode: per `bootstrap-lite.md`'s 4-section format. Formal mode: follow `audit/reference/output-contract.md`.
