# Claude Code Skills

Custom skills for [Claude Code](https://claude.ai/code). Drop them into `~/.claude/skills/` and they work instantly.

## Skills

### `/track` — Adaptive Project Dashboard

Auto-generates and maintains a visual project dashboard with progress bars, build health, security posture, and change logs. Works with any tech stack.

```
/track                          # auto-detect what changed
/track Added auth system        # describe what you did
```

**What it does:**
- Detects your tech stack (Node, Rust, Go, Python, etc.)
- Runs build checks and gathers metrics
- Creates/updates `INFRASTRUCTURE_STATUS.md` with visual progress bars
- Tracks decisions, learnings, and change history
- Calculates honest launch readiness % (blocker areas weighted 2x)

**Example output:**
```
OVERALL        [███████████████░░░░░]  75%  →  Production

Core Platform  [████████████████████] 100%  ✅ Ship-ready
Auth/Users     [████████████████████] 100%  ✅ Magic link + password
Payments       [████████████░░░░░░░░]  60%  ⚠️ Test mode only         ← BLOCKER
Security       [███████████████░░░░░]  75%  🟡 Hardened, 2 items left
Deploy Prod    [██████████░░░░░░░░░░]  50%  🔴 Env vars + domain       ← BLOCKER
```

## Installation

### Quick (one skill)

```bash
mkdir -p ~/.claude/skills/track
cp track/SKILL.md ~/.claude/skills/track/SKILL.md
```

### All skills (symlink)

```bash
git clone https://github.com/durang/claude-skills.git ~/claude-skills

# Link individual skills
ln -s ~/claude-skills/track ~/.claude/skills/track
```

### Verify

Open Claude Code in any project and type `/track`. That's it.

## How skills work

Claude Code loads skills from `~/.claude/skills/<name>/SKILL.md`. Each skill:

- Has YAML frontmatter (name, description, allowed tools)
- Contains markdown instructions that Claude follows
- Appears as a `/slash-command` in the Claude Code interface
- Can read/write files, run commands, and use any Claude Code tool

## License

MIT
