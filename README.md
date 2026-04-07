# [◠‿◠] Scan — AI Project Intelligence Engine

> From idea to 100% launch. One command. Any project. Zero config.

### What started as a progress tracker evolved into a complete project intelligence system for Claude Code — goal orchestration, verified task completion, security auditing, multi-language intent detection, and a living dashboard that never lets you lose context.

```
/track
```

That's it. It auto-detects your stack, runs your build, audits dependencies, measures git velocity, profiles your coding habits, tracks tasks with subtask ownership, hunts TODOs — and generates a branded, visual progress dashboard with honest launch readiness %.

```
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║          Y  O  U  R  P  R  O  J  E  C  T             ║
║                                                       ║
║          [◠‿◠]  Scan · Progress Dashboard             ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
```

## Install (10 seconds)

```bash
mkdir -p ~/.claude/skills/track && curl -sL https://raw.githubusercontent.com/durang/claude-skills/master/track/SKILL.md -o ~/.claude/skills/track/SKILL.md
```

Done. Open [Claude Code](https://claude.ai/code) in any project and type `/track`.

---

## What You Get

### Branded header with your project name

Every dashboard starts with your project name displayed large in spaced letters inside a clean box-drawing border. Your project feels like a product from day one.

### Launch readiness with honest math

```
OVERALL        [████████████████░░░░]  80%  →  Production

Core Platform  [████████████████████] 100%  ✅ Ship-ready
Auth/Users     [████████████████████] 100%  ✅ Magic link + password
AI Chat        [████████████████████] 100%  ✅ DeepSeek V3 integrated
Payments       [████████████░░░░░░░░]  60%  ⚠️ Test mode only         ← BLOCKER
Security       [█████████████████░░░]  85%  🟡 2 items left
Deploy Prod    [██████████░░░░░░░░░░]  50%  🔴 Env vars + domain       ← BLOCKER
```

Blocker areas count **2x** in the weighted average. Roadmap items are excluded. Your % reflects what actually matters for shipping — not optimism.

### Active Tasks with ownership tracking

When you tell Claude "we need Gmail login" or "nos falta analytics", it creates a task with auto-generated subtasks tagged by who can do them:

```
### Gmail Login                              Auth · +5%
- [ ] Configure Google OAuth in Supabase       ← user
- [ ] Add provider env vars to Vercel          ← user
- [ ] Create Google sign-in button             ← auto
- [ ] Handle OAuth callback route              ← auto
- [ ] Update authState for Google provider     ← auto
- [ ] Test end-to-end                          ← user
> 0/6 · Next: needs OAuth config first
```

- `← auto` = Claude can execute it right now without your credentials
- `← user` = needs your dashboard access, API keys, or manual verification

**When you say "let's go" / "sigamos" / "avancemos"** — Claude reads the dashboard, finds all `← auto` subtasks, and starts coding the highest-impact ones immediately. No menus. No "what would you like to do?" — just execution.

### Visual charts from real git data

**Daily commit activity:**
```
                    Daily Commits (last 7 days)
  Tue 31  ████████████████████  20
  Wed 01  ██████               6
  Thu 02  ██████████████████   18
  Fri 03  █████                5
  Sat 04  ████                 4
  Sun 05  ███████              7
  Mon 06  █████                5   ← today
```

**Your peak coding hours:**
```
                    Peak Hours (when you code)
  4pm-8pm   ████████████████████  28 commits   ← peak
  midnight  ████████████████░░░░  21 commits
  9pm-11pm  ██████████████░░░░░░  16 commits
```

**Codebase breakdown by language:**
```
 TypeScript    ██████████████░░░░░░  14,498 lines
 TSX (React)   ████████████████████  22,669 lines
 CSS            █░░░░░░░░░░░░░░░░░░   1,648 lines
               ─────────────────────
 Total                                38,815 lines
```

**Commit type distribution:**
```
  fix     █████████████████████████████████████████████  45%
  feat    ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░  20%
  chore   ████████████████████████████░░░░░░░░░░░░░░░░  35%
```

**Progress timeline — your journey to launch:**
```
                    Launch % Over Time
  Mar 26  ░░░░░░░░░░░░░░░░░░░░   0%   Project created
  Mar 29  ██████████░░░░░░░░░░  50%   Core + Auth
  Mar 30  ██████████████░░░░░░  70%   UI + AI Chat
  Apr 05  ███████████████░░░░░  75%   Security hardening
  Apr 06  ████████████████░░░░  80%   Vulns fixed + Tasks
```

**Milestone map:**
```
  ◉────◉────◉────◉────○────○────○────○
  10   25   50   75   85   90   95  100
                       ↑
                   you are here
```

### Incremental scanning — saves tokens

The dashboard stores the last scanned commit hash. On re-scan:

| Mode | When | What runs | Savings |
|------|------|-----------|---------|
| **FULL** | First scan | Everything | Baseline |
| **INCREMENTAL** | New commits since last scan | Build, audit, velocity, health | ~50% |
| **SKIP** | Zero changes | Nothing — just reports status | ~95% |

### Architecture diagram

Auto-generated ASCII diagram showing your real project structure:

```
                    ┌──────────────────┐
                    │   Vercel (CDN)   │
                    └────────┬─────────┘
                             │
               ┌─────────────┴──────────────┐
               │    Next.js 16 App Router    │
               └──┬──────────┬──────────┬───┘
                  │          │          │
           ┌──────┘          │          └──────┐
    ┌──────┴──────┐   ┌──────┴──────┐   ┌──────┴──────┐
    │    Pages    │   │  API Routes │   │    Libs     │
    └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
           │                 │                  │
    ┌──────┘    ┌────────────┼────────────┐     │
    ▼           ▼            ▼            ▼     ▼
 Zustand    Supabase    Lemon Squeezy  DeepSeek  Web Audio
```

### Everything else

- **Build health** — pass/fail, errors, warnings, route count
- **Dependency audit** — outdated count, vulnerability scan
- **Code health** — every TODO, FIXME, HACK with file:line
- **Security posture** — headers, rate limiting, auth, CSRF, audit
- **Legal compliance** — privacy, terms, disclaimers, GDPR
- **Business context** — pricing, audience, model
- **Feature map** — shipped, pending, roadmap
- **Logs** — changes, decisions, learnings (append-only, never deleted)

---

## Usage

```bash
# Auto-detect everything and scan
/track

# Tell it what you just did, then scan
/track Added Gmail authentication

# After a big session
/track Refactored API layer, added rate limiting, fixed 14 vulnerabilities

# Ask what's next — it reads the dashboard and tells you
que sigue?
```

## Works With Everything

| Stack | Detection | Checks |
|-------|-----------|--------|
| **Node / Next.js / React / Vue** | `package.json` | build, audit, outdated, routes |
| **Rust** | `Cargo.toml` | cargo check, cargo outdated |
| **Go** | `go.mod` | go build, modules |
| **Python** | `requirements.txt` / `pyproject.toml` | compileall, pip audit |
| **Ruby** | `Gemfile` | bundle audit |
| **Java / Kotlin** | `pom.xml` / `build.gradle` | build, deps |
| **PHP** | `composer.json` | composer audit |
| **Monorepo** | Workspaces / Turborepo / Nx | per-package + overall |

Auto-detects: Vercel, Docker, AWS, Fly, Netlify, Railway, Supabase, Prisma, Firebase, GitHub Actions, GitLab CI, Jest, Vitest, Playwright, pytest.

## How It Adapts

| Project Type | Areas Tracked |
|-------------|---------------|
| **SaaS / Web App** | Core, Frontend, Auth, Payments, Security, Legal, SEO, Monitoring, Deploy |
| **CLI / Library** | Core, API Design, Docs, Testing, CI/CD, Publishing |
| **Mobile App** | Core, UI/UX, Auth, Push Notifications, App Store, Analytics |
| **API / Backend** | Endpoints, Auth, Database, Rate Limiting, Docs, Deploy |

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
Yes. Installed globally at `~/.claude/skills/track/`. Works in any directory.

**Does it waste tokens on re-scans?**
No. Incremental mode only re-checks what changed since the last commit hash. If nothing changed, it skips entirely (~95% savings).

## Alternative Install

```bash
# Clone for easy updates
git clone https://github.com/durang/claude-skills.git ~/claude-skills
ln -s ~/claude-skills/track ~/.claude/skills/track

# Update later
cd ~/claude-skills && git pull
```

## Requirements

- [Claude Code](https://claude.ai/code) (CLI, desktop, VS Code, JetBrains, or web)
- A git repo
- That's it

## License

MIT

---

Built with [Claude Code](https://claude.ai/code).
