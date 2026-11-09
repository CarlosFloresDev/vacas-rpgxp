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

## Estado final / orden de lotes

1. Protagonista y familia: Steven, madre, Perro y Lucy instalados y comparados. Lucy reverificada el 2026-11-09: referencia, dos retratos y sprite coinciden en moño rubio ceniza, bata pálida, vestido gris y tarro; lote_lucy.json presente.
2. NPCs completos: Cripps, Guernsey (retratos y rejilla de matadero), Benito, Encarna, Rubio, Chato, Sierra, Remedios, Anselmo, Molina, borracho, reclutador, transeúnte y vacas de corral/fondo. Rubio/Sierra conservan la hoja compartida autorizada por el juego.
3. Enemigos completos: nueve visiones de ENEMIGOS.json, ocho sustituciones y Vaca aprobada conservada; actor mental de Steven verificado y con manifiesto propio.
4. Sustos completos: siete, seis sustituciones y camión aprobado conservado; mismos motivos, nombres e IDs.
5. Fondos y objetos completos: tres battlebacks, seis hojas de objetos, tileset, autotile, título, gameover y windowskin. `vacas_vacio` conservado transparente.
6. Láminas 1x/2x generadas en `../capturas/fase2_personajes.png`, `fase2_enemigos.png` y `fase2_sustos.png`. Auditoría final: 72 PNG, 67 de fase 2 + 4 aprobados + 1 técnico, cero errores de tamaño/celdas/modo/ocupación/alpha técnica o integridad de archivos protegidos. Ver `verificacion_fase2.json` y `estado_fase2.json`.

## Problemas y decisiones

- `vacas_obrero2` es compartido por Rubio y Sierra (`contenido2.py`, 414 y 603). Sin editar eventos no se pueden ofrecer dos sprites distintos. Referencias y retratos deben ser compatibles con una silueta equipada común; conservar identidades narrativas separadas.
- Retratos Steven se comparten entre casa y trabajo: conservar camisa aprobada; el cambio de mono solo existe en sprite. No añadir heridas condicionadas en imágenes compartidas.
- La Guernsey usa la rejilla de `vacas_matadero`; la vaca canela del corral es otra identidad.
- No generar nuevas nieblas/luces integradas ni sustituir RTP de piso/calle: no hay slots autorizados ni archivos existentes que reemplazar.
- No marcar un personaje completo sin comparar todos sus assets adaptados con la referencia usando view_image.

## Para continuar

Leer biblia y este registro; consultar `inventario_fase2.json`. Adjuntar referencia correspondiente a cada llamada y neutral base a las expresiones. Guardar fuentes y prompts. Adaptar manteniendo tamaños del inventario y comprobar frente a respaldo. No ejecutar generadores de mapas, BD, eventos ni scripts.

### Continuación: Guernsey

- Referencia frontal/lateral y retratos neutral/susurro generados en la nube, guardados y comparados con view_image. Rombo crema, canela, cuernos y ojo castaño coherentes; susurro compuesto solo en rostro. lote_guernsey.json y prompt_guernsey_*.json.
- Rejilla cotidiana confirmada en contenido2.py: dirección 8, patrón 0 de vacas_matadero. Esa celda se adapta en el lote de objetos para conservar toda la hoja indexada. No tiene sprite independiente; vaca_canela es otra identidad.


### Rubio: instalado

- Referencia frontal/lateral, retrato neutral y hoja compartida vacas_obrero2 generados con image_gen; fuentes y prompts guardados. Adaptación lote_rubio.json: 240x340 y 128x192/celda 32x48. Comparados con view_image: rubio visible, casco crema, gafas, respirador, mono y guantes coherentes. Equipo compatible con Sierra; identidades distintas.
- La fuente muestra color de fondo residual, pero alpha real 0–254; el umbral 128 lo elimina. Sin GPU local. Caminata en motor pendiente.


### Chato: instalado

- Referencia existente inspeccionada; retrato y sprite generados adjuntando referencia. lote_chato.json conserva 240x340 y vacas_obrero4 128x192/celda 32x48. Comparados con view_image: rostro ancho, nariz achatada, pelo castaño, mono gris, cinturón y puños marrones coherentes. Fuentes y prompts guardados.


### Sierra: instalado

