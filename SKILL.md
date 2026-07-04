---
name: audit
description: "Router for repository audits. Use when the user asks to audit, review, or assess a codebase for dead code/duplication/refactoring, architecture/bugs/performance/readability, cybersecurity/infrastructure risk, or a full technical due diligence. Delegates to dedicated, already-tuned skills instead of re-implementing their logic; picks the project-tuned version when the target repo is personal-finance-app, and the stack-agnostic version otherwise."
argument-hint: "[deadcode|arch|security|dd|context|recheck] [target]"
user-invocable: true
license: MIT
---

# Audit router

Single entry point for the four audit types this toolkit supports, plus
two commands for managing the standing context file directly. This skill
does not contain audit logic itself — every sub-command loads and follows
an existing dedicated skill/reference file in full. Its only job is
routing and, where relevant, picking the project-tuned variant over the
generic one.

**Never re-derive the underlying methodology from memory.** Always `Read`
the delegated `SKILL.md` (and any `references/*.md` it points to) before
running commands — that file is the source of truth, this router is not.

## Commands

| Command | Category | Description | Reference |
|---|---|---|---|
| `deadcode [target]` | Quality | Dead code, duplication, refactoring/simplification candidates | [reference/deadcode.md](reference/deadcode.md) |
| `arch [target]` | Quality | Hidden bugs, performance issues, readability, architectural smells (10-category review) | [reference/arch.md](reference/arch.md) |
| `security [target]` | Risk | Cybersecurity weaknesses and infrastructure/operability criticalities | [reference/security.md](reference/security.md) |
| `dd [target]` | Risk | Full technical due diligence (composes the three above + deal framing) | [reference/dd.md](reference/dd.md) |
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
   spirit as impeccable's free-text case. Don't guess which of the four
   this means — ask (e.g. "review this for bugs" → `arch`, "is this
   secure?" → `security`) since the four audits are not interchangeable and
   picking wrong wastes the whole run.

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

If a fifth audit type is needed later: create the dedicated skill first
(or confirm one already exists), then add one row to the table above and
one short `reference/<name>.md` that says which skill file to load and
under what conditions. Do not inline the new skill's logic into this
router.
