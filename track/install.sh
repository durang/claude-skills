#!/bin/bash
# /track skill installer for Claude Code
# Usage: bash install.sh
# Or:    curl -sL <url> | bash

SKILL_DIR="$HOME/.claude/skills/track"

mkdir -p "$SKILL_DIR"
cp "$(dirname "$0")/SKILL.md" "$SKILL_DIR/SKILL.md"

echo "✓ /track skill installed at $SKILL_DIR/SKILL.md"
echo "  Open Claude Code in any project and type: /track"
