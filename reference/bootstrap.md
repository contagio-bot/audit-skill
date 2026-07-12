# Audit bootstrap

Shared mechanics for every substantive run: capability detection,
inventory, coverage selection, and run order. Persistence has its own
file — [persistence-protocol.md](persistence-protocol.md) — because it
governs writes, not analysis, and is read separately by commands that
only care about writes (e.g. `context`, `baseline`).

## Sequence

1. resolve target and repository root
2. detect capabilities (below)
3. inventory the repository (below)
4. resolve coverage (below)
5. resolve persistence mode — see [persistence-protocol.md](persistence-protocol.md)
6. load profile, context, and baseline only when the command needs them
7. execute the methodology
8. record evidence; normalize, deduplicate, and baseline-compare findings
9. compute scoring/confidence when scoring applies
10. validate the output; export when requested
11. write the report by default; write context/baseline only with
    `--persist` (or when the command's own job is to write them)
12. disclose limits, writes, and skipped steps

Rules: don't skip straight to the methodology; prefer the bundled
`scripts/` utilities over redoing deterministic work by hand; downgrade
coverage if the run can't finish the planned sequence; don't mutate
context/baseline files unless `--persist` applies; don't write the report
itself when `--read-only` applies.

## 1. Capability detection

Detect before choosing tools, confidence level, or persistence behavior:
git availability, network availability, write access to the target repo,
runtimes/package managers, Docker/container tools, test runners,
static-analysis tools already installed, and any visible time/context
limits.

Prefer `scripts/detect_capabilities.py <target>`.

```text
Detected: TypeScript / pnpm, PostgreSQL / Prisma
Available: git, node, pnpm
Unavailable: network, docker
Skipped: live advisory refresh, container runtime verification
```

Rules: never install tools automatically; missing tools reduce
coverage/confidence, they never justify guessing; the manifest must
appear in the final output for non-trivial audits.

## 2. Inventory

Build a measurable inventory before deep analysis: first-party source,
tests, configuration, infrastructure, migrations/schema, docs, and
generated/vendor/cache/build output (excluded by default unless it
exposes a concrete risk).

Prefer `scripts/inventory.py <target>`.

State: repository root, requested scope, resolved scope, top-level
areas, relevant file groups found, excluded paths and why. Don't claim
whole-repo review without a concrete inventory — the inventory is what
coverage selection is based on.

## 3. Coverage

Declare coverage up front and repeat it in the final output, so a
partial review is never presented as exhaustive.

- **`full`** — the entire in-scope target (whole repo, or the full
  explicitly requested path/service/package). Normal exclusions
  (`node_modules`, vendored code, build output) still apply.
- **`partial`** — scope deliberately bounded (one service, one named
  path, one category checked only in a subset). State the exact
  boundary, e.g. "partial: backend/api and backend/domain only;
  frontend and infra excluded."
- **`batched`** — exhaustive for the requested scope, but area-by-area
  or service-by-service (large monorepos, several deployable units).
- **`risk-based`** — intentionally prioritizes the highest-risk surfaces
  first (auth/authz, payments, public entry points, secrets,
  deploy/infra, sensitive data). State what was prioritized and
  deprioritized.
- **`sample`** — necessarily non-exhaustive (repo too large for the
  budget, interrupted run, tooling/network restrictions). State the
  sampling rationale, what was sampled, and the main blind spots.

Selection: prefer `full` when reasonably inspectable; prefer `partial`
over `sample` when the boundary is clear and deliberate; use `batched`
when scope is broad but partitionable; use `risk-based` when constraints
force prioritization over equal coverage; use `sample` when the boundary
is fuzzy or constraints block exhausting the intended scope. If a run
starts `full` but can't complete, downgrade it in the final output and
say why.

Every result must state: `Coverage`, `Scope inspected` (concrete paths),
`Excluded areas` (concrete paths/reasons), and a one-line `Confidence
impact` when coverage isn't `full`.

Examples: vague request on a small single-app repo → usually `full`;
monorepo where the user asked only for `payments/` → `partial`; huge
monorepo with no scope clarification and a tight budget → ask first, and
`sample` only if forced to proceed.
