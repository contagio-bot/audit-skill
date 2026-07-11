# Audit boundaries

Use this file to avoid duplicated ownership across audit commands.

## Pattern

```yaml
primary_owner: supply-chain
related_audits:
  - deps
  - ci
```

## Rules

- every audit area has one primary owner
- secondary areas may reference it, but should redirect when the owner is
  clearly more appropriate
- aggregated reports should deduplicate by fingerprint and show cross-links
- related audits may cross-reference a finding, but should not duplicate it

## Suggested ownership

- `deadcode`: dead code, duplication, refactoring
- `arch`: architecture, design, code health
- `perf`: query/index/data-path performance
- `security`: cyber risk and infrastructure hardening
- `pentest`: static attack surface and live verification
- `deps`: runtime and dependency freshness
- `supply-chain`: provenance and dependency integrity
- `ci`: workflow integrity and release pipeline trust
- `testing`: test strategy and regression resistance
- `data`: data modeling and lifecycle
- `api`: APIs and webhooks
- `cloud`: cloud/IaC/container runtime
- `operability`: production operability
- `privacy`: technical privacy behavior
- `ai`: model/agent risk
- `licensing`: license and asset risk
