# Audit persistence protocol

Separate analytical behavior from file-writing behavior. An audit can be
valuable even when it should not modify the repository beyond the one
artifact it exists to produce.

## Modes

### default: persist (report, plus context/baseline when relevant)

The default mode for every report-producing command (`deadcode`, `arch`,
`perf`, `security`, `pentest`, `deps`, `supply-chain`, `ci`, `testing`,
`data`, `api`, `cloud`, `operability`, `privacy`, `ai`, `licensing`, `dd`)
is `--persist`-equivalent: write the report, and also create or update
`AUDIT-CONTEXT.md` and baseline files under `.audit/baselines/` when the
methodology calls for it. This does not bypass the per-write confirmation
rules in [reference/context-protocol.md](context-protocol.md) and
[reference/baseline-protocol.md](baseline-protocol.md) — persisting by
default only permits those writes to happen at all; judgment-recording
writes still require summarizing the intended write and getting
confirmation first.

In this default mode:

- unless a report path is otherwise specified by the command or an
  existing repo profile, write the report to
  `docs/audit/<YYYY-MM-DD>-<command>.md` at the target repo root,
  creating `docs/audit/` if it does not exist. A same-day rerun of the
  same command may overwrite that day's file.
- do not write the report if the repository is not writable; report the
  limitation instead and fall back to chat-only output
- create or update `AUDIT-CONTEXT.md` and baseline files when the
  methodology calls for it, subject to the per-write confirmation rules
  above
- do not create profile files unless the command is `--profile` or the
  user explicitly asks for one
- you may still read any of those files if they already exist, and use
  them (accepted risks, standing facts, existing profile) to shape the
  report

If a methodology would normally persist something beyond the report and
per-write confirmation is declined for that item, say what would have
been written and continue without writing it.

Always treat the run this way (full persist) when:

- the command is `context`
- the command is `--profile`
- the command is `baseline`
- the user explicitly asks to write/update audit artifacts beyond the
  report (e.g. "save this to AUDIT-CONTEXT.md", "create a baseline")

These commands exist specifically to write their artifact, so they
persist regardless of any flag.

### `--read-only`

Full read-only: suppress even the report-file write. Use only when the
user explicitly asks for it (e.g. "just review", "don't write anything",
"chat only", "don't create a report").

In `--read-only` mode:

- do not write the report file
- do not create or update `AUDIT-CONTEXT.md`
- do not create or update baseline files
- do not create profile files
- produce the full analysis in chat output instead

You may still read any of those files if they already exist.

## Resolution rules

1. Default for every report-producing command: write the report, and
   allow context/baseline writes when the methodology calls for it
   (still gated by per-write confirmation) — i.e. persist by default.
2. `context`, `baseline`, and `--profile` always persist their own
   artifact regardless of flags — that's their whole job.
3. If the user says "just review", "don't write anything", "read-only",
   or similar, treat that single run as `--read-only` (no writes at
   all, including the report file).
4. If the target repo is not writable, behave as `--read-only` even if
   writes would otherwise happen by default, and report that downgrade.

## Mandatory disclosure

Every audit result must include:

- `Persistence mode`: `persist` (default: report plus any context/baseline
  writes the methodology called for) or `read-only` (nothing written,
  explicitly requested or forced by a non-writable repo)
- `Writes performed`: concrete files or `none`
- `Writes skipped`: concrete files and reasons, when relevant
