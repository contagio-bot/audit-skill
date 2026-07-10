# Fintech Rules Checklist

Verificare ogni regola. Violazione = finding con severity appropriata.

| # | Regola | Come verificare | Severity tipica |
|---|--------|-----------------|-----------------|
| 1 | Mai float per importi | `rg '\bfloat\b' backend/app --glob '*.py'` | Major se amount |
| 2 | Ogni endpoint usa `effective_user_id` | Router dati utente devono usare `get_effective_user_id` | Critical se leak |
| 3 | Importer = pure functions | `importers/` no import DB/session | Major |
| 4 | Business logic in `domain/` | Router sottili, calcoli in `domain/calculations/` | Major |
| 5 | Formule testate | Ogni file calculations ha test con oracle | Major |
| 6 | Frontend non fa security | UI hide != authz | Minor |
| 7 | Backend valida sempre | Pydantic su input | Major |
| 8 | No business logic in React | Logica in hooks | Minor |
| 9 | Mutations via TanStack Query | No fetch diretti mutating | Minor |
| 10 | No localStorage dati sensibili | Token in httpOnly cookie | Critical |

## Check aggiuntivi produzione

- `COOKIE_SECURE=true` enforced in prod startup
- `REDIS_URL` obbligatoria in prod
- `OTP_HMAC_SECRET` diverso da `JWT_SECRET`
- demo pubblica protetta e non admin
- OpenAPI docs disabilitati in prod
- Postgres non esposto in compose prod
- scheduler isolato dal backend web

## Integrazioni finanziarie

- Stripe webhook: signature verify
- Powens webhook: bearer obbligatorio quando configurato
- Powens redirect URI allowlist
- Enable Banking: JWT/key handling
- Token bancari at rest: encryption o risk acceptance documentata
