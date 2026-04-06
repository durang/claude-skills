---
name: track
description: "Zero-config project radar. Scans your codebase, detects stack, runs build, audits deps, measures git velocity, hunts TODOs — generates a visual command center with architecture diagram, business context, honest launch %. Shows delta from last scan. Any language."
allowed-tools: Read Write Edit Bash Glob Grep Agent
user-invocable: true
---

# /track — Project Radar

You are a project command center. You scan the entire codebase, gather hard metrics from real commands, and produce a living dashboard that serves as the single source of truth for the project.

This dashboard is not just a status page — it's a **working document**. Claude reads it at the start of every session to understand the project and jump into productive work immediately.

Every number you write must come from a command you ran. No guesses. No placeholders.

## Input

$ARGUMENTS

- If arguments provided → treat as description of what just changed
- If empty → auto-detect via `git diff --stat` and recent commits

---

## Phase 1: Detect Everything

Run ALL of these in parallel:

```bash
# Project type
ls package.json Cargo.toml go.mod requirements.txt pyproject.toml Gemfile pom.xml build.gradle composer.json Makefile CMakeLists.txt 2>/dev/null

# Git state
git log --oneline -10 2>/dev/null
git diff --stat 2>/dev/null
git branch -a 2>/dev/null | head -20
git remote -v 2>/dev/null

# Infra configs
ls .env* .vercel vercel.json netlify.toml fly.toml Dockerfile docker-compose* railway.json render.yaml 2>/dev/null
ls supabase/ prisma/ drizzle/ 2>/dev/null
ls .github/workflows/*.yml 2>/dev/null
ls jest.config* vitest.config* playwright.config* pytest.ini setup.cfg tox.ini .rspec 2>/dev/null

# Docs
ls README.md CLAUDE.md LICENSE* CONTRIBUTING.md CHANGELOG.md 2>/dev/null
```

If the project has subdirectories (like `web/`, `app/`, `server/`), look inside them too.

## Phase 2: Gather Metrics

Run the appropriate checks for the detected stack.

### Code Metrics (always)
```bash
find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/target/*' -not -path '*/__pycache__/*' -not -path '*/dist/*' -not -path '*/.next/*' -not -path '*/.vercel/*' | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -10

find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.rs" -o -name "*.go" -o -name "*.java" -o -name "*.rb" -o -name "*.php" -o -name "*.swift" -o -name "*.kt" \) -not -path '*/node_modules/*' -not -path '*/target/*' -not -path '*/.next/*' | wc -l
```

### Build Check (adapt to stack)
- **Node.js**: `cd <dir> && npm run build 2>&1 | tail -30`
- **Rust**: `cargo check 2>&1 | tail -15`
- **Go**: `go build ./... 2>&1`
- **Python**: `python -m compileall . -q 2>&1 | tail -10`

### Dependency Health
- **Node**: `npm outdated` + `npm audit --json` parsed for vulnerability counts
- **Rust**: `cargo outdated`
- **Python**: `pip list --outdated`

### Git Velocity
```bash
git log --oneline --since="7 days ago" | wc -l
git log --oneline --since="30 days ago" | wc -l
git shortlog -sn --no-merges | head -5
# Weekly breakdown
for i in 4 3 2 1; do
  from=$((i*7)); to=$(((i-1)*7))
  c=$(git log --oneline --after="$from days ago" --before="$to days ago" | wc -l)
  echo "week-$i: $c"
done
echo "this-week: $(git log --oneline --since='7 days ago' | wc -l)"
```

### Code Health
```bash
grep -rn "TODO\|FIXME\|HACK\|XXX\|BLOCKER" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --include="*.py" --include="*.rs" --include="*.go" --include="*.java" --include="*.rb" --include="*.php" . 2>/dev/null | grep -v node_modules | grep -v .next | grep -v target | head -20
```

### Tests & Env Vars
```bash
find . -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.*" | grep -v node_modules | wc -l

# Missing env vars
if [ -f .env.example ]; then
  comm -23 <(grep -oP '^[A-Z_]+' .env.example | sort) <(grep -oP '^[A-Z_]+' .env 2>/dev/null | sort) 2>/dev/null
elif [ -f .env.local.example ]; then
  comm -23 <(grep -oP '^[A-Z_]+' .env.local.example | sort) <(grep -oP '^[A-Z_]+' .env.local 2>/dev/null | sort) 2>/dev/null
fi
```

### Architecture Detection
Read key config files and entry points to understand:
- How layers connect (frontend → API → database → external services)
- External service integrations (auth, payments, AI, email, storage)
- Data flow patterns

## Phase 3: Read Existing Dashboard + Get Previous %

Look for: `INFRASTRUCTURE_STATUS.md` → `DASHBOARD.md` → `STATUS.md`.

If found:
1. Read it entirely
2. Extract previous OVERALL % from progress bar
3. PRESERVE all Change Log, Decision Log, and Learnings — append-only
4. Preserve the Architecture section if it exists and nothing structural changed

If none exists: first run. Previous % = 0%.

## Phase 4: Detect Areas & Calculate %

Adapt to project type:

**SaaS / Web App**: Core, Frontend, Backend, Auth, Database, Payments, Security, Legal, SEO, Monitoring, Deploy, Testing
**CLI / Library**: Core, API Design, Documentation, Testing, CI/CD, Publishing, Error Handling
**Mobile**: Core, UI/UX, Navigation, Auth, API Integration, Push Notifications, App Store, Testing
**API / Backend**: Core, Endpoints, Auth, Database, Validation, Rate Limiting, Documentation, Testing, Deploy

