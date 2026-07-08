# audit deadcode

Dead code, duplication, and structural-refactoring audit. This command has
no logic of its own — it delegates entirely to one of two existing skills.

## Context detection

1. Resolve the target's repo root per `SKILL.md` » Context detection (shared rule).
2. If the root path contains `personal-finance-app/`, or the repo's own
   `CLAUDE.md` / `PROJECT.md` identifies it as the personal-finance-app
   monorepo:
   - `Read` and follow **`/Users/giorgio.contarini/contagio/personal/personal-finance-app/skills/code-health-audit/SKILL.md`** in full.
   - This variant is tuned to this repo: it knows about `frontend/knip.json`,
     the repo's own `npm run check:dead` / `check:dup` scripts, vulture
     confidence thresholds for FastAPI/SQLAlchemy/Pydantic false positives,
     and known duplication hotspots (scheduler/email campaigns, seed
     scripts, spending aggregation logic).
3. Otherwise:
   - `Read` and follow **`~/.agents/skills/deadcode-refactor-audit/SKILL.md`** in full.
   - This variant auto-detects the stack (Python via `pyproject.toml`/
     `requirements.txt`, frontend via `package.json`) and runs the generic
     equivalent tooling (`knip`, `jscpd`, `ruff`, `vulture`) without
     repo-specific assumptions.

## After delegating

Both skills only *report* findings — they never apply fixes. If the user
wants fixes applied after reviewing the report, hand off explicitly to the
`knip` skill (frontend), `ruff --fix` (backend), or the `dry-refactoring`
skill (clone elimination), as the delegated skill itself instructs.

## Notes

- Do not merge or summarize the two source skills' instructions from memory
  — always read the one selected above fresh, since it may have been
  updated since this router was written.
- If neither skill file exists at the path above when you check (moved,
  renamed, deleted), stop and tell the user rather than improvising a
  replacement audit.
