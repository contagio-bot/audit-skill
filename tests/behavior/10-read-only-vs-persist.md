# Scenario: read-only vs default vs persist

## Input

Three runs on the same repo:

1. `audit security --read-only`
2. `audit security` (default)
3. `audit security --persist`

## Expected behavior

- run 1 performs no writes at all, including no report file
- run 2 writes only the report file (`docs/audit/<date>-security.md`);
  `AUDIT-CONTEXT.md` and baseline files stay untouched even if they exist
  and are read
- run 3 may additionally initialize or update `AUDIT-CONTEXT.md` and
  baseline files, only after disclosure and confirmation when judgment is
  being recorded

## Must not do

- treat all three runs as behaviorally identical
- write `AUDIT-CONTEXT.md` or a baseline file in run 2 without `--persist`
