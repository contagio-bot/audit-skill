# Scenario: audit interrupted halfway

## Input

The run begins as intended `full` coverage but stops early.

## Expected behavior

- downgrade final coverage to `partial` or `sample`
- disclose what was actually inspected
- avoid updating run history unless the user confirms a partial record in
  `persist` mode

## Must not do

- present the incomplete run as a full audit
