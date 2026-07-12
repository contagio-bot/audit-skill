# Output contract scenarios

## Default standard run

- a plain `audit security` with no special flags
- expected: 4 sections (Summary, Coverage and limits, Findings,
  Recommended next actions) — capability manifest and persistence
  disclosure folded into "Coverage and limits", not separate headings

## Formal run

- `audit security --formal`, or `--format json`, or `baseline` / `diff` /
  `verify` / `recheck` / `dd` regardless of flags
- expected: all 8 sections (executive summary, scope/coverage,
  capability manifest, method/evidence, detailed findings, normalized
  findings, remediation, persistence disclosure)

## Structured continuity run

- when baseline/diff/verify/fix-plan is requested, findings should be
  representable using `reference/finding-contract.md`

## Area-specific addendum

- expected: methodology-specific matrix/map/inventory appears in addition
  to the common output sections (in either mode), not instead of them
