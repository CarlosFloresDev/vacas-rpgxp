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

### Acto III «Lucy» — 2026-11-09

Ampliación de contenido autorizada después del cierre de fase 2. Esta vez sí se modifican mapas, BD y scripts para implementar el acto. El informe histórico anterior sigue describiendo su propia entrega; sus hashes protegidos de Data no son el estado actual del proyecto.

- **11 PNG nuevos instalados**, sin sustituir los 72 recursos anteriores: dos expresiones de Lucy (calma/quiebre), retrato neutral y hoja de Elena, cuatro battlers (Tarro, Factura, Camilla y Diagnóstico), sustos 8/9 y hoja de 16 objetos de hospital/laboratorio. Se mantienen dimensiones RGSS1: bustos 240×340, battlers 320×300, sustos 640×480, Elena 128×192/celda 32×48, objetos 128×256/celda 32×64.
- **16 generaciones en nube con image_gen, sin GPU local**: 11 recursos y cinco referencias frontal/lateral. Identidades nuevas en `referencias/elena.png`, `tarro.png`, `factura.png`, `camilla.png` y `diagnostico.png`. Lucy usa su referencia existente y el neutral aprobado. Los PNG fuente y los 16 prompts exactos quedan en `acto3/`; adaptación reproducible con [acto3/manifest.json](acto3/manifest.json) mediante `adaptar_arte.py`.
- Las dos expresiones usan máscara facial sobre el neutral y `preserve_canvas`, añadido al adaptador para conservar literalmente cuerpo, manos, tarro, ropa y alpha. La auditoría verifica alpha idéntica y píxeles bajo el rostro. No se modifica el neutral. Elena mantiene rizos grises, cárdigan carbón, blusa azul y llaves en referencia, sprite y retrato. Referencias y salidas revisadas con `view_image`.
- Los cuatro enemigos conservan identidad entre referencia, battler y susto cuando corresponde. Diagnóstico es una silla vacía dentro de un tarro; no convierte a Lucy en monstruo ni añade heridas al personaje. La nueva biblia documenta las entidades.
- Objetos: cama, cortina azul, microscopio, tarros, hígado, riñón, gotero, reactivo, sofá, tetera, lámpara, pinza, fichero, taburete, armario y lavabo. Son objetos estáticos indexados, fijando dirección/patrón; no son una caminata. Layout técnico separado y fuente original preservada. No se generan tiles nuevos porque se reutiliza el tileset 51 aprobado y sus pasajes.
- [acto3/verificacion.json](acto3/verificacion.json): **11 assets, cinco referencias, 16 prompts, cero errores; 72 PNG anteriores sin cambios**, con hashes de fuentes y salidas. Lámina: [acto3_arte.png](../capturas/acto3_arte.png). Renders de los cinco mapas: `../capturas/acto3_12.png` a `acto3_16.png`, con eventos de primera página y marcadores técnicos invisibles en el juego.
- Contenido jugable: cinco mapas, 46 eventos en los mapas nuevos y un acceso añadido en la calle, diálogos VN, tres preparaciones de inventario y control limpio, veneno/huella, persecución de persiana con refugio y capturas recuperables, tres visiones opcionales, jefe obligatorio, relación con Lucy y elección final conservada para Acto IV. Guía y recorrido en [ACTO_III.md](../ACTO_III.md).
- Nuevos rangos: interruptores **81–107** (87/89 reservados), variables **19–23**, objetos **14–29**, enemigos/tropas **10–13**, sustos **8–9** con marcas **99/100** e imagen **98** existente. Nombres y usos documentados en SISTEMAS.md. Se conserva la continuidad 34–36 y 38. Atajo: **Ctrl + Nueva partida**; **Ctrl+Mayús** prueba resistencia.
- Respaldo completo anterior a la primera escritura: `../respaldos/antes_acto3_20261109_185019/Data/`. Sin commits ni escrituras en `.git`.
- **Verificación real en Game.exe:** 31 rxdata cargados y serializados por Marshal RGSS1; 16 spritesets; retratos VN nuevos; sustos y limpieza; los cuatro accesos de Nueva partida; progresión completa por ambas ramas y decisiones; conservación de muestras tras captura/tiempo agotado y refugio; control obligatorio y ausencia de duplicados; 120 simulaciones y batalla completa del jefe nativo. Main original restaurado tras cada arnés. Regresión anterior de I/II también completada. Logs en `../verificacion_rgss_acto3.txt` y `../verificacion_rgss.txt`.
- Validación: **99 scripts** con Ruby portable; **871 referencias** sin ausencias; **16 mapas y 67 transferencias** sin errores; auditoría XP en seis estados narrativos. Se corrigió el fallo compartido `Tone != nil` al restaurar la pantalla tras combate. Las primeras pruebas también permitieron corregir un nombre de BGS y un setter de RGSS1 antes de la entrega.
- **Pendiente:** revisión humana del ritmo del texto, persecución, mezcla sonora y composición durante una partida completa; desarrollo del Acto IV. Las pruebas automatizadas ejecutan el intérprete y las escenas reales, pero no sustituyen esa valoración. No queda arte provisional nuevo ni funcionalidad del Acto III pendiente.

