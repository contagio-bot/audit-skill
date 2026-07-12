---
name: audit
description: "Router for repository audits, baselines, diffs, verification, and remediation planning. Delegates only to bundled methodologies, references, schemas, and local stdlib scripts. Supports explicit coverage, persistence, capability, evidence, and export protocols without external skill dependencies."
argument-hint: "[command] [target] [--read-only|--persist] [--formal] [--format ...]"
user-invocable: true
license: MIT
---

# Audit router

Single entry point for the audit framework. The router stays thin:

- recognize user intent
- resolve target and repo root
- resolve coverage and persistence mode
- resolve profile and capability/inventory manifests
- delegate to the bundled methodology/reference files needed for that command

It must not inline specialist audit logic.

**Never re-derive methodology from memory.** Always `Read` the delegated
local file and any references it names before running that command.

## Commands

The canonical command → category/reference/methodology mapping lives in
[config/audits.json](config/audits.json).

Resolve explicit commands with:

`scripts/resolve_command.py <command> [--formal] [--format ...] [--persist]`

— it prints the full loading plan (mode, files, scripts, validation) for
that command. For the no-argument menu, use:

`scripts/resolve_command.py --menu`

`target` defaults to the current working directory if omitted.

## Optional modifiers

- `--read-only` / `--persist`: writes gate — default is report-only, see
  [reference/persistence-protocol.md](reference/persistence-protocol.md)
- `--full` / `--partial` / `--batched` / `--risk-based` / `--sample`:
  coverage mode — see [reference/bootstrap-lite.md](reference/bootstrap-lite.md)
- `--standard` (default) / `--formal`: report shape — `formal` always
  applies for `baseline`/`diff`/`verify`/`recheck`/`dd` or non-markdown
  `--format`
- `--format markdown|json|csv|sarif|github-issues`: per
  [reference/export-formats.md](reference/export-formats.md); non-markdown
  implies `--formal`

## Routing rules

1. No argument: render the command menu (below) and ask what the user
   wants.
2. `--profile`: load [reference/profile.md](reference/profile.md).
3. Known command: run `scripts/resolve_command.py <command>` and `Read`
   every file its loading plan lists, then follow them exactly.
4. Natural-language request: map it only when intent is materially clear.
5. If ambiguity would change the outcome, ask instead of guessing.

### No-argument menu

Render `scripts/resolve_command.py --menu`'s output, grouped by category,
not the full table. Don't dump the modifier list up front — only mention
`--read-only` exists, and surface the rest (`--persist`, coverage flags,
`--formal`, `--format`) only if the user asks or their answer needs one.

## Shared protocols

Every substantive run resolves [reference/bootstrap-lite.md](reference/bootstrap-lite.md)
first (capability detection, inventory, coverage, persistence defaults,
run order, standard 4-section output). `scripts/resolve_command.py
<command>` decides what else to add: persistence-protocol.md when the run
persists beyond the report; formal-delta.md + finding-contract.md +
output-contract.md when the run is `formal` (always true for
`baseline`/`diff`/`verify`/`recheck`/`dd`, non-markdown `--format`, or
`--formal`).

Load these only when the command actually needs them, not on every run:

- [reference/scoring-rubric.md](reference/scoring-rubric.md) — only when scoring applies
- [reference/baseline-protocol.md](reference/baseline-protocol.md) — only for `baseline`, `diff`, `verify`, `recheck`, or `--persist` with historical comparison
- [reference/remediation-protocol.md](reference/remediation-protocol.md) — only for `fix-plan`/`issue`
- [reference/export-formats.md](reference/export-formats.md) and [reference/versioning.md](reference/versioning.md) — only when `--format` is not the default markdown

## Self-contained rule

This package must be self-contained. Do not delegate to `~/.claude`,
`~/.agents`, absolute machine-local paths, or marketplace skills — every
delegation must point to `reference/`, `methodologies/`, `profiles/`,
`scripts/`, or `schemas/` inside this package. If a needed bundled file is
missing, stop and tell the user exactly which one.

## Standing context across runs

If `AUDIT-CONTEXT.md` exists, delegated methodologies must read it per
[reference/context-protocol.md](reference/context-protocol.md). This file
records standing facts, accepted risks, audit plan state, and open
follow-ups. It may always be read, but is only created or modified with
`--persist` (or when the command is itself `context`).

## Adding a new area

1. add one entry to [config/audits.json](config/audits.json) — set
   `reference` to `null` unless the command needs logic beyond plain
   delegation to its methodology
2. add one bundled methodology under `methodologies/`
3. update tests, schemas, and protocols if the new area changes shared
   behavior

Do not inline the new area's logic into this router.
