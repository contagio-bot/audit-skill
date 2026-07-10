# audit-skill

Claude Code skill: a router for repository audits (`/audit`).

Delegates to bundled local methodologies and references for audit,
comparison, remediation, and continuity workflows. The package is
self-contained: no external skill paths are required for `deadcode`,
`arch`, `perf`, `security`, `pentest`, `deps`, `supply-chain`, `ci`,
`testing`, `data`, `api`, `cloud`, `operability`, `privacy`, `ai`,
`licensing`, `dd`, `baseline`, `diff`, `verify`, `fix-plan`, `issue`,
`context`, `recheck`, and `--profile`.

The skill now also includes:

- `reference/coverage-protocol.md` for explicit `full` / `partial` /
  `batched` / `risk-based` / `sample` coverage disclosure
- `reference/persistence-protocol.md` for `read-only` vs `persist` behavior
- `reference/capability-protocol.md`, `reference/inventory-protocol.md`,
  `reference/evidence-protocol.md`, `reference/finding-schema.md`, and
  `reference/output-contract.md` for shared audit mechanics
- `scripts/` with bundled stdlib helpers for inventory, capability
  detection, normalization, comparison, validation, SARIF export, and fix-plan building
- `schemas/` for finding, context, and report shapes
- `tests/behavior/` for scenario-based behavioral regression fixtures
- `tests/fixtures/` and `tests/test_*.md` for routing, context,
  baseline/diff, and failure-mode checks
