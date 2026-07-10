---
name: privacy-local
description: Bundled technical privacy-behavior audit methodology.
license: MIT
---

# Privacy audit

Resolve the shared protocols first:

- `audit/reference/capability-protocol.md`
- `audit/reference/inventory-protocol.md`
- `audit/reference/coverage-protocol.md`
- `audit/reference/persistence-protocol.md`
- `audit/reference/evidence-protocol.md`
- `audit/reference/finding-schema.md`
- `audit/reference/output-contract.md`

Then inspect:

- data collected and retained
- minimization and deletion/export mechanisms
- consent and analytics signals
- data in logs
- third-party data sharing
- PII sent to models/providers when present

Always distinguish:

- Observed technical behavior
- Potential compliance implication
- Legal conclusion: not determinable from repository alone

## Output

Follow `audit/reference/output-contract.md`.
