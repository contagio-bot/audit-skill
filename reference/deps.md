# audit deps

Fast, isolated dependency/runtime freshness sweep: EOL/support-status
across direct dependencies and primary runtimes, plus a known-CVE scan.
This command has no logic of its own — it delegates entirely to a bundled
local methodology.

## Delegation

`Read` and follow **`methodologies/deps/SKILL.md`** in full.

No context branching is needed here: the bundled methodology
auto-detects ecosystems and adapts its tooling accordingly.

## Notes

- `dd` may reuse the same evidence categories, but `deps` remains the
  dedicated narrower pass for dependency/runtimes specifically.
- `arch`'s "Dependency & Runtime Currency" category is intentionally
  narrower (4-5 central components, one line in a 10-category review) —
  don't treat it as equivalent to `deps` if the user wants full coverage.
