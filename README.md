# audit-skill

Claude Code skill: a router for repository audits (`/audit`).

Delegates to six sub-commands — `deadcode`, `arch`, `security`, `pentest`,
`deps`, `dd` — each of which loads and follows a dedicated audit skill
rather than reimplementing the logic here. `pentest` is the only one with
a gated dynamic phase: it maps the attack surface statically, then only
runs live exploit checks against a target the user explicitly confirms
they're authorized to test. `deps` is a fast, isolated EOL/support-status
and CVE sweep across every direct dependency, narrower and quicker than
running a full `dd`. See `SKILL.md` for the full routing rules, and
`reference/context-protocol.md` for the shared `AUDIT-CONTEXT.md`
mechanism that prevents repeat audits from re-flagging decisions already
accepted as intentional.
