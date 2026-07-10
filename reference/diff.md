# audit diff

Compare findings across two revisions using fingerprints.

## Delegation

Read and follow:

- `reference/baseline-protocol.md`
- `reference/finding-schema.md`
- `scripts/load_baseline.py`
- `scripts/compare_findings.py`

## Workflow

1. Resolve `base` and `head`.
2. Determine changed files and affected scope.
3. Compare normalized findings by fingerprint.
4. Classify: `new`, `resolved`, `worsened`, `improved`, `unchanged`, `not-revalidated`.
