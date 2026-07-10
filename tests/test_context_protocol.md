# Context protocol scenarios

## File absent in read-only

- expected: do not create `AUDIT-CONTEXT.md`

## File absent in persist

- expected: propose initialization before writing

## Legacy file without audit plan

- expected: note or patch depending on persistence mode

## Accepted risk pertinent

- expected: suppress only the matching finding and list it under previously accepted

## Accepted risk obsolete

- expected: classify as stale or no longer applicable
