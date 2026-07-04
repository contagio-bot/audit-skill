# audit deps

Fast, isolated dependency/runtime freshness sweep: EOL/support-status
across every direct dependency, plus a known-CVE scan. This command has
no logic of its own — it delegates entirely to an existing skill.

## Delegation

`Read` and follow **`~/.claude/skills/deps-auditor/SKILL.md`** in full.

No context branching is needed here: the skill auto-detects every
ecosystem present in the target repo and adapts its tooling accordingly.
Use it unchanged for any target, including personal-finance-app.

## Notes

- `dd` already runs an equivalent pass internally as its own "Fase 5 —
  Dependency & Runtime Currency" step (hand-picked components: Python/
  Node runtime, FastAPI, React, Authlib/PyJWT, Stripe SDK, banking
  integration, plus a CVE scan). If the user just ran `dd`, don't re-run
  `deps` right after for the same repo — point them at that section of
  the `dd` report instead. Run `deps` on its own when they want the full
  direct-dependency sweep without the rest of a due-diligence engagement,
  or want a fresher check between `dd` runs.
- `arch`'s "Dependency & Runtime Currency" category is intentionally
  narrower (4-5 central components, one line in a 10-category review) —
  don't treat it as equivalent to `deps` if the user wants full coverage.
