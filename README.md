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

- `config/audits.json`, the single source of truth for command →
  category/reference/methodology, resolvable deterministically with
  `scripts/resolve_command.py <command>`
- `config/loading-budget.json`, a regression guard capping how many
  common references/methodology files each command may load
- `reference/bootstrap-lite.md` for capability detection, inventory,
  explicit `full` / `partial` / `batched` / `risk-based` / `sample`
  coverage disclosure, and the standard 4-section output shape — the only
  common file every command loads
- `reference/persistence-protocol.md` for `read-only` / default
  (report written, repo otherwise untouched) / `--persist` behavior,
  loaded only when a run persists beyond the report
- `reference/formal-delta.md`, `reference/finding-contract.md`, and
  `reference/output-contract.md` for the `formal` shape (normalized
  findings, evidence ledger, full 8-section report) — loaded only when
  the run is formal; `formal` always applies to
  `baseline`/`diff`/`verify`/`recheck`/`dd` and to any non-markdown
  `--format`
- `config/audit-boundaries.json` for cross-audit finding ownership and
  `config/modes.json` for standard/formal mode capability flags
- `methodologies/dd/SKILL.md` runs its 10 phases sequentially, normalizing
  and scratching each phase's findings to `.audit/tmp/` (or in-memory in
  `--read-only` runs) instead of holding all phases in context at once
- `scripts/` with bundled stdlib helpers for inventory, capability
  detection, command resolution, normalization, comparison, validation
  (`standard`/`formal` modes), SARIF export, and fix-plan building
- `schemas/` for finding, context, and report shapes
- `tests/behavior/` for scenario-based behavioral regression fixtures
- `tests/fixtures/` and `tests/test_*.md` for routing, context,
  baseline/diff, and failure-mode checks
- `tests/test_loading_plan.py` and `tests/test_reference_budget.py` for
  automated regression checks on what each command loads
