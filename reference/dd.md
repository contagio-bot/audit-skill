# audit dd

Full technical due diligence. Composes five of the six atomic audits
internally: `deadcode`, `arch`, `security` (via the delegated
`tech-due-diligence` skill), plus `perf` and `deps` (run as their own
full dedicated passes — see "Additional composed audits" below). Only
`pentest` is excluded, since its dynamic phase needs a live-target
authorization gate a due-diligence run shouldn't trigger on its own.

## Context detection

The delegated skill (`tech-due-diligence`) composes `codebase-auditor` +
`cybersecurity-infra-auditor` + investment/deal framing + a full-repo
security subagent — but its own `SKILL.md` and
`references/fintech-rules-checklist.md` are written specifically for
personal-finance-app: hardcoded recon paths (`backend/app`,
`frontend/src`, `alembic`), a fixed bounded-context list (transactions,
investments, wealth, billing, health, admin), fintech-specific grep
targets (Powens/Enable Banking webhooks, `effective_user_id`), and a
readiness-matrix framing built around that project's own user-scale
tiers. None of that is safe to apply unchanged to an arbitrary target —
conditioning only the fintech-rules-checklist step on `CLAUDE.md`/
`PROJECT.md` presence, as the skill does today, is not enough by itself.

1. Resolve the target's repo root per `SKILL.md` » Context detection (shared rule).
2. If the root path contains `personal-finance-app/`, or the repo's own
   `CLAUDE.md`/`PROJECT.md` identifies it as that project:
   - `Read` and follow **`~/.claude/skills/tech-due-diligence/SKILL.md`**
     in full, including its own `references/` (`investigation-protocol.md`,
     `output-template.md`, `fintech-rules-checklist.md`), unchanged — it's
     already tuned for this repo.
3. Otherwise (any other target — this is the common case, don't skip it
   just because the target "looks similar enough"):
   - `Read` the same file for its *methodology* only: the 10-phase
     workflow shape, the non-negotiable principles (evidence tagging,
     file:line on Critical/Major, full-repo not a sample, run commands
     don't just read statically), the severity labels, and the report
     skeleton in `output-template.md`. That structure is transferable.
   - Do **not** reuse, unchanged: the Fase 1 hardcoded recon paths (derive
     the actual structure with generic `find`/`rg --files` against
     whatever this repo actually has), the Fase 2 bounded-context list
     (derive the domains that actually exist in this codebase instead),
     the Fase 4 grep patterns naming this other project's specific
     auth/webhook vendors (build the equivalent patterns for whatever
     auth/session/webhook stack this target actually uses — same rule as
     `audit security`'s generalization step), or
     `fintech-rules-checklist.md` (only relevant if this target's own
     `CLAUDE.md`/`PROJECT.md` defines an equivalent project-specific rule
     set — otherwise skip that step entirely rather than forcing fintech
     rules onto an unrelated project).
   - **Before Fase 0**, understand what this project actually is. Read its
     README, `package.json`/`pyproject.toml` description, top-level docs,
     and any `CLAUDE.md`/`PROJECT.md` to infer: what the product does, who
     it's for, roughly what stage it's at (pre-launch, live with real
     users, internal tool, etc.), and who owns/maintains it (solo, small
     team, org — from git history/CODEOWNERS/docs if visible). Never
     assume a specific vertical (fintech, SaaS, e-commerce, or any other),
     a specific user-base scale (do not default to a "SaaS with 20k
     users" framing or any other borrowed template), or a specific
     business model. If this can't be confidently inferred from the repo,
     use `AskUserQuestion` to ask directly — this is always better than
     guessing, since it determines what "production readiness" even means
     here and what counts as Critical vs Minor. Fold the answer into Fase
     0's deal-context capture rather than treating it as a separate step.
   - Tell the user this run is a generalized pass of a project-specific
     skill, same as `audit security` does in the equivalent situation.

## Additional composed audits (perf, deps)

`tech-due-diligence`'s own Fase 5 (dependencies) and Fase 6 (performance)
are intentionally narrow hand-picked passes, not the full sweeps. To give
`dd` real coverage of both, after the steps above also run, against the
same target:

1. `Read` and follow **`reference/perf.md`** in full — the dedicated
   performance/indices/query deep dive, exactly as if `audit perf` had
   been invoked standalone.
2. `Read` and follow **`reference/deps.md`** in full — the dedicated
   EOL/support-status + CVE sweep, exactly as if `audit deps` had been
   invoked standalone.

Don't skip either just because Fase 5/Fase 6 already touched the same
area lightly — those two phases stay in the main due-diligence narrative
as a quick summary, while `perf` and `deps` produce their own full,
separately-reported analysis (see `SKILL.md` » Report output). If a
finding from `perf` or `deps` duplicates something Fase 5/6 already
flagged, don't repeat it verbatim in both places — the component report
is the authoritative one; the main `tech-due-diligence` narrative can
just point at it.

## Notes

- This is the only sub-command under `audit` that is itself a composite —
  don't also separately run `audit arch` / `audit security` / `audit
  deadcode` / `audit perf` / `audit deps` before or after it for the same
  target; that duplicates work `dd` already does internally (see
  "Additional composed audits" above for `perf`/`deps`).
- `dd` never runs `audit pentest`'s dynamic phase — mention it as a
  separate opt-in follow-up if the user wants live exploit verification
  too.
- The delegated skill has its own marketplace-comparison section; if the
  user asks whether a better public skill exists for due diligence
  specifically, let that section answer rather than re-researching from
  scratch.
- Never carry over personal-finance-app's framing (fintech, self-hosted,
  ~20k-user scale tiers) into a generic `dd` run just because it's the
  most detailed example available — a mismatched vertical produces a
  report that misjudges severity throughout, not just in one section.
