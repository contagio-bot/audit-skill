# Investigation Protocol — 10 Fasi

## Fase 1 — Reconnaissance

Mappa stack, dimensione, maturita.

Checklist:

- Linguaggi, framework, DB, cache, reverse proxy
- Numero router, service, migration, test
- Presenza CI/CD, Makefile, deploy docs
- Stato git e commit recenti
- Documenti strategici

## Fase 2 — Architecture & Domain

Valuta separazione concern, modello dominio, coesione.

Checklist:

- layering rispettato
- domain/calculations con funzioni pure e test
- aggregati e bounded contexts identificabili
- duplicazione service/repository
- feature flags e plan guards coerenti

Rating DDD 0-10 o N/A.

## Fase 3 — Database & Data Modeling

Checklist:

- FK e ON DELETE coerenti
- indici su lookup frequenti
- UNIQUE su natural keys
- nullable giustificati
- importi monetari come interi in centesimi
- migration reversibility e drift schema

## Fase 4 — Security

Checklist critica:

- cookie HttpOnly, Secure, SameSite in prod
- JWT secret strength e invalidazione
- OTP throttling e segreti separati
- admin impersonation fail-closed
- filtri `user_id` sugli endpoint dati utente
- webhook verificati
- OAuth redirect allowlist
- rate limit su auth/import/webhook
- secrets at rest e nella git history
- CORS ristretto in prod
- startup safety checks coprono i toggle pericolosi

Subagent full-repo obbligatorio (`general-purpose`, non diff-only).

## Fase 5 — Dependency & Runtime Currency

Verifica solo i componenti centrali:

1. runtime backend
2. runtime frontend
3. framework backend
4. framework frontend
5. auth lib
6. 1-2 integrazioni critiche

Esegui anche uno scan CVE noto (`pip-audit` / `npm audit` o equivalente).

**Night report (standard Magellano):** subito dopo l’analisi deps/CVE, esegui
la pipeline operativa equivalente a **`audit night-report`**:

1. Se esiste `scripts/nightly-audit/run.sh`, segui
   `methodologies/night-report/SKILL.md` con **`AUDIT_MAIL_DRY=1`**
   (mai invio SMTP in DD salvo richiesta esplicita).
2. Registra nel finding set della fase: **overall** OK/WARN/FAIL/ERROR,
   tabella da `checks.tsv`, exit code, path assoluto della run dir,
   eventuali allowlist (`accepted-deps.json`) rilevanti.
3. **FAIL/ERROR su deps** in night-report → almeno **Major** in DD
   (allineato a CVE operativi); **WARN** → Minor o nota in accepted risk
   se già in `AUDIT-CONTEXT.md`.
4. Se **`scripts/nightly-audit/` assente** → finding **Minor**:
   manca il monitoraggio notturno standard; raccomandare bootstrap da
   repo Magellano (bridge-jtt / click2job / track-feed template).

Il night-report **non sostituisce** i punti 1–6 e lo scan CVE della fase:
valida che il checkout passerebbe i controlli cron EC2 (Docker + lockfile).

## Fase 6 — Performance & Scalability

Checklist:

- paginazione bounded
- cache/materialized views
- scheduler separato dai worker web
- rate limit coerente multi-worker
- job async vs sync sui percorsi caldi

## Fase 7 — Code Quality & Patterns

- repository pattern consistente
- importers puri
- duplicazione
- type safety frontend

## Fase 8 — Testability & Testing

- unit test del dominio
- integration test auth/plan guard
- frontend test aree critiche
- e2e presence
- test rotti = blocker

## Fase 9 — Bug Risks & Robustness

- transaction boundaries
- idempotency import/webhook
- scheduler concurrency
- silent failures
- validation coverage
- edge case finanziari

## Fase 10 — Documentation & Operability

- README onboarding
- deploy docs
- backup/restore
- architecture doc
- gap doc vs codice

## Risk rating definitions

| Label | Criterio |
|-------|----------|
| Critical | Exploit o perdita dati probabile, fix immediato |
| Major | Rischio significativo pre-pilot o pre-scale |
| Minor | Debito gestibile, fix pianificabile |
| Nice-to-have | Miglioramento qualità |
