# Audit persistence protocol

Separate analytical behavior from file-writing behavior. An audit can be
valuable even when it should not modify the repository.

## Modes

### `read-only`

Default mode for `deadcode`, `arch`, `security`, `dd`, and `recheck`
unless the user explicitly asks for persistence.

In `read-only` mode:

- do not create `AUDIT-CONTEXT.md`
- do not update `AUDIT-CONTEXT.md`
- do not create report files
- do not create profile files

You may still read any of those files if they already exist.

If a methodology would normally persist something, say what would have
been written and continue without writing it.

### `persist`

Use `persist` when:

- the user explicitly asks to write/update audit artifacts
- the command is `context`
- the command is `--profile`
- the user confirms a proposed write during the run

In `persist` mode:

- write only the files relevant to the command
- summarize the intended write before doing it when the write records
  judgment, acceptance, or status
- do not write if the repository is not writable; report the limitation
  instead

## Resolution rules

1. Explicit user intent beats defaults.
2. `context` and `--profile` are inherently persistent commands.
3. If the user says "just review" or similar, treat that as `read-only`
   unless they also ask for artifact creation.
4. If the target repo is not writable, behave as `read-only` even if
   `persist` was requested, and report that downgrade.

## Mandatory disclosure

Every audit result must include:

- `Persistence mode`: `read-only` or `persist`
- `Writes performed`: concrete files or `none`
- `Writes skipped`: concrete files and reasons, when relevant
