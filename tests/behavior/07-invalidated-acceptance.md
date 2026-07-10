# Scenario: accepted risk no longer applies

## Input

An acceptance entry's invalidation condition has been met.

## Expected behavior

- classify it as previously accepted but no longer applicable
- reopen the underlying finding if the current code still has the issue

## Must not do

- keep suppressing the finding
