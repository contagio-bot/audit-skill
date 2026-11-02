# audit dd

Full technical due diligence. This command has no logic of its own — it
delegates entirely to bundled local methodology files.

## Delegation

1. Resolve the target's repo root.
2. Look for a matching profile under `profiles/*.md`.
3. If a matching profile names a dedicated due-diligence methodology,
   `Read` and follow that file in full.
4. Otherwise, `Read` and follow **`methodologies/dd/SKILL.md`** in full,
   including its local `references/` (`investigation-protocol.md`,
   `output-template.md`, `fintech-rules-checklist.md`).

The bundled DD methodology already composes the local architecture and
security methodologies, plus investment/deal framing and a full-repo
security subagent. It degrades gracefully on repos without a dedicated
profile.

## Notes

- This is the only sub-command under `audit` that is itself a composite —
  don't also separately run `audit arch` / `audit security` / `audit
  deadcode` before or after it for the same target; that duplicates work
  the local DD methodology already does internally.
- **Night report is part of DD by default:** phase 5 runs
  `scripts/nightly-audit/` (see [reference/night-report.md](night-report.md))
  after the DD dependency/CVE pass. You do not need a separate
  `audit night-report` invocation unless the user asked for night-report
  alone; inside `dd`, it is mandatory in phase 5.
