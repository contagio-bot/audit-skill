# audit security

Cybersecurity and infrastructure/operability audit. This command has no
logic of its own — it delegates to bundled local methodology files.

## Profile detection

1. Resolve the target's repo root.
2. Look for a matching profile under `profiles/*.md`.
3. If a matching profile exists and names a dedicated security
   methodology, `Read` and follow that local file in full.
4. Otherwise, `Read` and follow
   **`methodologies/security/generic.md`** in full.

## Notes

- Keep the "fewer high-confidence findings over many speculative ones"
  standard from the selected bundled file regardless of which branch is
  taken.
- If the user actually wants a due-diligence-scoped security pass (with a
  full-repo subagent and CVE scanning), redirect to `audit dd` instead —
  that flow already extends this one with those steps.
