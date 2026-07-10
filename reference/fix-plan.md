# audit fix-plan

Build a remediation roadmap from normalized findings.

## Delegation

Read and follow:

- `reference/remediation-protocol.md`
- `scripts/build_fix_plan.py`

## Workflow

1. Load findings from the current run, a baseline, or an imported JSON file.
2. Group them into remediation buckets.
3. Order work by risk reduction and dependency constraints.
