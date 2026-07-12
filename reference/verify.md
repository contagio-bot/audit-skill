# audit verify

Revalidate one finding and its immediate dependencies.

## Delegation

Read and follow:

- `reference/finding-contract.md`
- `reference/baseline-protocol.md`
- `scripts/load_baseline.py`

## Workflow

1. Resolve the target finding by ID or fingerprint.
2. Inspect only the immediate code/config/test dependencies needed to revalidate it.
3. Classify it as `resolved`, `still-present`, `worsened`, or `not-verifiable`.

Do not rerun a full audit unless the user explicitly asks for that.
