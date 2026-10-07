#!/usr/bin/env python3
"""SessionStart (Claude Code y Cursor): inyecta el bloque vivo de HANDOFF.md y avisa si el
ledger quedó atrás del trabajo real. Solo actúa en repos con estado/ESTADO.json o HANDOFF.md.

- Claude Code: el repo es el cwd (o CLAUDE_PROJECT_DIR). Sale JSON con additionalContext.
- Cursor: el repo sale de workspace_roots en el JSON de stdin. Sale JSON con additional_context.
No redacta nada: solo muestra el estado y dice si falta registrar.
"""
import json, os, subprocess, sys, time
from pathlib import Path

try:
    entrada = json.load(sys.stdin)
except Exception:
    entrada = {}

cursor = isinstance(entrada.get("workspace_roots"), list)
if cursor and entrada["workspace_roots"]:
    raiz = Path(entrada["workspace_roots"][0])
else:
    raiz = Path(os.environ.get("CLAUDE_PROJECT_DIR") or entrada.get("cwd") or os.getcwd())


def git(*args):
    try:
        return subprocess.run(["git", "-C", str(raiz), *args], capture_output=True, text=True, timeout=8).stdout.strip()
    except Exception:
        return ""


top = git("rev-parse", "--show-toplevel")
if top:
    raiz = Path(top)
estado = raiz / "estado" / "ESTADO.json"
handoff = raiz / "HANDOFF.md"
if not estado.exists() and not handoff.exists():
    sys.exit(0)

partes = []
texto = handoff.read_text(encoding="utf-8") if handoff.exists() else ""
ini, fin = "<!-- ledger:inicio -->", "<!-- ledger:fin -->"
if ini in texto and fin in texto:
    partes.append(texto.split(ini, 1)[1].split(fin, 1)[0].strip())
elif texto:
    partes.append(texto[:6000])

# ¿El ledger quedó atrás?
avisos = []
if estado.exists():
    t_estado = estado.stat().st_mtime
    try:
        citado = str(json.loads(estado.read_text(encoding="utf-8")).get("commit") or "").split()[0].strip("`")
    except Exception:
        citado = ""
    if citado and git("cat-file", "-t", citado) == "commit":
        n = git("rev-list", "--count", f"{citado}..HEAD")
        if n and n != "0":
            avisos.append(f"{n} commit(s) después del commit que cita el ledger ({citado}).")
    sucios = [l[3:] for l in git("status", "--porcelain").splitlines()
              if l[3:] and not l[3:].startswith(("estado/", "HANDOFF.md"))]
    nuevos = [s for s in sucios if (raiz / s).is_file() and (raiz / s).stat().st_mtime > t_estado + 60]
    if nuevos:
        avisos.append(f"{len(nuevos)} archivo(s) cambiados después del último registro (p. ej. {nuevos[0]}).")
else:
    avisos.append("Hay HANDOFF.md escrito a mano pero no estado/ESTADO.json: migra con /handoff.")

encabezado = ("HANDOFF VIVO (estado/ESTADO.json → HANDOFF.md). Empieza por aquí y verifica la deuda antes de construir. "
              "Al cerrar cada bloque: python3 estado/registrar.py --id <slug> --estado <...> --titulo ... --publico ... --interno ...")
if avisos:
    encabezado = "LEDGER ATRÁS: " + " ".join(avisos) + " Ponlo al día primero.\n" + encabezado
ctx = (encabezado + "\n\n" + "\n\n".join(partes))[:9500]

if cursor:
    print(json.dumps({"additional_context": ctx}))
else:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": ctx}}))
