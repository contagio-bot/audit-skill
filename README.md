# audit-skill

Claude Code skill: a router for repository audits (`/audit`).

Delegates to four sub-commands — `deadcode`, `arch`, `security`, `dd` —
plus `--profile`, each of which loads and follows a bundled local
methodology rather than depending on external skill paths. See
`SKILL.md` for the full routing rules, `profiles/` for repo-specific
selection, and `reference/context-protocol.md` for the shared
`AUDIT-CONTEXT.md` mechanism that prevents repeat audits from re-flagging
decisions already accepted as intentional.

The skill now also includes:

- `reference/coverage-protocol.md` for explicit `full` / `partial` /
  `sample` coverage disclosure
- `reference/persistence-protocol.md` for `read-only` vs `persist` behavior
- `tests/behavior/` for scenario-based behavioral regression fixtures
