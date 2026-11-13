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
- **container images (mandatory whenever a Dockerfile or compose file exists)**

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

## Container images (mandatory)

Library manifests are only half of what runs in production: the database,
cache, proxy and the OS layer of every app image ship their own packages
and bundled binaries. A `deps` run on a repo with a `Dockerfile*` or
`*compose*.yml` that does not scan images is **incomplete** — report it as
a coverage gap, never as OK.

1. Inventory every image that runs in production:
   - `docker compose -f <prod compose> config --images` (resolves built
     app images and pulled ones such as `postgres`, `redis`, `nginx`);
   - every `FROM` in every `Dockerfile*` (all stages; the final stage is
     what ships, builder stages matter for supply chain only);
   - Kubernetes/IaC image references if present.
2. Scan each image with Trivy (`aquasec/trivy`, pinned tag, via Docker):
   `image --scanners vuln --severity HIGH,CRITICAL --ignore-unfixed`.
   Scan the image actually deployed (on the server) when reachable; a
   laptop copy of a built image may be stale — say which one you scanned.
3. Classify each finding by where it lives, since remediation differs:
   - **OS packages** (apt/apk: openssl, zlib, krb5, curl…) → bump to the
     latest patch tag of the same major, or rebuild with a package upgrade;
   - **app libraries inside the image** (pip/npm in site-packages /
     node_modules) → fix in the lockfile;
   - **bundled helper binaries** (e.g. `gosu` in every official `postgres`
     image, Go `stdlib` CVEs) → judge reachability; remediation is a
     derived image that removes the binary (run as `user: postgres` so the
     entrypoint never needs it) or a time-boxed accepted exception.
4. Also check, per image: tag pinned (no `latest`/floating major in prod),
   base age, and major-version support window (e.g. PostgreSQL majors are
   supported 5 years: 14 EOL Nov 2026, 16 Nov 2028, 17 Nov 2029, 18 Nov 2030).
   Divergent majors of the same engine across sibling projects are a
   finding (standardization), not by themselves a vulnerability.
5. A major bump of a stateful engine (Postgres, MySQL, Redis persistence)
   is a **data migration** (dump/restore or pg_upgrade, volume layout may
   change — e.g. `postgres:18` moved PGDATA under `/var/lib/postgresql/18`):
   never propose it as a drop-in tag change; propose testing with a copy of
   production data first.

## Output

Standard mode: per `bootstrap-lite.md`'s 4-section format. Formal mode: follow `audit/reference/output-contract.md`.

Area-specific addendum:

- inventory of ecosystems
- runtime/dependency risk summary
- major-version currency gaps (installed major vs. latest stable major),
  listed as findings independent of EOL/CVE status
- support/EOL unknowns when network is unavailable
- container image table: image, source (compose/FROM), scanned where,
  HIGH/CRITICAL fixable count split OS / app libs / bundled binaries,
  recommended action
