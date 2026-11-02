# audit night-report

Operational smoke pass: run the repo’s **`scripts/nightly-audit/`** CLI
pipeline (the same checks used on Magellano EC2 cron) and interpret results.
This command has no logic of its own — it delegates entirely to a bundled
local methodology.

## Delegation

`Read` and follow **`methodologies/night-report/SKILL.md`** in full.

## Notes

- **`night-report` is not a substitute for `audit deps`.** `deps` covers
  EOL/support, manifest/lock coherence, and breadth; `night-report` runs
  the **production-shaped** toolchain (Docker + `pip-audit` or
  `npm audit --package-lock-only` + allowlist) plus lightweight
  deadcode/dup signals.
- Recommended order in a full hygiene pass:
  **`deps` → remediate → `night-report`** (confirm cron-equivalent green),
  or **`night-report` alone** for a fast CVE/deadcode smoke on a checkout.
- If `scripts/nightly-audit/run.sh` is **missing**, the methodology
  describes bootstrap sources (Magellano repos) and falls back to manual
  equivalent checks — do not silently skip.
- Default persistence: **`read-only`** (logs under `/tmp` or
  `AUDIT_LOG_ROOT`). Use `--persist` only when the user wants a report
  file under `docs/audit/` and/or an `AUDIT-CONTEXT.md` run-log line.
