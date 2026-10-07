#!/usr/bin/env python3
"""Stop hook: si hubo trabajo en el repo más nuevo que estado/ESTADO.json (últimas 3 h),
pide UNA vez registrar el estado antes de terminar. Respeta stop_hook_active para no ciclar."""
import json, os, sys, time
from pathlib import Path

try:
    entrada = json.load(sys.stdin)
except Exception:
    entrada = {}
if entrada.get("stop_hook_active"):
    sys.exit(0)

raiz = Path(os.environ.get("CLAUDE_PROJECT_DIR") or entrada.get("cwd") or os.getcwd())
try:
    import subprocess
    _t = subprocess.run(["git", "-C", str(raiz), "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=8).stdout.strip()
    raiz = Path(_t) if _t else raiz
except Exception:
    pass
estado = raiz / "estado" / "ESTADO.json"
if not estado.exists():
    sys.exit(0)
t_estado = estado.stat().st_mtime if estado.exists() else 0
limite = time.time() - 3 * 3600
OMITIR = {".git", "node_modules", "estado", ".next", ".claude", "build", "DerivedData", "daily-logs",
          "work", "frames", ".hf-segments", "__pycache__", "PUBLICACION"}
EXT = {".ts", ".tsx", ".js", ".mjs", ".py", ".sh", ".swift", ".yml", ".json", ".md", ".sql", ".html", ".mp4"}

reciente = None
for base, dirs, archivos in os.walk(raiz):
    dirs[:] = [d for d in dirs if d not in OMITIR and not d.startswith(".")]
    for a in archivos:
        if Path(a).suffix not in EXT or a == "HANDOFF.md":
            continue
        p = Path(base) / a
        try:
            m = p.stat().st_mtime
        except OSError:
            continue
        if m > limite and m > t_estado + 60:
            reciente = p.relative_to(raiz)
            break
    if reciente:
        break

if reciente:
    print(json.dumps({
        "decision": "block",
        "reason": (f"Handoff vivo: hay cambios recientes (p. ej. {reciente}) que no están en estado/ESTADO.json. "
                   "Antes de terminar, registra el bloque con `python3 estado/registrar.py --id <slug> --estado <...> "
                   "--titulo \"...\" --publico \"...\" --interno \"...\"` (y --cortado-en si cambió dónde nos quedamos). "
                   "Si no hubo nada que registrar, corre `python3 estado/registrar.py` sin argumentos para marcarlo al día."),
    }))
sys.exit(0)
