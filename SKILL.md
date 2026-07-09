---
name: audit
description: "Router for repository audits. Use when the user asks to audit, review, or assess a codebase for dead code/duplication/refactoring, architecture/bugs/performance/readability, database/query/index performance optimization, cybersecurity/infrastructure risk, penetration testing/exploit verification, dependency/EOL/CVE freshness, or a full technical due diligence. Delegates to dedicated, already-tuned skills instead of re-implementing their logic; picks the project-tuned version when the target repo is personal-finance-app, and the stack-agnostic version otherwise. Every command writes its full analysis and action items to a markdown report under docs/audit/ in the target repo."
argument-hint: "[deadcode|arch|perf|security|pentest|deps|dd|context|recheck] [target]"
user-invocable: true
license: MIT
---

# Audit router

Single entry point for the seven audit types this toolkit supports, plus
two commands for managing the standing context file directly. This skill
does not contain audit logic itself — every sub-command loads and follows
an existing dedicated skill/reference file in full (`perf` is the one
exception: no external skill exists for it yet, so its reference file
carries the methodology directly). Its only job is routing and, where
relevant, picking the project-tuned variant over the generic one — plus,
for every atomic/composite audit command, making sure a markdown report
actually gets written to disk at the end (see "Report output", below).

**Never re-derive the underlying methodology from memory.** Always `Read`
the delegated `SKILL.md` (and any `references/*.md` it points to) before
running commands — that file is the source of truth, this router is not.

## Commands

| Command | Category | Description | Reference |
|---|---|---|---|
| `deadcode [target]` | Quality | Dead code, duplication, refactoring/simplification candidates | [reference/deadcode.md](reference/deadcode.md) |
| `arch [target]` | Quality | Hidden bugs, performance issues, readability, architectural smells (10-category review) | [reference/arch.md](reference/arch.md) |
| `perf [target]` | Quality | Performance optimization deep dive: indices, query patterns, query plans, caching/batching | [reference/perf.md](reference/perf.md) |
| `security [target]` | Risk | Cybersecurity weaknesses and infrastructure/operability criticalities | [reference/security.md](reference/security.md) |
| `pentest [target]` | Risk | Attack-surface mapping + gated, authorized-only dynamic exploit verification | [reference/pentest.md](reference/pentest.md) |
| `deps [target]` | Risk | EOL/support-status sweep across every direct dependency + known-CVE scan | [reference/deps.md](reference/deps.md) |
| `dd [target]` | Risk | Full technical due diligence (composes `deadcode` + `arch` + `security` + `perf` + `deps` + deal framing — only `pentest` is excluded, gated behind live-target authorization) | [reference/dd.md](reference/dd.md) |
| `context [target]` | Context | Create or update `AUDIT-CONTEXT.md` explicitly | [reference/context.md](reference/context.md) |
| `recheck [target]` | Context | Check only the open follow-ups in `AUDIT-CONTEXT.md` against current repo state | [reference/recheck.md](reference/recheck.md) |

`target` is a path or repo; defaults to the current working directory / repo if omitted.

### Routing rules

1. **No argument**: render the table above as the user-facing command menu,
   grouped by category. Ask what they'd like to do.
2. **First word matches a command**: load its reference file and follow its
   instructions exactly — including any context-detection step. Everything
   after the command name is the `target`.