### Escala de objetos — 2026-11-09

- Regla: baldosa 32 px, celda humana 48 px y silueta visible de Lucy/Steven **40 px**. Frascos 10–16 px; microscopio 24 px sobre mesa; lámpara 38 px, menor que el personaje; asientos 26–28 px. Composiciones modificadas apoyadas en el borde inferior de sus celdas, conservando proporciones, dimensiones de hoja e índices.
- `vacas_laboratorio.png`: frasco azul **63→14 px**, tarros **24→14**, microscopio/mesa **64→48** (instrumento 24 + mesa 24), bandejas **28→16**, gotero **64→56**, tetera/taburete **47→36** (12 + 24), lámpara **64→38**, pinza/paño **40→14**, fichero **64→48**, taburete **50→26**, armario **63→56**, lavabo **51→30**. Cama/cortina de 64 px y sofá de 28 px conservados: la cama se compara como longitud.
- Actos I/II: `vacas_muebles.png`, ocho estados de TV **38→32**, inodoro **37→28**, sillón **33→28**; `vacas_cosas.png`, cuencos **13→8**, plato **15→8**, nota **20→16**, botellas **20→14**, cenicero **11→6**, cesta **18→14**; `vacas_matadero.png`, panel **36→32**, herramienta **41→24**, cubo **23→20**. Medidas de altura visible. Puertas, tablones/señales, furgoneta, canales, armarios anteriores y cajas auditados y conservados.
- Cuatro hojas readaptadas desde fuentes guardadas, sin generaciones nuevas. Reglas reproducibles por índice y componente en `lote_escala.json`, en los manifiestos originales y en `adaptar_arte.py`. Verificación de siete hojas, ocupación, alturas, apoyo inferior y reproducción exacta desde fuentes en `verificacion_escala.json` y `verificar_escala.py`.
- **14 capturas regeneradas y abiertas**, con personajes y objetos a la misma escala en una franja: `acto3_12..16.png`; `mapa2_el_piso.png`, `mapa2_salon_y_cocina_x2.png`, `mapa3_la_escalera.png`, `mapa4_la_calle.png`; `acto2_mapa5/8/9/10/11_eventos.png`. El detalle 2× amplía también la franja. Lámina completa antes/después: `escala_auditoria_completa.png`, dividida en `escala_auditoria_1..4.png`. Las escenas muestran primera página; las franjas incluyen también objetos de otras páginas.
- Originales de hojas/capturas en `../respaldos/antes_escala_20261109/`. **Data y .rxdata intactos**, comprobados mediante hashes; sin mover eventos/frames ni tocar `.git`. Verificación visual estática completada; no se ejecutó una partida interactiva en esta corrección.

