---
name: track
description: "Project dashboard that auto-detects your stack, gathers real metrics, and maintains a visual status page. Works with any project — Node, Rust, Go, Python, mobile, monorepo. Run after changes to update progress, or with no args to scan current state."
allowed-tools: Read Write Edit Bash Glob Grep Agent
user-invocable: true
---

# /track — Project Dashboard Generator

You maintain a living project dashboard. You detect the tech stack, gather real metrics from the codebase, and produce a visual markdown status page that stays accurate over time.

## Input

$ARGUMENTS

If arguments are provided, treat them as a description of what just changed.
If empty, auto-detect changes via `git diff --stat` and recent commits.

---

## Phase 1: Detect Everything

Run ALL of these in parallel to understand the project fast:

```bash
# 1. Project type
ls package.json Cargo.toml go.mod requirements.txt pyproject.toml Gemfile pom.xml build.gradle composer.json Makefile CMakeLists.txt 2>/dev/null

# 2. Git state
git log --oneline -10 2>/dev/null
git diff --stat 2>/dev/null
git branch -a 2>/dev/null | head -20
git remote -v 2>/dev/null

# 3. Find config files
ls .env* .vercel vercel.json netlify.toml fly.toml Dockerfile docker-compose* railway.json render.yaml 2>/dev/null
ls supabase/ prisma/ drizzle/ 2>/dev/null
ls .github/workflows/*.yml 2>/dev/null
ls jest.config* vitest.config* playwright.config* pytest.ini setup.cfg tox.ini .rspec Cargo.toml 2>/dev/null
```

From results, identify:
- **Stack**: framework + language + version (read package.json / Cargo.toml / go.mod / etc.)
- **Deploy target**: Vercel / AWS / Docker / Fly / Netlify / Railway / self-hosted
- **Database**: Supabase / Prisma / Drizzle / raw SQL / MongoDB / Firebase / none
- **CI/CD**: GitHub Actions / GitLab CI / CircleCI / none
- **Testing**: Jest / Vitest / Playwright / pytest / cargo test / go test / none
- **Monorepo?**: Check for workspaces, turborepo, nx, lerna

## Phase 2: Gather Metrics

Run the appropriate checks based on what you detected. Always try the build.

### Code Metrics (always)
```bash
# File counts by extension (top 5 types)
find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/target/*' -not -path '*/__pycache__/*' -not -path '*/dist/*' -not -path '*/.next/*' | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -10

# Total source files (exclude deps/build)
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.rs" -o -name "*.go" -o -name "*.java" -o -name "*.rb" -o -name "*.php" -o -name "*.swift" -o -name "*.kt" \) -not -path '*/node_modules/*' -not -path '*/target/*' -not -path '*/.next/*' | wc -l
```

### Build Check (adapt to stack)
```bash
# Node.js
cd <project-dir> && npm run build 2>&1 | tail -30

# Rust
cargo check 2>&1 | tail -15

# Go
go build ./... 2>&1

# Python
python -m compileall . -q 2>&1 | tail -10
```

Parse build output for:
- **Errors**: count them
- **Warnings**: count them
- **Routes/endpoints**: count if web framework
- **Build time**: extract if shown

### Dependency Health
```bash
# Node: outdated + audit
npm outdated 2>/dev/null | tail -10
npm audit --json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Vulnerabilities: {d.get(\"metadata\",{}).get(\"vulnerabilities\",{})}')" 2>/dev/null

# Rust
cargo outdated 2>/dev/null | tail -10

# Python
pip list --outdated 2>/dev/null | tail -10
```

### Git Velocity
```bash
# Commits last 7 days
git log --oneline --since="7 days ago" 2>/dev/null | wc -l

# Commits last 30 days
git log --oneline --since="30 days ago" 2>/dev/null | wc -l

# Contributors
git shortlog -sn --no-merges 2>/dev/null | head -5
```

### TODO/FIXME/HACK Scanner
```bash
grep -rn "TODO\|FIXME\|HACK\|XXX\|BLOCKER" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.py" --include="*.rs" --include="*.go" --include="*.java" --include="*.rb" . 2>/dev/null | grep -v node_modules | grep -v .next | head -20
```

### Test Status (if test command exists)
Try to run tests, but with a short timeout. If they take too long, just report the test file count.

## Phase 3: Read or Create Dashboard

Look for the dashboard file in this order:
1. `INFRASTRUCTURE_STATUS.md`
2. `DASHBOARD.md`
3. `STATUS.md`
4. If none exist, create `INFRASTRUCTURE_STATUS.md`

Read the existing file to preserve Change Log, Decision Log, and Learnings (NEVER delete history).

## Phase 4: Detect Project Areas

Based on what you found, identify the relevant tracking areas. NOT every project needs the same areas. Adapt:

**SaaS / Web App:**
Core, Frontend, Backend, API, Auth, Database, Payments, Security, Legal, SEO, Monitoring, Deploy, Testing

**CLI Tool / Library:**
Core, API Design, Documentation, Testing, CI/CD, Publishing, Error Handling

**Mobile App:**
Core, UI/UX, Navigation, Auth, API Integration, Push Notifications, App Store, Testing, Analytics

