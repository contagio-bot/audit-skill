---
name: ci-local
description: Bundled CI/CD integrity and reproducibility audit methodology.
license: MIT
---

# CI/CD audit

Resolve the shared protocols first:

- `audit/reference/bootstrap-lite.md`

Load conditionally: `audit/reference/persistence-protocol.md` only for
`--persist`/writes beyond the report; `audit/reference/finding-contract.md`
+ `audit/reference/formal-delta.md` + `audit/reference/output-contract.md`
only when the run is formal.

Then inspect:

- workflow permissions
- `pull_request_target`
- secret exposure
- mutable third-party actions
- cache poisoning opportunities
- artifact handling
- branch/environment protection evidence
- ignored exit codes / non-blocking critical tests
- rollback and release-signing evidence

## Output

Standard mode: per `bootstrap-lite.md`'s 4-section format. Formal mode: follow `audit/reference/output-contract.md`.

Generate the flow map:

`commit -> build -> test -> scan -> artifact -> deploy`

Call out where integrity or traceability is lost.
