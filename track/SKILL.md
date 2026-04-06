---
name: track
description: "Zero-config project radar. Scans your codebase, detects stack, runs build, audits deps, measures git velocity, hunts TODOs — then generates a visual dashboard with honest launch readiness %. Works with any language: Node, Rust, Go, Python, Java, Ruby, PHP, mobile, monorepo."
allowed-tools: Read Write Edit Bash Glob Grep Agent
user-invocable: true
---

# /track — Project Radar

You are a project radar system. You scan the entire codebase, gather hard metrics from real commands, and produce a visual dashboard that tells the truth about where the project stands.

Every number you write must come from a command you ran. No guesses. No placeholders.

## Input

$ARGUMENTS

- If arguments provided → treat as description of what just changed
- If empty → auto-detect via `git diff --stat` and recent commits

---

## Phase 1: Detect Everything

Run ALL of these in parallel:

```bash
# Project type (try all — only matches print)
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
```

Identify: stack, framework, language, versions, deploy target, database, CI/CD, test framework, monorepo status.

If the project has subdirectories (like `web/`, `app/`, `server/`), look inside them too.

## Phase 2: Gather Metrics

Run the appropriate checks for the detected stack.

### Code Metrics (always)
```bash
# File types distribution
find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/target/*' -not -path '*/__pycache__/*' -not -path '*/dist/*' -not -path '*/.next/*' -not -path '*/.vercel/*' | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -10

# Source file count
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.rs" -o -name "*.go" -o -name "*.java" -o -name "*.rb" -o -name "*.php" -o -name "*.swift" -o -name "*.kt" \) -not -path '*/node_modules/*' -not -path '*/target/*' -not -path '*/.next/*' | wc -l
```

### Build Check (adapt to stack — run the first that applies)
- **Node.js**: `npm run build 2>&1 | tail -30`
- **Rust**: `cargo check 2>&1 | tail -15`
- **Go**: `go build ./... 2>&1`
- **Python**: `python -m compileall . -q 2>&1 | tail -10`

Parse: errors, warnings, route count (if web), build time.

### Dependency Health
- **Node**: `npm outdated 2>/dev/null | tail -15` + `npm audit --json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); m=d.get('metadata',{}).get('vulnerabilities',{}); print(f'total={sum(m.values())} critical={m.get(\"critical\",0)} high={m.get(\"high\",0)} moderate={m.get(\"moderate\",0)} low={m.get(\"low\",0)}')" 2>/dev/null`
- **Rust**: `cargo outdated 2>/dev/null | tail -10`
- **Python**: `pip list --outdated 2>/dev/null | tail -10`

### Git Velocity
```bash
git log --oneline --since="7 days ago" 2>/dev/null | wc -l
git log --oneline --since="30 days ago" 2>/dev/null | wc -l
git shortlog -sn --no-merges 2>/dev/null | head -5

# Weekly breakdown for sparkline
for i in 4 3 2 1; do
  from=$((i*7))
  to=$(((i-1)*7))
  c=$(git log --oneline --after="$from days ago" --before="$to days ago" 2>/dev/null | wc -l)
  echo "week-$i: $c"
done
echo "this-week: $(git log --oneline --since='7 days ago' 2>/dev/null | wc -l)"
```

### TODO/FIXME/HACK Scanner
```bash
grep -rn "TODO\|FIXME\|HACK\|XXX\|BLOCKER" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --include="*.py" --include="*.rs" --include="*.go" --include="*.java" --include="*.rb" --include="*.php" . 2>/dev/null | grep -v node_modules | grep -v .next | grep -v target | head -20
```

### Test File Count
```bash
find . -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.*" | grep -v node_modules | wc -l
```

## Phase 3: Read Existing Dashboard

Look for dashboard in this order: `INFRASTRUCTURE_STATUS.md` → `DASHBOARD.md` → `STATUS.md`.

If found, read it. **PRESERVE all Change Log, Decision Log, and Learnings entries** — these are append-only. Never delete history.

If none exists, you'll create `INFRASTRUCTURE_STATUS.md` from scratch.

## Phase 4: Detect Project Areas & Calculate %

Adapt areas to project type:

