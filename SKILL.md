---
name: audit
description: "Router for repository audits, baselines, diffs, verification, and remediation planning. Delegates only to bundled methodologies, references, schemas, and local stdlib scripts. Supports explicit coverage, persistence, capability, evidence, and export protocols without external skill dependencies."
argument-hint: "[deadcode|arch|perf|security|pentest|deps|supply-chain|ci|testing|data|api|cloud|operability|privacy|ai|licensing|dd|baseline|diff|verify|fix-plan|issue|context|recheck|--profile] [target] [--read-only|--persist] [--full|--partial|--batched|--risk-based|--sample] [--format markdown|json|csv|sarif|github-issues]"
user-invocable: true
license: MIT
---

# Audit router

Single entry point for the audit framework. The router stays thin:

- recognize user intent
- resolve target and repo root
- resolve coverage and persistence mode
- resolve profile and capability/inventory manifests
- delegate to the bundled methodology/reference files needed for that command

It must not inline specialist audit logic.

**Never re-derive methodology from memory.** Always `Read` the delegated
local file and any references it names before running that command.

## Commands

| Command | Category | Description | Reference |
|---|---|---|---|
| `deadcode [target]` | Quality | Dead code, duplication, refactoring/simplification candidates | [reference/deadcode.md](reference/deadcode.md) |
| `arch [target]` | Quality | Architecture, bug risk, performance, readability, and design-smell review | [reference/arch.md](reference/arch.md) |
| `perf [target]` | Quality | Query-path, indexing, and hot-path performance deep dive | [reference/perf.md](reference/perf.md) |
| `security [target]` | Risk | Cybersecurity and infrastructure/operability criticalities | [reference/security.md](reference/security.md) |
| `pentest [target]` | Risk | Static attack-surface mapping plus gated dynamic verification | [reference/pentest.md](reference/pentest.md) |
| `deps [target]` | Risk | Runtime/dependency freshness and known-CVE sweep | [reference/deps.md](reference/deps.md) |
| `supply-chain [target]` | Risk | Software supply-chain integrity and provenance audit | [reference/supply-chain.md](reference/supply-chain.md) |
| `ci [target]` | Risk | CI/CD security, integrity, and reproducibility audit | [reference/ci.md](reference/ci.md) |
| `testing [target]` | Quality | Test strategy and regression-resistance audit | [reference/testing.md](reference/testing.md) |
| `data [target]` | Risk | Data modeling, lifecycle, and protection audit | [reference/data.md](reference/data.md) |
| `api [target]` | Risk | API and webhook security/consistency/operability audit | [reference/api.md](reference/api.md) |
| `cloud [target] [aws|gcp|azure|kubernetes]` | Risk | Cloud, IaC, container, and Kubernetes audit | [reference/cloud.md](reference/cloud.md) |
| `operability [target]` | Risk | Production operability, resilience, and observability audit | [reference/operability.md](reference/operability.md) |
| `privacy [target]` | Risk | Technical privacy-behavior audit without legal conclusions | [reference/privacy.md](reference/privacy.md) |
| `ai [target]` | Risk | LLM/agent/ML integration risk audit | [reference/ai.md](reference/ai.md) |
| `licensing [target]` | Risk | Dependency and asset licensing-risk audit | [reference/licensing.md](reference/licensing.md) |
| `dd [target]` | Risk | Full technical due diligence | [reference/dd.md](reference/dd.md) |
| `baseline [target]` | Continuity | Create or refresh an audit baseline snapshot | [reference/baseline.md](reference/baseline.md) |
| `diff [base..head] [target]` | Continuity | Compare findings across revisions using fingerprints | [reference/diff.md](reference/diff.md) |
| `verify [finding-id] [target]` | Continuity | Revalidate a single finding and its immediate dependencies | [reference/verify.md](reference/verify.md) |
| `fix-plan [target]` | Remediation | Build a grouped remediation roadmap from findings | [reference/fix-plan.md](reference/fix-plan.md) |
| `issue [finding-id] [target]` | Remediation | Generate an issue-ready remediation brief | [reference/issue.md](reference/issue.md) |
| `context [target]` | Context | Create or update `AUDIT-CONTEXT.md` explicitly | [reference/context.md](reference/context.md) |
| `recheck [target]` | Context | Recheck only open follow-ups against current repo state | [reference/recheck.md](reference/recheck.md) |
| `--profile [target]` | Profiles | Create or update a local repo-specific audit profile | [reference/profile.md](reference/profile.md) |

`target` defaults to the current working directory if omitted.

## Optional modifiers

- `--read-only`: never create or modify files in the target repo
- `--persist`: allow writing context/baseline/report artifacts when the delegated workflow calls for them
- `--full`: intended exhaustive pass over the in-scope target
- `--partial`: bounded subset only
- `--batched`: exhaustive-by-area across batches/services
- `--risk-based`: prioritize highest-risk surfaces first
- `--sample`: representative sampling only
- `--format markdown|json|csv|sarif|github-issues`: choose an output format per [reference/export-formats.md](reference/export-formats.md)

## Routing rules

1. No argument: render the command menu and ask what the user wants.
2. `--profile`: load [reference/profile.md](reference/profile.md).
3. Known command: load its reference file and follow it exactly.
4. Natural-language request: map it only when intent is materially clear.
5. If ambiguity would change the outcome, ask instead of guessing.

## Shared protocols

Every substantive run must resolve and apply:

- [reference/capability-protocol.md](reference/capability-protocol.md)
- [reference/inventory-protocol.md](reference/inventory-protocol.md)
- [reference/coverage-protocol.md](reference/coverage-protocol.md)
- [reference/persistence-protocol.md](reference/persistence-protocol.md)
- [reference/evidence-protocol.md](reference/evidence-protocol.md)
- [reference/finding-schema.md](reference/finding-schema.md)
- [reference/scoring-rubric.md](reference/scoring-rubric.md) when scoring applies

When findings are persisted, baseline-compared, or exported, also use:

- [reference/baseline-protocol.md](reference/baseline-protocol.md)
- [reference/remediation-protocol.md](reference/remediation-protocol.md)
- [reference/export-formats.md](reference/export-formats.md)

## Self-contained rule

This package must be self-contained. Do not delegate to `~/.claude`,
`~/.agents`, absolute machine-local paths, or marketplace skills. All
delegations must point to files bundled inside this package:

- `reference/`
- `methodologies/`
- `profiles/`
- `scripts/`
- `schemas/`

If a needed bundled file is missing, stop and tell the user exactly which
file is missing.

## Standing context across runs

If `AUDIT-CONTEXT.md` exists, delegated methodologies must read it per
[reference/context-protocol.md](reference/context-protocol.md). This file
records standing facts, accepted risks, audit plan state, and open
follow-ups. In `read-only` mode it may be read but must not be modified.

## Adding a new area

To add another audit area later:

1. add one router row above
2. add one `reference/<name>.md`
3. add one bundled methodology under `methodologies/`
4. update tests, schemas, and protocols if the new area changes shared behavior

Do not inline the new area's logic into this router.
