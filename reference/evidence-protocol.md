# Audit evidence protocol

Maintain an evidence ledger for every substantial run.

## Evidence IDs

Use stable IDs in run order:

- `E-001`
- `E-002`
- `E-003`

## Evidence types

- `file`
- `command`
- `inference`

## Recommended shape

```yaml
- id: E-001
  type: file
  source: .github/workflows/release.yml
  location: lines 18-31
  summary: third-party action referenced by mutable tag
```

## Rules

- Every substantive finding must reference at least one evidence ID.
- `Inferred` findings must cite the evidence they are based on.
- Do not use standards or generic best practices as a substitute for evidence.
