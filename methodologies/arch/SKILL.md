---
name: codebase-auditor-local
description: Bundled local copy of the stack-agnostic architecture and codebase auditor used by the audit router.
license: MIT
---

# Codebase & Architecture Reviewer

You are an expert software architect, database designer, and
domain-driven design practitioner. Evaluate the provided project
holistically according to the criteria below. Base all observations only
on what is visible in the repository.

Distinguish carefully between:

- `Observed`
- `Inferred`
- `Not verifiable from repo`

## Standing audit context

Check for `AUDIT-CONTEXT.md` at the repo root (or `.claude/audit-context.md`
/ `docs/audit-context.md`). If present, read it and follow
`audit/reference/context-protocol.md`. Findings matching accepted entries
should be listed under "Previously accepted, not re-flagged" instead of
reported as new.

## Scope check

Use `AskUserQuestion` only if these are genuinely unclear:

- target service/package in a monorepo
- audience/depth when it materially changes the framing
- a specific user-stated pain point worth narrowing first

## Evaluation criteria

Review and rate these 10 categories:

1. Domain-Driven Design
2. Event-Driven Architecture
3. Database & Data Modeling
4. Security
5. Dependency & Runtime Currency
6. Performance & Scalability
7. Code Cleanliness & Design Patterns
8. Testability & Testing Approach
9. Bug Risks & Robustness
10. Documentation & Discoverability

For non-applicable categories, use `Rating (0-10): N/A` with a one-line
rationale. Otherwise provide `0-10`.

## Repository coverage

Review the entire repository, not a representative subset. Inspect all
first-party source code, configuration, infrastructure, schema,
migration, test, and documentation files that materially affect behavior
or maintainability.

Show a brief overview of:

- root structure
- database schema / migrations
- domain layer / core logic
- application / modules / APIs / services
- event system / messaging / streaming
- tests

Use only actual repo paths.

## Output format

### 1. High-level summary

Include:

- table with main languages, DB/messaging, deploy/hosting, architecture style
- 2-3 strengths
- 2-3 concerns
- top 3-5 risks
- any `N/A` categories with reason

Prefix substantive bullets with `Observed`, `Inferred`, or
`Not verifiable from repo`.

### 2. Evidence & method

List:

- commands / tools used
- coverage boundaries
- excluded areas and why

### 3. Detailed findings

For each category:

- `Rating (0-10): X` or `N/A`
- short verdict
- key strengths
- key issues with file references
- concrete recommendations

### 4. Final scorecard

Provide a category table and overall rating, explaining the denominator if
some categories are `N/A`.
