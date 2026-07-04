# Audit context protocol

Shared by every skill in the `audit` family (`deadcode-refactor-audit`,
`code-health-audit`, `codebase-auditor`, `cybersecurity-infra-auditor`,
`pentest-auditor`, `deps-auditor`, `tech-due-diligence`). One file,
created on first use and read at the start of every run. It tracks two
independent things:

- **Accepted risks / intentional decisions** — updated at the end when
  the user accepts a finding as intentional, so it doesn't get re-flagged
  as new on the next audit.
- **Audit plan** — which of the five atomic audits (`deadcode`, `arch`,
  `security`, `pentest`, `deps`) have been run, when, and what was
  deliberately skipped each time, so the family as a whole has a standing
  to-do list that gets checked off and re-annotated as the codebase
  evolves.

## File location and name

`AUDIT-CONTEXT.md` at the target repo's root. Case-insensitive; if it's
not at the root, check `.claude/audit-context.md` and `docs/audit-context.md`
before concluding it doesn't exist. Never create it in more than one of
these locations for the same repo.

## Read step (start of every audit, mandatory)

1. Look for the file. If absent, create it immediately with the template
   below — this includes the **Audit plan** section, populated with the
   five atomic audits (`deadcode`, `arch`, `security`, `pentest`, `deps`)
   all marked pending and `Started: <today's date>`. This initial creation is
   bookkeeping, not a judgment call, so it doesn't need user confirmation
   (unlike appending to Accepted risks — see Write step). Tell the user in
   one line that you created it, then proceed with the audit.
2. If present, read it in full before running any tooling. If it predates
   this protocol version and has no **Audit plan** section, add one (same
   population rule as above) before proceeding.
3. While producing findings, before reporting one, check whether it
   matches an entry under **Accepted risks / intentional decisions**.
   Match on topic/substance, not exact wording (e.g. an entry about
   "GitHub used as private backup, .env committed on purpose" should
   suppress a fresh "secrets committed to git history" finding even if
   phrased differently).
4. A match means: do not report it as a new finding needing action. Instead
   list it once, briefly, under a **"Previously accepted (not re-flagged)"**
   note near the end of the report, citing the entry's date — so the user
   can see it was considered, not missed.
5. Do not suppress a finding just because something *nearby* is mentioned
   in the file — match the specific risk, not the general area. "We accept
   that this app has no rate limiting on `/auth/login`" does not cover a
   newly-introduced unauthenticated `/admin/debug` endpoint.
6. If an entry looks stale relative to what you're observing now (e.g. the
   accepted risk was scoped to a component that has since been rewritten,
   or a dependency that's been replaced), say so explicitly instead of
   either blindly suppressing or silently ignoring the stale entry.

## Write step (end of the audit, only on explicit user confirmation)

Never write to this file silently. Only append an entry when:

- you reported a finding, and
- the user responded that it's intentional / accepted / already known /
  not worth fixing (in this conversation or a linked one), and
- you've asked "should I record this in `AUDIT-CONTEXT.md` so future audits
  don't flag it again?" and they said yes.

If the file doesn't exist yet, create it with the template below. Otherwise
append under the matching section (create the section if missing).

Keep entries factual and short — one bullet, not a paragraph:

```
- <one-line description of the finding/decision> — Accepted <YYYY-MM-DD>. Reason: <why, in the user's words or close to it>.
```

## Audit plan write step (end of every run of `deadcode`/`arch`/`security`/`pentest`/`deps`, confirmation required)

