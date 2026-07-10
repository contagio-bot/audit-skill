---
name: audit
description: "Router for repository audits. Use when the user asks to audit, review, or assess a codebase for dead code/duplication/refactoring, architecture/bugs/performance/readability, cybersecurity/infrastructure risk, or a full technical due diligence. Delegates only to methodologies bundled inside this skill package, and can create repo-specific local profiles via --profile."
argument-hint: "[deadcode|arch|security|dd|context|recheck|--profile] [target]"
user-invocable: true
license: MIT
---

# Audit router

Single entry point for the four audit types this toolkit supports, plus
two commands for managing the standing context file directly and one
command for generating repo-specific audit profiles. This skill does not
contain audit logic itself — every sub-command loads and follows a
bundled methodology/reference file in full. Its job is routing and, where
relevant, selecting a local profile-specific methodology over the generic
one.

**Never re-derive the underlying methodology from memory.** Always `Read`
the delegated local file (and any `references/*.md` it points to) before
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
| `--profile [target]` | Profiles | Create or update a local repo-specific audit profile and any dedicated methodology files it needs | [reference/profile.md](reference/profile.md) |

`target` is a path or repo; defaults to the current working directory / repo if omitted.

### Routing rules

1. **No argument**: render the table above as the user-facing command menu,
   grouped by category. Ask what they'd like to do.
2. **First word is `--profile`**: load
   [reference/profile.md](reference/profile.md) and follow it exactly.
3. **First word matches a command**: load its reference file and follow its
   instructions exactly — including any context-detection step. Everything
   after the command name is the `target`.
4. **First word doesn't match any command**: general audit invocation, same
   spirit as impeccable's free-text case. Don't guess which of the four
   this means — ask (e.g. "review this for bugs" → `arch`, "is this
   secure?" → `security`) since the four audits are not interchangeable and
   picking wrong wastes the whole run.

### Bundled methodologies only

This package must be self-contained. Do not delegate to `~/.claude`,
`~/.agents`, or absolute paths on the author's machine. All delegated
methodologies live under:

- `methodologies/arch/`
- `methodologies/deadcode/`
- `methodologies/security/`
- `methodologies/dd/`
- `profiles/`

If a needed methodology file is missing from those directories, stop and
tell the user which bundled file is absent instead of falling back to an
external path.

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

The same file also carries an **Audit plan**: a checklist of the three
atomic audits (`deadcode`, `arch`, `security`) created automatically the
first time this file is initialized for a repo, with a start date. Each
atomic audit checks off its own row and appends a dated **Run log** entry
(including anything it deliberately skipped) when it completes, after a
quick confirmation with the user — see context-protocol.md for the exact
mechanics. This is what lets the family answer "what audits has this repo
had, when, and what did we skip" without re-deriving it from memory.

### Ambiguity handling

Each delegated skill now asks the user directly (via `AskUserQuestion`)
when it hits genuine ambiguity it can't resolve from the repo alone —
unclear scope in a monorepo, missing/stale conventions, unclear trust
boundaries, unspecified due-diligence purpose/audience. Don't pre-empt
that by guessing here in the router; let the delegated skill's own
judgment call decide whether to ask.

### Context detection (shared rule)

Before delegating, resolve the target's repo root (`git rev-parse
--show-toplevel` from the target, or cwd if no target was given) and look
for a matching file under `profiles/*.md`. A profile can match by repo
name, root path fragment, marker files, package name, or explicit
convention text. If a profile matches and it points to a dedicated local
methodology file, use that methodology. Otherwise use the generic bundled
methodology for that audit type.

If no profile matches and the user wants a dedicated repo-tuned variant,
use `audit --profile [target]` first to create one.

## Adding a new audit type

If a fifth audit type is needed later: create the dedicated skill first
(or confirm one already exists), then add one row to the table above and
one short `reference/<name>.md` that says which skill file to load and
under what conditions. Keep it bundled inside this package. Do not inline
the new skill's logic into this router.
