# audit --profile

Create or update a repo-specific local audit profile inside this skill
package. Use this when a repository needs tuned grep patterns, preferred
commands, known false-positive suppressions, or a dedicated methodology
variant beyond the bundled generic one.

## Goal

Given a target repo:

1. Resolve its repo root.
2. Inspect the repo's conventions and stack.
3. Create or update `profiles/<repo-slug>.md`.
4. If the generic bundled methodologies are not enough, also create or
   update dedicated local methodology files under:
   - `methodologies/deadcode/<repo-slug>.md`
   - `methodologies/security/<repo-slug>.md`
   - `methodologies/dd/<repo-slug>.md` only if DD truly needs a
     repo-specific variant
5. Keep all paths relative to this `audit` package. Never point back to
   `~/.claude`, `~/.agents`, or an absolute path on disk.

## Profile workflow

### 1. Discover repo identity

Read the minimum set of files that explains the repo:

- `CLAUDE.md`, `PROJECT.md`, `README*`, `package.json`,
  `pyproject.toml`, `docker-compose*.yml`, top-level app directories
- any existing `AUDIT-CONTEXT.md`

Extract:

- repo name / slug
- path markers worth matching
- package or project names
- major frameworks, runtimes, DB, queue/scheduler, auth stack
- repo-local scripts the audits should prefer
- conventions that would change audit interpretation

### 2. Create or update the profile file

Use this structure:

```markdown
# Audit Profile: <repo name>

## Match rules
- Repo name: `<name>`
- Root path contains: `<fragment>` or `none`
- Marker files: `<paths>` or `none`
- Package/project identifiers: `<names>` or `none`

## Methodology selection
- Deadcode: `methodologies/deadcode/<file>.md`
- Architecture: `methodologies/arch/SKILL.md`
- Security: `methodologies/security/<file>.md`
- Due diligence: `methodologies/dd/SKILL.md` or a dedicated `<file>.md`

## Repo conventions
- <short bullets>

## Preferred audit commands
- <repo-specific scripts first, then fallback tools>

## Known false positives / intentional patterns
- <short bullets>

## High-sensitivity areas
- <short bullets>

## Extra checks to add
- <short bullets>
```

Keep it short and operational. The profile is not a second methodology;
it is a selector plus a delta.

### 3. Decide whether dedicated methodologies are needed

Create dedicated local methodology files only when the repo truly needs
repo-specific instructions that would be noisy or misleading in the
generic flow. Good reasons:

- project-provided audit scripts should replace generic commands
- framework-driven false positives are predictable and recurring
- the repo has domain-specific hot spots worth prioritizing
- the security audit needs custom grep patterns for its trust boundaries

If the generic methodology already works, point the profile to it instead
of forking instructions unnecessarily.

### 4. Wire it into the router

The router and per-command references already know to look inside
`profiles/`. You only need to ensure the new profile states the correct
methodology file names and match rules clearly enough for the model to
pick it.

## Example

`personal-finance-app` is the model:

- `profiles/personal-finance-app.md`
- `methodologies/deadcode/personal-finance-app.md`
- `methodologies/security/personal-finance-app.md`

Use that shape for future repos unless there is a better reason not to.
