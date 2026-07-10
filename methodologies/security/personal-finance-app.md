---
name: security-personal-finance-app
description: Repo-specific cybersecurity and infrastructure audit for personal-finance-app, bundled inside the audit router.
---

# Cybersecurity And Infrastructure Auditor

Run a repo-grounded audit focused on exploitability, blast radius, and
production failure modes for the `personal-finance-app` monorepo.

## Scope

Always inspect:

- auth, session, cookie, OAuth, OTP, admin impersonation, webhook, and demo-entry flows
- Docker Compose, Caddy or reverse-proxy assumptions, env loading, secret handling
- schedulers, background jobs, cron-like tasks, cache, DB, health/readiness behavior
- Stripe, Powens, Enable Banking, and any connector moving financial data
- dependency/runtime currency for the main runtime, framework, auth stack, and critical integrations

Tag statements as `Observed`, `Inferred`, or `Not verifiable from repo`.

## Workflow

1. Inventory the stack and trust boundaries.
2. Read runtime-defining files, not just README text.
3. Search for auth, secrets, cookies, CORS, webhook auth, demo switches, schedulers, external HTTP calls, and health checks.
4. Check whether production safeguards fail closed or fail open.
5. Identify the highest-impact findings first:
   - unauthenticated entry points
   - insecure defaults or dangerous prod toggles
   - duplicated schedulers or background jobs
   - weak secret handling
   - third-party data exfiltration risks
   - missing dependency/readiness checks
6. Verify runtime currency online using primary sources only.
7. Return a severity-ordered report with concrete file references and remediation steps.

## Recommended commands

```bash
rg --files .
rg -n "SECRET|TOKEN|PASSWORD|KEY|CORS|COOKIE|JWT|OTP|OAUTH|WEBHOOK|ALLOW_PUBLIC_DEMO|self_registration" .
rg -n "scheduler|BackgroundScheduler|cron|celery|rq|apscheduler|health|readiness|liveness" .
rg -n "httpx|requests|fetch\\(|axios|stripe|powens|enablebanking|googleapis|webhook" .
rg -n "SessionMiddleware|CORSMiddleware|set_cookie|Authorization|Bearer|SameSite|Secure|HttpOnly" backend frontend
```

Use the bundled checklist when needed:

- `methodologies/security/references/checklist.md`
- `methodologies/dd/references/fintech-rules-checklist.md`

## Output contract

Findings come first, ordered by severity. Each finding should include:

- severity
- why it matters
- evidence with repo path and line
- exploit or failure scenario
- remediation

Then provide:

- concise overall risk summary
- dependency/runtime currency summary with dates
- residual unknowns
- prioritized remediation backlog

## Standard

- Prefer fewer high-confidence findings over many speculative ones.
- Treat fintech-style data paths as high sensitivity.
- Distinguish code risk from deployment risk.
- Call out intentionally risky features protected only by configuration.
