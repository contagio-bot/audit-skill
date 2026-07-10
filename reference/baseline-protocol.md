# Audit baseline protocol

Baselines make successive audits comparable.

## What a baseline stores

- target repo and scope
- commit hash when available
- coverage mode
- persistence mode
- finding fingerprints and statuses
- timestamp

## Rules

- Do not mutate accepted risks automatically while creating a baseline.
- Baselines may be produced in memory in `read-only` mode, but are only
  written in `persist` mode.
- `diff` and `verify` should prefer normalized findings with fingerprints.
