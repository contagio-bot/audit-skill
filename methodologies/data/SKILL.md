---
name: data-local
description: Bundled data modeling, lifecycle, and protection audit methodology.
license: MIT
---

# Data audit

Resolve the shared protocols first:

- `audit/reference/capability-protocol.md`
- `audit/reference/inventory-protocol.md`
- `audit/reference/coverage-protocol.md`
- `audit/reference/persistence-protocol.md`
- `audit/reference/evidence-protocol.md`
- `audit/reference/finding-schema.md`
- `audit/reference/output-contract.md`

Then inspect:

- schema and constraints
- ownership and multi-tenant isolation
- PII/data classification clues
- retention/deletion signals
- encryption and secrets around data stores
- migrations, compatibility, backup/recovery evidence
- data in logs and non-production environments

## Output

Follow `audit/reference/output-contract.md`.
