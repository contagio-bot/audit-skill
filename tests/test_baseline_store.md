# Baseline store scenarios

## Save baseline

- expected: writes `.audit/baselines/<audit_type>/current.json`
- expected: archives a timestamped history snapshot

## Load baseline

- expected: returns current snapshot when available
- expected: falls back to latest history snapshot

## No baseline

- expected: explicit not-found result instead of a crash
