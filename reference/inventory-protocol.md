# Audit inventory protocol

Build a measurable inventory before deep analysis.

## Goal

Identify:

- first-party source
- tests
- configuration
- infrastructure
- migrations / schema
- docs
- generated/vendor/cache/build output

Prefer the bundled script:

`scripts/inventory.py <target>`

## Output contract

The inventory must state:

- repository root
- requested scope
- resolved scope
- top-level areas
- relevant file groups found
- excluded paths and why

## Rules

- Do not claim whole-repo review without a concrete inventory.
- Generated/vendor/cache paths are excluded by default unless they expose
  a concrete risk.
- The inventory informs coverage mode selection.
