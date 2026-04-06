---
name: track
description: "Update project dashboard and tracking documents after changes. Use after completing features, fixes, refactors, or any significant work. Adapts to any project type by detecting tech stack, structure, and state automatically."
allowed-tools: Read Write Edit Bash Glob Grep Agent
user-invocable: true
---

# /track — Adaptive Project Dashboard Updater

You are a project tracking system. Your job is to analyze the current state of the project and update all tracking documents to reflect reality.

## Context

The user just completed work and wants the project dashboard updated. You must:

1. **Detect** what changed since the last tracking update
2. **Analyze** the current project state
3. **Update** all tracking documents accurately
4. **Report** a brief summary of what was updated

## Arguments

If the user provides arguments, treat them as a description of what was just done:
```
/track Added payment integration with Stripe
/track Fixed auth bug in login flow
/track                              ← no args = auto-detect changes
```

$ARGUMENTS

---

## Step 1: Project Detection (Adaptive)

Detect the project type and structure. This skill works with ANY project — adapt to what you find.

Run these commands to understand the project:

```bash
# What kind of project is this?
ls package.json Cargo.toml go.mod requirements.txt pyproject.toml Gemfile pom.xml build.gradle composer.json 2>/dev/null

# Git state
git log --oneline -5 2>/dev/null
git diff --stat HEAD~1 2>/dev/null || git diff --stat 2>/dev/null

# Build health
```

Detect:
- **Language/Framework**: Node/Next.js/React, Rust, Go, Python, Ruby, Java, PHP, etc.
- **Build system**: npm, cargo, go, pip, bundle, maven, gradle, composer
- **Deployment**: Vercel, AWS, Docker, Heroku, Netlify, Railway, Fly.io, etc.
- **Database**: Supabase, PostgreSQL, MongoDB, MySQL, SQLite, Firebase, etc.
- **Testing**: Jest, Playwright, pytest, cargo test, go test, RSpec, etc.

## Step 2: Gather Metrics

Based on what you detected, gather relevant metrics:

**For web apps (Next.js, React, Vue, etc.):**
- Route count, build errors, TypeScript errors
- Bundle size indicators
- API endpoints count
- Component count

**For any project:**
- Total files by type
- Test count and status (if CI output available)
- Dependencies count
- Recent git activity

**Try a build check if applicable:**
```bash
# For Node.js
npm run build 2>&1 | tail -20

# For Rust
cargo check 2>&1 | tail -10

# For Go
go build ./... 2>&1 | tail -10

# For Python
python -m py_compile main.py 2>&1
```

## Step 3: Update the main dashboard file

Look for the primary dashboard file in this order:
1. `INFRASTRUCTURE_STATUS.md` (preferred)
2. `DASHBOARD.md`
3. If neither exists, create `INFRASTRUCTURE_STATUS.md` from scratch.

### Dashboard Structure (adapt sections to project type):

```markdown
# [Project Name] — Project Dashboard

> Auto-generated control panel. Updated by `/track` after every significant change.
> Last sync: [DATE] | Session: [context]

---

## Launch Readiness

[ASCII progress bar showing overall %]

| Area | Progress | Status | Blocker? |
|------|----------|--------|----------|
[List every major area with accurate % based on completed vs pending items]

---

## Infrastructure
[Services, providers, environments, connection status]

## Tech Stack
[Detected technologies with versions]

## Build Health
[Latest build metrics — routes, errors, warnings, bundle size]

## Security Posture
[Security controls status — only if applicable]

## Legal & Compliance
[Legal documents status — only if applicable]

## Feature Map
### Shipped
[Completed features]

### Pending for Launch
[Checklist of remaining items]

### Post-Launch
[Future roadmap items]

## Change Log
| Date | Action | Impact | Area |
[Append new entry — never delete old ones]

## Decision Log
| Date | Decision | Rationale |
[Append if a new decision was made this session]

## Learnings
| Date | Learning | Context |
[Append if something was learned this session]
```

### Progress Calculation Rules:

Calculate the overall % as a **weighted average** of all areas:

- Areas marked as "Ship-ready" (100%) get their full weight
- Blocker areas get 2x weight (they gate launch)
- Post-launch features do NOT count toward launch readiness %

### Progress Bar Format:

```
[████████████████░░░░]  82%
```
- Use 20 characters total
- █ for filled, ░ for empty
- Round to nearest 5%

## Step 4: Update PROGRESS.md (if it exists)

If a `PROGRESS.md` file exists at the project root:
- Update the overall % to match DASHBOARD.md
- Update the ASCII progress bar
- Append a new entry to the Change Log table
- Update any stage/etapa checklists if items were completed

## Step 5: Update Supporting Documents

If any of these exist, update them too:
- `DASHBOARD.md` — if it exists and is not a redirect, sync it
- `TODO.md` or `ROADMAP.md` — mark completed items
- Any other tracking documents you find at the project root

## Step 6: Report

After updating, output a brief summary:

```
## /track complete

**Overall: XX% → YY%** (+Z%)

### Updated this session:
- [what was done / detected as changed]

### Files updated:
- DASHBOARD.md
- PROGRESS.md (if exists)
- [any other files]

### Next priority:
- [most impactful pending item]
```

---

## Principles

1. **Never lie about progress** — if something is broken, show it as broken
2. **Never delete history** — always append to logs, never overwrite
3. **Detect, don't assume** — run actual commands to verify state
4. **Adapt to the project** — a Rust CLI has different tracking needs than a SaaS app
5. **Be concise** — the dashboard should be scannable in 30 seconds
6. **Weighted accuracy** — blockers matter more than nice-to-haves in the overall %
