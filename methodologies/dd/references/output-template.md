# Output Template — tech-dd-report.md

Usare questa struttura verbatim nel report finale.

## 0. Deal context

- **Target**: `<repo/path>`
- **Purpose**: `<investment | M&A | pilot | internal | vendor>`
- **Date**: `<ISO date>`
- **Scope**: `<full repo | path>`

## 1. Executive summary

| Campo | Valore |
|-------|--------|
| Linguaggi | |
| Database / cache | |
| Deploy | |
| Stile architetturale | |

Includi:

- punti di forza
- preoccupazioni
- top 3-5 rischi
- verdetto one-liner

## 2. Evidence & method

Includi:

- commands / tools used
- evidence tags
- excluded areas
- repository coverage

## 3. Detailed findings

Per ciascuna delle 10 categorie:

- rating
- verdict
- key strengths
- key issues con file:line
- concrete recommendations

## 4. Security findings table

| Severity | Location | Finding | Remediation |
|----------|----------|---------|-------------|

## 5. Doc vs code gaps

| Documento | Afferma | Codice | Gap |
|-----------|---------|--------|-----|

## 6. Top 5 prioritized recommendations

Per item:

- title
- short explanation
- impact
- effort

## 7. Scorecard

| Category | Rating (0–10) | One-line comment |
|----------|---------------|------------------|

Indica anche il rating complessivo e il denominatore.

## 8. Readiness matrix

| Fase | Verdetto | Blockers |
|------|----------|----------|
| Dev / solo founder | | |
| Pilot chiuso 100–500 | | |
| 2k–5k utenti | | |
| ~20k utenti | | |

## 9. Residual unknowns

Cosa non e verificabile dal repo.

## 10. Glossary

Opzionale, utile per audience non tecnica.
