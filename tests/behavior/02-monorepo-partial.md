# Scenario: monorepo

## Input

Target repo contains multiple independent services and the user does not
name one.

## Expected behavior

- ask which service/package is in scope
- if the user picks one path, classify coverage as `partial`
- disclose excluded services explicitly

## Must not do

- silently pick the biggest service
- report the run as `full` for the whole monorepo
