# Audit evidence schema

Use this schema for evidence items referenced by findings.

```yaml
id: E-001
type: file
source: .github/workflows/release.yml
location: lines 18-31
summary: third-party action referenced by mutable tag
```

## Rules

- evidence IDs must be unique within a run
- every substantive finding must reference at least one evidence ID
- `Observed` findings should have at least one direct evidence item
- `Inferred` findings must explain what they are inferred from