### Revisi?n ambiental de mapas I?III ? 2026-11-09

- Auditados e intervenidos los 16 mapas; escala previa conservada y siete hojas verificadas. Laboratorio 25?20?20?15: ?40 % total, ?46,2 % de rect?ngulo interior, puestos pr?ximos, estantes de frascos, camilla manchada, papeles, cables/tubos, embalajes, residuos, l?mparas, tono verde y niebla ligera. Transferencia al laboratorio actualizada a (10,12).
- Nuevos tilesets por mapa y m?scaras de luz; originales conservados. Data y capturas respaldados antes de escribir en `../respaldos/antes_revision_mapas_20261109_193433/`; primera iteraci?n de hojas tambi?n respaldada. Sin escrituras en `.git`.
- Cero regresiones interactivas frente al respaldo: 18360 comprobaciones / 90 estados. Actos I?II: 78 escenarios sin problemas; acto III: 485 comprobaciones sin errores. Ambos arneses Game.exe pasan y restauran Main; conectividad y 939 referencias de recursos correctas.
- Capturas de los 16 mapas regeneradas; comparativa `../capturas/revision_mapas.png` y cuatro partes abiertas, m?s laboratorio a escala legible. Informe por mapa, tama?os y l?mites en [REVISION_MAPAS.md](../REVISION_MAPAS.md). Pendiente: valoraci?n humana del recorrido y ambiente; las capturas no simulan el tono narrativo ni la niebla animada.


### Acto IV «Bajo la ciudad»: continuación completada — 2026-11-09

- Recuperados mapas 17–21 y herramientas interrumpidas, conservando `../respaldos/antes_acto4_20261109_194935/Data/`. No se repitió el respaldo ni se escribió en `.git`; cambios previos conservados. Cinco mapas compactos, 47 eventos, linterna RGSS con batería/veneno, manada/reputación, VN, dos cazas con refugios, dos puzles, tres visiones y jefe, dos sustos y pacto. [Guía e IDs](../ACTO_IV.md), [sistemas](../SISTEMAS.md).
- **13 PNG instalados**: tileset 256×64, objetos 128×256/celda 32×64, tres vacas 192×192/celda 48×48, dos retratos 240×340, cuatro battlers 320×300 y dos sustos 640×480. [Manifiesto reproducible](acto4/manifest.json), fuentes, hashes y prompts nuevos guardados. **Seis llamadas image_gen en nube, cinco fuentes aceptadas**: sprite Junco, tiles, objetos y dos retratos. Edición de retratos dobles descartada por fondo residual y conservada sin instalar. Sin GPU local. Se reutilizan fuentes recuperadas; Guernsey canela aprobada; Cencerro/Pastor recortados de referencia y sustos reencuadrados de Coro/Pulmón. No estaban disponibles los prompts originales de las seis fuentes recuperadas; no se inventan.
- Escala: celdas nuevas de 48 px, siluetas ≤44; Steven conserva 40 px. Pila 14, etiqueta 12, botas/mapa ≤16 px; proporciones/apoyo y límites por índice documentados. Filas desiguales de sprites corregidas. Siete hojas históricas pasan `verificar_escala.py --permitir-data-modificada`; Data cambia legítimamente por el acto nuevo. [Lámina de arte](../capturas/acto4_arte.png) y renders `acto4_17.png` a `acto4_21.png` generados y abiertos. Son vistas estáticas con marcadores técnicos; no simulan tono ni niebla/cono animados.
- Atajo **Alt + Nueva partida**, confirmar con Z; añadir Mayús prueba 97, sin Mayús 96. Continuación normal desde el III o hospital. Switches **113–139**, variables **51–56**, objetos **30–34**, enemigos/tropas **14–17**, sustos **10–11**. Pacto 132, alternativas 133/134 y ruta V 135; decisiones heredadas conservadas.
- **Verificación:** 1.210 comprobaciones/16 estados sin errores; 983 referencias sin ausencias; 21 mapas/84 transferencias válidas sin avisos; 101 scripts con Ruby portable. `../verificacion_rgss_acto4.txt`: Game.exe/RGSS104E real en 96/97 × ambos pactos, seis accesos de título, entrada física, puzles, capturas/contacto/tiempo/refugios, batería/veneno, 21 spritesets, retratos/sustos, 120 simulaciones y batalla nativa del Pastor. Main restaurado. Corregidos intérprete y `Range#step` incompatibles con RGSS1; accesos de eventos con comando 201 explícito. La llegada automática no requiere acceso físico; auditoría renovada sin abrir agua ni paredes.
- **Pendiente:** revisión humana de recorrido, texto, persecuciones, sonido y luz/niebla; actos V–VI. El arnés evita esperas de foco de Graphics y no equivale a partida manual. Un intento adicional de captura de ventana normal agotó 55 s sin imágenes, restauró Main y sus auxiliares se retiraron. Se entregan capturas estáticas revisadas. No quedan recursos ausentes ni bloqueos conocidos en los escenarios auditados.

