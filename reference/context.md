# audit context

Explicit command to create or update `AUDIT-CONTEXT.md` — the standing
context file described in
[context-protocol.md](context-protocol.md). Use this when the user wants
to seed or edit context directly, rather than waiting for the implicit
"should I record this?" offer that happens at the end of a full audit run
(e.g. a fresh repo where they already know their trade-offs, or cleaning
up stale entries).

## If the file doesn't exist yet

1. Resolve the target's repo root per `SKILL.md` » Context detection (shared rule).
2. Tell the user you're creating `AUDIT-CONTEXT.md` there, using the
   template in context-protocol.md. This includes the **Audit plan**
   section (the six atomic audits marked pending, start date = today) —
   that part is created automatically, no need to ask about it.
3. Ask what to seed the rest with — don't invent entries. Useful prompts:
   - "Any standing facts I should know that would otherwise look like a
     finding? (e.g. private repo used as backup, `.env` committed on
     purpose, intentional legacy code kept around)"
   - "Any risks or trade-offs your team has already discussed and decided
     to accept?"
   - If the user has nothing to add yet, create the file with just the
     template headers and stop — don't pad it with speculative entries.
4. Write the file with `Write`, following the template structure exactly
   (Standing facts / Audit plan / Accepted risks per section / Open
   follow-ups).

## If the file already exists

1. Read it in full.
2. Summarize its current contents briefly (section by section, one line
   each) so the user has a quick refresher, not a full reprint.
3. Ask what to add, change, or remove.
4. Apply with `Edit`. For removals the user explicitly requests, just do
   it — don't ask for confirmation twice.
5. Keep the one-bullet-per-entry style from the template; don't let an
   edit balloon a bullet into a paragraph.

## Notes

- This command never runs any audit tooling itself (no `knip`, `ruff`,
  `rg` scans) — it only manages the context file. If the user actually
  wants findings verified against the codebase, that's `deadcode` / `arch`
  / `security` / `dd`, not this.
- If the user asks to record something you have reason to doubt (e.g. a
  claimed "accepted risk" that looks like it contradicts something you
  just observed in the repo), say so before writing it — don't silently
  encode a mistaken belief into standing context that will suppress real
  findings later.
