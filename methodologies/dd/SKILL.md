---
name: tech-due-diligence-local
description: Bundled local technical due diligence methodology used by the audit router.
disable-model-invocation: false
---

# Technical Due Diligence

Composite methodology for evidence-based technical due diligence. It
combines:

- `methodologies/arch/SKILL.md`
- `methodologies/security/generic.md` or a profile-selected security methodology
- investment/deal framing
- a full-repo security subagent

## Non-negotiable rules

1. No speculation: every claim is `Observed`, `Inferred`, or `Not verifiable from repo`.
2. Every Critical/Major finding cites `file:line`.
3. Review the entire repo, not a random sample.
4. Security findings fail closed when something important is not verifiable.
5. Execute commands; do not limit the review to static reading.
6. Declare coverage and persistence mode explicitly in the final output.

## Phase -1 — standing audit context

Check `AUDIT-CONTEXT.md` at the repo root (or `.claude/audit-context.md`
/ `docs/audit-context.md`). If present, read it and follow
`audit/reference/context-protocol.md`. Match against all sections,
including Security, Dead code, Architecture, and Due diligence.

Resolve coverage and persistence first:

- follow `audit/reference/bootstrap-lite.md`

Load conditionally: follow `audit/reference/persistence-protocol.md` only
for `--persist`/writes beyond the report; follow
`audit/reference/finding-contract.md` + `audit/reference/formal-delta.md`
+ `audit/reference/output-contract.md` only when the run is formal.

## Phase 0 — deal context

Use `AskUserQuestion` if these are unclear and materially change the
report:

- purpose: investment / acquisition / pilot / internal / vendor
- scope in a monorepo
- audience: technical, non-technical, or both

If the user explicitly asked for a generic DD without questions, proceed
with a general technical assessment.

## Workflow (sequential, one phase in context at a time)

Read and follow:

- `references/investigation-protocol.md`
- `references/output-template.md`
- `references/fintech-rules-checklist.md` when the target repo has
  matching fintech-style conventions or a dedicated profile says to use it

Mandatory structure — the 10 phases in `investigation-protocol.md`:

1. Reconnaissance
2. Architecture & domain
3. Data & database
4. Security + one full-repo subagent
5. Dependencies & runtime currency + CVE scan
6. Performance & scalability
7. Tests & quality
8. Build, deploy, ops
9. Team & process inference
10. Final report using the bundled output template

Run phases 1-9 one at a time rather than holding all of them in context
together:

1. Execute the phase's checklist against the repo.
2. Normalize that phase's findings (`scripts/normalize_findings.py`).
3. If the run is `--persist` or default (not `--read-only`), write the
   normalized result to a scratch file at
   `.audit/tmp/dd-<phase-number>-<phase-name>.json` and drop the phase's
   raw exploration output from working context — the next phase only
   needs the normalized findings, not how you got there. In `--read-only`
   runs, keep the same normalized result in working memory instead of
   writing it (no writes at all in that mode).
4. Move to the next phase.

After phase 9: read back the phase scratch files (or in-memory
equivalents), deduplicate by fingerprint per
`audit/reference/finding-contract.md`, and aggregate into the phase-10
final report using the bundled output template. Delete
`.audit/tmp/dd-*.json` scratch files once the final report is produced —
they are working state, not an audit deliverable.

The final report must still satisfy `audit/reference/output-contract.md`
in `formal` mode (due diligence is always `formal`, see that file); the
DD template is the due-diligence-specific addendum on top of the shared
contract, not a replacement for it.

## Notes

- `dd` is composite: do not also separately run `arch`, `security`, and
  `deadcode` for the same target unless the user explicitly wants the
  extra pass.
- Report-file writing follows the standard default in
  `audit/reference/persistence-protocol.md`: write the report unless
  `--read-only` applies.
