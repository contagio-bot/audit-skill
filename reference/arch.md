# audit arch

Architecture, hidden bugs, performance, readability, and design-smell
audit. This command has no logic of its own — it delegates entirely to a
bundled local methodology.

## Delegation

`Read` and follow **`methodologies/arch/SKILL.md`** in full.

No context branching is needed here: this skill is already stack-agnostic
and repo-agnostic (it makes no assumptions about language or framework and
explicitly marks non-applicable categories as `N/A`). Use it unchanged for
any target, including repos that also have a dedicated local profile.

It already covers, as scored categories: DDD/domain modeling, event-driven
architecture, database/data modeling, security, dependency/runtime
currency, performance & scalability, code cleanliness & patterns,
testability, bug risk & robustness, and documentation — i.e. "hidden bugs",
"performance issues", "readability", and "architectural smells" are each
one or more of its 10 rated categories, not something to re-derive here.

## Notes

- If the user's request is really about cybersecurity/infra exploitability
  specifically (not general code quality), redirect to `audit security`
  instead — this skill's own Security category is intentionally narrower
  (code-quality lens, not exploit/blast-radius lens).
- If the user's request is really a full due-diligence engagement, redirect
  to `audit dd`, which already composes this skill with the others.
