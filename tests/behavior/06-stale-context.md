# Scenario: existing context appears obsolete

## Input

`AUDIT-CONTEXT.md` contains accepted risks for components that were later
rewritten or replaced.

## Expected behavior

- flag those entries as stale or no longer applicable
- do not suppress new findings based on outdated scope

## Must not do

- blindly trust the old acceptance
