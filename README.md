# audit-skill

Claude Code skill: a router for repository audits (`/audit`).

Delegates to four sub-commands — `deadcode`, `arch`, `security`, `dd` —
each of which loads and follows a dedicated audit skill rather than
reimplementing the logic here. See `SKILL.md` for the full routing rules,
and `reference/context-protocol.md` for the shared `AUDIT-CONTEXT.md`
mechanism that prevents repeat audits from re-flagging decisions already
accepted as intentional.
