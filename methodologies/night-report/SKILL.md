---
name: night-report-local
description: Run and interpret scripts/nightly-audit (Magellano nightly CLI pipeline).
license: MIT
---

# Night report (nightly-audit runner)

Resolve first (same as other audit commands):

- `audit/reference/bootstrap-lite.md`
- `audit/reference/persistence-protocol.md`
- `audit/reference/context-protocol.md` if `AUDIT-CONTEXT.md` exists

**Default persistence:** `read-only` — execute checks, summarize, do not
modify the target repo unless the user passed `--persist` or explicitly
asked to record results.

## Goal

1. Detect whether the target repo ships **`scripts/nightly-audit/`**.
2. Run the pipeline **safely** (no production email, no code changes).
3. Map results to **OK / WARN / FAIL / ERROR** per check and overall.
4. Tell the user what to fix and whether to run full **`audit deps`** /
   **`audit deadcode`** next.

## What this replicates

Magellano “nightly CLI audit” (Flavio Lombardi / team):

| Repo flavor | Deps check | Other checks (typical) |
|-------------|------------|-------------------------|
| **Node monorepo** (click2job) | `checks/deps_npm_audit.sh` — `npm audit --package-lock-only` in `node:22-alpine`, clean temp dir per workspace | knip@5, jscpd, large files (WARN) |
| **Python** (bridge-jtt, track-feed-new) | `checks/deps_pip_audit.sh` — `pip-audit -r requirements.lock` in `python:3.12-slim`, Docker `--network=host` by default | ruff F401/F841 (WARN), optional jscpd |

**Email:** Mandrill only on FAIL/ERROR by default. Agent runs must set
**`AUDIT_MAIL_DRY=1`** always unless the user explicitly requests a live
send (almost never).

**Read-only on deployed tree:** scripts do not `git pull` or patch code.

## Workflow

### 1. Inventory

From repo root, verify:

```text
scripts/nightly-audit/run.sh
scripts/nightly-audit/README.md
scripts/nightly-audit/lib/status.sh
scripts/nightly-audit/checks/
```

Classify flavor:

- **`deps_npm_audit.sh` present** → Node (`AUDIT_REPO_ALIAS` often `click2job`).
- **`deps_pip_audit.sh` present** → Python; lock path is usually
  `requirements.lock` (bridge-jtt root) or `backend/requirements.lock`
  (track-feed — script still expects `REPO_ROOT/requirements.lock` OR
  read README for that repo’s layout).

Read **`scripts/nightly-audit/README.md`** in the target repo for EC2
paths, secrets, and repo-specific env vars.

If the tree is **missing**, stop with a clear finding and offer bootstrap
(see § Bootstrap).

### 2. Capabilities

Prefer **Docker** (matches production). Record in the capability manifest:

| Tool | Role |
|------|------|
| `docker` | Node/Python audit containers |
| `python3` | Aggregator in `deps_npm_audit.sh`, `mail_mandrill.py` |
| `bash` | Entrypoint |
| `flock` | Single-instance lock in `run.sh` (often **missing on macOS**) |
| `npm` / `npx` | Only if `AUDIT_ALLOW_HOST_TOOLS=1` |

Network: **required** for `pip-audit` / registry-backed audit (unless
using pre-pulled images only — still needs PyPI/npm metadata fetch).

### 3. Safe execution

Set at minimum:

```bash
export TZ=Europe/Rome
export AUDIT_MAIL_DRY=1
export AUDIT_LOG_ROOT="${AUDIT_LOG_ROOT:-/tmp/magellano-audit/<repo-alias>}"
```

Optional speed / laptop toggles (document in report if used):

```bash
export AUDIT_KNIP=0          # skip knip if no node_modules / slow
export AUDIT_JSCPD=0
export AUDIT_LARGE_FILES=0
export AUDIT_ALLOW_HOST_TOOLS=1   # no Docker — weaker parity with prod
export AUDIT_SKIP_DOTENV=1      # avoid sourcing prod .env on laptop
```

**Run full pipeline:**

```bash
cd <repo-root>
./scripts/nightly-audit/run.sh
echo "exit=$?"
```

**If `flock` is missing or lock fails** (common on Mac): do not treat as
CVE FAIL. Re-run checks individually with the same exports `run.sh` sets:

```bash
export AUDIT_REPO_ROOT="<repo-root>"
export AUDIT_RUN_DIR="${AUDIT_LOG_ROOT}/$(date +%Y-%m-%d)"
mkdir -p "$AUDIT_RUN_DIR"
bash scripts/nightly-audit/checks/deps_npm_audit.sh   # or deps_pip_audit.sh
# … other checks listed in README …
```

Then compute overall status with the same ranking as `lib/status.sh`:

- Python repos: **ERROR > FAIL > WARN > OK**
- Node repos: **FAIL > WARN > OK** (no ERROR tier on deps unless wrapper fails)

