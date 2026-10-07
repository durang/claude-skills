# Arquetipo del ledger

Una fuente (`ESTADO.json`) genera dos salidas. No se editan las salidas.

## Estados

| Estado | Significa | Sale en el tablero público como |
|---|---|---|
| `verificado` | Alguien lo vio funcionar, y `evidencia` dice cómo | Listo |
| `desplegado` | Compiló, pruebas verdes, el sitio responde. Nadie lo vio en pantalla | En producción, falta verlo |
| `construyendo` | Es lo que se está haciendo | En curso |
| `decide` | No es código. Espera una decisión humana | Falta una decisión |
| `detectado` | Se vio el problema y no se arregló | Solo si tiene texto `publico` |

`verificado` con `evidencia` vacía es un error: el generador no escribe nada y sale con código 1.

## Dos audiencias

- `interno` — archivos, el porqué, qué se rompe si se cambia. Nunca va al HTML.
- `publico` — la misma cosa, para quien la va a usar. Sin rutas, sin cifras internas, sin los términos de `prohibido_publico`.
- `prueba` — pasos que puede seguir alguien que no programa.
- `evidencia` — qué se comprobó y cómo. Vacío si no se comprobó.

`publico` es obligatorio salvo en `detectado`.

## Bien

```json
{
  "id": "aviso-portada",
  "titulo": "El aviso de ventas sin registrar",
  "estado": "desplegado",
  "fecha": "2026-10-01",
  "interno": "lib/ventas-pendientes.ts. La antigüedad usa updated_at: diasPendiente devolvía 0 cuando no había vendedor, y el aviso decía 'hoy' sobre ventas de hace meses.",
  "publico": "En la portada del panel aparecen las ventas que se marcaron vendidas y todavía no se registraron. Las de más de dos semanas van aparte.",
  "prueba": "Entra al panel. Si hay alguna venta sin registrar, el aviso está arriba del inicio.",
  "evidencia": ""
}
```

`desplegado` y evidencia vacía es honesto: está afuera y nadie lo ha mirado.

## Mal

La misma entrada con `"estado": "verificado"` y `"evidencia": ""`. El generador la rechaza.
También es malo un `publico` que dice la comisión, el ingreso o el nombre de un archivo:
eso es `interno`.
