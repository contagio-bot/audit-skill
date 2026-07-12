# Audit bootstrap

1. Resolve target and repository root.
2. Detect capabilities — prefer `scripts/detect_capabilities.py <target>`
   (git/network/write access, runtimes, tools). Missing tools reduce
   coverage/confidence; never install anything automatically; never guess
   around a gap they leave.
3. Inventory the repository — prefer `scripts/inventory.py <target>`
   (source, tests, config, infra, migrations, docs; vendor/build output
   excluded unless it shows a concrete risk).
4. Choose coverage and state it in the output: `full`, `partial`,
   `batched`, `risk-based`, or `sample`. Prefer `full`; use `partial` when
   the boundary is clear and deliberate; `batched` for broad but
   partitionable scope; `risk-based` when constraints force prioritizing
   auth/payments/entry-points/secrets/infra; `sample` only when the
   boundary is fuzzy or constraints block exhausting the intended scope.
   Downgrade `full` in the final output if the planned coverage wasn't
   completed, and say why.
5. Persistence defaults (full protocol only when it applies — see
   [persistence-protocol.md](persistence-protocol.md)):
   - default: write the report only, everything else read-only
   - `--read-only`: write nothing, chat-only output
   - `--persist`: also allow context/baseline/profile writes when the
     methodology calls for them
6. Load profile, context, baseline, scoring, export, or the finding
   contract only when the command actually needs them.
7. Execute the selected methodology.
8. Validate the result — `scripts/validate_output_contract.py`.
9. Disclose scope, exclusions, confidence impact, skipped steps, and
   writes performed/skipped.

## Standard output (default mode)

1. **Summary** — 3-8 lines: top strengths, top concerns, top risks.
2. **Coverage and limits** — resolved scope, coverage mode, excluded
   areas, confidence impact when not `full`; capability manifest and
   persistence disclosure folded in as sub-bullets.
3. **Findings** — severity-ordered, each with inline evidence
   (`file:line` or command output), classified `Observed`, `Inferred`,
   or `Not verifiable`.
4. **Recommended next actions** — prioritized, with acceptance criteria
   when actionable work is proposed.

Formal mode (normalized findings, evidence ledger, 8 sections) is a
delta on top of this — see [formal-delta.md](formal-delta.md).
