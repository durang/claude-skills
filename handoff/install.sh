#!/bin/bash
# Instala /handoff para cualquier proyecto.
# Uso: bash install.sh
# El skill queda en ~/.claude/skills/handoff/ (SKILL.md + plantilla/).

set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills/handoff"

mkdir -p "$DEST/plantilla"
cp "$SRC/SKILL.md" "$DEST/SKILL.md"
cp "$SRC/plantilla/generar.py" "$DEST/plantilla/generar.py"
cp "$SRC/plantilla/ARQUETIPO.md" "$DEST/plantilla/ARQUETIPO.md"
cp "$SRC/plantilla/ESTADO.ejemplo.json" "$DEST/plantilla/ESTADO.ejemplo.json"
cp "$SRC/plantilla/revisar.py" "$DEST/plantilla/revisar.py"
cp "$SRC/plantilla/registrar.py" "$DEST/plantilla/registrar.py"
cp "$SRC/plantilla/cerrar.py" "$DEST/plantilla/cerrar.py"
chmod +x "$DEST/plantilla/"*.py

python3 - "$DEST" <<'PY'
import json, sys
from pathlib import Path

dest = Path(sys.argv[1])
script = dest / "plantilla" / "revisar.py"
home = Path.home()

# Claude Code: SessionStart. No pisa los ganchos que ya existen.
settings_path = home / ".claude" / "settings.json"
if settings_path.is_file():
    settings = json.loads(settings_path.read_text())
    hooks = settings.setdefault("hooks", {})
    session = hooks.setdefault("SessionStart", [])
    cmd = f'python3 "{script}"'
    already = any(
        cmd in json.dumps(item)
        for item in session
        if isinstance(item, dict)
    )
    if not already:
        session.append({"hooks": [{"type": "command", "command": cmd, "timeout": 15}]})
        print(f"✓ gancho SessionStart de Claude Code en {settings_path}")
    else:
        print("✓ gancho SessionStart de Claude Code ya estaba")
    # Stop: pide registrar UNA vez si hubo cambios después del último registro (solo repos con ledger)
    stop = hooks.setdefault("Stop", [])
    cerrar = f'python3 "{dest / "plantilla" / "cerrar.py"}"'
    if not any(cerrar in json.dumps(item) for item in stop if isinstance(item, dict)):
        stop.append({"hooks": [{"type": "command", "command": cerrar, "timeout": 20}]})
        print(f"✓ gancho Stop de Claude Code en {settings_path}")
    else:
        print("✓ gancho Stop de Claude Code ya estaba")
    settings_path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n")

# Cursor: sessionStart. El script usa workspace_roots, no el directorio desde
# el que corre el gancho.
cursor_hooks = home / ".cursor" / "hooks"
cursor_hooks.mkdir(parents=True, exist_ok=True)
link = cursor_hooks / "handoff-revisar.py"
if link.is_symlink() or link.exists():
    link.unlink()
link.symlink_to(script)
hooks_path = home / ".cursor" / "hooks.json"
hooks = {"version": 1, "hooks": {}}
if hooks_path.is_file():
    try:
        loaded = json.loads(hooks_path.read_text())
        if isinstance(loaded, dict):
            hooks = loaded
    except json.JSONDecodeError:
        pass
hooks.setdefault("version", 1)
table = hooks.setdefault("hooks", {})
starts = table.setdefault("sessionStart", [])
rel = "./hooks/handoff-revisar.py"
if not any(isinstance(item, dict) and item.get("command") == rel for item in starts):
    starts.append({"command": rel, "timeout": 15})
    hooks_path.write_text(json.dumps(hooks, indent=2, ensure_ascii=False) + "\n")
    print(f"✓ gancho de Cursor en {hooks_path}")
else:
    print("✓ gancho de Cursor ya estaba")
PY

echo "✓ /handoff instalado en $DEST"
echo "  Revisa al abrir cualquier repo que tenga HANDOFF.md o estado/ESTADO.json"
