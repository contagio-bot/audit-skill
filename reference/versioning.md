# Audit versioning

Version these fields in reports, baselines, and normalized findings:

- `schema_version`
- `framework_version`
- `methodology_version`
- `fingerprint_version`

## Rules

- incompatible versions must not be compared silently
- the report must declare the versions it used
- the baseline store must persist versions alongside findings
- fingerprinting changes require a version bump

## Suggested defaults

- `schema_version`: `"1.0"`
- `framework_version`: `"0.4.0"`
- `fingerprint_version`: `"1"`
- `methodology_version`: a short string such as `"security/2.1"`