- Referencia propia frontal/lateral y retrato neutral generados y comparados con view_image, además del sprite compartido vacas_obrero2. Mandíbula/hombros más anchos y pelo rubio oscuro; mismo equipo protector compatible con Rubio. lote_sierra.json instala solo el retrato 240x340. No se añade hoja ni se modifican eventos.


### Remedios: instalada

- Retrato y sprite comparados con referencia frontal/lateral usando view_image: anciana encorvada, moño canoso, chal oscuro, vestido marrón gris y manos entrelazadas. lote_remedios.json: retrato 240x340, hoja 128x192/celda 32x48. Fuentes y prompts guardados.


### Anselmo: instalado

- Referencia, retrato y sprite comparados con view_image: anciano delgado, bigote gris ancho, entradas, chaqueta marrón con codos remendados. lote_anselmo.json conserva retrato 240x340 y hoja 128x192/celda 32x48; fuentes/prompts guardados.


### Molina: instalado

- Referencia, retrato molina y sprite vacas_carnicero comparados con view_image; bigote oscuro, brazos robustos, camisa crema y delantal burdeos coherentes. lote_molina.json conserva 240x340 y 128x192/celda 32x48. Fuentes y prompts guardados.


### Borracho: instalado

- Referencia, retrato y sprite comparados con view_image: abrigo largo gastado, barba incipiente, nariz roja y botella verde. lote_borracho.json mantiene 240x340 y 128x192/celda 32x48. Fuentes y prompts guardados; animación en motor pendiente.


### Reclutador y transeúnte: instalados

- Referencias, sprite y retrato del reclutador comparados con view_image: gorra/chaqueta gris y carpeta ocre coherentes; lote_reclutador.json. Transeúnte: referencia y sprite comparados, impermeable y sombrero gris de poco contraste, sin paraguas; lote_transeunte.json. No existe retrato suyo en inventario. Tamaños originales preservados.
- Corrección del borracho: inspección detectó filas desiguales en fuente. source_rows=[0,392,740,1097,1536] en lote_borracho.json preserva poses completas, sin restos entre filas. Reinspeccionado tras readaptar. Soporte opcional añadido solo al adaptador de arte.


### Vacas cotidianas: instaladas

- Referencias y ambas hojas comparadas con view_image: corral crema/parches marrón y fondo canela sin rombo, ambas con anatomía bovina pesada y pezuñas. lote_vaca_corral.json y lote_vaca_canela.json preservan 320x320/celda 80x80. La hoja canela usa límites de fila explícitos para no cortar pezuñas. Fuentes/prompts guardados.
- NPCs cotidianos completos salvo celda de rejilla Guernsey, reservada a la hoja vacas_matadero del lote de objetos. Se continúa con las nueve visiones.


### Visiones: Madre de yeso instalada

- Referencia cotidiana y battler adaptado comparados con view_image: moño, cara pesada y bata mostaza reconocibles; yeso roto, manos enormes y bajo hueco. lote_enemigo_madre.json conserva 320x300 con alpha. Fuentes/prompts guardados.
- Vaca de la muestra y screamer_3 inspeccionados nuevamente; se conservan aprobados, referencia vaca_vision generada desde la fuente aprobada.


### Visiones: Sombra de Cripps instalada

- Referencia y battler adaptado comparados con view_image: rapado, cuello grueso, camisa gris, delantal marfil y correas conservados; manos fundidas con ganchos y silueta prolongada. lote_enemigo_sombra_cripps.json, 320x300 con transparencia. Fuentes/prompts guardados.


### Visiones: túnel y Guernsey instalados

- Cada referencia y battler adaptado comparados con view_image. Túnel conserva cuerpo largo sin rostro, huesos y ojos al fondo del conducto. Guernsey conserva canela, rombo y ojo castaño, con cuernos-tubería y costillas expuestas; humo con semitransparencia (sin alpha_threshold). lote_tunel_guernsey.json: ambos 320x300. Fuentes/prompts guardados.


### Visiones: canal instalada

- Referencia frontal/lateral y battler comparados con view_image: canal suspendida, gancho, costillas-barrotes, grasa y vísceras con peso. lote_enemigo_canal.json, 320x300 con alpha. Fuentes/prompts guardados.
- Incidencias en iteración: primer Rey rechazado por servicio; se reintenta composición con ropa completa y sangre sobre camisa. Primera moscas copió el motivo bovino de la referencia de estilo: fuente conservada como descartada, nunca instalada; se regenera desde su referencia propia. Familia de nieve requiere tres adultos: primera referencia conservada como descartada y corregida antes de generar battler.


