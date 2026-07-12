# audit perf

Performance-optimization deep dive: database indexing, query efficiency,
and hot-path bottlenecks. Unlike the other commands, no dedicated external
skill exists for this yet, so the methodology below is self-contained —
follow it directly rather than delegating to another `SKILL.md`.

This is deliberately narrower and deeper than `arch`'s "Performance &
Scalability" category (one of 10 rated categories there, a few bullets).
`perf` exists for when the user specifically wants indices, query plans,
and data-access patterns actually inspected, not a general architecture
pass that happens to touch performance.

## Standing audit context (load before scoping)

Check for `AUDIT-CONTEXT.md` per
[context-protocol.md](context-protocol.md) before starting. Suppress
findings that match an already-accepted entry (any section), listing them
under "Previously accepted (not re-flagged)" per that protocol. At the
end, offer to persist any newly-accepted finding under a **Performance**
section (create it if the file predates this command).

Resolve the shared protocols first:

- `reference/bootstrap-lite.md`

Load conditionally: `reference/persistence-protocol.md` only for
`--persist`/writes beyond the report; `reference/finding-contract.md` +
`reference/formal-delta.md` + `reference/output-contract.md` only when the
run is formal.

## Scope check (ask, don't guess)

Use `AskUserQuestion` when genuinely unclear from the repo/request —
otherwise proceed:

- **Target datastore(s)**: if the repo talks to more than one datastore
  (e.g. Postgres + Redis + Elasticsearch) and it's not obvious which one
  the user cares about, ask.
- **Live access**: whether a running instance / real `EXPLAIN` output is
  available, or this must be a static, schema-and-code-only pass. This
  materially changes what can be `Observed` vs only `Inferred` — don't
  silently assume one or the other.
- **Known pain points**: if the user already suspects a slow endpoint or
  report, ask where before spending the budget searching blind.

## Analysis steps

1. **Inventory the data-access surface.** Find schema/migration files,
   ORM models, raw SQL, query builders, and any datastore client usage
   (cache, search index, queue). List concrete repo-relative paths found,
   or `None found`.
2. **Indexing.**
   - For every table/collection, cross-reference columns used in
     `WHERE`, `JOIN`, `ORDER BY`, `GROUP BY`, and foreign keys against
     actual indexes/constraints defined in schema or migrations.
   - Flag missing indexes on foreign keys, high-cardinality filter
     columns, and columns backing unique/business constraints.
   - Flag indexes that look unused or redundant (e.g. a composite index
     fully shadowed by a wider one) if migration history/usage evidence
     supports it — don't guess without evidence.
   - Note composite-index column order versus actual query predicates
     (a composite index only helps a query if the leading columns match).
3. **Query patterns.**
   - N+1 queries: loops that issue one query per iteration instead of a
     batched/joined fetch (classic ORM lazy-loading trap).
   - Unbounded queries: missing `LIMIT`/pagination on endpoints or jobs
     that can grow with data volume.
   - Overfetching: `SELECT *` / fetching full objects/relations where
     only a few fields are used downstream.
   - Full-table scans implied by filtering/sorting on non-indexed or
     function-wrapped columns (e.g. `WHERE LOWER(email) = ...` without a
     matching expression index).
   - Inefficient joins, unnecessary subqueries, or queries re-run inside
     loops that could be hoisted/batched.
   - Synchronous heavy queries on hot request paths that could be
     cached, precomputed, or moved to a background job.
4. **Query plans (only if live access is available).** Run `EXPLAIN` /
   `EXPLAIN ANALYZE` (or the datastore's equivalent) on the queries found
   to be most consequential — highest-traffic endpoints, largest tables,
   or ones the user flagged. Cite actual plan output (seq scan vs index
   scan, estimated vs actual rows, cost) as `Observed` evidence. If no
   live access exists, mark plan-dependent claims `Not verifiable from
   repo` rather than guessing at what the planner would do.
5. **Connection & transaction handling.** Connection pool sizing and
   reuse, transaction scope (too broad = lock contention, too narrow =
   lost atomicity), long-running transactions holding locks, retry/
   timeout behavior under load.
6. **Caching & batching.** Presence and correctness of caching layers
   (in-process, Redis/Memcached, HTTP/CDN), cache invalidation strategy,
   batching of external calls (bulk insert/update vs row-by-row), use of
   `DataLoader`-style batching where applicable.
7. **Background/async work.** Whether expensive aggregation, reporting,
   or fan-out work runs synchronously in the request path versus queued/
   scheduled; whether jobs themselves have the same N+1/indexing issues
   as request-path code.

## Output

Standard mode: per `bootstrap-lite.md`'s 4-section format. Formal mode:
follow `reference/output-contract.md`.

Area-specific addendum:

- datastore/query-layer summary
- live-access vs static-only disclosure
- findings grouped by the 7 analysis areas
- prioritized recommendation table with `Recommendation | Area | Impact | Effort | Evidence`

## Notes

- If the user's request is really about general architecture/code-quality
  with performance as one facet among many, redirect to `audit arch`
  instead — this command is for when performance/indices/queries are the
  specific ask.
- `dd` does not run `perf` internally (same reasoning as `pentest`/`deps`:
  it composes only `deadcode` + `arch` + `security`). Mention `perf` as a
  separate opt-in follow-up if the due-diligence user cares specifically
  about data-layer performance.
- Every recommendation must be traceable to actual schema/code/plan
  evidence inspected during this run — never suggest an index or query
  rewrite "in general" without pointing at the specific query/table that
  needs it.
