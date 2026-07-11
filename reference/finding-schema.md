# Audit finding schema

Use this schema for normalized findings when the run supports structured
output, baseline comparison, or remediation planning.

## Logical fields

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

## Required rules

- `classification` must be `Observed`, `Inferred`, or `Not verifiable`
- `severity` is potential damage
- `confidence` is evidence strength
- `exploitability` is ease of exploitation
- `priority` is operational order
- `fingerprint` should stay stable across line moves
- `affected_paths` must contain only real repo paths when verified
