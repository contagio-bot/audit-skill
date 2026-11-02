# Routing scenarios

## No argument

- expected: render command menu
- must not: start an audit implicitly

## Valid command

- input: `audit security ./repo`
- expected: load `reference/security.md`, then delegated local methodology

## night-report

- input: `audit night-report ./click2job`
- expected: load `reference/night-report.md`, then `methodologies/night-report/SKILL.md`; run `scripts/nightly-audit/` if present with `AUDIT_MAIL_DRY=1`

## Unknown command

- input: `audit frobnicate ./repo`
- expected: ask or map only if natural-language intent is clear

## Natural-language request

- input: `can you compare what changed since the last audit?`
- expected: route to `diff`

## Target omitted

- expected: use current working directory
