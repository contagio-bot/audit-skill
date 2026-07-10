# Audit capability protocol

Every run begins with a capability manifest. Detect what the environment
can support before choosing tools, confidence level, and persistence
behavior.

## Detect

- Git availability
- network availability
- write access to the target repo
- runtimes and package managers
- Docker / container tools
- test runners
- static-analysis tools already installed
- time or context limits visible from the environment

Prefer the bundled script:

`scripts/detect_capabilities.py <target>`

## Minimum output

```text
Detected:
- TypeScript / pnpm
- PostgreSQL / Prisma

Available:
- git
- node
- pnpm

Unavailable:
- network
- docker

Skipped:
- live advisory refresh
- container runtime verification
```

## Rules

- Do not install tools automatically.
- Missing tools reduce coverage/confidence; they do not justify guessing.
- The manifest must appear in the final output for non-trivial audits.
