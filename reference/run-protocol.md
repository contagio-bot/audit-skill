# Audit run protocol

Standard sequence for all substantive runs:

1. resolve target and repository root
2. detect capabilities
3. inventory the repository
4. resolve scope and coverage
5. resolve persistence mode
6. load profile, context, and baseline
7. execute the methodology
8. record evidence
9. normalize findings
10. deduplicate and compare with baseline
11. compute scoring and confidence
12. validate the output
13. export when requested
14. persist only if allowed
15. disclose limits, writes, and skipped steps

## Rules

- do not skip directly to the methodology
- use the bundled `scripts/` utilities for deterministic steps where available
- downgrade coverage if the run cannot complete the planned sequence
- do not mutate context or baseline files in `read-only` mode
