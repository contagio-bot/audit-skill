---
name: deps-local
description: Bundled dependency and runtime freshness methodology.
license: MIT
---

# Dependency and runtime audit

Resolve first:

- `audit/reference/bootstrap-lite.md`

Load conditionally: `audit/reference/persistence-protocol.md` only for
`--persist`/writes beyond the report; `audit/reference/finding-contract.md`
+ `audit/reference/formal-delta.md` + `audit/reference/output-contract.md`
only when the run is formal.

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
7. Flag major-version currency gaps even absent EOL/CVE signals: for each
   direct dependency, compare the installed major against the latest
   stable major. A gap of 2+ majors behind (1+ for a runtime/framework)
   is a finding on its own — severity `medium` by default, `high` if the
   installed major is unsupported/unmaintained upstream (no security
   patches) or the changelog between majors shows breaking API/security
   changes. Do not let "not EOL yet" or "no known CVE" suppress this —
   major-version drift is scored independently of EOL/CVE status, since
   it signals accumulating breaking-change and upgrade risk regardless
   of current vulnerability.

## Output

Standard mode: per `bootstrap-lite.md`'s 4-section format. Formal mode: follow `audit/reference/output-contract.md`.

Area-specific addendum:

- inventory of ecosystems
- runtime/dependency risk summary
- major-version currency gaps (installed major vs. latest stable major),
  listed as findings independent of EOL/CVE status
- support/EOL unknowns when network is unavailable
