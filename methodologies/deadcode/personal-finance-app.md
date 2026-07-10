---
name: deadcode-personal-finance-app
description: Repo-specific code health audit for the personal-finance-app monorepo, bundled inside the audit router.
---

# Code Health Audit

This methodology is specialized for `personal-finance-app`. Use it for
dead code analysis, duplicate code analysis, refactoring opportunities,
oversized modules, and simplification reviews.

## 1. Load project conventions

Read:

- `CLAUDE.md`
- `frontend/package.json`
- `frontend/knip.json` if present
- `backend/pyproject.toml`
- `audit/reference/context-protocol.md`

Respect these repo conventions:

- React components should stay under 200 lines where possible
- business logic should not leak into React components
- backend services should orchestrate, not accumulate duplicated calculation logic

## 2. Frontend audit

Run from `frontend/`:

```bash
npm run check:dead
npm run check:dup
find src -name '*.tsx' -o -name '*.ts' | xargs wc -l | sort -rn | sed -n '1,40p'
```

Interpretation rules:

- Treat `knip` output as triage, not truth.
- Verify every unused file or export with `rg`.
- Generated code under `src/api/generated/**` is a special case.
- Exports used only by tests are not production-used, not automatically dead.
- If a hook is only used by a dead component, report the whole dead chain.

Useful checks:

```bash
rg -n "SymbolName" src tests
rg -n "@/api/generated|api/generated" src tests
rg -n "from '@/api/client'|from \"@/api/client\"" src
```

## 3. Backend audit

Run from `backend/`:

```bash
./.venv/bin/ruff check app --select F401,F811,F821 --statistics
./.venv/bin/ruff check app --statistics
./.venv/bin/vulture app --min-confidence 80
./.venv/bin/vulture app --min-confidence 60 | grep -vE "unused (attribute|method)"
../frontend/node_modules/.bin/jscpd --reporters console --min-lines 10 app tests scripts
find app -name '*.py' | xargs wc -l | sort -rn | sed -n '1,40p'
```

Ignore recurring `vulture` noise on FastAPI route handlers, SQLAlchemy
models/relationships, Pydantic fields/config, protocol parameters, and
event hook callback arguments unless verified manually.

## 4. Prioritize findings

Report in this order:

1. Confirmed dead code safe to remove
2. Dead-code candidates requiring human confirmation
3. Duplicate clusters with highest extraction payoff
4. Structural refactoring candidates

Prioritize these repo patterns:

- unused route-less pages
- orphaned hooks/components
- generated frontend clients not actually used
- duplicated modal/form flows
- duplicated scheduler/email campaign flows
- duplicated seed scripts
- duplicated spending aggregation logic across repositories
- oversized services that repeat post-write refresh/projection logic

## 5. Output format

Produce an evidence-based report with file and line references, a short
reason per finding, and one label:

- `safe to remove`
- `safe after confirmation`
- `needs human review`

Do not suggest broad rewrites. Prefer small extractable seams.