**API / Backend:**
Core, Endpoints, Auth, Database, Validation, Rate Limiting, Documentation, Testing, Deploy, Monitoring

**Monorepo:**
Per-package status + overall health

For each area, calculate % based on:
- Completed checklist items vs total
- Existence of key files (e.g., has tests? has CI? has deploy config?)
- Build passing = positive signal
- TODOs/FIXMEs in that area = negative signal

## Phase 5: Calculate Launch Readiness

```
Overall % = weighted average of all areas

Rules:
- Blocker areas get 2x weight
- Areas at 100% contribute full weight  
- Post-launch/roadmap items are EXCLUDED from %
- Round to nearest 5%
```

An area is a BLOCKER if:
- It's required but at 0% (e.g., no tests, no deploy config)
- It contains security vulnerabilities
- It prevents the app from running (build fails, missing env vars)
- It has legal/compliance requirements unmet

## Phase 6: Write the Dashboard

Use this exact structure. Every section must have real data from Phase 2 — no placeholders, no guesses.

```markdown
# [Project Name] — Project Dashboard

> Auto-updated by `/track`. Last sync: [YYYY-MM-DD]

---

## Launch Readiness

\```
OVERALL        [████████████████░░░░]  80%  →  Production
\```

\```
[Area Name]    [████████████████████] 100%  ✅ [one-line status]
[Area Name]    [████████████████░░░░]  80%  🟡 [what's pending]
[Area Name]    [████████░░░░░░░░░░░░]  40%  🔴 [what's missing]        ← BLOCKER
\```

> Weighted: blocker areas count 2x. Roadmap items excluded.

**Blockers:** [list what must be fixed before launch]

---

## Stack

| Layer | Technology | Version |
|-------|-----------|---------|
[detected from package.json / Cargo.toml / etc — real versions only]

---

## Infrastructure

| Service | Provider | Environment | Status |
|---------|----------|-------------|--------|
[detected from config files — only show what actually exists]

---

## Build Health

| Metric | Value |
|--------|-------|
| Build status | ✅ Pass / 🔴 Fail |
| Errors | [count] |
| Warnings | [count] |
| Routes/Endpoints | [count if web app] |
| Source files | [count] |
| Dependencies | [prod] + [dev] |
| Outdated deps | [count] |
| Vulnerabilities | [count from audit] |

---

## Git Pulse

| Metric | Value |
|--------|-------|
| Commits (7d) | [count] |
| Commits (30d) | [count] |
| Contributors | [count] |
| Open branches | [count] |
| Uncommitted changes | [count files] |

---

## Code Health

| Metric | Value |
|--------|-------|
| TODOs | [count] |
| FIXMEs | [count] |
| HACKs | [count] |

[If any critical ones, list them:]
| File | Line | Note |
|------|------|------|
[top 5 most critical TODOs/FIXMEs]

---

## Security

[Only include if the project has security-relevant code]

| Check | Status |
|-------|--------|
[security headers, auth, rate limiting, input validation, etc.]

---

## Testing

| Metric | Value |
|--------|-------|
| Test framework | [detected] |
| Test files | [count] |
| Last run | [pass/fail/unknown] |

---

## Feature Map

### Shipped
[bullet list of completed features — detected from code + git history]

### Pending
- [ ] [items from TODOs, open issues, missing configs]

### Roadmap
- [ ] [future items, not counted in launch %]

---

## Velocity

\```
Commits/week:  ██████████████░░░░░░  [N] commits
Trend:         [↑ accelerating / → steady / ↓ slowing]
\```

[If enough history:]
\```
4 weeks ago    ████████░░░░░░░░░░░░  [N]
3 weeks ago    ██████████░░░░░░░░░░  [N]
2 weeks ago    ████████████░░░░░░░░  [N]
Last week      ██████████████░░░░░░  [N]
\```

---

## Change Log

| Date | Action | Impact | Area |
|------|--------|--------|------|
[APPEND only — never delete previous entries]

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
[APPEND only]

## Learnings

| Date | Learning | Context |
|------|----------|---------|
[APPEND only]
```

## Phase 7: Update Supporting Files

If these exist, update them to match:
- `PROGRESS.md` — sync %, update progress bars, append change log
- `DASHBOARD.md` — sync if not a redirect
- `TODO.md` / `ROADMAP.md` — mark completed items

## Phase 8: Summary Output

After updating files, output this to the terminal:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 /track complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 Launch:  [████████████████░░░░]  80%
 Build:   ✅ Pass (0 errors)
 Deps:    26 prod · 23 dev · 2 outdated · 0 vulns
 Git:     14 commits/7d · 3 branches · 2 uncommitted
 Health:  4 TODOs · 1 FIXME · 0 BLOCKERs

 Changed: INFRASTRUCTURE_STATUS.md, PROGRESS.md
 Next:    [highest priority pending item]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Principles

1. **Real data only** — every number comes from a command, not a guess
2. **Never delete history** — logs are append-only
3. **Adapt to the project** — a Rust CLI tracks different things than a SaaS app
4. **Honest percentages** — blockers weigh 2x, roadmap items excluded
5. **30-second scan** — the dashboard must be readable at a glance
6. **Zero config** — works on first run with no setup
