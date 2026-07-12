---
name: privacy-local
description: Bundled technical privacy-behavior audit methodology.
license: MIT
---

# Privacy audit

Resolve the shared protocols first:

- `audit/reference/bootstrap-lite.md`

Load conditionally: `audit/reference/persistence-protocol.md` only for
`--persist`/writes beyond the report; `audit/reference/finding-contract.md`
+ `audit/reference/formal-delta.md` + `audit/reference/output-contract.md`
only when the run is formal.

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

Standard mode: per `bootstrap-lite.md`'s 4-section format. Formal mode: follow `audit/reference/output-contract.md`.
