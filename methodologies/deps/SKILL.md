---
name: deps-local
description: Bundled dependency and runtime freshness methodology.
license: MIT
---

# Dependency and runtime audit

Resolve first:

- `audit/reference/capability-protocol.md`
- `audit/reference/inventory-protocol.md`
- `audit/reference/coverage-protocol.md`
- `audit/reference/persistence-protocol.md`
- `audit/reference/evidence-protocol.md`
- `audit/reference/finding-schema.md`

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

- inventory of ecosystems
- top runtime/dependency risks
- explicit `Observed` / `Inferred` / `Not verifiable`
- normalized findings when structured output is requested
