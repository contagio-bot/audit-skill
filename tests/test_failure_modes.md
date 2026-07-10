# Failure mode scenarios

## Missing methodology

- expected: stop and name the missing bundled file

## Invalid JSON

- expected: validation failure from local script, no silent fallback

## SARIF export with non-localizable finding

- expected: exclude that finding from SARIF

## Tool command failed

- expected: disclose skip/failure and downgrade confidence

## Interrupted audit

- expected: downgrade final coverage
