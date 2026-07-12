# Audit context protocol

Shared by every skill in the `audit` family. One file, created only with
`--persist` (or when the command is itself `context`) and read at the
start of every run if present. It tracks two independent things:

- **Accepted risks / intentional decisions** — updated at the end when
  the user accepts a finding as intentional, so it doesn't get re-flagged
  as new on the next audit.
- **Audit plan** — which of the three atomic audits (`deadcode`, `arch`,
  `security`) have been run, when, and what was deliberately skipped each
  time, so the family as a whole has a standing to-do list that gets
  checked off and re-annotated as the codebase evolves.

## File location and name

`AUDIT-CONTEXT.md` at the target repo's root. Case-insensitive; if it's
not at the root, check `.claude/audit-context.md` and `docs/audit-context.md`
before concluding it doesn't exist. Never create it in more than one of
these locations for the same repo.

## Read step (start of every audit, mandatory if the file exists)

1. Resolve persistence mode first using
   `reference/persistence-protocol.md`.
2. Look for the file.
3. If absent and the run is `--read-only` or the (report-only) default,
   proceed without creating it. Mention once that no standing context
   file exists and no file was created because the run isn't
   `--persist`ing beyond the report.
4. If absent and the run is `--persist`, ask whether to initialize it
   now. Do not auto-create it silently. If the user declines, proceed
   without it.
5. If present, read it in full before running any tooling. If it predates
   this protocol version and has no **Audit plan** section, add one (same
   population rule as above) only with `--persist` and only after telling
   the user what will be added. Otherwise, note the missing section
   instead of patching it.
6. While producing findings, before reporting one, check whether it
   matches an entry under **Accepted risks / intentional decisions**.
   Match on topic/substance, not exact wording (e.g. an entry about
   "GitHub used as private backup, .env committed on purpose" should
   suppress a fresh "secrets committed to git history" finding even if
   phrased differently).
7. A match means: do not report it as a new finding needing action. Instead
   list it once, briefly, under a **"Previously accepted (not re-flagged)"**
   note near the end of the report, citing the entry's date — so the user
   can see it was considered, not missed.
8. Do not suppress a finding just because something *nearby* is mentioned
   in the file — match the specific risk, not the general area. "We accept
   that this app has no rate limiting on `/auth/login`" does not cover a
   newly-introduced unauthenticated `/admin/debug` endpoint.
9. If an entry looks stale relative to what you're observing now, say so
   explicitly. A stale entry is one whose scope no longer matches reality,
   whose review date has passed, or whose invalidation condition has been
   met.
10. When an accepted risk no longer applies, report it as
   **"Previously accepted but no longer applicable"** rather than
   suppressing the finding.

## Write step (end of the audit, only on explicit user confirmation)

Never write to this file silently. Only append an entry when:

- you reported a finding, and
- the user responded that it's intentional / accepted / already known /
  not worth fixing (in this conversation or a linked one), and
- you've asked "should I record this in `AUDIT-CONTEXT.md` so future audits
  don't flag it again?" and they said yes.

If the file doesn't exist yet, create it first only with `--persist` and
only after the user approves initialization. Otherwise append under the
matching section (create the section if missing).

Accepted risks must be structured, factual, and reviewable:

```
- Risk: <one-line description>
  Scope: <repo-wide | path | component | endpoint | dependency>
  Accepted: <YYYY-MM-DD>
  Review by: <YYYY-MM-DD | none>
  Invalidates when: <condition that should reopen this risk>
  Reason: <why, in the user's words or close to it>
```

Do not accept vague entries like "security risk accepted for now" with no
scope or invalidation condition.

## Audit plan write step (end of every run of `deadcode`/`arch`/`security`, confirmation required)

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
   - <name> run <YYYY-MM-DD>. Coverage: <full|partial|sample>. Skipped: <steps skipped and why, or "none">.
   ```
3. Do not touch the other two audits' rows or entries — each is updated
   only by its own run.
4. `dd` runs all three atomic audits internally: apply this same
   confirm-then-write step for each of the three as they complete inside
   the `dd` run, rather than adding a separate `dd` row (there isn't one —
   see template).

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
<!-- `dd` has no row of its own — it's composite and updates the three rows below as it runs each one internally. -->

- [ ] deadcode — dead code / duplication / refactoring
- [ ] arch — architecture, bugs, performance, readability
- [ ] security — cybersecurity & infrastructure

### Run log
<!-- Each atomic audit appends its own line here when it completes, after confirming with the user (see context-protocol.md, "Audit plan write step"). -->
<!-- e.g. "- security run 2026-04-01. Skipped: dependency-CVE pass (no network access)." -->

## Accepted risks / intentional decisions

### Security
<!--
- Risk: No rate limiting on /internal/*
  Scope: /internal/*
  Accepted: 2026-03-01
  Review by: 2026-06-01
  Invalidates when: endpoint becomes internet-facing or auth model changes
  Reason: internal-network-only, not internet-facing
-->

### Dead code / duplication
<!--
- Risk: frontend/src/legacy/** kept unused on purpose as reference for migration
  Scope: frontend/src/legacy/**
  Accepted: 2026-02-10
  Review by: none
  Invalidates when: migration completes or references disappear
  Reason: reference implementation still needed
-->

### Architecture
<!--
- Risk: Anemic domain model in billing accepted as a deliberate trade-off
  Scope: billing/
  Accepted: 2026-01-20
  Review by: 2026-09-01
  Invalidates when: billing rewrite starts or team adds a second billing flow
  Reason: pre-PMF, will revisit later
-->

### Due diligence
<!--
- Risk: Bus factor of 1 acknowledged for this pilot phase
  Scope: repo-wide
  Accepted: 2026-04-01
  Review by: 2026-07-01
  Invalidates when: pilot exits founder-only operation
  Reason: temporary founder-led phase
-->

## Open follow-ups (known, not yet resolved)
<!-- Findings the user acknowledged but wants to fix later, not accept permanently -->
```

## Notes

- This file is meant to be read by humans too — don't compress it into
  something only a model can parse. Plain bullets, plain dates.
- Don't let it become a dumping ground: only entries where a human
  explicitly confirmed "yes, intentional, don't re-flag" belong here, not
  every finding from every run.
- If a structured entry is missing `Scope`, `Review by`, or
  `Invalidates when`, flag it as incomplete rather than treating it as a
  fully valid acceptance.
- If the user asks you to remove or correct an entry, do it directly with
  `Edit` — don't ask for elaborate confirmation for a deletion they just
  requested.
- The **Audit plan** checklist is a status snapshot, not a one-time gate:
  an audit already marked `[x]` should still run again on request (e.g.
  new code was written since). Re-running just appends a new **Run log**
  line with a fresh date and confirms the checkbox stays checked — it
  doesn't block re-runs or reset history.
