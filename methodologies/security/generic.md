---
name: security-generic
description: Generic cybersecurity and infrastructure audit bundled inside the audit router.
---

# Cybersecurity And Infrastructure Auditor

Run a repo-grounded audit focused on exploitability, blast radius, and
production failure modes. Work only from evidence in the repository,
command output, and explicitly cited external sources for runtime/version
support status.

Resolve coverage and persistence first:

- follow `audit/reference/capability-protocol.md`
- follow `audit/reference/inventory-protocol.md`
- follow `audit/reference/coverage-protocol.md`
- follow `audit/reference/persistence-protocol.md`
- follow `audit/reference/evidence-protocol.md`
- follow `audit/reference/finding-schema.md`
- follow `audit/reference/output-contract.md`

## Scope

Always inspect:

- auth, session, cookie, OAuth, OTP, admin, webhook, and demo-entry flows
- Docker, compose, runtime images, reverse-proxy assumptions, env loading, secret handling
- schedulers, background jobs, cron-like tasks, queues, cache, DB, health/readiness behavior
- third-party connectors that move money or sensitive data
- dependency/runtime currency for the main runtime, main framework, auth stack, and up to 2 critical integrations

Tag statements as `Observed`, `Inferred`, or `Not verifiable from repo`.

## Workflow

1. Inventory the stack and trust boundaries.
2. Read runtime-defining files, not just README text.
3. Search for auth, secrets, cookies, CORS, webhook auth, demo switches, schedulers, external HTTP calls, and health checks.
4. Check whether production safeguards fail closed or fail open.
5. Identify the highest-impact findings first.
6. Verify runtime currency online using primary sources only.
7. Return a severity-ordered report with concrete file references and remediation steps.

## Recommended commands

```bash
rg --files .
rg -n "SECRET|TOKEN|PASSWORD|KEY|CORS|COOKIE|JWT|OTP|OAUTH|WEBHOOK|ALLOW_PUBLIC_DEMO|self_registration" .
rg -n "scheduler|BackgroundScheduler|cron|celery|rq|apscheduler|health|readiness|liveness" .
rg -n "httpx|requests|fetch\\(|axios|webhook|oauth|auth" .
rg -n "SessionMiddleware|CORSMiddleware|set_cookie|Authorization|Bearer|SameSite|Secure|HttpOnly" .
```

Before step 3, identify the target repo's actual auth library,
session/cookie mechanism, secret-loading approach, scheduler/queue
system, and sensitive third-party integrations. Adapt the grep patterns
to what the repo actually uses.

## Output

Follow `audit/reference/output-contract.md`.

Area-specific addendum:

- dependency/runtime currency summary with dates
- residual unknowns for runtime/deploy behavior

## Standard

- Prefer fewer high-confidence findings over many speculative ones.
- Distinguish code risk from deployment risk.
- Call out intentionally risky features protected only by configuration.