Unlike the plan's initial creation (auto, see Read step), updating a row
after a run is not silent bookkeeping — it also records skip decisions,
which are judgment calls worth a human's eyes. Before writing, summarize
what you're about to log in one or two lines and ask for confirmation
(e.g. "I'll mark `security` as done today and note that I skipped the
dependency-CVE pass since there's no network access here — ok?").

Once confirmed:

1. Flip that audit's checklist box from `[ ]` to `[x]` in **Audit plan**.
2. Append one line to that audit's entry under **Run log**, in this
   format:
   ```
   - <name> run <YYYY-MM-DD>. Skipped: <steps skipped and why, or "none">.
   ```
3. Do not touch the other audits' rows or entries — each is updated only
   by its own run.
4. `dd` runs three of the five atomic audits internally (`deadcode`,
   `arch`, `security` — never `pentest`, since its dynamic phase needs a
   live-target authorization gate a due-diligence run shouldn't trigger on
   its own, and never the full `deps` sweep, since it already runs its own
   narrower internal dependency+CVE pass): apply this same
   confirm-then-write step for each of those three as they complete inside
   the `dd` run, rather than adding a separate `dd` row (there isn't one —
   see template).
5. For `pentest` specifically, note in the **Run log** line whether phase 2
   (dynamic verification) actually ran or was skipped for lack of an
   authorized target — e.g. `- pentest run 2026-07-04. Skipped: phase 2
   (no authorized live target).`

## Template (used when creating the file for the first time)

```markdown
# Audit Context

> Maintained by the `audit` skill family. Human-editable — correct or
> remove entries directly if they stop applying. Records standing facts
> and accepted risks so repeated audits don't re-flag decisions already
> made.

## Standing facts
<!-- Context that changes how findings should be interpreted, not a finding itself -->
<!-- e.g. "This repo is a private GitHub repo used as the only code backup; .env is intentionally committed." -->

## Audit plan
<!-- Created automatically on first initialization of this file. Started: <YYYY-MM-DD> -->
<!-- `dd` has no row of its own — it's composite and updates the deadcode/arch/security rows below as it runs each one internally. It never runs `pentest` or the full `deps` sweep. -->

- [ ] deadcode — dead code / duplication / refactoring
- [ ] arch — architecture, bugs, performance, readability
- [ ] security — cybersecurity & infrastructure
- [ ] pentest — attack-surface mapping + gated dynamic exploit verification
- [ ] deps — EOL/support-status sweep + known-CVE scan across direct dependencies

### Run log
<!-- Each atomic audit appends its own line here when it completes, after confirming with the user (see context-protocol.md, "Audit plan write step"). -->
<!-- e.g. "- security run 2026-04-01. Skipped: dependency-CVE pass (no network access)." -->
<!-- e.g. "- pentest run 2026-07-04. Skipped: phase 2 (no authorized live target)." -->
<!-- e.g. "- deps run 2026-07-04. Skipped: none." -->

## Accepted risks / intentional decisions

### Security
<!-- e.g. "- No rate limiting on /internal/* — accepted 2026-03-01. Reason: internal-network-only, not internet-facing." -->

### Dead code / duplication
<!-- e.g. "- frontend/src/legacy/** kept unused on purpose as reference for migration — accepted 2026-02-10." -->

### Architecture
<!-- e.g. "- Anemic domain model in billing/ accepted as a deliberate trade-off for now — accepted 2026-01-20. Reason: pre-PMF, will revisit post-Series A." -->

### Penetration test
<!-- e.g. "- IDOR on /internal/reports/:id accepted — exposed only on an internal-only network, not internet-facing. Accepted 2026-07-04." -->

### Dependencies
<!-- e.g. "- Node 18 kept despite approaching EOL — accepted 2026-07-04. Reason: upgrade blocked on a transitive dep, planned for Q3." -->

### Due diligence
<!-- e.g. "- Bus factor of 1 acknowledged and accepted for this pilot phase — accepted 2026-04-01." -->

## Open follow-ups (known, not yet resolved)
<!-- Findings the user acknowledged but wants to fix later, not accept permanently -->
```

## Notes

- This file is meant to be read by humans too — don't compress it into
  something only a model can parse. Plain bullets, plain dates.
- Don't let it become a dumping ground: only entries where a human
  explicitly confirmed "yes, intentional, don't re-flag" belong here, not
  every finding from every run.
- If the user asks you to remove or correct an entry, do it directly with
  `Edit` — don't ask for elaborate confirmation for a deletion they just
  requested.
- The **Audit plan** checklist is a status snapshot, not a one-time gate:
  an audit already marked `[x]` should still run again on request (e.g.
  new code was written since). Re-running just appends a new **Run log**
  line with a fresh date and confirms the checkbox stays checked — it
  doesn't block re-runs or reset history.