3. **First word doesn't match any command**: general audit invocation, same
   spirit as impeccable's free-text case. Don't guess which of the seven
   this means — ask (e.g. "review this for bugs" → `arch`, "is this
   secure?" → `security`, "can someone actually break in?" → `pentest`,
   "what needs updating / is anything EOL?" → `deps`, "queries/indices are
   slow" → `perf`) since the seven audits are not interchangeable and
   picking wrong wastes the whole run.

### Report output (mandatory for every command)

Every atomic or composite audit command (`deadcode`, `arch`, `perf`,
`security`, `pentest`, `deps`, `dd`) must end by writing its full analysis
to a markdown report on disk, in addition to presenting it in the
conversation — the delegated skill producing findings in chat is not
sufficient by itself. `context` and `recheck` are exempt: they manage
`AUDIT-CONTEXT.md` directly and don't produce a fresh audit report.

1. Resolve the target repo root the same way as context detection
   (`git rev-parse --show-toplevel`, or cwd if no target given). Derive
   `{nome_progetto}` as the basename of that repo root (e.g. repo root
   `/Users/x/contagio/personal/personal-finance-app` → `nome_progetto` =
   `personal-finance-app`).
2. Ensure `docs/audit/` exists under that root, creating `docs/` and
   `docs/audit/` if either is missing.
3. Write the full analysis to
   `docs/audit/<command>-<YYYY-MM-DD>.md` (e.g.
   `docs/audit/perf-2026-07-08.md`). If a report for that command already
   exists for today's date, overwrite it rather than creating a
   duplicate-numbered file — re-running the same command same-day means
   the previous run is superseded.
4. The report must contain, at minimum:
   - A one-line header at the very top of the file stating the project
     name, e.g. `Progetto: {nome_progetto}`, so reports remain
     identifiable once copied out of `docs/audit/` into an external
     archive (filenames alone lose that context once moved).
   - The full analysis exactly as produced by the delegated skill
     (summary, evidence, detailed findings — whatever structure that
     skill's own output format specifies).
   - A clearly separated, actionable section titled **"Implementazioni da
     fare"** listing the concrete follow-up work, derived from that
     skill's own prioritized-recommendations section (don't invent a new
     prioritization scheme — reuse the one the delegated skill already
     produced).
5. **One report per sub-skill, never one merged file for several.** For
   `dd`, which composes five atomic audits internally (`deadcode`, `arch`,
   `security`, `perf`, `deps`), write five separate component reports —
   `docs/audit/deadcode-<date>.md`, `docs/audit/arch-<date>.md`,
   `docs/audit/security-<date>.md`, `docs/audit/perf-<date>.md`,
   `docs/audit/deps-<date>.md` — each containing the `Progetto:
   {nome_progetto}` header, its own analysis, and its own
   "Implementazioni da fare", exactly as if that component had been run
   standalone. Then write one additional
   `docs/audit/dd-<date>.md` containing only the composite layer that
   doesn't belong to any single component — deal context, executive
   summary, cross-cutting prioritized recommendations, readiness matrix —
   and linking to the five component reports rather than repeating their
   content.
6. Tell the user, in one line, where each report was written (all six
   paths for `dd`). Do not treat writing the file as a substitute for
   showing the analysis in the conversation — do both.

### Standing context across runs

Every delegated skill now loads `AUDIT-CONTEXT.md` (repo root, or
`.claude/audit-context.md` / `docs/audit-context.md`) before scoping, per
[reference/context-protocol.md](reference/context-protocol.md). This is
what stops repeat audits from re-flagging decisions already accepted (e.g.
a private repo intentionally used as the only backup, with `.env`
committed on purpose). The router doesn't need to do anything extra here —
each delegated skill handles the read/write itself — but if the user asks
*where* this history lives, point them at that one file at the target
repo's root.

The same file also carries an **Audit plan**: a checklist of the six
atomic audits (`deadcode`, `arch`, `perf`, `security`, `pentest`, `deps`)
created automatically the first time this file is initialized for a
repo, with a start date. Each atomic audit checks off its own row and
appends a dated **Run log** entry (including anything it deliberately
skipped) when it completes, after a quick confirmation with the user —
see context-protocol.md for the exact mechanics. This is what lets the
family answer "what audits has this repo had, when, and what did we skip"
without re-deriving it from memory.

`perf`, `pentest`, and `deps` are tracked in the plan like the other
three, and `dd` now composes five of the six internally — `deadcode`,
`arch`, `security`, `perf`, and `deps` — running `perf` and `deps` as
their own full dedicated passes rather than relying only on
`tech-due-diligence`'s narrower internal Fase 5/Fase 6 (see
`reference/dd.md` » "Additional composed audits"). Only `pentest` stays
excluded: its dynamic phase needs a live-target authorization gate a
due-diligence run shouldn't silently trigger. Run `pentest` separately
when live exploit verification is wanted alongside a `dd` engagement.

### Ambiguity handling

Each delegated skill now asks the user directly (via `AskUserQuestion`)
when it hits genuine ambiguity it can't resolve from the repo alone —
unclear scope in a monorepo, missing/stale conventions, unclear trust
boundaries, unspecified due-diligence purpose/audience. Don't pre-empt
that by guessing here in the router; let the delegated skill's own
judgment call decide whether to ask.

### Context detection (shared rule)

Several sub-commands have two variants: one tuned to a specific repo
(`personal-finance-app`, with its own `CLAUDE.md` conventions), one
stack-agnostic. Before delegating, resolve the target's repo root
(`git rev-parse --show-toplevel` from the target, or cwd if no target was
given) and check whether the path contains `personal-finance-app/` or the
root's `package.json`/`pyproject.toml` identifies that project. Each
reference file states which variant to use in each case — follow it
verbatim, don't skip the detection step even if the answer seems obvious.

## Adding a new audit type

If another audit type is needed later: prefer creating a dedicated skill
first (or confirm one already exists), then add one row to the table
above and one short `reference/<name>.md` that says which skill file to
load and under what conditions — do not inline that skill's logic into
this router. If no dedicated skill exists yet and creating one isn't
warranted, a self-contained `reference/<name>.md` carrying the
methodology directly is acceptable (this is what `perf` does) — but keep
it narrowly scoped and evidence-based, the same standard delegated skills
are held to. Either way, remember to also wire the new command into the
"Report output" section above (it isn't a special case — every atomic/
composite command writes a report) and add it to `context-protocol.md`'s
Audit plan.
