# audit baseline

Create or refresh a baseline snapshot for later comparison.

## Delegation

Read and follow:

- `reference/baseline-protocol.md`
- `reference/finding-schema.md`
- `reference/persistence-protocol.md`
- `scripts/normalize_findings.py`

## Workflow

1. Resolve target, coverage, persistence, capabilities, and inventory.
2. Run the relevant audit methodology or import an existing normalized result.
3. Normalize findings and generate fingerprints.
4. Store or present the baseline snapshot depending on persistence mode.
