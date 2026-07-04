# audit security

Cybersecurity and infrastructure/operability audit. This command has no
logic of its own — it delegates to an existing skill, generalizing it only
when necessary.

## Context detection

1. Resolve the target's repo root.
2. If the root path contains `personal-finance-app/`, or the repo's own
   `CLAUDE.md` / `PROJECT.md` identifies it as the personal-finance-app
   monorepo:
   - `Read` and follow **`/Users/giorgio.contarini/contagio/personal/personal-finance-app/skills/cybersecurity-infra-auditor/SKILL.md`** in full, unchanged.
   - This variant already has the right grep patterns for this stack:
     Google OAuth/Authlib sessions, `effective_user_id`, Powens/Enable
     Banking webhooks, Docker Compose + Caddy, APScheduler-style jobs.
3. Otherwise (no dedicated tailored skill exists for this target yet):
   - `Read` **the same file** (`cybersecurity-infra-auditor/SKILL.md`) for
     its *methodology* (scope categories, workflow steps 1-7, output
     contract, evidence tagging rules) — that structure is stack-agnostic.
   - Do **not** reuse its literal grep patterns as-is (they name this
     repo's specific libraries/vendors). Instead, before step 3 of its
     workflow, spend one pass identifying the target's actual auth
     library, session/cookie mechanism, secret-loading approach, scheduler/
     queue system, and third-party integrations that move sensitive data —
     then build the equivalent `rg` patterns for what's actually there.
   - Tell the user this run is a generalized pass of a project-specific
     skill, and that a dedicated tuned skill is worth creating if they'll
     audit this repo regularly (same pattern as `code-health-audit` vs
     `deadcode-refactor-audit`).

## Notes

- Keep the "fewer high-confidence findings over many speculative ones"
  standard from the source skill regardless of which branch is taken.
- If the user actually wants a due-diligence-scoped security pass (with a
  full-repo subagent and CVE scanning), redirect to `audit dd` instead —
  that flow already extends this one with those steps.
