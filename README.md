# audit-skill

Claude Code skill: a router for repository audits (`/audit`).

Delegates to seven sub-commands — `deadcode`, `arch`, `perf`, `security`,
`pentest`, `deps`, `dd` — each of which loads and follows a dedicated
audit skill rather than reimplementing the logic here (`perf` is the
exception: no external skill exists for it yet, so its methodology lives
directly in `reference/perf.md`). `pentest` is the only one with a gated
dynamic phase: it maps the attack surface statically, then only runs live
exploit checks against a target the user explicitly confirms they're
authorized to test. `deps` is a fast, isolated EOL/support-status and CVE
sweep across every direct dependency, narrower and quicker than running a
full `dd`. `perf` is a dedicated deep dive on database indices, query
patterns, and query plans — narrower and deeper than the "Performance &
Scalability" category inside `arch`'s 10-category review. `dd` composes
five of the six atomic audits internally (`deadcode`, `arch`, `security`,
`perf`, `deps`) plus deal framing — only `pentest` stays separate, gated
behind live-target authorization. See `SKILL.md` for the full routing
rules, and `reference/context-protocol.md` for the shared
`AUDIT-CONTEXT.md` mechanism that prevents repeat audits from re-flagging
decisions already accepted as intentional.

Every command (except `context`/`recheck`) also writes its full analysis
and a concrete action-item list to a markdown report under `docs/audit/`
in the target repo, creating that folder if it doesn't exist yet — see
`SKILL.md`'s "Report output" section.