### Visiones: enjambre y Rey instalados

- Segunda fuente del enjambre comparada con referencia y battler adaptado usando view_image: cara incompleta de insectos con huecos alpha, sin cabeza bovina. lote_enemigo_moscas.json conserva semitransparencia de alas y 320x300.
- Rey: reintento correcto; Steven reconocible, camisa marrón, corona de ganchos y espejo fragmentado; comparado con referencia y adaptado 320x300, lote_enemigo_rey.json. El servicio no produjo fuente en el primer intento rechazado. Fuentes/prompts de reintentos guardados.
- Auditoría detectó que steven_mente ya instalado no tenía entrada en manifiesto: se añade lote_steven_mente.json con los parámetros documentados, sin regenerar identidad. Battler existente vuelto a inspeccionar contra referencia.


### Nueve visiones: lote completo

- Familia de nieve: referencia corregida (tres adultos) y battler adaptado comparados con view_image; gabinete, antena, caras de estática y cables coherentes. lote_enemigo_televisor.json, 320x300 con alpha.
- Nueve enemigos de ENEMIGOS.json disponibles y revisados: ocho sustituciones y Vaca aprobada conservada. El actor steven_mente también conserva identidad y tamaño. Se continúa con sustos, sin cambiar IDs ni motivos.


### Sustos 2, 5 y 7: instalados

- Referencias y adaptados comparados con view_image: familia de tres adultos/estática, ojo castaño de Guernsey tras rejilla con rombo parcial, Steven/corona/reflejo. lote_sustos_2_5_7.json conserva IDs y 640x480 opacos. Fuentes/prompts guardados.
- Servicio rechazó primer espejo, referencia sumidero y primer capataz; se reintentan sin heridas explícitas conservando los motivos. No se instala ninguna fuente rechazada.


- Corrección técnica: destinos accidentales Graphics/0,1,2 del primer lote de sustos retirados; manifiesto corregido a Pictures, readaptado y reinspeccionado. El adaptador ahora rechaza carpetas ajenas a RGSS1 y la auditoría rechaza destinos fuera del inventario.


### Siete sustos: lote completo

- Espejo, sumidero y capataz reintentados correctamente conservando motivo, con grietas/óxido/sombra en vez de heridas abiertas. Adaptados y comparados con sus referencias usando view_image. lote_susto_1.json y lote_sustos_4_6.json. Todos 640x480 opacos; screamer_3 aprobado conservado. No se modifican IDs, tiempos ni disparadores.
- Fuentes de los siete y prompts de cada llamada/reintento disponibles. Los rechazos del servicio no dejaron imágenes fuente. Comienza lote de fondos/objetos.


### Fondos de combate: instalados

- Tres fuentes originales generadas en nube desde referencias de uso. Comparados referencia/fuente/adaptado con view_image: piso nicotina, matadero clínico y túnel verde negro; centros despejados, periferia oscura. lote_fondos.json conserva 640x480 opacos; sin enemigos ni texto. No se copiaron texturas del arte anterior.


### Objetos pequeños: instalados

- Fuente, respaldo y adaptación comparados con view_image: cuencos vacío/lleno, plato, charco, nota, botellas, cenicero y cesta en sus ocho índices; filas inferiores vacías conservadas. lote_cosas.json: 128x128/celda 32x32.
- Tipo indexed en adaptar_arte.py usa ocupación y anclas de cada celda del respaldo, sin inventar caminata. No modifica mapas ni índices. Primera fuente de muebles conservada como descartada: se retiran detalles orgánicos no solicitados debajo de las teles cotidianas antes de instalar.


### Matadero, puertas y furgoneta: instalados

- Respaldo, fuentes y adaptados comparados con view_image. Matadero: cinta, canales, herramientas y cuatro estados de rejilla en los mismos índices; ojo/hocico coherentes con referencia Guernsey. Puertas: estados cerrado/parcial/abierto en sus celdas. Furgoneta: una fuente original repetida idéntica dieciséis veces, conserva celda 96x64 y hoja 384x256, rótulo municipal.
- lote_matadero_puertas_furgoneta.json mantiene tamaños y anclas de respaldo. Guernsey cotidiana queda completa incluida rejilla; no se cambian eventos.


