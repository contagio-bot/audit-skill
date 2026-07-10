# audit deadcode

Dead code, duplication, and structural-refactoring audit. This command has
no logic of its own — it delegates entirely to one of the local bundled
methodologies.

## Profile detection

1. Resolve the target's repo root.
2. Look for a matching profile under `profiles/*.md`.
3. If a matching profile exists and names a dedicated deadcode
   methodology, `Read` and follow that local file in full.
4. Otherwise, `Read` and follow
   **`methodologies/deadcode/generic.md`** in full.

## After delegating

Both bundled methodologies only *report* findings — they never apply
fixes. If the user
wants fixes applied after reviewing the report, hand off explicitly to the
`knip` skill (frontend), `ruff --fix` (backend), or the `dry-refactoring`
skill (clone elimination), as the delegated skill itself instructs.

## Notes

- Do not merge or summarize source instructions from memory — always read
  the selected bundled file fresh.
- If the selected local methodology file is missing, stop and tell the
  user rather than improvising a replacement audit.
