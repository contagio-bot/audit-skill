---
name: milestones-local
description: Bundled milestone/roadmap verification methodology — audits the actual implementation against a milestone or roadmap document without trusting any of its claims.
license: MIT
---

# Milestone verification audit

Development-progress audit. A milestone/roadmap document (e.g.
`milestone.md`, `ROADMAP.md`, `CHANGELOG.md`-style planning docs) is used
only as an **index** of what should exist — never as evidence that it
does. Every status, checkbox, or claim in it ("done", "implemented",
"fixed", "tested") must be independently verified against the actual
code, or refuted.

Resolve shared protocols first:

- `audit/reference/bootstrap-lite.md`

Load conditionally: `audit/reference/persistence-protocol.md` only for
`--persist`/writes beyond the report; `audit/reference/finding-contract.md`
+ `audit/reference/formal-delta.md` + `audit/reference/output-contract.md`
only when the run is formal.

## Non-negotiable rules

1. **Distrust the document by default.** Its wording, checkmarks, and
   status labels are claims, not facts. Never repeat a claim in the
   report as true because the document says so — restate it as "doc
   claims X" and pair it with what was actually verified.
2. For every milestone in scope, read the full files its scope touches —
   not excerpts, not just the diff that introduced it.
3. Classify every doc claim as one of: `Confirmed`, `Partially confirmed`,
   `Contradicted`, `Not verifiable from repo` — each with `file:line`
   evidence for Critical/Major items.
4. Actively hunt beyond what the document claims to cover: bugs, silently
   swallowed errors, `TODO`/`FIXME`/`XXX`/`HACK` markers, stub/placeholder
   implementations, dead branches, missing error handling, untested
   critical paths, and points the doc itself leaves ambiguous or
   unresolved — even inside milestones the doc marks complete.
5. Do not sample. If the milestone range is large, process one milestone
   at a time and do not hold every milestone's raw exploration in context
   simultaneously (see Workflow step 3).
6. A milestone is only `Confirmed` complete when its code, tests, and
   integration all check out — a passing-looking doc entry with no
   corresponding code, or code that doesn't do what's claimed, is
   `Contradicted`, not `Partially confirmed`.

## Phase 0 — scope

Use `AskUserQuestion` only if genuinely unclear:

- which file is the milestone/roadmap document, if more than one
  candidate exists
- the milestone range, if the user didn't give one explicitly (default:
  every milestone in the document)

## Workflow

1. Read the milestone document once, fully, for structure only — the
   list of milestones and what each claims. This pass builds the index;
   it verifies nothing.
2. For each milestone `N` in range, sequentially:
   a. Extract milestone `N`'s claimed scope and status from the doc.
   b. Identify every source file, config, schema, and test the scope
      implies — including files the doc doesn't mention but that
      obviously belong to the same feature area.
   c. Read that code in full. Verify existence, correctness, completeness,
      and whether it matches what's claimed.
   d. Independently of the doc's claims, search the same area for bugs,
      dev debt, and points left in doubt.
   e. Record findings with the classification from rule 3 and evidence.
   f. If the run is persist/default, write milestone `N`'s normalized
      findings to `.audit/tmp/milestones-<N>.json`
      (`scripts/normalize_findings.py`) and drop that milestone's raw
      exploration output from working context before starting `N+1`. In
      `--read-only` runs, keep it in memory instead (no writes).
3. After the last milestone in range: read back the per-milestone scratch
   files (or in-memory equivalents), deduplicate by fingerprint per
   `audit/reference/finding-contract.md`, and aggregate into the final
   report. Delete `.audit/tmp/milestones-*.json` once the report is
   produced — they are working state, not a deliverable.

## Output

Standard mode: `bootstrap-lite.md`'s 4-section format. Formal mode:
`audit/reference/output-contract.md`.

Area-specific addendum — one block per milestone, in order:

- **Milestone N — `<title from doc>`**
  - Doc-claimed status (quote it) vs verified status: `Confirmed` /
    `Partially confirmed` / `Contradicted` / `Not verifiable from repo`
  - Evidence: `file:line` for each claim checked
  - Bugs / dev debt / unresolved points found in that milestone's code,
    regardless of what the doc claims
- Closing summary: how much of the document's claimed overall progress
  holds up against the code, and which milestones most disagree with
  their doc entry
