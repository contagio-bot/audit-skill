---
name: deps-local
description: Bundled dependency and runtime freshness methodology.
license: MIT
---

# Dependency and runtime audit

Resolve first:

- `audit/reference/bootstrap.md`
- `audit/reference/persistence-protocol.md`
- `audit/reference/finding-contract.md`
- `audit/reference/output-contract.md`

## Goal

Inspect:

- main runtimes
- direct dependencies
- lockfiles and manifest coherence
- known vulnerable versions
- outdated or EOL core components

## Workflow

1. Inventory manifests and lockfiles.
2. Determine ecosystems present.
3. Identify installed versions from repo evidence.
4. If network is available, compare central components against official support/latest sources.
5. If network is unavailable, report support/latest status as `Not verifiable`.
6. Flag missing lockfiles, stale manifests, floating Git refs, or missing provenance where visible.

## Output

Follow `audit/reference/output-contract.md`.

Area-specific addendum:

- inventory of ecosystems
- runtime/dependency risk summary
- support/EOL unknowns when network is unavailable
