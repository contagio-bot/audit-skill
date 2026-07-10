# Audit coverage protocol

Every audit run must declare its coverage level up front and repeat it in
the final output. This avoids presenting a partial review as if it were
exhaustive.

## Coverage classes

### `full`

Use `full` only when the intent is to inspect the entire in-scope target:

- whole repo, or
- the full explicitly requested path/service/package

`full` does not mean "every generated file and dependency"; normal
exclusions still apply (`node_modules`, vendored code, build outputs,
large generated artifacts) unless they expose a concrete risk.

### `partial`

Use `partial` when scope is deliberately bounded:

- one service in a monorepo
- one path the user named explicitly
- one category inspected only in a subset of the codebase

State the exact boundary. Example: "partial coverage: backend/api and
backend/domain only; frontend and infra excluded."

### `batched`

Use `batched` when the review can still be exhaustive for the requested
scope, but only area-by-area or service-by-service:

- large monorepos
- several independently deployable units
- one audit split across clear subsystem batches

### `risk-based`

Use `risk-based` when the run intentionally prioritizes the highest-risk
surfaces first:

- auth/authz
- payments
- public entry points
- secret handling
- deploy/infrastructure
- sensitive data paths

State which areas were prioritized and which were deprioritized.

### `sample`

Use `sample` when the run is necessarily non-exhaustive:

- repository too large for an exhaustive pass in the available budget
- interrupted run
- tooling/network restrictions materially reduce reachable evidence
- the methodology explicitly chooses representative spots instead of full coverage

State the sampling rationale, what was sampled, and the main blind spots.

## Selection rules

1. Prefer `full` when the repo/path is reasonably inspectable.
2. Use `partial` instead of `sample` when the boundary is clear and
   deliberate.
3. Use `batched` when scope is broad but partitionable.
4. Use `risk-based` when constraints force prioritization by risk rather
   than equal coverage.
5. Use `sample` when the boundary is fuzzy or constraints prevent
   exhausting the intended scope.
6. If a run starts as `full` but cannot complete, downgrade it in the
   final output and explain why.

## Mandatory output

Every audit report or chat result must include:

- `Coverage`: `full` / `partial` / `batched` / `risk-based` / `sample`
- `Scope inspected`: concrete paths or components
- `Excluded areas`: concrete paths or reasons
- `Confidence impact`: one short sentence if coverage was not `full`

## Examples

- Vague request on a small single-app repo: usually `full`
- Monorepo where the user asked for only `payments/`: `partial`
- Huge monorepo with no scope clarification and a tight budget: ask first;
  if forced to proceed, `sample`
