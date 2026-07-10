---
name: ci-local
description: Bundled CI/CD integrity and reproducibility audit methodology.
license: MIT
---

# CI/CD audit

Resolve the shared protocols first, then inspect:

- workflow permissions
- `pull_request_target`
- secret exposure
- mutable third-party actions
- cache poisoning opportunities
- artifact handling
- branch/environment protection evidence
- ignored exit codes / non-blocking critical tests
- rollback and release-signing evidence

Generate the flow map:

`commit -> build -> test -> scan -> artifact -> deploy`

Call out where integrity or traceability is lost.
