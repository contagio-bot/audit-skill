# Checklist

Use this checklist only when needed during the audit.

## Critical Security Checks

- Public/demo login paths and feature flags
- Admin impersonation or acting-as logic
- Cookie flags, token lifetime, refresh/invalidation strategy
- OAuth callback handling and account-linking logic
- OTP throttling, hashing, replay prevention, cooldowns
- Webhook verification and fail-open behavior
- Secret defaults, placeholder acceptance, env precedence
- Third-party export of financial or personal data

## Infrastructure Checks

- Health endpoint validates dependencies or only process liveness
- Scheduler singleton guarantees across workers/replicas
- Multi-worker rate limiting consistency
- Reverse-proxy assumptions documented and enforced
- DB exposure in prod vs dev
- Backup/restore and secret rotation guidance
- Retry, timeout, and idempotency behavior for external providers

## Dependency Currency

Check only the most central pieces:

- main runtime
- backend framework
- frontend runtime/framework
- auth/security library
- 1-2 critical financial integrations

Use official release/support pages whenever possible.
