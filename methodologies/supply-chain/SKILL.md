---
name: supply-chain-local
description: Bundled software supply-chain audit methodology.
license: MIT
---

# Supply-chain audit

Resolve the shared protocols first, then inspect:

- manifests and lockfiles
- direct and central transitive dependencies when visible
- Git URL / floating branch dependencies
- GitHub Actions pinned vs mutable refs
- SBOM/provenance/attestation status if present
- dependency confusion / typosquatting indicators
- release provenance and artifact-signing evidence if present

Output:

- dependency inventory
- top transitive risks
- provenance gaps
- SBOM status
