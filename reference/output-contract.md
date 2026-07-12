# Audit output contract (formal)

This is the `formal` shape. `standard` (the default) lives inline in
[bootstrap-lite.md](bootstrap-lite.md) — read this file only when the run
is formal (see [formal-delta.md](formal-delta.md) for the triggers). This
choice is about output shape/rigor only — it's independent of
[persistence-protocol.md](persistence-protocol.md), which governs writes.

Validate with `scripts/validate_output_contract.py <path> [--mode standard|formal] [--strict]`.

## `formal`

The full eight-section contract, each a top-level heading, each finding
normalized per [finding-contract.md](finding-contract.md):

1. **Executive summary** — 3-8 lines, top strengths/concerns/risks.
2. **Scope and coverage** — requested scope, resolved scope, coverage
   mode, excluded areas, confidence impact.
3. **Capability manifest** — available tools, unavailable tools,
   network/git/write status.
4. **Method and evidence** — commands used, evidence ledger summary,
   skipped steps and why.
5. **Detailed findings** — severity ordered, each linked to evidence
   IDs, each classified `Observed`/`Inferred`/`Not verifiable`.
6. **Normalized findings** — conforms to
   [finding-contract.md](finding-contract.md).
7. **Remediation** — prioritized recommendations, acceptance criteria.
8. **Persistence disclosure** — persistence mode, writes performed,
   writes skipped.

Version fields (`schema_version`, `framework_version`,
`methodology_version`, `fingerprint_version`) are required in `formal`
mode; optional in `standard`.

### Always use `formal`, regardless of flags

- `baseline`, `diff`, `verify`, `recheck` (they compare fingerprints —
  need the normalized shape)
- `dd` (composite due-diligence deliverable)
- `--format json|csv|sarif|github-issues` (exports need the normalized schema)
- `--persist` combined with historical/baseline comparison
- the user explicitly asks for the full/formal report

Otherwise use `standard`. `--formal` forces it explicitly for any command.

## Area-specific addendum

Each methodology may append one required area-specific artifact (matrix,
flow map, dependency inventory, endpoint control table, ...). It
supplements the sections above in both modes; it never replaces them.
