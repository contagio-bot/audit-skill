# audit dd

Full technical due diligence. This command has no logic of its own — it
delegates entirely to an existing skill.

## Delegation

`Read` and follow **`~/.claude/skills/tech-due-diligence/SKILL.md`** in
full, including its own `references/` (`investigation-protocol.md`,
`output-template.md`, `fintech-rules-checklist.md`).

No context branching is needed here: that skill already composes
`codebase-auditor` + `cybersecurity-infra-auditor` + investment/deal
framing + a full-repo security subagent, and it already conditions its
fintech-specific checklist step ("Conformità regole progetto ...") on
whether the target actually has a matching `CLAUDE.md`/`PROJECT.md` — so
it degrades gracefully on non-fintech, non-personal-finance-app repos too.

## Notes

- This is the only sub-command under `audit` that is itself a composite —
  don't also separately run `audit arch` / `audit security` / `audit
  deadcode` before or after it for the same target; that duplicates work
  `tech-due-diligence` already does internally.
- The delegated skill has its own marketplace-comparison section; if the
  user asks whether a better public skill exists for due diligence
  specifically, let that section answer rather than re-researching from
  scratch.
