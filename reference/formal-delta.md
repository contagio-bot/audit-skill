# Formal audit delta

In addition to [bootstrap-lite.md](bootstrap-lite.md):

- maintain an evidence ledger (stable IDs in run order) per
  [finding-contract.md](finding-contract.md)
- normalize every finding to the schema in
  [finding-contract.md](finding-contract.md) /
  `schemas/finding.schema.json`
- generate stable fingerprints; apply lifecycle status and baseline
  comparison; deduplicate cross-audit findings by fingerprint
- include version fields (`schema_version`, `framework_version`,
  `methodology_version`, `fingerprint_version`)
- validate with `scripts/validate_output_contract.py --mode formal --strict`
- use the 8-section formal output contract —
  [output-contract.md](output-contract.md)

Always applies to `baseline`/`diff`/`verify`/`recheck`/`dd`, any
non-markdown `--format`, and `--formal`.
