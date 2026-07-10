# audit recheck

Fast, narrow command: check only the **Open follow-ups** section of
`AUDIT-CONTEXT.md` against the current state of the repo. Not a full
audit — no `knip`/`ruff`/`vulture`/full-repo subagent runs. Use this when
the user wants to know "did we fix the things we said we'd fix" without
paying for a full re-audit.

## Steps

1. Locate `AUDIT-CONTEXT.md` per
   [context-protocol.md](context-protocol.md). If it's missing, or its
   **Open follow-ups** section is empty, tell the user there's nothing to
   recheck — suggest `audit context` to seed it, or a full audit
   (`deadcode`/`arch`/`security`/`dd`) if they've never run one.
2. For each open follow-up entry, look for concrete evidence in the
   current repo that it's been addressed: targeted `rg`/`grep` for the
   symbol or pattern named in the entry, `git log` since the entry's date
   on the relevant path, or reading the specific file/function it
   referenced.
3. Classify each one:
   - **Resolved** — evidence directly shows the issue is gone (e.g. the
     dead file was deleted, the missing rate limit is now present).
   - **Still open** — no evidence of change; state exactly is as it was.
   - **Ambiguous** — something changed nearby but you can't confirm the
     specific follow-up is addressed; don't guess, list it separately and
     ask the user to judge.
4. Report item by item, grouped by classification, most actionable first
   (Still open, then Ambiguous, then Resolved). If an accepted risk entry
   is now stale or its invalidation condition has been met, include a
   separate **No longer applicable** group.
5. Offer to update the file: for confirmed **Resolved** items, remove them
   from Open follow-ups (ask once per batch, not once per item, unless the
   user wants line-by-line control). For items the user says are now
   intentionally accepted rather than fixed, move them to the matching
   **Accepted risks** section instead of deleting.
6. Never edit the file without the user confirming the classification
   first — this command's whole value is being trustworthy about "did we
   actually fix it," so a wrong silent removal defeats the point.

## Notes

- If a follow-up entry is vague enough that you can't tell what evidence
  would even confirm it (e.g. "improve error handling" with no file/scope),
  say so and suggest rewriting it via `audit context` with more specifics,
  rather than guessing at what counts as resolved.
