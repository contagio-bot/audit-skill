---
name: ci-local
description: Bundled CI/CD integrity and reproducibility audit methodology.
license: MIT
---

# CI/CD audit

Resolve the shared protocols first:

- `audit/reference/capability-protocol.md`
- `audit/reference/inventory-protocol.md`
- `audit/reference/coverage-protocol.md`
- `audit/reference/persistence-protocol.md`
- `audit/reference/evidence-protocol.md`
- `audit/reference/finding-schema.md`
- `audit/reference/output-contract.md`

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

Follow `audit/reference/output-contract.md`.

Generate the flow map:

`commit -> build -> test -> scan -> artifact -> deploy`

Call out where integrity or traceability is lost.