### Muebles y tablón: instalados

- Respaldo, fuentes finales y adaptados comparados con view_image; teles cotidianas corregidas sin tejidos/cables, estados de pantalla preservados, demás muebles en sus índices. lote_muebles_tablon.json: muebles 128x256/celda 32x64.
- Tablón 128x192/celda 32x48 conserva los paneles anchos que abarcan DOS celdas en las filas superiores, además de cartel/buzón/poste/corona en filas inferiores. Adaptación resize indexada con alpha del respaldo para no separar esos paneles como objetos distintos.
- Se corrigieron límites de filas de fuente matadero: cinta vuelve a ocupar ancho completo32, sin fragmentos del gancho de fila siguiente. Resultado reinspeccionado.


### Tiles, autotile y pantallas: instalados

- Respaldo/fuente/adaptado comparados con view_image. Tileset 256x256,64 tiles32x32 con mismos tipos, huecos y uniones; autotile384x128 con cuatro marcos96x128 y cuartos16x16, materiales rojo/azulejo. lote_tiles_autotile.json conserva alpha técnica exacta y distribución. Mezcla de geometría de layout20% solo en tileset.
- Título y gameover640x480 comparados con fuente y referencia: textos completos, gameover dividido en dos líneas para corregir recorte original. Windowskin192x128 conserva máscaras técnicas de frame/cursor/flechas y fondo oscuro; lote_pantallas_ventana.json. Fuentes y prompts guardados.
- Todos los recursos del inventario están ahora sustituidos o conservados expresamente. Se ejecuta auditoría final y revisión de láminas.

### Cierre de la continuación — 2026-11-09

- **48 PNG nuevos instalados** en esta continuación; Lucy ya existente verificada sin regeneración. Cobertura final: **67 PNG de fase 2, cuatro aprobados de fase 1 conservados byte a byte y un recurso técnico transparente intacto**. No quedan assets pendientes del inventario.
- `verificacion_fase2.json`: **72 PNG, cero errores**, mismos tamaños/modos/celdas que inventario y respaldo. Hojas indexadas: ocupación vacía/llena y anclas conservadas; máscaras técnicas de tiles/autotile/windowskin verificadas; dieciséis celdas de furgoneta idénticas. Hashes de Data y scripts protegidos intactos. No se ejecutaron ni editaron generadores de mapas, BD, eventos o scripts; no se tocó `.git`.
- Fuente y prompt de cada generación guardados. `PROMPTS_CONTINUACION.json`: 70 llamadas, 63 salidas aceptadas (48 recursos + 15 referencias), tres descartes visuales y cuatro rechazos del servicio sin fuente. Incluye hashes de entradas/salidas y referencias antiguas congeladas en el respaldo. Los descartes nunca se instalan. Parámetros reproducibles en los manifiestos `lote_*.json`; [detalles de adaptación](ADAPTACION_FASE2.md).
- Láminas finales 1×/2×: `../capturas/fase2_personajes.png` (3024×10400), `fase2_enemigos.png` (3024×3000), `fase2_sustos.png` (1968×7180). Revisión de disposición y muestras a escala legible con view_image. Lámina adicional `fase2_objetos_fondos.png` y composición estática de ventana `fase2_ventana_muestra.png`.
- El manifiesto recuperado de Steven mental reproduce exactamente los píxeles del battler instalado. Verificada la denegación de una ruta ajena a las carpetas RGSS1 sin escribir archivos. Retirados todos los archivos/carpetas accidentales de la primera adaptación de sustos, incluidos sus respaldos creados en esta continuación; originales válidos conservados.
- **Pendiente de revisión dentro de Game.exe:** caminata, mezcla con tonos/Fogs y veneno, lectura del menú/título y diálogo, ritmo y encuadre de sustos durante un recorrido. La muestra estática de windowskin es legible; no sustituye esa prueba del motor. No se afirma haberla ejecutado en esta continuación.
- Limitaciones conservadas: Rubio/Sierra usan una hoja equipada compartida y retratos/referencias propios. Espejo/sumidero/capataz y Rey mantienen sus motivos con menos heridas abiertas tras los rechazos del servicio; el gore explícito de las otras visiones permanece. No se amplían slots ni se sustituyen recursos RTP externos de piso/calle.

