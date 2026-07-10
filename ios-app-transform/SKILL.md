---
name: ios-app-transform
description: Convierte cualquier proyecto web (SaaS, landing, PWA) en una app iOS nativa SwiftUI que comparte backend, cuentas, contenido y reglas de negocio con el sitio — un solo repo, una sola fuente de verdad, todo manejable desde Claude Code. Triggers: "haz la app iOS", "convierte esto en app", "quiero subirlo a App Store", "app nativa de mi sitio", "iOS app transform".
---

# iOS APP Transform — de sitio web a app nativa ligada

Convierte un proyecto web en una app iOS nativa que NO es una copia: es un
segundo cliente del mismo cerebro. Referencia viva: Freqium
(`web/` Next.js + `ios/` SwiftUI en el mismo repo, freqium.com + iPhone).

## El modelo mental: los 3 tipos de sincronía

Antes de escribir código, explica esto al usuario (es SU duda #1):

1. **Datos de usuarios — sincronía instantánea, automática.**
   Cuentas, suscripciones, progreso viven en el backend (Supabase/Firebase/API),
   no en los clientes. Registrarse en el iPhone = existir en la web al segundo.
   No hay nada que "sincronizar": es la misma base de datos.
2. **Contenido y lógica — sincronía por flujo de trabajo.**
   Catálogos, precios y reglas de negocio tienen UNA fuente canónica en el repo
   (`shared/`). El usuario pide el cambio una vez; el agente actualiza ambos
   clientes porque el CLAUDE.md del proyecto se lo exige.
3. **Publicación — divergen, y es normal.**
   Web = deploy en segundos. iOS = revisión de Apple (1-2 días). Por eso todo lo
   que cambia seguido debe vivir en el backend, no compilado en la app.

## Fase -1 · Análisis del proyecto (siempre primero)

Detecta con comandos, no supongas:

```bash
# Stack y backend
cat package.json | grep -E "next|react|vue|supabase|firebase|stripe|lemonsqueezy"
grep -rn "createClient\|initializeApp" lib/ src/ --include="*.ts" | head -5
# Tablas / esquema que ambos clientes usarán
grep -ro "\.from('[a-z_]*'" lib/ app/ --include="*.ts" | sort -u
# Credenciales públicas del cliente (anon key ES pública; la seguridad es RLS)
grep -E "SUPABASE_URL|SUPABASE_ANON_KEY|FIREBASE" .env.local | sed 's/=.*/=***/'
# Identidad visual (para que la app se sienta de la misma marca)
grep -nE "^\s*--(accent|primary|brand)[a-z-]*:" styles/globals.css tailwind.config.*
```

Identifica: (a) auth y su proveedor, (b) tabla de entitlements/suscripciones,
(c) contenido canónico (¿archivos TS/JSON? ¿DB?), (d) qué feature es el corazón
del producto (eso se porta nativo primero), (e) modelo de pagos.

## Fase 0 · La unión (el pegamento — hazla ANTES que la app)

1. **`shared/content/`** — exporta el contenido canónico a JSON neutral:
   script `web/scripts/export-shared-content.ts` + npm script `export:content`
   (correr con `tsx`). La web sigue leyendo sus TS; iOS empaqueta los JSON.
2. **`PLATFORM_SPEC.md`** en la raíz — el contrato web↔iOS:
   backend compartido (URL + tablas), entitlements (tier efectivo = fila activa
   en la tabla de suscripciones), reglas de negocio NO NEGOCIABLES (límites
   freemium, seguridad), identidad visual (colores hex), y un checklist
   "si tocas X, actualiza Y".
3. **CLAUDE.md del proyecto** — sección "Platform Parity": contenido canónico +
   comando de export, esquema afecta a ambos clientes, `ios/project.yml` se
   edita y se regenera con `xcodegen` (NUNCA editar el .xcodeproj a mano),
   pagos divergen (IAP vs web) pero escriben a la misma tabla.

## Fase 1 · Proyecto iOS con XcodeGen

Por qué XcodeGen y no "Create New Project" en Xcode: el proyecto queda definido
en un `project.yml` de texto que el agente controla, reproducible, sin
conflictos de merge del .xcodeproj.

```bash
which xcodegen || brew install xcodegen
# Si xcodebuild falla con "requires Xcode": no uses sudo xcode-select, usa
DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer xcodebuild ...
```

`ios/project.yml` esencial:

```yaml
name: AppName
options:
  deploymentTarget: { iOS: "17.0" }
packages:
  Supabase: { url: https://github.com/supabase/supabase-swift, from: 2.5.0 }
targets:
  AppName:
    type: application
    platform: iOS
    sources:
      - path: AppName
      - path: ../shared/content     # contenido compartido → bundle
        buildPhase: resources
    dependencies: [{ package: Supabase, product: Supabase }]
    settings:
      base: { PRODUCT_BUNDLE_IDENTIFIER: com.marca.app, CODE_SIGN_STYLE: Automatic }
    info:
      path: AppName/Info.plist
      properties:
        UIBackgroundModes: [audio]   # solo si aplica (audio/location/etc.)
        ITSAppUsesNonExemptEncryption: false
```

`ios/.gitignore`: `AppName.xcodeproj/`, `xcuserdata/`, `DerivedData/`.

Estructura de código que funciona (Freqium):
```
ios/AppName/
├── AppNameApp.swift          # @main, EnvironmentObjects, .preferredColorScheme
├── RootView.swift            # TabView
├── Theme/Theme.swift         # colores hex de la marca web + Card modifier
├── Models/Models.swift       # Codable espejo de shared/content (CodingKeys = snake_case del JSON)
├── Content/ContentStore.swift # carga Bundle.main JSON, agrupa por categoría
├── Audio|Core/…Engine.swift  # el corazón del producto, NATIVO
├── Supabase/SupabaseService.swift # cliente + auth + entitlements
└── Features/{Auth,Library,Player,Profile}/…View.swift
```

## Fase 2 · Backend compartido en Swift

- **Misma URL + misma anon key que la web** (es pública; la seguridad es RLS).
- supabase-swift v2: `client.auth.signIn(email:password:)`,
  `for await change in client.auth.authStateChanges`,
  `client.from("t").select().eq(...).execute().value` (tipado con Decodable).
- **Entitlements**: lee la MISMA tabla que llena el webhook de pagos web
  (ej. `subscriptions`: `plan_id`, `status`). Tier efectivo = fila con status
  activo; mapea plan_id → tier con `contains` laxo. Sin fila → free.
- ⚠️ **Verifica RLS**: el usuario autenticado debe poder hacer SELECT de SU
  fila de suscripciones. Si el webhook escribe con service_role y no hay
  policy de lectura, la app siempre verá "free". Probar en dispositivo.

## Fase 3 · Reglas de negocio idénticas (donde se escapan los bugs)

Checklist de paridad — repásalo SIEMPRE contra la web:

- [ ] Límites freemium (ej. web limita sesiones a 5 min → iOS igual)
- [ ] Gating por tier (candados + sheet "tu suscripción funciona en ambos lados")
- [ ] Reglas de seguridad del dominio (ej. fades de audio, disclaimers médicos)
- [ ] Textos legales enlazados (privacy/terms del sitio — Apple los exige)
- [ ] Progreso del usuario escrito a las mismas tablas (rachas compartidas)

## Fase 4 · Lo nativo que la web no puede (el argumento de la app)

Porta el core como mejora, no como copia: audio en background + lock screen
(AVAudioEngine + MPNowPlayingInfoCenter + MPRemoteCommandCenter + UIBackgroundModes),
notificaciones push, widgets, HealthKit, cámara, háptica. Diseño SwiftUI nativo
con los colores de la marca — no un WebView.

## Fase 5 · Pagos (regla dura de Apple)

- Suscripciones digitales DENTRO de la app = **StoreKit 2 obligatorio**.
  Checkout externo (Stripe/Lemon Squeezy) dentro de la app = rechazo.
- Productos IAP espejo de los planes web. Al validar compra → upsert en la
  misma tabla de suscripciones con `platform: 'ios'`.
- Una compra en cualquier plataforma desbloquea ambas (ambas leen la misma tabla).

## Fase 6 · Verificación mecánica (nunca "ya quedó" sin comandos)

```bash
cd ios && xcodegen && DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer \
  xcodebuild -project AppName.xcodeproj -scheme AppName \
  -destination 'generic/platform=iOS Simulator' build 2>&1 | tail -3
# Recursos DENTRO del bundle compilado (si falta, la app se ve vacía):
ls ~/Library/Developer/Xcode/DerivedData/AppName-*/Build/Products/Debug-iphonesimulator/AppName.app/*.json
plutil -p .../AppName.app/Info.plist | grep -iE "backgroundmodes|bundleident"
# Integridad del JSON compartido vs modelos Swift (claves requeridas, refs huérfanas)
python3 - <<'EOF'
import json; d=json.load(open('shared/content/frequencies.json'))  # adapta
EOF
```

## Fase 7 · Camino a App Store (comparte estas fases con el usuario)

| # | Qué | Quién |
|---|---|---|
| 1 | Xcode → Signing & Capabilities → Team → ▶ en iPhone | Usuario (5 min) |
| 2 | Verificar RLS de entitlements desde el dispositivo | Agente |
| 3 | QA en dispositivo (/ios-qa si está instalado) | Agente |
| 4 | Progreso → tablas compartidas | Agente |
| 5 | Ícono + splash con el logo | Agente |
| 6 | StoreKit 2 + columna platform | Mixto |
| 7 | App Store Connect: ficha, screenshots, privacy labels | Usuario+agente |
| 8 | TestFlight → revisión de Apple → App Store | Usuario |

Notas de revisión de Apple: apps de salud/wellness necesitan disclaimers
("no es un dispositivo médico"); enlaces a "comprar en la web" dentro de la app
son terreno peligroso — mejor solo "gestiona tu suscripción en el sitio".

## Bugs conocidos que SIEMPRE hay que buscar (aprendidos en producción)

1. **Paridad freemium rota**: la app regala lo que la web cobra (límites de
   tiempo/cantidad no portados). Revisa el pricing de la web línea por línea.
2. **Transiciones sin fade** en audio/animaciones al cambiar de item mientras
   reproduce — respeta las reglas de seguridad del dominio.
3. **Lock screen desincronizado**: al pausar, actualiza
   `MPNowPlayingInfoPropertyPlaybackRate: 0` y el elapsed; con sesiones
   capadas, el total mostrado = duración de LA SESIÓN, no del contenido.
4. **RLS sin policy de SELECT** para el cliente → la app nunca ve el plan.
5. **Recursos compartidos fuera del bundle** → build verde pero app vacía.
   Verifica con `ls` dentro del .app compilado.
6. **xcodebuild apunta a CommandLineTools** → usa `DEVELOPER_DIR`, no sudo.

## Protocolo de auto-mejora (parte del skill, no opcional)

Cada vez que una conversión descubra algo nuevo (un bug-patrón, un truco de
XcodeGen/StoreKit, un rechazo de Apple y su causa):

1. Propón al usuario: *"Descubrí X — ¿lo adapto al skill para la próxima?"*
2. Con su OK: añade la lección a **Learnings** (append-only, con fecha) y,
   si cambia el método, actualiza la fase correspondiente.
3. Sincroniza a GitHub:
   ```bash
   cp ~/.claude/skills/ios-app-transform/SKILL.md ~/clawd/claude-skills/ios-app-transform/SKILL.md
   cd ~/clawd/claude-skills && git add -A && git commit -m "ios-app-transform: <lección>" && git push
   ```

## Learnings — append only

| Fecha | Lección | Contexto |
|---|---|---|
| 2026-07-08 | XcodeGen + project.yml permite que TODO el ciclo iOS viva en Claude Code; el usuario solo firma y pulsa ▶ | Freqium: proyecto generado y compilado sin abrir Xcode |
| 2026-07-08 | La anon key del backend puede ir embebida en la app (ya es pública en el bundle web); la seguridad real es RLS | Freqium: SupabaseService |
| 2026-07-08 | `sources: [{path: ../shared/content, buildPhase: resources}]` empaqueta el contenido compartido; verificar SIEMPRE con `ls` en el .app | Freqium: frequencies.json en bundle |
| 2026-07-09 | Los 3 bugs de paridad clásicos: freemium sin límite, transición sin fade, lock screen sin estado de pausa | Freqium: review post-scaffold |
| 2026-07-09 | Explicar los "3 tipos de sincronía" al usuario ANTES de que pregunte — es siempre su duda principal | Freqium: "¿cómo trabajamos ambos a la vez?" |
