#!/usr/bin/env python3
"""Genera el bloque vivo de HANDOFF.md y estado/tablero.html desde ESTADO.json.

No edites las salidas a mano. Si una entrada verificado no trae evidencia, o el
texto público contiene un término prohibido, este script sale con código 1 y
no escribe nada.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

ESTADOS = ("verificado", "desplegado", "construyendo", "decide", "detectado")
INICIO = "<!-- ledger:inicio -->"
FIN = "<!-- ledger:fin -->"
HIST = "<!-- ledger:historico -->"

ETIQUETA_PUBLICA = {
    "verificado": "Listo",
    "desplegado": "En producción, falta verlo",
    "construyendo": "En curso",
    "decide": "Falta una decisión",
    "detectado": "Detectado",
}


def fallar(msg: str) -> None:
    print(f"ledger: {msg}", file=sys.stderr)
    sys.exit(1)


def cargar(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fallar(f"no existe {path}")
    except json.JSONDecodeError as exc:
        fallar(f"{path} no es JSON válido: {exc}")
    if not isinstance(data, dict):
        fallar("ESTADO.json tiene que ser un objeto")
    return data


def validar(data: dict) -> list[dict]:
    entradas = data.get("entradas")
    if not isinstance(entradas, list) or not entradas:
        fallar("entradas tiene que ser una lista con al menos una")
    prohibido = [p.casefold() for p in data.get("prohibido_publico") or [] if isinstance(p, str)]
    vistos: set[str] = set()
    for i, e in enumerate(entradas, start=1):
        if not isinstance(e, dict):
            fallar(f"entrada {i} no es un objeto")
        eid = str(e.get("id") or "").strip()
        if not eid:
            fallar(f"entrada {i} no tiene id")
        if eid in vistos:
            fallar(f"id repetido: {eid}")
        vistos.add(eid)
        estado = e.get("estado")
        if estado not in ESTADOS:
            fallar(f"{eid}: estado '{estado}' no es uno de {', '.join(ESTADOS)}")
        publico = str(e.get("publico") or "").strip()
        evidencia = str(e.get("evidencia") or "").strip()
        if estado != "detectado" and not publico:
            fallar(f"{eid}: falta publico")
        if estado == "verificado" and not evidencia:
            fallar(f"{eid}: verificado sin evidencia. Si nadie lo vio, el estado es desplegado")
        blob = f"{publico}\n{e.get('prueba') or ''}".casefold()
        for term in prohibido:
            if term and term in blob:
                fallar(f"{eid}: el texto público contiene '{term}'")
        for campo in ("interno", "evidencia"):
            if str(e.get(campo) or "") and campo in ("interno", "evidencia"):
                # el HTML se arma solo con publico y prueba; esto solo documenta la regla
                pass
    return entradas


def lineas(texto: str) -> list[str]:
    texto = (texto or "").strip()
    if not texto:
        return ["(sin anotar)"]
    return texto.splitlines()


def bloque(data: dict, entradas: list[dict]) -> str:
    def de(estado: str) -> list[dict]:
        return [e for e in entradas if e["estado"] == estado]

    deuda = de("desplegado")
    construir = de("construyendo")
    decidir = de("decide")
    detectado = de("detectado")

    if deuda:
        siguiente = (
            "Verificar en pantalla, antes de construir nada: "
            + "; ".join(e["titulo"] for e in deuda)
            + "."
        )
    elif construir:
        siguiente = "Seguir con: " + construir[0]["titulo"] + "."
    elif decidir:
        siguiente = "Nada de código hasta una decisión: " + "; ".join(e["titulo"] for e in decidir) + "."
    else:
        siguiente = "Nada pendiente en el ledger. Preguntar qué sigue."

    out: list[str] = [
        INICIO,
        f"# {data.get('proyecto') or 'Proyecto'} — dónde me quedé",
        "",
        f"_Actualizado: {data.get('actualizado') or 'sin fecha'}._",
        "",
        "## 0. Dónde me quedé",
        "",
        f"**Árbol:** {data.get('arbol') or 'sin anotar'}.",
        f"**Commit:** `{data.get('commit') or 'sin anotar'}`.",
        f"**Pruebas:** {data.get('pruebas') or 'sin anotar'}.",
        "",
        "**Qué se hizo**",
        "",
        *lineas(str(data.get("resumen") or "")),
        "",
        "**En qué se cortó**",
        "",
        *lineas(str(data.get("cortado_en") or "")),
        "",
        "**Para probar y desplegar** (comandos de esta máquina, no de otro repo):",
        "",
        "```bash",
        *([c for c in data.get("comandos") or []] or ["# anota el comando que sí corrió aquí"]),
        "```",
        "",
        "## ▶ SIGUIENTE",
        "",
        siguiente,
        "",
        "## 1. Deuda de verificación",
        "",
    ]
    out.extend(lista(deuda, "Nada en producción pendiente de ver."))
    out.extend(["", "## 2. Lo único por construir", ""])
    out.extend(lista(construir, "Nada en construcción."))
    out.extend(["", "## 3. Lo que espera una decisión", ""])
    out.extend(lista(decidir, "Nada esperando decisión."))
    out.extend(["", "## 4. Detectado y no arreglado", ""])
    out.extend(lista(detectado, "Nada detectado sin arreglar."))
    url = str(data.get("tablero_url") or "").strip()
    out.extend(["", "## 5. Tablero", ""])
    if url:
        out.append(url)
    else:
        out.append("Sin publicar. Lo abre el humano cuando quiera compartirlo.")
    out.extend(["", FIN, ""])
    return "\n".join(out)


def lista(entradas: list[dict], vacio: str) -> list[str]:
    if not entradas:
        return [vacio]
    lineas_out: list[str] = []
    for e in entradas:
        lineas_out.append(f"- **{e['titulo']}** ({e['fecha']}) — {e['publico']}")
        interno = str(e.get("interno") or "").strip()
        if interno:
            lineas_out.append(f"  Para el agente: {interno}")
        prueba = str(e.get("prueba") or "").strip()
        if prueba:
            lineas_out.append(f"  Cómo probarlo: {prueba}")
        if e["estado"] == "desplegado":
            lineas_out.append("  Nadie lo ha visto en pantalla.")
    return lineas_out


def marcar_cumplidos(texto: str) -> str:
    lineas_out = []
    for linea in texto.splitlines():
        if "▶ SIGUIENTE" in linea and "CUMPLIDO" not in linea:
            linea = linea.rstrip() + " *(CUMPLIDO)*"
        lineas_out.append(linea)
    return "\n".join(lineas_out)


def escribir_handoff(path: Path, nuevo: str) -> None:
    if path.exists():
        viejo = path.read_text(encoding="utf-8")
        if INICIO in viejo and FIN in viejo:
            pre, resto = viejo.split(INICIO, 1)
            _, post = resto.split(FIN, 1)
            # post empieza con el salto que seguía al marcador; el bloque nuevo ya trae FIN
            cuerpo = pre + nuevo + post.lstrip("\n")
        else:
            historico = marcar_cumplidos(viejo).strip()
            cuerpo = nuevo + "\n" + HIST + "\n\n" + historico + "\n"
    else:
        cuerpo = nuevo
    path.write_text(cuerpo if cuerpo.endswith("\n") else cuerpo + "\n", encoding="utf-8")


def tablero(data: dict, entradas: list[dict]) -> str:
    tarjetas = []
    for e in entradas:
        publico = str(e.get("publico") or "").strip()
        if not publico:
            continue
        prueba = str(e.get("prueba") or "").strip()
        prueba_html = f"<p class='prueba'>{html.escape(prueba)}</p>" if prueba else ""
        tarjetas.append(
            "<article class='{estado}'>"
            "<p class='badge'>{badge}</p>"
            "<h2>{titulo}</h2>"
            "<p>{publico}</p>"
            "{prueba}"
            "</article>".format(
                estado=html.escape(e["estado"]),
                badge=html.escape(ETIQUETA_PUBLICA[e["estado"]]),
                titulo=html.escape(e["titulo"]),
                publico=html.escape(publico),
                prueba=prueba_html,
            )
        )
    nombre = html.escape(str(data.get("proyecto") or "Proyecto"))
    fecha = html.escape(str(data.get("actualizado") or ""))
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{nombre}</title>
<style>
  :root {{ color-scheme: light dark; --bg: #f6f4ef; --ink: #1c1915; --card: #fff; --line: #e4dfd4; --muted: #6b645b; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg: #161411; --ink: #f3efe6; --card: #221e19; --line: #3a342c; --muted: #b7aea2; }}
  }}
  body {{ margin: 0; font: 17px/1.45 Georgia, serif; background: var(--bg); color: var(--ink); }}
  main {{ max-width: 40rem; margin: 0 auto; padding: 1.5rem 1rem 3rem; }}
  h1 {{ font-size: 1.6rem; margin: 0 0 .25rem; }}
  .cuando {{ color: var(--muted); margin: 0 0 1.5rem; }}
  article {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 1rem 1.1rem; margin: 0 0 .8rem; }}
  h2 {{ font-size: 1.15rem; margin: .2rem 0 .4rem; }}
  .badge {{ margin: 0; font: 600 .75rem/1 system-ui, sans-serif; letter-spacing: .04em; text-transform: uppercase; color: var(--muted); }}
  article.verificado .badge {{ color: #1f7a3a; }}
  article.desplegado .badge {{ color: #9a6b12; }}
  .prueba {{ color: var(--muted); }}
</style>
</head>
<body>
<main>
  <h1>{nombre}</h1>
  <p class="cuando">{fecha}</p>
  {''.join(tarjetas)}
</main>
</body>
</html>
"""


def vigilar_html(data: dict, pagina: str) -> None:
    prohibido = [p.casefold() for p in data.get("prohibido_publico") or [] if isinstance(p, str)]
    bajo = pagina.casefold()
    for term in prohibido:
        if term and term in bajo:
            fallar(f"el tablero generado contiene '{term}'")


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera HANDOFF y tablero desde ESTADO.json")
    parser.add_argument("--estado", default="estado/ESTADO.json")
    parser.add_argument("--handoff", default="HANDOFF.md")
    parser.add_argument("--tablero", default="estado/tablero.html")
    parser.add_argument("--check", action="store_true", help="valida y no escribe")
    args = parser.parse_args()

    data = cargar(Path(args.estado))
    entradas = validar(data)
    nuevo = bloque(data, entradas)
    pagina = tablero(data, entradas)
    vigilar_html(data, pagina)
    if args.check:
        print("ledger: ok")
        return
    handoff = Path(args.handoff)
    tablero_path = Path(args.tablero)
    tablero_path.parent.mkdir(parents=True, exist_ok=True)
    escribir_handoff(handoff, nuevo)
    tablero_path.write_text(pagina, encoding="utf-8")
    print(f"ledger: {handoff} y {tablero_path}")


if __name__ == "__main__":
    main()
