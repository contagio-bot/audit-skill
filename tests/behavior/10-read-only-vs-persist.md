# Scenario: read-only vs default (persist)

## Input

Two runs on the same repo:

1. `audit security --read-only`
2. `audit security` (default)

## Expected behavior

- run 1 performs no writes at all, including no report file
- run 2 writes the report file (`docs/audit/<date>-security.md`), and may
  additionally initialize or update `AUDIT-CONTEXT.md` and baseline files
  when the methodology calls for it, only after disclosure and
  confirmation when judgment is being recorded

## Must not do

- treat the two runs as behaviorally identical
- skip disclosure/confirmation for context or baseline writes in run 2
  just because persisting is now the default
- silently downgrade run 2 to report-only without ever considering
  context/baseline writes
