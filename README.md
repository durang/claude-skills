# /track — Zero-Config Project Radar for Claude Code

One command. Any language. Real metrics. No setup.

```
/track
```

That's it. It scans your entire project, detects your stack, runs your build, audits dependencies, measures git velocity, hunts TODOs — and generates a visual dashboard with honest launch readiness %.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 /track complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 Launch:  [███████████████░░░░░]  75%
 Build:   ✅ Pass (0 errors)
 Deps:    26 prod · 23 dev · 15 outdated · 4 high vulns
 Git:     76 commits/7d · 1 branch · 6 uncommitted
 Health:  1 TODO · 0 FIXMEs · 0 BLOCKERs

 Changed: INFRASTRUCTURE_STATUS.md
 Next:    Configure production payment integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Install (10 seconds)

```bash
mkdir -p ~/.claude/skills/track && curl -sL https://raw.githubusercontent.com/durang/claude-skills/master/track/SKILL.md -o ~/.claude/skills/track/SKILL.md
```

Done. Open [Claude Code](https://claude.ai/code) in any project and type `/track`.

## Usage

```bash
# Scan current state — auto-detects everything
/track

# Log what you just did, then scan
/track Added authentication with Supabase

# After fixing a bug
/track Fixed memory leak in WebSocket handler

# After a big refactor
/track Migrated from Express to Hono, restructured API layer
```

## What You Get

### Visual progress bars with honest percentages

```
OVERALL        [███████████████░░░░░]  75%  →  Production

Core Platform  [████████████████████] 100%  ✅ Ship-ready
Auth/Users     [████████████████████] 100%  ✅ Magic link + password
AI Chat        [████████████████████] 100%  ✅ DeepSeek V3 integrated
Payments       [████████████░░░░░░░░]  60%  ⚠️ Test mode only         ← BLOCKER
Security       [███████████████░░░░░]  75%  🟡 2 items left
Deploy Prod    [██████████░░░░░░░░░░]  50%  🔴 Env vars + domain       ← BLOCKER
```

> Blocker areas count **2x** in the weighted average. Roadmap items are excluded. Your % reflects what actually matters for shipping.

### Git velocity sparklines

```
Commits/week:  ███████████████████░  76 commits
Trend:         ↑ accelerating

4 weeks ago    ░░░░░░░░░░░░░░░░░░░░   0
3 weeks ago    ░░░░░░░░░░░░░░░░░░░░   0
2 weeks ago    ██████████████░░░░░░  54
Last week      ███████████████████░  76
```

### Dependency audit

```
| Dependencies | 26 prod + 23 dev |
| Outdated     | 15               |
| Vulns        | 14 total (4 high, 1 moderate, 2 low) |
```

### Code health scanner

Finds every `TODO`, `FIXME`, `HACK`, and `BLOCKER` with file + line number:

```
| File                                     | Line | Note                                    |
| app/api/webhooks/lemonsqueezy/route.ts   | 231  | TODO: Map real variant IDs              |
```

### Build health, infrastructure, security posture, legal compliance, testing status, feature map, change/decision/learning logs

All in one markdown file. Updated every time you run `/track`.

## Works With Everything

| Stack | How It Detects | What It Checks |
|-------|---------------|----------------|
| **Node / Next.js / React / Vue** | `package.json` | `npm run build`, `npm audit`, `npm outdated`, routes |
| **Rust** | `Cargo.toml` | `cargo check`, `cargo outdated`, compile errors |
| **Go** | `go.mod` | `go build ./...`, modules, test coverage |
| **Python** | `requirements.txt` / `pyproject.toml` | `compileall`, `pip audit`, `pip outdated` |
| **Ruby** | `Gemfile` | `bundle audit`, gems |
| **Java / Kotlin** | `pom.xml` / `build.gradle` | build status, dependencies |
| **PHP** | `composer.json` | `composer audit`, packages |
| **Mobile** | Xcode / Android manifests | build, signing, store readiness |
| **Monorepo** | Workspaces / Turborepo / Nx | per-package + overall |

Auto-detects: Vercel, Docker, AWS, Fly, Netlify, Railway, Supabase, Prisma, Firebase, GitHub Actions, GitLab CI, Jest, Vitest, Playwright, pytest.

## How It Thinks

`/track` adapts what it tracks to your project type:

| Project Type | Areas Tracked |
|-------------|---------------|
| **SaaS / Web App** | Core, Frontend, Auth, Payments, Security, Legal, SEO, Monitoring, Deploy |
| **CLI Tool / Library** | Core, API Design, Docs, Testing, CI/CD, Publishing |
| **Mobile App** | Core, UI/UX, Auth, Push Notifications, App Store, Analytics |
| **API / Backend** | Endpoints, Auth, Database, Rate Limiting, Docs, Deploy |

### Honest Math

```
Overall % = weighted average of all areas

Blocker areas    → 2x weight (they gate your launch)
100% areas       → full weight
Roadmap items    → excluded (not needed to ship)
```

Result: your percentage reflects **reality**, not optimism.

## What It Creates

On first run, `/track` creates `INFRASTRUCTURE_STATUS.md` in your project root. On subsequent runs, it updates the same file — appending to logs, never deleting history.

It also syncs `PROGRESS.md`, `DASHBOARD.md`, `TODO.md`, or `ROADMAP.md` if they exist.

## FAQ

**Does it change my code?**
No. It only reads your codebase and writes markdown status files.

**Does it run my build?**
Yes — to verify build health. Uses your existing build command.

**What if I have no dashboard yet?**
Creates one from scratch on first run. Zero setup.

**Does it work in teams?**
Commit the dashboard to your repo. Everyone sees the same truth.

**Can I use it on multiple projects?**
Yes. It's installed globally at `~/.claude/skills/track/`. Works in any directory.

## Alternative Install

```bash
# Clone for easy updates
git clone https://github.com/durang/claude-skills.git ~/claude-skills
ln -s ~/claude-skills/track ~/.claude/skills/track

# Update later
cd ~/claude-skills && git pull
```

## Requirements

- [Claude Code](https://claude.ai/code) (CLI, desktop app, VS Code, JetBrains, or web)
- A git repo (for velocity tracking)
- That's it

## License

MIT

---

Built with [Claude Code](https://claude.ai/code).
