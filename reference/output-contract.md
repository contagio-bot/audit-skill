# Audit output contract

Use this contract for all specialist methodologies unless a more specific
output template explicitly overrides it.

## Required sections

1. **Executive summary**
   - 3-8 lines
   - top strengths
   - top concerns
   - top risks
2. **Scope and coverage**
   - requested scope
   - resolved scope
   - coverage mode
   - excluded areas
   - confidence impact
3. **Capability manifest**
   - available tools
   - unavailable tools
   - network / git / write status
4. **Method and evidence**
   - commands used
   - evidence ledger summary
   - skipped steps and why
5. **Detailed findings**
   - severity ordered
   - each substantive finding linked to evidence IDs
   - each finding classified `Observed`, `Inferred`, or `Not verifiable`
6. **Normalized findings**
   - if structured output or continuity workflow is requested, findings
     must also conform to `reference/finding-schema.md`
7. **Remediation**
   - prioritized recommendations
   - acceptance criteria when actionable work is proposed
8. **Persistence disclosure**
   - persistence mode
   - writes performed
   - writes skipped

## Area-specific addendum

Each methodology may append one required area-specific artifact, such as:

- matrix
- flow map
- dependency inventory
- endpoint control table

That addendum supplements, not replaces, the sections above.
