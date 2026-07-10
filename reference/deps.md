# audit deps

Fast, isolated dependency/runtime freshness sweep: EOL/support-status
across every direct dependency, plus a known-CVE scan. This command has
no logic of its own — it delegates entirely to an existing skill.

## Delegation

`Read` and follow **`~/.claude/skills/deps-auditor/SKILL.md`** in full.

No context branching is needed here: the skill auto-detects every
ecosystem present in the target repo and adapts its tooling accordingly.
Use it unchanged for any target.

## Notes

- `dd` now composes this full `deps` sweep internally (its own
  `docs/audit/deps-<date>.md` component report — see `reference/dd.md` »
  "Additional composed audits"), alongside `tech-due-diligence`'s lighter
  "Fase 5 — Dependency & Runtime Currency" narrative. If the user just ran
  `dd`, don't re-run `deps` right after for the same repo unless they
  specifically want a fresher check between `dd` runs — point them at the
  `deps` component report from that `dd` run instead.
- `arch`'s "Dependency & Runtime Currency" category is intentionally
  narrower (4-5 central components, one line in a 10-category review) —
  don't treat it as equivalent to `deps` if the user wants full coverage.
