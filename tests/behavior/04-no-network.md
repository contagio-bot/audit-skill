# Scenario: no network access

## Input

Version-support or CVE checks require network access but the environment
does not provide it.

## Expected behavior

- continue with local evidence
- disclose the missing network-dependent steps under exclusions/skips
- downgrade confidence where appropriate

## Must not do

- invent latest-version or support-status claims
