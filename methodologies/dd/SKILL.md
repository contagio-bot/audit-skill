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

- follow `audit/reference/capability-protocol.md`
- follow `audit/reference/inventory-protocol.md`
- follow `audit/reference/coverage-protocol.md`
- follow `audit/reference/persistence-protocol.md`
- follow `audit/reference/evidence-protocol.md`
- follow `audit/reference/finding-schema.md`
- follow `audit/reference/output-contract.md`

## Phase 0 — deal context

Use `AskUserQuestion` if these are unclear and materially change the
report:

- purpose: investment / acquisition / pilot / internal / vendor
- scope in a monorepo
- audience: technical, non-technical, or both

If the user explicitly asked for a generic DD without questions, proceed
with a general technical assessment.

## Workflow

Read and follow:

- `references/investigation-protocol.md`
- `references/output-template.md`
- `references/fintech-rules-checklist.md` when the target repo has
  matching fintech-style conventions or a dedicated profile says to use it

Mandatory structure:

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

The final report must still satisfy `audit/reference/output-contract.md`;
the DD template is the due-diligence-specific addendum on top of the
shared contract, not a replacement for it.

## Notes

- `dd` is composite: do not also separately run `arch`, `security`, and
  `deadcode` for the same target unless the user explicitly wants the
  extra pass.
- Save a report file only if the user asks for one or the context is a
  formal DD deliverable.
