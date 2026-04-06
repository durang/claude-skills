# /track — Project Dashboard for Claude Code

One command. Zero config. Works with any project.

`/track` scans your codebase, detects your stack, gathers real metrics, and generates a visual dashboard — automatically.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 /track complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 Launch:  [████████████████░░░░]  80%
 Build:   ✅ Pass (0 errors)
 Deps:    26 prod · 23 dev · 2 outdated · 0 vulns
 Git:     14 commits/7d · 3 branches · 2 uncommitted
 Health:  4 TODOs · 1 FIXME · 0 BLOCKERs

 Changed: INFRASTRUCTURE_STATUS.md
 Next:    Configure production payment integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## What It Does

```
/track                          → scan project, update dashboard
/track Added auth system        → log what you did, then update
```

On every run, `/track`:

1. **Detects your stack** — Node, Rust, Go, Python, Ruby, Java, PHP, mobile, monorepo
2. **Runs your build** — catches errors before you push
3. **Counts everything** — files, routes, deps, outdated packages, vulnerabilities
4. **Scans code health** — finds TODOs, FIXMEs, HACKs, BLOCKERs
5. **Measures git velocity** — commits/week with trend sparklines
6. **Calculates launch readiness** — honest %, weighted by blockers
7. **Writes the dashboard** — `INFRASTRUCTURE_STATUS.md` with visual progress bars
8. **Preserves history** — change log, decision log, learnings (append-only)

## Dashboard Output

```
OVERALL        [███████████████░░░░░]  75%  →  Production

Core Platform  [████████████████████] 100%  ✅ Ship-ready
Audio Engine   [████████████████████] 100%  ✅ Ship-ready
Auth/Users     [████████████████████] 100%  ✅ Magic link + password
AI Chat        [████████████████████] 100%  ✅ DeepSeek V3 integrated
Payments       [████████████░░░░░░░░]  60%  ⚠️ Test mode only         ← BLOCKER
Security       [███████████████░░░░░]  75%  🟡 Hardened, 2 items left
Deploy Prod    [██████████░░░░░░░░░░]  50%  🔴 Env vars + domain       ← BLOCKER
```

Plus: infrastructure status, build health, dependency audit, git pulse, code health scanner, velocity chart, and append-only logs.

## Install

```bash
# One command
mkdir -p ~/.claude/skills/track && curl -sL https://raw.githubusercontent.com/durang/claude-skills/master/track/SKILL.md -o ~/.claude/skills/track/SKILL.md
```

Or clone for updates:

```bash
git clone https://github.com/durang/claude-skills.git ~/claude-skills
ln -s ~/claude-skills/track ~/.claude/skills/track
```

Open [Claude Code](https://claude.ai/code) in any project and type `/track`.

## Works With

| Stack | Detected Via | What It Tracks |
|-------|-------------|----------------|
| **Next.js / React / Vue** | `package.json` | Routes, components, build errors, bundle |
| **Rust** | `Cargo.toml` | Crate deps, `cargo check`, compile errors |
| **Go** | `go.mod` | Modules, `go build`, test coverage |
| **Python** | `requirements.txt` / `pyproject.toml` | Packages, compile check, pip audit |
| **Ruby** | `Gemfile` | Gems, bundle audit |
| **Java / Kotlin** | `pom.xml` / `build.gradle` | Dependencies, build status |
| **PHP** | `composer.json` | Packages, composer audit |
| **Mobile** | Xcode / Android manifests | Build status, signing, store readiness |
| **Monorepo** | Turborepo / Nx / Lerna / Workspaces | Per-package + overall health |

Auto-detects deploy target (Vercel, Docker, AWS, Fly, Netlify, Railway), database (Supabase, Prisma, Drizzle, MongoDB, Firebase), CI/CD (GitHub Actions, GitLab CI), and testing framework (Jest, Vitest, Playwright, pytest, cargo test).

## What Gets Tracked

| Section | Description |
|---------|-------------|
| **Launch Readiness** | Visual progress bars per area, weighted % (blockers count 2x) |
| **Stack** | Detected technologies with real versions |
| **Infrastructure** | Services, providers, environments, connection status |
| **Build Health** | Errors, warnings, routes, source files, dependencies |
| **Git Pulse** | Commits/week, contributors, branches, uncommitted changes |
| **Code Health** | TODO/FIXME/HACK/BLOCKER scanner with file + line references |
| **Security** | Headers, auth, rate limiting, vulnerabilities (from audit) |
| **Dependency Health** | Outdated packages, known vulnerabilities |
| **Velocity** | Weekly commit sparkline with trend indicator |
| **Feature Map** | Shipped / Pending / Roadmap checklists |
| **Change Log** | Append-only history of what changed and when |
| **Decision Log** | Why decisions were made (with rationale) |
| **Learnings** | What was learned during development |

## How Progress Works

```
Overall % = weighted average of all areas

- Blocker areas count 2x (they gate your launch)
- 100% areas get full weight
- Roadmap/post-launch items are EXCLUDED
- Rounded to nearest 5%
```

An area becomes a **BLOCKER** when:
- Required but at 0% (no tests, no deploy, no auth)
- Contains security vulnerabilities
- Build fails
- Legal/compliance requirements unmet

This means your % is **honest** — it reflects what actually matters for shipping.

## Adaptive to Any Project

`/track` doesn't have a fixed template. It adapts:

- **SaaS**: Core, Frontend, Backend, Auth, Payments, Security, Legal, SEO, Monitoring, Deploy
- **CLI tool**: Core, API Design, Docs, Testing, CI/CD, Publishing
- **Mobile app**: Core, UI/UX, Navigation, Auth, Push Notifications, App Store
- **API**: Endpoints, Auth, Database, Validation, Rate Limiting, Docs, Deploy
- **Library**: Core, API, Types, Docs, Tests, CI/CD, npm/crates.io Publishing

## FAQ

**Does it modify my code?**
No. It only reads your codebase and writes/updates markdown status files.

**Does it run my build?**
Yes, to verify build health. It uses your existing build command (`npm run build`, `cargo check`, etc.)

**What if I don't have a dashboard yet?**
It creates `INFRASTRUCTURE_STATUS.md` from scratch on first run.

**Does it work in teams?**
Yes. Commit the dashboard to your repo — the whole team sees progress. Each `/track` run appends to the shared history.

**Can I customize the areas it tracks?**
It adapts automatically based on your project structure. The areas it detects come from what files and configs actually exist in your repo.

## Requirements

- [Claude Code](https://claude.ai/code) (CLI, VS Code extension, or web)
- A git repository (for velocity tracking)
- That's it

## License

MIT — use it, fork it, share it.

---

Built with [Claude Code](https://claude.ai/code).
