---
name: handoff
description: "Ledger vivo de sesión para cualquier repo. Al abrir, una sesión nueva sabe qué se hizo, qué está sin verificar y qué no debe empezar. Al cerrar, actualiza una sola fuente (estado/ESTADO.json) que genera el HANDOFF interno y el tablero público. Desplegado no es verificado."
allowed-tools: Read Write Edit Bash Glob Grep
user-invocable: true
---

# /handoff — ledger vivo, cualquier proyecto

Una sesión nueva tiene que poder contestar «¿qué hiciste?» leyendo el principio del
HANDOFF. Si solo dice qué sigue, está incompleto.

Esto no es `/track`. `/track` mide avance del producto. `/handoff` registra la sesión:
qué salió, por qué, qué está en producción sin que nadie lo haya visto, y qué no se
empieza sin una decisión humana.

## Cuándo correrlo

- Al abrir: «lee el HANDOFF», «dónde me quedé», «qué hiciste», «retoma».
- Al cerrar un bloque de trabajo, antes del commit.
- Cuando el usuario pida el tablero para el cliente.

## Reglas que no se negocian

1. **Una fuente.** Se edita `estado/ESTADO.json`. `HANDOFF.md` y `estado/tablero.html`
   los escribe `estado/generar.py`. Un HANDOFF editado a mano es el origen de la
   desincronización.
2. **Un solo puntero vigente.** El generador escribe un único `▶ SIGUIENTE`. Si el
   archivo ya tenía otros, los marca *(CUMPLIDO)*. No los borra: el histórico explica
   por qué se hizo cada cosa.
3. **Desplegado ≠ verificado.** Compilar, pruebas en verde y un HTTP 200 no son
   «visto en pantalla». El tablero público solo dice «listo» cuando `estado` es
   `verificado` y `evidencia` dice cómo se vio.
4. **Dos audiencias.** `interno` es para el agente (archivos, porqués, qué se rompe).
   `publico` es para quien lo usa. El HTML nunca incluye `interno` ni `evidencia`.
5. **No inventes el estado.** Si no sabes si se verificó, `evidencia` va vacía y el
   estado es `desplegado`, no `verificado`.
6. **No copies comandos de otro repo.** El PATH de nvm, el proyecto de Vercel y el
   curl de verificación se descubren en ESTE repo y en ESTA máquina. En la máquina
   de Sergio el Node de Homebrew está roto: si `node` falla, antepón
   `export PATH="$HOME/.nvm/versions/node/v24.13.0/bin:$PATH"` y comprueba que
   `node -v` responde. Si esa versión no existe, busca la que sí con `ls "$HOME/.nvm/versions/node"`.
   Anota en `comandos` la línea que funcionó, no una copiada de Vendau.

## Automático: al abrir y al cerrar (ganchos globales)

`install.sh` deja dos ganchos en `~/.claude/settings.json` (y el de inicio también en
Cursor). Actúan solo en repos con `estado/ESTADO.json` o `HANDOFF.md`; los demás no se tocan.

- **Al abrir (`plantilla/revisar.py`, SessionStart):** inyecta el bloque vivo del
  HANDOFF en la sesión, así un agente nuevo (otra ventana, Cursor, o la sesión que
  sigue cuando se acabó el crédito) arranca sabiendo dónde se quedó. Si hay commits
  después del que cita el ledger, o archivos cambiados después del último registro,
  antepone `LEDGER ATRÁS`.
- **Al cerrar cada respuesta (`plantilla/cerrar.py`, Stop):** si hubo cambios
  después del último registro (últimas 3 h), pide UNA vez registrar antes de
  terminar. Respeta `stop_hook_active`, así que nunca cicla. Esto deja el ledger a lo
  más una respuesta atrás: si el crédito se corta, la siguiente sesión pierde casi nada.

Ninguno redacta solo: el diff no sabe por qué se hizo algo, y un texto inventado es
peor que un hueco. El agente escribe el porqué; los ganchos solo garantizan que lo haga.

## Registrar en un comando (`estado/registrar.py`)

Crea o actualiza UNA entrada y regenera HANDOFF y tablero. Los campos que no pases
se conservan:

```bash
python3 estado/registrar.py --id <slug> --estado <verificado|desplegado|construyendo|decide|detectado> \
  --titulo "..." --publico "..." --interno "..." [--prueba "..."] [--evidencia "..."]
python3 estado/registrar.py --cortado-en "..." [--resumen "..."] [--commit "..."]   # solo «Dónde me quedé»
python3 estado/registrar.py   # sin argumentos: marca el ledger al día
```

**Tareas programadas también registran.** Un cron/launchd que produce algo cada
noche termina con `python3 "$REPO/estado/registrar.py" --id <tarea> --evidencia "..."`.
Así el HANDOFF de la mañana ya dice qué salió de madrugada.