### 4. Interpret results

Primary artifacts (under `AUDIT_RUN_DIR`):

- `checks.tsv` — `name|status|summary`
- `*.status` — per-check status
- `run-*.log`, `deps-*.log`, `email-body.txt`

**Deps — Node (`deps_npm_audit.sh`):**

- Scans: `web`, `api`, `worker`, `italia-spa` (paths in script).
- **FAIL:** high/critical not listed in `accepted-deps.json`.
- **WARN:** only allowlisted highs (e.g. `braces` / GHSA via eslint chain).
- **OK:** no actionable high/critical.
- Allowlist edits are **judgment** → only with `--persist` + user OK.

**Deps — Python (`deps_pip_audit.sh`):**

- **FAIL:** CVE markers in log (`GHSA-`, `CVE-`, …).
- **ERROR:** DNS/PyPI/install failures (`is_pip_infra_failure`) — not the
  same as “vulnerable”; retry on EC2 or fix network.
- **OK:** `pip-audit` rc 0.

**Non-deps checks:** usually **WARN** on findings; treat **ERROR** as
infra (ruff/knip/jscpd failed to install/run).

Exit codes from `run.sh`:

- `0` — OK or WARN finished
- `1` — FAIL (actionable, e.g. CVE)
- `2` — infra (lock, mail, missing docker)

### 5. Cross-link with `/audit`

| night-report | Follow-up |
|--------------|-----------|
| deps **FAIL** | Run **`audit deps --persist`** (or continue remediation); compare with `accepted-deps.json` |
| deps **OK** but last `audit deps` was bad | Likely remediated — suggest updating `AUDIT-CONTEXT.md` run-log |
| deadcode **WARN** | Optional **`audit deadcode`** for human triage |
| **ERROR** on Python deps | Fix Docker network / run on EC2; do not bump packages blindly |

### 6. Output (standard audit shape)

Use the **standard 4-section** report from `bootstrap-lite.md` unless the
user asked for `--formal`:

1. **Executive summary** — overall status, deps highlight, infra limits.
2. **Scope** — repo root, flavor, checks enabled/skipped, Docker vs host.
3. **Evidence** — commands, exit codes, path to log dir, `checks.tsv` table.
4. **Findings / next steps** — ordered by severity; explicit “no repo writes”.

With **`--persist`**, also:

- Write `docs/audit/YYYY-MM-DD-night-report.md` (same content).
- Append one line to **`AUDIT-CONTEXT.md` → Run log**:
  `night-report run YYYY-MM-DD. Overall: … Coverage: nightly-audit v1. …`
  (confirm with user if context write policy requires it.)

Do **not** commit `accepted-deps.json` changes without explicit user request.

## Bootstrap (when scripts are missing)

Canonical copies live in Magellano private repos (same team layout):

- `bridge-jtt/scripts/nightly-audit/` — Python template + `cleanup_logs.sh`
- `click2job/scripts/nightly-audit/` — Node template + `accepted-deps.json`
- `track-feed-new/scripts/nightly-audit/` — Python (lock under `backend/`)

Bootstrap steps for the agent (only if user asks to install):

1. Copy the matching tree into `scripts/nightly-audit/`.
2. Adjust README paths/alias and lockfile location.
3. Ensure `requirements.lock` exists for Python Docker builds.
4. Dry-run with `AUDIT_MAIL_DRY=1`.

## Environment cheat sheet

| Variable | Effect |
|----------|--------|
| `AUDIT_MAIL_DRY=1` | Never SMTP; print body when mail would send |
| `AUDIT_MAIL_ALWAYS=1` | Heartbeat on OK/WARN (avoid in agent runs) |
| `AUDIT_LOG_ROOT` | Log directory (default `/var/log/magellano-audit/…` on EC2) |
| `AUDIT_ALLOW_HOST_TOOLS=1` | Host npm/pip instead of Docker |
| `AUDIT_DOCKER_NETWORK` | Default `host` on Python (Bridge EC2) |
| `AUDIT_NODE_IMAGE` | Default `node:22-alpine` |
| `AUDIT_PYTHON_IMAGE` | Default `python:3.12-slim` |
| `AUDIT_ACCEPTED_DEPS` | Path to allowlist JSON (Node) |
| `AUDIT_SKIP_DOTENV=1` | Do not source repo `.env` |

## Limits

- Does not replace CI gates in `buildspec.yml` unless the user adds them.
- knip needs `node_modules` unless `AUDIT_KNIP_INSTALL=1` (slow).
- `npm audit --package-lock-only` ≠ full `npm audit --omit=dev` in tree;
  intentional for reproducibility and web `extraneous` workaround.
- macOS lacks `flock` → use per-check invocation or Linux/EC2 for parity.
