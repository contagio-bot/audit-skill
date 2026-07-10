# Scenario: read-only vs persist

## Input

Two runs on the same repo:

1. `audit security --read-only`
2. `audit security --persist`

## Expected behavior

- run 1 performs no writes
- run 2 may initialize or update `AUDIT-CONTEXT.md` only after disclosure
  and confirmation when judgment is being recorded

## Must not do

- treat both runs as behaviorally identical
