---
name: supply-chain-local
description: Bundled software supply-chain audit methodology.
license: MIT
---

# Supply-chain audit

Resolve the shared protocols first:

- `audit/reference/bootstrap-lite.md`

Load conditionally: `audit/reference/persistence-protocol.md` only for
`--persist`/writes beyond the report; `audit/reference/finding-contract.md`
+ `audit/reference/formal-delta.md` + `audit/reference/output-contract.md`
only when the run is formal.

Then inspect:

- manifests and lockfiles
- direct and central transitive dependencies when visible
- Git URL / floating branch dependencies
- GitHub Actions pinned vs mutable refs
- SBOM/provenance/attestation status if present
- dependency confusion / typosquatting indicators
- release provenance and artifact-signing evidence if present

## Output

Standard mode: per `bootstrap-lite.md`'s 4-section format. Formal mode: follow `audit/reference/output-contract.md`.

- dependency inventory
- top transitive risks
- provenance gaps
- SBOM status
