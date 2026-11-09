# Fase 2 — registro de producción

Inicio: 2026-11-09. Muestra 10d731b aprobada íntegramente. No se modifica Data ni scripts; no hacer commit. Herramientas de imagen: image_gen integrado y adaptar_arte.py, sin GPU local.

## Hecho

- Lectura de guía, prompts/fuentes de Fase 1, sistemas, plan, actos I–II y enemigos.
- `../BIBLIA_PERSONAJES.md` creada antes de generar: rasgos, ropa con hex, cambios de acto, alias, restricciones de hojas compartidas.
- Inventario y hashes iniciales en `inventario_fase2.json`; respaldo de originales existentes en `../arte_provisional/sd_v1/Graphics/`, sin sobreescribir respaldos anteriores.
- Hashes de Data y scripts en `protegidos_fase2.json` para comprobación final.
- Referencia Steven frontal/lateral de cuerpo entero: `referencias/steven.png`, derivada de retrato y sprite aprobados. Inspeccionada con view_image: pelo, camisa marrón, bolsillo y cara coherentes. Fondo oscuro generado a pesar de solicitar alpha: utilizable como referencia, no como sprite recortable.

### Steven: primer lote instalado

- Nuevos: `retrato_steven_miedo.png`, `vacas_steven_mono.png`, `steven_mente.png`. Se conservan neutral y sprite de calle aprobados.
- Referencia, ambos sprites, ambos retratos y battler inspeccionados con view_image. Pelo negro, camisa marrón, bolsillo y rostro coherentes; mono como cambio narrativo de ropa.
- Miedo reutiliza literalmente base aprobada fuera de polígono facial mediante `expression_base` en adaptar_arte.py. Parámetros reproducibles en `lote_steven.json`.
- Battler: adaptar fuente `steven_mente_fuente.png` como battler, size 240x340, max_height 340, alpha_threshold 128, resample box.
- Corrección de nota anterior: la referencia tiene alpha real (0–254), el visor muestra color residual en zonas transparentes. La hoja del mono también: alpha 0 en fondo y ~252 en figura; umbral 128 elimina halo.
- Pendientes relacionados, para sus lotes posteriores: enemigo_rey y screamer_7. Caminata dentro del motor no probada.

### Madre: lote cotidiano instalado

- Referencia `referencias/madre.png`, neutral e ira y sprite 192x268 (celdas 48x67), comparados con view_image. Bata mostaza, moño bajo, puños oscuros, cara ancha y complexión coherentes.
- Reproducible mediante `lote_madre.json`; ira compuesta solo dentro del rostro. `pad_grid` añade hasta 3 píxeles transparentes al borde de fuentes que no sean múltiplo de cuatro, sin reordenar celdas.
- Pendientes en lotes de enemigos y sustos: Madre de yeso y screamer_1.

### Perro: instalado

- Referencia frontal/lateral, retratos neutral y miedo, sprite 160x160 (40x40), generados e inspeccionados con view_image; sin collar, mismo patrón marrón/crema, patas traseras arrastradas.
- Miedo desde neutral con composición facial; parámetros en `lote_perro.json`. No tiene battler propio en inventario.

### Lucy: instalada

- Referencia, sprite y dos retratos comparados con view_image. Mismo moño rubio ceniza, bata pálida, vestido gris y tarro vacío; susurro desde neutral con máscara facial. `lote_lucy.json` reproduce el lote.
- Primer lote cotidiano completo: Steven, madre, Perro y Lucy. 12 PNG nuevos instalados; se conservan 2 PNG aprobados de Steven. Visiones y sustos asociados quedan para sus lotes.

### Cripps: instalado

- Referencia, sprite 168x240/celda 42x60, neutral e ira comparados con view_image; rapado, camisa gris, delantal marfil con correas marrones. `lote_cripps.json` reproduce el lote.
- Pendientes de lotes posteriores: enemigo_sombra_cripps y screamer_6.

### Benito: instalado

- Referencia frontal/lateral, retrato neutral y `vacas_obrero1` comparados con view_image. Mismo rostro veterano, canas, mono y remiendo. Parámetros: `lote_benito.json`.
- Cripps se readaptó sin cuantización de zona: la paleta matadero convertía grises cálidos en carne; la fuente conserva mejor camisa gris/delantal marfil. Revisado tras corregir.

### Encarna: instalada

- Referencia inspeccionada además sobre fondo gris (`capturas/referencia_encarna.png`) para evitar oscurecimiento del visor por alpha. Retrato y sprite `vacas_obrero3` comparados; misma redecilla, uniforme, delantal y guantes. `lote_encarna.json`.

## En curso / orden de lotes

1. Protagonista y familia: Steven, madre y Perro instalados y comparados; Lucy tiene referencia frontal/lateral generada y revisada, faltan retratos y sprite.
2. NPCs: Cripps, Guernsey, Benito, Encarna, Rubio, Chato, Sierra, Remedios, Anselmo, Molina, borracho, reclutador, transeúnte; vacas de corral/fondo.
3. Enemigos: las nueve visiones de ENEMIGOS.json.
4. Sustos: siete, conservando motivos e IDs.
5. Fondos y objetos: battlebacks, hojas de muebles/objetos, furgoneta, puertas, tablón, tileset, autotile, título, gameover, windowskin. `vacas_vacio` se conserva transparente.
6. Láminas 1x/2x: `../capturas/fase2_personajes.png`, `fase2_enemigos.png`, `fase2_sustos.png`; verificación de tamaños/celdas y referencias.

## Problemas y decisiones

- `vacas_obrero2` es compartido por Rubio y Sierra (`contenido2.py`, 414 y 603). Sin editar eventos no se pueden ofrecer dos sprites distintos. Referencias y retratos deben ser compatibles con una silueta equipada común; conservar identidades narrativas separadas.
- Retratos Steven se comparten entre casa y trabajo: conservar camisa aprobada; el cambio de mono solo existe en sprite. No añadir heridas condicionadas en imágenes compartidas.
- La Guernsey usa la rejilla de `vacas_matadero`; la vaca canela del corral es otra identidad.
- No generar nuevas nieblas/luces integradas ni sustituir RTP de piso/calle: no hay slots autorizados ni archivos existentes que reemplazar.
- No marcar un personaje completo sin comparar todos sus assets adaptados con la referencia usando view_image.

## Para continuar

Leer biblia y este registro; consultar `inventario_fase2.json`. Adjuntar referencia correspondiente a cada llamada y neutral base a las expresiones. Guardar fuentes y prompts. Adaptar manteniendo tamaños del inventario y comprobar frente a respaldo. No ejecutar generadores de mapas, BD, eventos ni scripts.
