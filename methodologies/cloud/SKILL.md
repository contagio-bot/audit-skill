---
name: cloud-local
description: Bundled cloud, IaC, container, and Kubernetes audit methodology.
license: MIT
---

# Cloud audit

Resolve the shared protocols first:

- `audit/reference/capability-protocol.md`
- `audit/reference/inventory-protocol.md`
- `audit/reference/coverage-protocol.md`
- `audit/reference/persistence-protocol.md`
- `audit/reference/evidence-protocol.md`
- `audit/reference/finding-schema.md`
- `audit/reference/output-contract.md`

Then inspect whichever provider or runtime evidence is present:

- IAM and access boundaries
- public exposure and networking
- encryption and secret management
- storage and database exposure
- logging, backup, disaster recovery evidence
- container hardening
- Kubernetes RBAC / pod security when present
- IaC state/drift clues

Support provider-specific framing when the user names `aws`, `gcp`,
`azure`, or `kubernetes`, but do not require a provider flag to run.

## Output

Follow `audit/reference/output-contract.md`.
