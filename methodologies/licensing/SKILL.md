---
name: licensing-local
description: Bundled dependency and asset licensing-risk audit methodology.
license: MIT
---

# Licensing audit

Resolve the shared protocols first:

- `audit/reference/bootstrap-lite.md`

Load conditionally: `audit/reference/persistence-protocol.md` only for
`--persist`/writes beyond the report; `audit/reference/finding-contract.md`
+ `audit/reference/formal-delta.md` + `audit/reference/output-contract.md`
only when the run is formal.

Then inspect:

- dependency licenses
- copyleft risk
- missing or incompatible licenses
- notices/attribution evidence
- copied code / bundled assets where visible
- fonts, images, datasets, models, and SDK restrictions when visible

## Output

Standard mode: per `bootstrap-lite.md`'s 4-section format. Formal mode: follow `audit/reference/output-contract.md`.
