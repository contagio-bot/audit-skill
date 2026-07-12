# Audit finding contract

Semantic rules for findings, evidence, lifecycle, and cross-audit
ownership. Field names, types, and enums are the source of truth in
`schemas/finding.schema.json` and `schemas/audit-report.schema.json` —
don't re-derive them here; read the schema when you need exact shape.

## Findings

Normalize findings to this schema whenever the run supports structured
output, baseline comparison, or remediation planning:

```yaml
id: SEC-AUTH-004
title: Missing object-level authorization
audit_type: api
category: authorization
status: new
classification: Observed
severity: high
confidence: high
exploitability: medium
likelihood: medium
impact: high
priority: P1
summary: User-controlled object identifiers are fetched without ownership checks.
evidence:
  - E-014
affected_paths:
  - services/api/routes/invoices.ts
scope:
  component: billing-api
recommendation: Enforce tenant and owner checks in the repository layer.
fingerprint: api:invoice-id:missing-owner-check
first_seen: 2026-07-10
last_seen: 2026-07-10
schema_version: "1.0"
framework_version: "0.4.0"
methodology_version: "api/1.0"
fingerprint_version: "1"
```

Rules: `classification` is `Observed` / `Inferred` / `Not verifiable`;
`severity` is potential damage, `confidence` is evidence strength,
`exploitability` is ease of exploitation, `priority` is operational
order; `fingerprint` should stay stable across line moves;
`affected_paths` must contain only real repo paths when verified.

## Evidence

Maintain an evidence ledger for every substantial run. Use stable IDs in
run order (`E-001`, `E-002`, ...). Types: `file`, `command`, `inference`.

```yaml
- id: E-001
  type: file
  source: .github/workflows/release.yml
  location: lines 18-31
  summary: third-party action referenced by mutable tag
```

Rules: every substantive finding must reference at least one evidence
ID; `Observed` findings should have at least one direct evidence item;
`Inferred` findings must cite/explain what they're inferred from; never
substitute a generic best-practice claim for evidence.

## Lifecycle

States: `new`, `existing`, `changed`, `resolved`, `accepted`, `deferred`,
`false-positive`, `not-verifiable`, `superseded`, `regressed`.

- `new` — first observed in the current baseline/diff window
- `existing` — same issue, unchanged
- `changed` — same issue, materially modified
- `resolved` — no longer present in the current target
- `accepted` — intentionally kept with an explicit user-approved risk note
- `deferred` — not fixed yet, intentionally postponed
- `false-positive` — current evidence disproves the concern
- `not-verifiable` — not enough evidence to confirm
- `superseded` — replaced by a newer equivalent finding
- `regressed` — returned after being resolved

Typical transitions: `new -> existing|changed|resolved|accepted|deferred|false-positive`,
`existing -> changed|resolved|accepted`, `resolved -> regressed`,
`changed -> superseded`.

Rules: `first_seen` records the earliest observation of the underlying
issue; `last_seen` updates while the issue is still present; `accepted`
and `deferred` states must carry a review condition; `superseded`
findings should reference their replacement fingerprint when possible.

## Cross-audit ownership (boundaries)

Avoid duplicated ownership across audit commands:

```yaml
primary_owner: supply-chain
related_audits:
  - deps
  - ci
```

Rules: every audit area has one primary owner; secondary areas may
reference a finding but should redirect when the owner is clearly more
appropriate; aggregated reports (e.g. `dd`) deduplicate by fingerprint
and show cross-links; related audits may cross-reference a finding but
must not duplicate it.

Suggested ownership: `deadcode` — dead code, duplication, refactoring;
`arch` — architecture, design, code health; `perf` — query/index/data-path
performance; `security` — cyber risk and infrastructure hardening;
`pentest` — static attack surface and live verification; `deps` —
runtime and dependency freshness; `supply-chain` — provenance and
dependency integrity; `ci` — workflow integrity and release pipeline
trust; `testing` — test strategy and regression resistance; `data` —
data modeling and lifecycle; `api` — APIs and webhooks; `cloud` —
cloud/IaC/container runtime; `operability` — production operability;
`privacy` — technical privacy behavior; `ai` — model/agent risk;
`licensing` — license and asset risk.
