---
name: deadcode-generic
description: Generic dead code, duplication, and structural refactoring audit bundled inside the audit router.
license: MIT
---

# Dead code, duplication & refactoring audit

Produces evidence-based findings only. No fixes are applied automatically.
Follow up with `knip`, `ruff --fix`, or `dry-refactoring` only after the
audit is reviewed.

## Step -1 — load standing audit context

Before anything else: check for `AUDIT-CONTEXT.md` at the repo root (or
`.claude/audit-context.md` / `docs/audit-context.md`). If present, read it
and follow `audit/reference/context-protocol.md`. Findings that match an
accepted entry should be listed under "Previously accepted, not
re-flagged" instead of reported as new.

Resolve coverage and persistence first:

- follow `audit/reference/coverage-protocol.md`
- follow `audit/reference/persistence-protocol.md`

## Step 0 — detect stack

Check for `package.json` (frontend/JS-TS) and `pyproject.toml` /
`requirements.txt` (backend/Python) at the repo root or in subdirectories.
Only run the tooling that applies to what's present. If the project
defines its own dead-code or duplication scripts, prefer those over
generic flags.

## Step 0.5 — ask when detection is ambiguous

Use `AskUserQuestion` only for real ambiguity:

- several unrelated deployable units in a monorepo and no clear target
- no documented size convention and the threshold materially changes the review
- project-provided audit scripts look stale or contradictory

## Step 1 — frontend dead code & duplication

If TS/JS is present, start from:

```bash
npx knip --production
npx jscpd --min-lines 10 --reporters console <src-dirs>
```

Treat generated clients and other generated code separately. `knip` is
triage, not truth.

## Step 2 — backend dead code & duplication

If Python is present:

```bash
source .venv/bin/activate 2>/dev/null || true
ruff check app --select F401,F811,F821 --statistics
ruff check app --statistics
pip install -q vulture
vulture app --min-confidence 80
vulture app --min-confidence 60 | grep -vE "unused (attribute|method)"
npx jscpd --min-lines 10 --reporters console <backend-src-dir>
```

Do not report framework-driven false positives without verification.

## Step 3 — verify every unused candidate before reporting

For each candidate symbol, cross-check with `grep` or `rg`:

```bash
grep -rn '\bSYMBOL\b' <src-dir> <tests-dir> --include='*.py'
grep -rn '\bSYMBOL\b' <src-dir> <tests-dir> --include='*.ts' --include='*.tsx'
```

- one occurrence only at the definition: confirmed dead
- multiple occurrences: likely false positive or public surface

## Step 4 — structural refactoring signals

Cross-check against project conventions if present:

```bash
find <src-dir> -name '*.tsx' | xargs wc -l | awk '$1>200 && $2!="total"' | sort -rn
find <src-dir> -name '*.py' | xargs wc -l | sort -rn | head -20
```

If the repo does not document a limit, report outliers as candidates, not
violations.

## Step 5 — write the report

Use three tiers:

1. Confirmed dead code
2. Duplication clusters
3. Structural refactoring candidates

Each item should include file references, a short reason, and whether it
is safe to auto-fix or needs human review.

The output must also disclose:

- Coverage
- Scope inspected
- Excluded areas
- Persistence mode
- Writes performed or skipped
