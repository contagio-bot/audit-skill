# Audit finding lifecycle

## States

- `new`
- `existing`
- `changed`
- `resolved`
- `accepted`
- `deferred`
- `false-positive`
- `not-verifiable`
- `superseded`
- `regressed`

## Meaning

- `new`: first time observed in the current baseline or diff window
- `existing`: same issue already present and unchanged
- `changed`: same issue, but materially modified
- `resolved`: no longer present in the current target
- `accepted`: intentionally kept with an explicit user-approved risk note
- `deferred`: not fixed yet, but intentionally postponed
- `false-positive`: current evidence disproves the concern
- `not-verifiable`: not enough evidence to confirm
- `superseded`: replaced by a newer equivalent finding
- `regressed`: returned after being resolved

## Transitions

- `new -> existing`
- `new -> changed`
- `new -> resolved`
- `new -> accepted`
- `new -> deferred`
- `new -> false-positive`
- `existing -> changed`
- `existing -> resolved`
- `existing -> accepted`
- `resolved -> regressed`
- `changed -> superseded`

## Rules

- `first_seen` records the earliest observation of the underlying issue
- `last_seen` updates when the issue is still present
- accepted or deferred states must carry a review condition
- superseded findings should reference their replacement fingerprint when possible