**Agentes en segundo plano.** Si un subagente queda a medias (disco, crédito, sesión
cerrada), su entrada `construyendo` lleva en `interno` el comando exacto para retomarlo.

## Al empezar

1. Si llegó el aviso `LEDGER ATRÁS`, cubre ese hueco antes de cualquier otra cosa.
2. Lee `HANDOFF.md` si existe, de arriba abajo, solo hasta el primer bloque histórico.
3. Empieza por la **deuda de verificación** (entradas `desplegado`). No construyas
   nada nuevo mientras haya algo en producción que nadie ha visto, salvo que el
   usuario lo pida explícitamente.
4. Si no hay ledger, instala el arquetipo (abajo) y llénalo con el estado real.
   Di qué no pudiste verificar.

## Al cerrar un bloque

Si el repo tiene `estado/ESTADO.json`:

1. Registra con `python3 estado/registrar.py ...` (o edita solo `ESTADO.json`): una
   entrada por hecho, con el porqué de lo que no es obvio. El campo `commit` es el
   commit de producto que ese texto cubre.
2. `registrar.py` ya corre el generador; si editaste a mano, corre `python3 estado/generar.py` desde la raíz. Si sale distinto de 0, no hagas
   commit: el fallo dice qué entrada miente.
3. Un mismo commit incluye los tres: `estado/ESTADO.json`, `HANDOFF.md` y
   `estado/tablero.html`.

Si el repo solo tiene `HANDOFF.md` escrito a mano, actualiza la sección 0 (qué se
hizo, por qué, en qué se cortó, el commit que cubre) en el mismo bloque. No
migres a `ESTADO.json` a mitad de un trabajo salvo que te lo pidan.

Publicar el tablero lo decide el humano. El enlace va en `tablero_url`.

## Instalar el arquetipo en un repo que no lo tiene

La plantilla vive junto a este skill (`plantilla/`). Si el skill está en
`~/.claude/skills/handoff/`:

```bash
mkdir -p estado
cp ~/.claude/skills/handoff/plantilla/generar.py estado/generar.py
cp ~/.claude/skills/handoff/plantilla/ARQUETIPO.md estado/ARQUETIPO.md
cp ~/.claude/skills/handoff/plantilla/registrar.py estado/registrar.py
cp ~/.claude/skills/handoff/plantilla/ESTADO.ejemplo.json estado/ESTADO.json
```

Añade en `CLAUDE.md` y `AGENTS.md` (Cursor y otros agentes los leen) una sección
corta: «al empezar lee HANDOFF.md; al cerrar cada bloque corre estado/registrar.py».

Luego **reescribe** `ESTADO.json` con este repo. El ejemplo es ficción: no lo dejes
como estado real. Antes de escribir, averigua:

- ¿Ya hay `CLAUDE.md`, `AGENTS.md`, `HANDOFF.md`, `CHANGELOG.md`? ¿Cuál declara
  «el estado vive aquí»? Respeta ese archivo; el generador solo reemplaza el bloque
  entre `<!-- ledger:inicio -->` y `<!-- ledger:fin -->`.
- ¿Cómo se prueba y cómo se despliega aquí? ¿`git push` despliega, o hace falta
  otro comando?
- ¿Hay clientes, tenants o verticales? Cada entrada dice a cuál aplica.
- ¿Qué no puede ver el cliente? Eso va en `prohibido_publico` (ingresos, acuerdos,
  tokens, nombres en incidentes). El generador falla si `publico` contiene uno.

Estados válidos: `verificado`, `desplegado`, `construyendo`, `decide`, `detectado`.
Qué significa cada uno, y un ejemplo bueno y uno malo, está en `estado/ARQUETIPO.md`.

## Qué escribe el generador arriba del HANDOFF

0. Dónde me quedé — árbol, commit, pruebas, resumen por área con el porqué, en qué
   se cortó, comandos exactos de esta máquina.
1. Deuda de verificación — en producción, nadie lo ha visto.
2. Lo único por construir.
3. Lo que espera una decisión humana.
4. Detectado y no arreglado.
5. El tablero, si hay URL.

Cada entrada pendiente muestra también `Para el agente:` con su campo `interno`
(archivos, comandos para retomar), porque el HANDOFF es para agentes. El tablero
solo muestra `publico` y `prueba`.

El `▶ SIGUIENTE` apunta a la deuda de verificación si hay alguna. Si no, a lo que
se está construyendo. Si lo que sigue es una decisión, dice que no es código.

## Entregable de la primera instalación

1. `estado/ESTADO.json` lleno con el estado real, no con el ejemplo.
2. `HANDOFF.md` y `estado/tablero.html` generados.
3. El enlace del tablero, si el humano lo publicó.
4. Una línea de qué no se pudo verificar y por qué.
