# Audit baseline protocol

Baselines make successive audits comparable.

## What a baseline stores

- target repo and scope
- commit hash when available
- coverage mode
- persistence mode
- finding fingerprints and statuses
- timestamp
- version fields
- content hash
- approved flag when explicitly promoted

## Storage layout

Persisted baselines live under the target repo at:

- `.audit/baselines/<audit_type>/current.json`
- `.audit/baselines/<audit_type>/history/<timestamp>-<commit>.json`

Use the bundled scripts:

- `scripts/save_baseline.py`
- `scripts/load_baseline.py`
- `scripts/validate_output_contract.py`

## Rules

- Do not mutate accepted risks automatically while creating a baseline.
- Baselines may be produced in memory without `--persist`, but are only
  written to disk with `--persist` (or when the command is itself
  `baseline`).
- `diff` and `verify` should prefer normalized findings with fingerprints.
- The current baseline should represent the latest snapshot for the target
  scope; `approved.json` stores the last explicitly promoted baseline.
