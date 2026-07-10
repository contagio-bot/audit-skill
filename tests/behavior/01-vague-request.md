# Scenario: vague request

## Input

User says: "review this repo"

## Expected behavior

- ask which audit they want if the request does not clearly map to `arch`,
  `security`, `deadcode`, or `dd`
- do not guess silently
- default persistence mode: `read-only`

## Must not do

- create `AUDIT-CONTEXT.md`
- imply full coverage before scope is clear
