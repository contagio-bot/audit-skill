# Audit baseline protocol

Baselines make successive audits comparable.

## What a baseline stores

- target repo and scope
- commit hash when available
- coverage mode
- persistence mode
- finding fingerprints and statuses
- timestamp

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
- Baselines may be produced in memory in `read-only` mode, but are only
  written in `persist` mode.
- `diff` and `verify` should prefer normalized findings with fingerprints.
- The current baseline should represent the latest approved snapshot for
  the target scope; history preserves prior runs for comparison.