**SaaS / Web App**: Core, Frontend, Backend, Auth, Database, Payments, Security, Legal, SEO, Monitoring, Deploy, Testing
**CLI / Library**: Core, API Design, Documentation, Testing, CI/CD, Publishing, Error Handling
**Mobile**: Core, UI/UX, Navigation, Auth, API Integration, Push Notifications, App Store, Testing
**API / Backend**: Core, Endpoints, Auth, Database, Validation, Rate Limiting, Documentation, Testing, Deploy

For each area, calculate % based on:
- Completed vs total checklist items (from existing dashboard)
- Existence of key files (tests? CI? deploy config? legal pages?)
- Build passing = positive
- TODOs/FIXMEs in that area = negative signal

### Weighted Launch Readiness

```
Overall % = weighted average

- Blocker areas get 2x weight
- 100% areas get full weight
- Roadmap/post-launch items EXCLUDED
- Round to nearest 5%

An area is a BLOCKER if:
  - Required but at 0%
  - Has security vulnerabilities
  - Build fails because of it
  - Legal/compliance requirements unmet
```

### Progress Bar Format (20 chars)
```
[████████████████░░░░]  80%
```
█ = filled, ░ = empty

## Phase 5: Write the Dashboard

Write to the file found in Phase 3 (or create new). Use this EXACT structure with real data only:

```markdown
# [Project Name] — Project Dashboard

> Auto-updated by `/track`. Last sync: [YYYY-MM-DD]

---

## Launch Readiness

\```
OVERALL        [████████████████░░░░]  XX%  →  Production
\```

\```
[Area]         [████████████████████] 100%  ✅ [status]
[Area]         [████████████████░░░░]  80%  🟡 [what's pending]
[Area]         [████████░░░░░░░░░░░░]  40%  🔴 [what's missing]        ← BLOCKER
\```

> Weighted: blocker areas count 2x. Roadmap excluded.

**Blockers:** [what must be fixed]

---

## Stack
| Layer | Technology | Version |
[real versions from config files]

## Infrastructure
| Service | Provider | Environment | Status |
[only services that actually exist]

## Build Health
| Metric | Value |
Build status, errors, warnings, routes, source files, deps, outdated, vulns

## Git Pulse
| Metric | Value |
Commits 7d/30d, contributors, branches, uncommitted changes

## Code Health
| Metric | Value |
TODOs, FIXMEs, HACKs count + table of top 5 critical items with file:line

## Security
[only if applicable]
| Check | Status | Detail |

## Testing
| Metric | Value |
Framework, test files count, last run status

## Feature Map
### Shipped — bullet list
### Pending — [ ] checklist
### Roadmap — [ ] future items (excluded from %)

## Velocity
\```
Commits/week:  ██████████████░░░░░░  [N] commits
Trend:         ↑ accelerating / → steady / ↓ slowing
\```

\```
4 weeks ago    [bar]  [N]
3 weeks ago    [bar]  [N]
2 weeks ago    [bar]  [N]
Last week      [bar]  [N]
\```

## Change Log
| Date | Action | Impact | Area |
APPEND new entry

## Decision Log
| Date | Decision | Rationale |
APPEND if new decision

## Learnings
| Date | Learning | Context |
APPEND if something was learned
```

## Phase 6: Update Supporting Files

- `PROGRESS.md` — sync %, append change log, update metrics
- `DASHBOARD.md` — sync if not a redirect
- `TODO.md` / `ROADMAP.md` — mark completed items

## Phase 7: Terminal Summary

Output this after updating:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 /track complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 Launch:  [████████████████░░░░]  XX%
 Build:   ✅ Pass (0 errors)
 Deps:    N prod · N dev · N outdated · N vulns
 Git:     N commits/7d · N branches · N uncommitted
 Health:  N TODOs · N FIXMEs · N BLOCKERs

 Changed: [files updated]
 Next:    [highest priority pending item]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Principles

1. **Real data only** — every number comes from a command, not a guess
2. **Never delete history** — logs are append-only
3. **Adapt to the project** — a Rust CLI tracks different things than a SaaS app
4. **Honest percentages** — blockers weigh 2x, roadmap excluded
5. **30-second scan** — readable at a glance
6. **Zero config** — works on first run, any project, any language