### Interfaz propia completa — 2026-11-09

- Nueva capa `Vacas_Interfaz`, después de BajoCiudad: título y Game Over animados, pausa, objetos, estado/cordura, notas, archivos, ajustes persistentes, presentación del combate mental, HUD integrado y VN con indicador propio. Skin, tipografía, cursores e iconos compartidos. Atajos Mayús/Ctrl/Alt y lógica narrativa conservados.
- **Diez fuentes nuevas image_gen en nube, 24 recursos instalados** mediante `adaptar_arte.py`: seis battlebacks por zona, tres fondos, windowskin 192×128, iconos 24×24, cursores, barras y niebla. Fuentes, prompts, hashes y manifiesto reproducible en `interfaz/`. Sin GPU local ni sustitución del arte previo.
- Audio central con cuatro canales globales, tabla editable y ausencia silenciosa. **24 archivos de audio pendientes de otro proceso**, ninguno descargado; nombres, tipos y loops en [AUDIO.md](../AUDIO.md). Ajustes en `Vacas.cfg`, separado de partidas; brillo visual, texto, intensidad, subtítulos y guía Alt+Enter.
- Respaldo previo de Data/scripts en `../respaldos/antes_interfaz_20261109_202703/`. **Solo Scripts.rxdata cambia en Data**: VN y sección nueva; los demás scripts, Main, mapas, BD y eventos conservados. Sin escrituras en `.git`.
- **Game.exe/RGSS104E real:** 79 comprobaciones de interfaz, ocho combates completos por los cuatro accesos y tarjeta de derrota; decisiones VN, guardado restringido, persistencia y volúmenes. Regresiones I–II/III/IV pasan, incluidos jefes, recorridos y simulaciones. Los arneses antiguos avanzan ahora el contador gráfico y presentan un fotograma nativo periódico para evitar su watchdog en modo acelerado. 102 scripts con Ruby portable, 983 referencias previas sin ausencias y 24 recursos nuevos reproducibles.
- **20 capturas reales del cliente 640×480**, [lámina UI](../capturas/ui_resumen.png) y [fondos](../capturas/ui_fondos.png). GDI después de fotogramas nativos; no son maquetas. Pruebas con entrada simulada, sin afirmar una partida manual completa. Resultados y límites en [INTERFAZ.md](../INTERFAZ.md), `../verificacion_interfaz.json` y logs RGSS.
- Pendiente: audio externo y valoración humana del recorrido, ritmo, mezcla y pantalla completa. El Acto I no tiene jefe final independiente: se verifican Madre y una tropa de prueba sin añadir eventos al argumento. Actos V–VI mantienen su estado anterior.