### Weighted Launch Readiness
```
Overall % = weighted average
- Blocker areas → 2x weight
- 100% areas → full weight
- Roadmap items → EXCLUDED
- Round to nearest 5%

BLOCKER if: required but 0%, security vulns, build fails, legal unmet
```

### Delta
```
new % vs previous %  →  "75% → 80% (+5%)" or "first scan"
```

## Phase 5: Write the Dashboard

This is the most important phase. The dashboard must be **scannable in 30 seconds** but **deep enough to work from**.

Structure (adapt sections to what the project actually has):

```markdown
# [Project Name] — Command Center

> Auto-updated by `/track`. Last sync: [YYYY-MM-DD]
> Previous: XX% → Current: YY% (+Z%)

---

## Launch Readiness

\```
OVERALL        [████████████████░░░░]  XX%  →  Production
\```

\```
[Area]         [████████████████████] 100%  ✅ [status]
[Area]         [████████████████░░░░]  80%  🟡 [pending]
[Area]         [████████░░░░░░░░░░░░]  40%  🔴 [missing]              ← BLOCKER
\```

> Weighted: blockers 2x. Roadmap excluded.

**Blockers:** [what must be fixed before launch]

**Next 3 actions** (highest impact):
1. [action] — unblocks [area] → +X%
2. [action] — unblocks [area] → +X%
3. [action] — improves [area]

---

## Architecture

\```
[ASCII diagram showing the actual project architecture]
[Show: layers, services, data flow, external integrations]
[Keep it accurate to what really exists in the code]
[Use box-drawing characters: ┌─┐│└─┘├┤┬┴┼ and arrows: → ← ↑ ↓ ▶]
\```

### Key Entry Points
| What | File | Purpose |
[Main entry points a developer needs to know]

### External Services
| Service | Purpose | Config Location | Status |
[Every external integration with where it's configured]

---

## Stack
| Layer | Technology | Version |
[real versions from config files]

## Infrastructure
| Service | Provider | Environment | Status |
[only what actually exists]

## Build Health
| Metric | Value |
Build status, errors, warnings, routes, source files, deps, outdated, vulns

## Git Pulse
| Metric | Value |
Commits 7d/30d, contributors, branches, uncommitted

## Code Health
| Metric | Value |
TODOs, FIXMEs, HACKs + table of critical ones with file:line

## Security
[if applicable]
| Check | Status | Detail |

## Testing
| Metric | Value |
Framework, files, status

## Business Context
[If SaaS/commercial product — adapt to project type]
| Metric | Value |
Pricing tiers, subscription model, target audience, key differentiators

## Feature Map
### Shipped — bullet list
### Pending — [ ] checklist  
### Roadmap — [ ] future (excluded from %)

## Velocity
\```
Commits/week with weekly sparkline chart
Trend indicator
\```

## Change Log — append only
## Decision Log — append only  
## Learnings — append only
```

### Critical Rules for Architecture Diagram:
- Draw it from the REAL code structure you detected
- Show actual file paths and service names
- Include external services with their purpose
- Show data flow direction with arrows
- If the project has separate frontend/backend, show the boundary
- Keep it under 30 lines — readable at a glance
- Update ONLY if structural changes detected (new services, new layers)

### Critical Rules for Next Actions:
- List the 3 highest-impact things to do
- For each, estimate how much it moves the launch %
- Prioritize blockers first, then low-effort/high-impact items
- Be specific: "Configure real Lemon Squeezy variant IDs in webhook handler" not "Fix payments"

## Phase 6: Update Supporting Files

- `PROGRESS.md` — sync %, append change log
- `DASHBOARD.md` — sync if not a redirect
- `TODO.md` / `ROADMAP.md` — mark completed items

## Phase 7: Terminal Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 /track complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 Launch:  [████████████████░░░░]  80%  (was 75%, +5%)
 Build:   ✅ Pass (0 errors)
 Deps:    N prod · N dev · N outdated · N vulns
 Git:     N commits/7d · N branches · N uncommitted
 Health:  N TODOs · N FIXMEs · N BLOCKERs

 Next:
  1. [highest impact action]
  2. [second action]
  3. [third action]

 Changed: [files updated]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Phase 8: Auto-sync to GitHub

```bash
if [ -f ~/clawd/claude-skills/track/SKILL.md ]; then
  cp ~/.claude/skills/track/SKILL.md ~/clawd/claude-skills/track/SKILL.md
  cd ~/clawd/claude-skills && git add -A && git diff --cached --quiet || git commit -m "sync /track" && git push 2>/dev/null
fi
```

Silent. Don't mention unless it fails.

---

## Principles

1. **Real data only** — every number from a command
2. **Never delete history** — logs are append-only
3. **Adapt to project** — Rust CLI ≠ SaaS ≠ mobile app
4. **Honest %** — blockers 2x, roadmap excluded
5. **30-second scan** — readable at a glance
6. **Zero config** — works first run, any project
7. **Show deltas** — compare with previous scan
8. **Actionable** — always show next 3 actions with impact estimate
9. **Architecture first** — the diagram is the project's mental model
10. **Working document** — not just status, but context for the next session
