# Audit finding contract

Loaded only for `formal` mode (see [formal-delta.md](formal-delta.md)) or
structured commands. Field names, types, and enums (including lifecycle
`status` and `classification`) are the source of truth in
`schemas/finding.schema.json` and `schemas/audit-report.schema.json` —
read those for exact shape, and see
`tests/fixtures/finding-example.yaml` for a full example. Use
`scripts/normalize_findings.py` to fill derived fields (id, fingerprint,
versions, first/last seen) rather than hand-authoring them.

Semantic rules:

- every finding cites at least one evidence ID; `Observed` needs direct
  evidence, `Inferred` must cite what it's inferred from
- `fingerprint` stays stable across line moves; dedupe by fingerprint
- preserve `first_seen` across reruns of the same underlying issue
- `accepted`/`deferred` require user confirmation and a review condition
- `resolved` findings may reference historical paths
- one primary owner per audit area — see
  [config/audit-boundaries.json](../config/audit-boundaries.json);
  secondary/related audits may cross-reference but not duplicate
