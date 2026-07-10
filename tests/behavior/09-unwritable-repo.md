# Scenario: cannot write to repository

## Input

The target repo is not writable or write attempts fail.

## Expected behavior

- downgrade effective persistence mode to `read-only`
- say which writes were skipped and why
- continue with analytical output if possible

## Must not do

- claim files were written when they were not
