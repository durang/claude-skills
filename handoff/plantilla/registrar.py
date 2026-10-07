#!/usr/bin/env python3
"""Crea o actualiza UNA entrada de estado/ESTADO.json y regenera HANDOFF.md + tablero.

Uso (cualquier agente, script o la producción diaria):
  python3 estado/registrar.py --id produccion-diaria --estado verificado \
      --evidencia "corrida 2026-10-08: ..." [--titulo ...] [--publico ...] [--interno ...] [--prueba ...]
  python3 estado/registrar.py --cortado-en "..." --resumen "..."   # solo los campos de 'Dónde me quedé'

Los campos que no pases se conservan. Si la entrada no existe, --titulo, --estado y --publico
son obligatorios (salvo estado 'detectado').
"""
import argparse, datetime, json, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
P = RAIZ / "estado" / "ESTADO.json"

ap = argparse.ArgumentParser()
for c in ("id", "titulo", "estado", "publico", "interno", "prueba", "evidencia",
          "cortado-en", "resumen", "arbol", "commit", "pruebas"):
    ap.add_argument(f"--{c}")
a = ap.parse_args()

d = json.loads(P.read_text(encoding="utf-8"))
hoy = datetime.date.today().isoformat()
d["actualizado"] = hoy
for campo in ("cortado_en", "resumen", "arbol", "commit", "pruebas"):
    v = getattr(a, campo)
    if v is not None:
        d[campo] = v

if a.id:
    e = next((x for x in d["entradas"] if x["id"] == a.id), None)
    if e is None:
        if not (a.titulo and a.estado and (a.publico or a.estado == "detectado")):
            sys.exit("registrar: entrada nueva necesita --titulo, --estado y --publico")
        e = {"id": a.id, "titulo": "", "estado": "", "fecha": hoy, "interno": "",
             "publico": "", "prueba": "", "evidencia": ""}
        d["entradas"].append(e)
    for campo in ("titulo", "estado", "publico", "interno", "prueba", "evidencia"):
        v = getattr(a, campo)
        if v is not None:
            e[campo] = v
    e["fecha"] = hoy

P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
sys.exit(subprocess.call([sys.executable, str(RAIZ / "estado" / "generar.py")], cwd=RAIZ))
