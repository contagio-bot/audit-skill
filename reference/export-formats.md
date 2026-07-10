# Audit export formats

Supported formats:

- `markdown`
- `json`
- `csv`
- `sarif`
- `github-issues`

## Rules

- `markdown`: human-readable default
- `json`: normalized findings and metadata
- `csv`: backlog/table workflows
- `sarif`: only for findings localizable to code
- `github-issues`: preview only unless the user explicitly asks to create issues

Do not emit SARIF for purely organizational findings with no meaningful
location.
