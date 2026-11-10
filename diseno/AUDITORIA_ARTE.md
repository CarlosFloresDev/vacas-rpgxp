# Auditoría de arte de Vacas

**Estado:** auditoría terminada e integración prioritaria hecha; todavía no puede afirmarse que todo el juego tenga arte propio.

Inventario inicial: 445 archivos gráficos distintos. Inventario actual: 495. La tabla cuenta archivos; el catálogo posterior distingue variantes de tono/uso. Un recurso correcto en un acto y mal reutilizado en otro recibe aquí la categoría más grave.

| Categoría por archivo | Inicial | Actual |
|---|---:|---:|
| OK | 108 | 211 |
| REUTILIZADO o TINTADO | 9 | 0 |
| PLACEHOLDER o RTP | 326 | 284 |
| INCORRECTO | 2 | 0 |
| FALTA | 0 | 0 |

No hay referencias gráficas inexistentes entre las 2.055 ocurrencias rastreadas. Falta funcional aparte: seguidor de Perro entre mapas; su arte/sprites estáticos existen.

## Pasada de arte de mapas1–16 — 10 de noviembre de2026

Terminada con ocho fuentes nuevas de **image_gen integrado**, adaptación con `adaptar_arte.py` y composición CPU del mismo modo que22–32. No se ha dibujado utilería nueva en PIL. [Prompts y fuentes](arte_hd2d/arte_mapas/generaciones.json), [manifiesto con hashes y respaldos](arte_hd2d/arte_mapas/manifest.json), [método/reproducción](arte_hd2d/arte_mapas/README.md).

- 24 PNG integrados: las16 hojas `revision_mapaNN` reemplazadas y ocho recursos RTP sustituidos mediante archivos locales (siete autotiles y `185-Light02`). Se conserva la base industrial aprobada y los personajes/objetos ya aprobados; se recomponen1.955 tiles de decoración y122 instancias de mobiliario con sus anclas originales. Las bases doméstica/urbana RTP tienen materiales nuevos.
- Se mantienen exactamente dimensiones de hoja, cuadrícula de32px, índices de cada tile, capas, coordenadas, eventos, pasabilidad, prioridades y terreno. Las hojas se reconstruyeron antes de intervenir y coincidieron píxel a píxel con las16 originales. Los siete autotiles conservan alfa, disposición, número de fotogramas y1.330 equivalencias de aristas de cuartos16px; el agua tiene cuatro fases propias.
- `185-Light02` conserva128×256, celdas32×64 y las cuatro filas/patrones. Su evento no cambió. Se conservan las máscaras de luz técnicas existentes. Tres pantallas de lámpara del laboratorio se adaptaron a sus huellas.
- Las referencias `battleback_name` de los tilesets53/54/55 (mapas2–4) apuntan a `ui_piso`, el mismo fondo propio que usa su zona en `Scene_Battle`. Los registros RTP originales18/9 siguen como recursos de BD sin mapa; no se modificaron fuera de alcance.
- Revisión visual de las16 láminas a escala nativa y del resumen con luz. Se corrigió ruido en suelos, anclas de bandas del atlas urbano y rampas de grises. El sofá generado para banco y la camilla girada se descartaron: se usan los diseños aprobados de banco y camilla, con la mancha PIL de esta última sustituida por sangre generada. Objetos de mesa pequeños y camilla de64px conservados.
- No quedaron tiles RTP pendientes por riesgo de unión en esta pasada. Los materiales ya aprobados conservados no constituyen excepciones RTP. Las seis hojas de autotile declaradas para la calle se han sustituido aunque el mapa4 no contiene celdas de autotile.

Respaldo inmutable de los reemplazos locales, originales RTP, Data completo y auditoría: [antes_arte_mapas](respaldos/antes_arte_mapas/). No se accedió a `.git`, no se modificó `Vacas.cfg` y no se inició ni cerró `Game.exe`.

Validación: [47 archivos Marshal](verificacion_arte_mapas_marshal.json),46 idénticos byte a byte; los32 mapas permanecen idénticos. Solo cambian tres cadenas de fondo en `Tilesets.rxdata`; **todas** las tablas de pasabilidad, prioridades y terreno son idénticas. [125.280 pasos direccionales](verificacion_arte_mapas.json) en cuatro estados por mapa, cero diferencias. [Gráficos/audio](validacion_assets_arte_mapas.json):1.051 referencias, cero ausencias; auditoría ampliada de gráficos/scripts:2.055 ocurrencias, cero ausencias. Carga y round-trip con el lector Marshal de RGSS/MCP; no se ejecutó el motor.

Láminas antes/después a1×:

- [Mapa 01](capturas/arte_mapas_comparacion_01.png)
- [Mapa 02](capturas/arte_mapas_comparacion_02.png)
- [Mapa 03](capturas/arte_mapas_comparacion_03.png)
- [Mapa 04](capturas/arte_mapas_comparacion_04.png)
- [Mapa 05](capturas/arte_mapas_comparacion_05.png)
- [Mapa 06](capturas/arte_mapas_comparacion_06.png)
- [Mapa 07](capturas/arte_mapas_comparacion_07.png)
- [Mapa 08](capturas/arte_mapas_comparacion_08.png)
- [Mapa 09](capturas/arte_mapas_comparacion_09.png)
- [Mapa 10](capturas/arte_mapas_comparacion_10.png)
- [Mapa 11](capturas/arte_mapas_comparacion_11.png)
- [Mapa 12](capturas/arte_mapas_comparacion_12.png)
- [Mapa 13](capturas/arte_mapas_comparacion_13.png)
- [Mapa 14](capturas/arte_mapas_comparacion_14.png)
- [Mapa 15](capturas/arte_mapas_comparacion_15.png)
- [Mapa 16](capturas/arte_mapas_comparacion_16.png)

[Resumen con máscaras de luz reales](capturas/arte_mapas_luz_resumen.png). También se guardan renders individuales antes/después y sus vistas con luz. Los cuadrados azules son marcadores del render MCP; no aparecen en el juego. Los renders no simulan tono narrativo, niebla animada ni transiciones del motor.

## Correcciones integradas de la pasada22–32

- 75 PNG integrados: 62 nuevos y 13 reemplazos. Originales en [respaldo](respaldos/antes_arte_final/).
- Nueve battlers exclusivos para enemigos 18–21 y 33–37, sin tintes RGSS. Se conservan las visiones anteriores de los mismos personajes.
- Sustos 10–13 con composiciones nuevas; ya no son reencuadres de battlers/sustos anteriores. Cuatro placas cine_piso/matadero/ciudad/altar originales 640×480.
- Madre envejecida: edición de cabeza anclada al busto original, ropa/encuadre conservados y seis claves de retrato cambiadas solo en VI.
- Trono/altar de 64 px y 56 tipos de utilería (52 del atlas más cuatro muebles domésticos) adaptados a huellas existentes en mapas 22–32; los objetos aprobados se conservan. Los objetos de mesa siguen a10–16px.
- Guernsey de mapa con rombo crema, independiente de vaca_canela; madre y Cripps en hojas 128×192/celdas 32×48. Muesca/Junco son bovinos y conservan sus 192×192.
- Cuarenta iconos de objeto y diez de habilidades mentales propios 24×24. Aferrarse a Perro se deriva de su referencia aprobada.
- Autotile de muro y niebla propios. Se actualizaron defaults gráficos de System y fuentes de eventos para impedir que reaparezcan tintes/iconos viejos; los constructores PIL históricos se protegen contra ejecución directa.

Fuentes: 31 generaciones en nube, 30 seleccionadas y una descartada por encuadre. [Prompts y fuentes](arte_hd2d/arte_final/generaciones.json), [manifiesto](arte_hd2d/arte_final/manifest.json). Los sustos/retratos conservan acabado ilustrado como fase 2; las paletas de zona se dirigen en prompts y los battlers/objetos se cuantizan sin dithering, conservando rampas de material.

## Verificación y láminas de la pasada22–32

4.005 comprobaciones de referencias de producción, tamaño, reproducción, estadísticas, eventos y respaldo; 158.400 pasos direccionales comparados en 12 escenarios de 11 mapas, sin diferencias. Comparación Marshal de 16 archivos: únicamente campos gráficos/iconos/tablas y seis claves de retrato; resto de textos y objetos conservados. Vacas.cfg y Scripts.rxdata mantienen sus hashes iniciales. No se ejecutó ni cerró Game.exe; no se accedió a .git.

Mapas renderizados y las seis láminas revisadas visualmente a1×:
- [Mapas 22–23](capturas/arte_final_comparacion_22.png)
- [Mapas 24–25](capturas/arte_final_comparacion_24.png)
- [Mapas 26–27](capturas/arte_final_comparacion_26.png)
- [Mapas 28–29](capturas/arte_final_comparacion_28.png)
- [Mapas 30–31](capturas/arte_final_comparacion_30.png)
- [Mapas 32–32](capturas/arte_final_comparacion_32.png)

[Enemigos](capturas/arte_final_enemigos.png), [personajes](capturas/arte_final_personajes.png), [madre](capturas/arte_final_madre.png), [iconos1×/3×](capturas/arte_final_iconos.png), [sustos 10/11](capturas/arte_final_sustos_10.png), [sustos 12/13](capturas/arte_final_sustos_12.png), [cinemáticas1](capturas/arte_final_cinematicas_1.png), [cinemáticas2](capturas/arte_final_cinematicas_2.png). También se revisaron vistas con las máscaras reales de luz.

Los marcadores azules pertenecen al render de eventos MCP: no son gráficos del juego. Los renders no simulan niebla animada, tono narrativo ni movimiento/transición dentro de Game.exe. Queda la pasada humana en motor.

## Pendientes reales, por prioridad

1. Recursos sin mapa asociado:259 variantes solo en BD (incluidos los dos battlebacks RTP que ya no se usan en mapas2–4). Resolver uso efectivo antes de regenerar o limpiar registros; no se presume que estén muertos.
2. Treinta y dos componentes técnicos propios:27 máscaras de luz y cinco de marca Feka. Conservan su clasificación estricta PLACEHOLDER por procedencia CPU; su geometría y alfa se mantienen. No equivalen a utilería plana pendiente.
3. Seguidor de Perro: pendiente de lógica de arrastre entre mapas; sus assets existen.

Las291 variantes no OK equivalen a284 archivos distintos. Hay211 archivos OK de495; no quedan recursos ilustrativos RTP/PIL asociados a mapas en el inventario actual. No se afirma que todo el inventario de BD tenga arte propio. La valoración humana de la partida en motor sigue pendiente.

## Reproducción histórica de la pasada22–32

Desde la raíz: generar snapshot con inspeccionar.mjs desde su carpeta; instalar_arte_final.py → componer_arte_final.py → instalar_iconos_arte_final.py → aplicar_arte_final.mjs → aplicar_iconos_arte_final.mjs. Volver a inspeccionar, ejecutar verificar_arte_final.py y verificar_arte_final_marshal.mjs, renderizar b_arte_final_despues.json y componer laminas_arte_final.py. Auditar con auditoria_arte_final.py --initial y sin argumento; finalizar_arte_final.py añade este resumen. Todos los comandos de Python bajo diseno/herramientas se ejecutan con -X utf8.

Los manifiestos históricos de fase2/acto4 conservan la evidencia anterior; los PNG sustituidos se reproducen con el manifiesto final. No ejecutar arte_acto4.py/maps5.py/maps6.py ni b_cine_render.json para volver a dibujar recursos con sus constructores provisionales.


La pasada1–16 se reproduce con `arte_mapas.py install`, `extras`, `floors`, `corrections`, y `verificar_arte_mapas.mjs --apply`; ver su [README](arte_hd2d/arte_mapas/README.md). No ejecutar `finalizar_arte_final.py` para cerrar esta pasada: usar `finalizar_arte_mapas.py` después de la auditoría, para conservar los recuentos actuales.

## Inventario actual completo

## Catálogo completo

| ID | Recurso | Hue | Categoría | Mapas | Tamaño | Evidencia |
|---:|---|---:|---|---|---|---|
| 1 | Characters/vacas_steven | 0 | OK | BD/scripts | [128, 192] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 2 | Battlers/steven_mente | 0 | OK | BD/scripts | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 3 | Characters/010-Lancer02 | 0 | PLACEHOLDER o RTP | BD/scripts | [128, 192] | RTP genérico; existencia no acredita autoría propia. |
| 4 | Battlers/010-Lancer02 | 0 | PLACEHOLDER o RTP | BD/scripts | [120, 200] | RTP genérico; existencia no acredita autoría propia. |
| 5 | Characters/013-Warrior01 | 0 | PLACEHOLDER o RTP | BD/scripts | [128, 192] | RTP genérico; existencia no acredita autoría propia. |
| 6 | Battlers/013-Warrior01 | 0 | PLACEHOLDER o RTP | BD/scripts | [125, 190] | RTP genérico; existencia no acredita autoría propia. |
| 7 | Characters/019-Thief04 | 0 | PLACEHOLDER o RTP | BD/scripts | [128, 192] | RTP genérico; existencia no acredita autoría propia. |
| 8 | Battlers/019-Thief04 | 0 | PLACEHOLDER o RTP | BD/scripts | [120, 165] | RTP genérico; existencia no acredita autoría propia. |
| 9 | Characters/022-Hunter03 | 0 | PLACEHOLDER o RTP | BD/scripts | [128, 192] | RTP genérico; existencia no acredita autoría propia. |
| 10 | Battlers/022-Hunter03 | 0 | PLACEHOLDER o RTP | BD/scripts | [109, 170] | RTP genérico; existencia no acredita autoría propia. |
| 11 | Characters/023-Gunner01 | 0 | PLACEHOLDER o RTP | BD/scripts | [128, 192] | RTP genérico; existencia no acredita autoría propia. |
| 12 | Battlers/023-Gunner01 | 0 | PLACEHOLDER o RTP | BD/scripts | [131, 215] | RTP genérico; existencia no acredita autoría propia. |
| 13 | Characters/029-Cleric05 | 0 | PLACEHOLDER o RTP | BD/scripts | [128, 192] | RTP genérico; existencia no acredita autoría propia. |
| 14 | Battlers/029-Cleric05 | 0 | PLACEHOLDER o RTP | BD/scripts | [112, 170] | RTP genérico; existencia no acredita autoría propia. |
| 15 | Characters/038-Mage06 | 0 | PLACEHOLDER o RTP | BD/scripts | [128, 192] | RTP genérico; existencia no acredita autoría propia. |
| 16 | Battlers/038-Mage06 | 0 | PLACEHOLDER o RTP | BD/scripts | [118, 155] | RTP genérico; existencia no acredita autoría propia. |
| 17 | Animations/001-Action01 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 384] | RTP genérico; existencia no acredita autoría propia. |
| 18 | Animations/002-Action02 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 384] | RTP genérico; existencia no acredita autoría propia. |
| 19 | Animations/003-Attack01 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 384] | RTP genérico; existencia no acredita autoría propia. |
| 20 | Animations/004-Attack02 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 384] | RTP genérico; existencia no acredita autoría propia. |
| 21 | Animations/005-Attack03 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 192] | RTP genérico; existencia no acredita autoría propia. |
| 22 | Animations/006-Weapon01 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 768] | RTP genérico; existencia no acredita autoría propia. |
| 23 | Animations/007-Weapon02 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 960] | RTP genérico; existencia no acredita autoría propia. |
| 24 | Animations/008-Weapon03 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 768] | RTP genérico; existencia no acredita autoría propia. |
| 25 | Animations/009-Weapon04 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 960] | RTP genérico; existencia no acredita autoría propia. |
| 26 | Animations/010-Weapon05 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 576] | RTP genérico; existencia no acredita autoría propia. |
| 27 | Animations/011-Weapon06 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 576] | RTP genérico; existencia no acredita autoría propia. |
| 28 | Animations/012-Heal01 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 192] | RTP genérico; existencia no acredita autoría propia. |
| 29 | Animations/013-Heal02 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 384] | RTP genérico; existencia no acredita autoría propia. |
| 30 | Animations/014-Heal03 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 384] | RTP genérico; existencia no acredita autoría propia. |
| 31 | Animations/015-Fire01 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 384] | RTP genérico; existencia no acredita autoría propia. |
| 32 | Animations/016-Ice01 | 0 | PLACEHOLDER o RTP | BD/scripts | [957, 960] | RTP genérico; existencia no acredita autoría propia. |
| 33 | Animations/017-Thunder01 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 384] | RTP genérico; existencia no acredita autoría propia. |
| 34 | Animations/018-Water01 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 576] | RTP genérico; existencia no acredita autoría propia. |
| 35 | Animations/019-Earth01 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 384] | RTP genérico; existencia no acredita autoría propia. |
| 36 | Animations/020-Wind01 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 576] | RTP genérico; existencia no acredita autoría propia. |
| 37 | Animations/021-Light01 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 576] | RTP genérico; existencia no acredita autoría propia. |
| 38 | Animations/022-Darkness01 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 576] | RTP genérico; existencia no acredita autoría propia. |
| 39 | Animations/023-Burst01 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 384] | RTP genérico; existencia no acredita autoría propia. |
| 40 | Animations/024-Support01 | 0 | PLACEHOLDER o RTP | BD/scripts | [959, 384] | RTP genérico; existencia no acredita autoría propia. |
| 41 | Animations/025-Support02 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 384] | RTP genérico; existencia no acredita autoría propia. |
| 42 | Animations/026-Support03 | 200 | PLACEHOLDER o RTP | BD/scripts | [960, 192] | RTP genérico; existencia no acredita autoría propia. |
| 43 | Animations/026-Support03 | 340 | PLACEHOLDER o RTP | BD/scripts | [960, 192] | RTP genérico; existencia no acredita autoría propia. |
| 44 | Animations/026-Support03 | 60 | PLACEHOLDER o RTP | BD/scripts | [960, 192] | RTP genérico; existencia no acredita autoría propia. |
| 45 | Animations/026-Support03 | 130 | PLACEHOLDER o RTP | BD/scripts | [960, 192] | RTP genérico; existencia no acredita autoría propia. |
| 46 | Animations/027-Support04 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 576] | RTP genérico; existencia no acredita autoría propia. |
| 47 | Animations/027-Support04 | 150 | PLACEHOLDER o RTP | BD/scripts | [960, 576] | RTP genérico; existencia no acredita autoría propia. |
| 48 | Animations/008-Weapon03 | 290 | PLACEHOLDER o RTP | BD/scripts | [960, 768] | RTP genérico; existencia no acredita autoría propia. |
| 49 | Animations/011-Weapon06 | 140 | PLACEHOLDER o RTP | BD/scripts | [960, 576] | RTP genérico; existencia no acredita autoría propia. |
| 50 | Animations/011-Weapon06 | 200 | PLACEHOLDER o RTP | BD/scripts | [960, 576] | RTP genérico; existencia no acredita autoría propia. |
| 51 | Animations/028-State01 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 384] | RTP genérico; existencia no acredita autoría propia. |
| 52 | Animations/029-Emotion01 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 384] | RTP genérico; existencia no acredita autoría propia. |
| 53 | Animations/030-Explosion01 | 0 | PLACEHOLDER o RTP | BD/scripts | [960, 384] | RTP genérico; existencia no acredita autoría propia. |
| 54 | Icons/009-Shield01 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 55 | Icons/010-Head01 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 56 | Icons/011-Head02 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 57 | Icons/013-Body01 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 58 | Icons/014-Body02 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 59 | Icons/015-Body03 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 60 | Icons/016-Accessory01 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 61 | Pictures/retrato_steven_neutral | 0 | OK | 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18, 20, 24, 26, 28, 29, 30, 32 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 62 | Battlers/enemigo_vaca | 0 | OK | BD/scripts | [320, 300] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 63 | Battlers/enemigo_madre | 0 | OK | BD/scripts | [320, 300] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 64 | Battlers/enemigo_tunel | 0 | OK | BD/scripts | [320, 300] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 65 | Battlers/enemigo_sombra_cripps | 0 | OK | BD/scripts | [320, 300] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 66 | Battlers/enemigo_moscas | 0 | OK | BD/scripts | [320, 300] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 67 | Battlers/enemigo_guernsey | 0 | OK | BD/scripts | [320, 300] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 68 | Battlers/enemigo_canal | 0 | OK | BD/scripts | [320, 300] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 69 | Battlers/enemigo_televisor | 0 | OK | BD/scripts | [320, 300] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 70 | Battlers/enemigo_rey | 0 | OK | BD/scripts | [320, 300] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 71 | Battlers/enemigo_tarro | 0 | OK | BD/scripts | [320, 300] | Fuente image_gen documentada: diseno/arte_hd2d/acto3/manifest.json; aprobación final no presumida. |
| 72 | Battlers/enemigo_factura | 0 | OK | BD/scripts | [320, 300] | Fuente image_gen documentada: diseno/arte_hd2d/acto3/manifest.json; aprobación final no presumida. |
| 73 | Battlers/enemigo_camilla | 0 | OK | BD/scripts | [320, 300] | Fuente image_gen documentada: diseno/arte_hd2d/acto3/manifest.json; aprobación final no presumida. |
| 74 | Battlers/enemigo_diagnostico | 0 | OK | BD/scripts | [320, 300] | Fuente image_gen documentada: diseno/arte_hd2d/acto3/manifest.json; aprobación final no presumida. |
| 75 | Battlers/enemigo_coro | 0 | OK | BD/scripts | [320, 300] | Fuente image_gen documentada: diseno/arte_hd2d/acto4/manifest.json; aprobación final no presumida. |
| 76 | Battlers/enemigo_pulmon | 0 | OK | BD/scripts | [320, 300] | Fuente image_gen documentada: diseno/arte_hd2d/acto4/manifest.json; aprobación final no presumida. |
| 77 | Battlers/enemigo_cencerro | 0 | OK | BD/scripts | [320, 300] | Fuente image_gen documentada: diseno/arte_hd2d/acto4/manifest.json; aprobación final no presumida. |
| 78 | Battlers/enemigo_pastor | 0 | OK | BD/scripts | [320, 300] | Fuente image_gen documentada: diseno/arte_hd2d/acto4/manifest.json; aprobación final no presumida. |
| 79 | Battlers/enemigo_turno_noche | 0 | OK | BD/scripts | [320, 300] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 80 | Battlers/enemigo_res_cuenta | 0 | OK | BD/scripts | [320, 300] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 81 | Battlers/enemigo_gancho_respira | 0 | OK | BD/scripts | [320, 300] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 82 | Battlers/enemigo_cripps_matarife | 0 | OK | BD/scripts | [320, 300] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 83 | Battlers/073-Bird03 | 0 | PLACEHOLDER o RTP | BD/scripts | [364, 256] | RTP genérico; existencia no acredita autoría propia. |
| 84 | Battlers/077-Devil03 | 0 | PLACEHOLDER o RTP | BD/scripts | [339, 256] | RTP genérico; existencia no acredita autoría propia. |
| 85 | Battlers/081-Angel03 | 0 | PLACEHOLDER o RTP | BD/scripts | [252, 256] | RTP genérico; existencia no acredita autoría propia. |
| 86 | Battlers/054-Undead04 | 0 | PLACEHOLDER o RTP | BD/scripts | [441, 320] | RTP genérico; existencia no acredita autoría propia. |
| 87 | Battlers/058-Snake04 | 0 | PLACEHOLDER o RTP | BD/scripts | [449, 320] | RTP genérico; existencia no acredita autoría propia. |
| 88 | Battlers/062-Aquatic04 | 0 | PLACEHOLDER o RTP | BD/scripts | [447, 320] | RTP genérico; existencia no acredita autoría propia. |
| 89 | Battlers/066-Beast04 | 0 | PLACEHOLDER o RTP | BD/scripts | [449, 320] | RTP genérico; existencia no acredita autoría propia. |
| 90 | Battlers/070-Goblin04 | 0 | PLACEHOLDER o RTP | BD/scripts | [409, 320] | RTP genérico; existencia no acredita autoría propia. |
| 91 | Battlers/074-Bird04 | 0 | PLACEHOLDER o RTP | BD/scripts | [497, 320] | RTP genérico; existencia no acredita autoría propia. |
| 92 | Battlers/078-Devil04 | 0 | PLACEHOLDER o RTP | BD/scripts | [439, 320] | RTP genérico; existencia no acredita autoría propia. |
| 93 | Battlers/082-Angel04 | 0 | PLACEHOLDER o RTP | BD/scripts | [411, 320] | RTP genérico; existencia no acredita autoría propia. |
| 94 | Battlers/enemigo_censo_bocas | 0 | OK | BD/scripts | [320, 300] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 95 | Battlers/enemigo_mesa_exige | 0 | OK | BD/scripts | [320, 300] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 96 | Battlers/enemigo_rey_sin_rostro | 0 | OK | BD/scripts | [320, 300] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 97 | Battlers/enemigo_numero_cadena | 0 | OK | BD/scripts | [320, 300] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 98 | Battlers/enemigo_puerta_muerde | 0 | OK | BD/scripts | [320, 300] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 99 | Icons/vacas_item_01 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 100 | Icons/vacas_item_02 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 101 | Icons/vacas_item_03 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 102 | Icons/vacas_item_04 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 103 | Icons/vacas_item_05 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 104 | Icons/vacas_item_06 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 105 | Icons/vacas_item_07 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 106 | Icons/vacas_item_08 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 107 | Icons/vacas_item_09 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 108 | Icons/vacas_item_10 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 109 | Icons/vacas_item_11 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 110 | Icons/vacas_item_12 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 111 | Icons/vacas_item_13 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 112 | Icons/vacas_item_14 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 113 | Icons/vacas_item_15 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 114 | Icons/vacas_item_16 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 115 | Icons/vacas_item_17 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 116 | Icons/vacas_item_18 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 117 | Icons/vacas_item_19 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 118 | Icons/vacas_item_20 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 119 | Icons/vacas_item_21 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 120 | Icons/vacas_item_22 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 121 | Icons/vacas_item_23 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 122 | Icons/vacas_item_24 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 123 | Icons/vacas_item_25 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 124 | Icons/vacas_item_26 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 125 | Icons/vacas_item_27 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 126 | Icons/vacas_item_28 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 127 | Icons/vacas_item_29 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 128 | Icons/vacas_item_30 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 129 | Icons/vacas_item_31 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 130 | Icons/vacas_item_32 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 131 | Icons/vacas_item_33 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 132 | Icons/vacas_item_34 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 133 | Icons/vacas_item_35 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 134 | Icons/vacas_item_36 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 135 | Icons/vacas_item_37 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 136 | Icons/vacas_item_38 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 137 | Icons/vacas_item_39 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 138 | Icons/vacas_item_40 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 139 | Pictures/retrato_dog_neutral | 0 | OK | 1, 2, 4, 5, 7, 29, 30, 31, 32 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 140 | Tilesets/revision_mapa01 | 0 | OK | 1 | [256, 608] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 141 | Autotiles/053-Wall01 | 0 | OK | 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32 | [96, 128] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 142 | Autotiles/vacas_canal | 0 | OK | 1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32 | [384, 128] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 143 | Fogs/002-Clouds01 | 0 | OK | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32 | [256, 256] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 144 | Characters/vacas_madre | 0 | OK | 2, 30 | [128, 192] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 145 | Pictures/retrato_madre_ira | 0 | OK | 2, 30 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 146 | Pictures/retrato_madre_neutral | 0 | OK | 2 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 147 | Pictures/screamer_7 | 0 | OK | 2 | [640, 480] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 148 | Characters/vacas_muebles | 0 | OK | 2, 12 | [128, 256] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 149 | Pictures/screamer_1 | 0 | OK | 2 | [640, 480] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 150 | Characters/vacas_cosas | 0 | OK | 2, 3, 4 | [128, 128] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 151 | Pictures/screamer_2 | 0 | OK | 2 | [640, 480] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 152 | Characters/vacas_perro | 0 | OK | 2, 30, 32 | [160, 160] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 153 | Pictures/retrato_dog_miedo | 0 | OK | 2 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 154 | Characters/vacas_vacio | 0 | OK | 2, 4, 5 | [128, 192] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 155 | Autotiles/052-Carpet02 | 0 | OK | 2, 3 | [96, 128] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 156 | Battlebacks/ui_piso | 0 | OK | 1, 2, 3, 4, 30 | [640, 480] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 157 | Tilesets/revision_mapa02 | 0 | OK | 2 | [256, 1312] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 158 | Characters/vacas_puerta | 0 | OK | 3, 4 | [128, 256] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 159 | Characters/vacas_remedios | 0 | OK | 3 | [128, 192] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 160 | Pictures/retrato_remedios_neutral | 0 | OK | 3 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 161 | Characters/vacas_anselmo | 0 | OK | 3 | [128, 192] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 162 | Pictures/retrato_anselmo_neutral | 0 | OK | 3 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 163 | Characters/185-Light02 | 0 | OK | 3 | [128, 256] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 164 | Characters/vacas_lucy | 0 | OK | 3, 12, 16 | [128, 192] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 165 | Pictures/retrato_lucy_susurro | 0 | OK | 3 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 166 | Tilesets/revision_mapa03 | 0 | OK | 3 | [256, 1056] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 167 | Characters/vacas_tablon | 0 | OK | 4, 5 | [128, 192] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 168 | Pictures/retrato_molina_neutral | 0 | OK | 4, 13 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 169 | Characters/vacas_carnicero | 0 | OK | 4, 13 | [128, 192] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 170 | Characters/vacas_borracho | 0 | OK | 4 | [128, 192] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 171 | Pictures/retrato_borracho_neutral | 0 | OK | 4 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 172 | Characters/vacas_transeunte | 0 | OK | 4 | [128, 192] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 173 | Characters/vacas_furgoneta | 0 | OK | 4, 5 | [384, 256] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 174 | Characters/vacas_reclutador | 0 | OK | 4 | [128, 192] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 175 | Pictures/retrato_reclutador_neutral | 0 | OK | 4 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 176 | Autotiles/048-Water01 | 0 | OK | 4 | [384, 128] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 177 | Autotiles/002-G_Shadow01 | 0 | OK | 4 | [96, 128] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 178 | Autotiles/003-G_Ground01 | 0 | OK | 4 | [96, 128] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 179 | Autotiles/005-G_Road01 | 0 | OK | 4 | [96, 128] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 180 | Autotiles/006-G_Road02 | 0 | OK | 4 | [96, 128] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 181 | Autotiles/050-Roof02 | 0 | OK | 4 | [96, 128] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 182 | Tilesets/revision_mapa04 | 0 | OK | 4 | [256, 1504] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 183 | Pictures/retrato_steven_miedo | 0 | OK | 5, 7, 12, 14, 16, 17, 22, 23, 24, 25, 26, 27 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 184 | Pictures/screamer_3 | 0 | OK | 5 | [640, 480] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 185 | Characters/vacas_obrero1 | 0 | OK | 5, 8, 22, 29 | [128, 192] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 186 | Pictures/retrato_benito_neutral | 0 | OK | 5, 8, 22 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 187 | Characters/vacas_cripps | 0 | OK | 5, 8, 9, 10, 14, 25, 26 | [128, 192] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 188 | Pictures/retrato_cripps_neutral | 0 | OK | 5, 8, 9, 10, 26 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 189 | Characters/vacas_matadero | 0 | OK | 5, 8, 9, 10, 11 | [128, 256] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 190 | Tilesets/revision_mapa05 | 0 | OK | 5 | [256, 928] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 191 | Pictures/screamer_4 | 0 | OK | 6 | [640, 480] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 192 | Characters/vacas_obrero3 | 0 | OK | 6, 8, 24, 27, 29 | [128, 192] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 193 | Pictures/retrato_encarna_neutral | 0 | OK | 6, 8 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 194 | Characters/vacas_obrero4 | 0 | OK | 6, 24, 27 | [128, 192] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 195 | Pictures/retrato_chato_neutral | 0 | OK | 6, 24, 27 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 196 | Tilesets/revision_mapa06 | 0 | OK | 6 | [256, 544] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 197 | Characters/vacas_vaca | 0 | OK | 7, 23, 27, 29 | [320, 320] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 198 | Characters/vacas_vaca_canela | 0 | OK | 7, 8, 23, 27 | [320, 320] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 199 | Characters/vacas_obrero2 | 0 | OK | 7, 8, 23 | [128, 192] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 200 | Pictures/retrato_rubio_neutral | 0 | OK | 7, 24, 27, 29, 31 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 201 | Tilesets/revision_mapa07 | 0 | OK | 7 | [256, 768] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 202 | Pictures/retrato_cripps_ira | 0 | OK | 8, 9, 10, 25, 26 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 203 | Pictures/retrato_sierra_neutral | 0 | OK | 8, 23 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 204 | Tilesets/revision_mapa08 | 0 | OK | 8 | [256, 1024] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 205 | Pictures/screamer_6 | 0 | OK | 9, 10 | [640, 480] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 206 | Tilesets/revision_mapa09 | 0 | OK | 9 | [256, 832] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 207 | Tilesets/revision_mapa10 | 0 | OK | 10 | [256, 576] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 208 | Pictures/screamer_5 | 0 | OK | 11 | [640, 480] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 209 | Pictures/retrato_guernsey_susurro | 0 | OK | 11, 16, 17, 20, 22, 23, 25, 26, 27, 28, 29, 32 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 210 | Tilesets/revision_mapa11 | 0 | OK | 11 | [256, 704] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 211 | Pictures/retrato_lucy_neutral | 0 | OK | 12, 16, 28 | [240, 340] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 212 | Characters/vacas_laboratorio | 0 | OK | 12, 13, 14, 15, 16 | [128, 256] | Fuente image_gen documentada: diseno/arte_hd2d/acto3/manifest.json; aprobación final no presumida. |
| 213 | Pictures/retrato_lucy_calma | 0 | OK | 12, 16, 28 | [240, 340] | Fuente image_gen documentada: diseno/arte_hd2d/acto3/manifest.json; aprobación final no presumida. |
| 214 | Tilesets/revision_mapa12 | 0 | OK | 12 | [256, 928] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 215 | Tilesets/revision_mapa13 | 0 | OK | 13 | [256, 704] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 216 | Pictures/screamer_8 | 0 | OK | 14 | [640, 480] | Fuente image_gen documentada: diseno/arte_hd2d/acto3/manifest.json; aprobación final no presumida. |
| 217 | Tilesets/revision_mapa14 | 0 | OK | 14 | [256, 640] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 218 | Characters/vacas_elena | 0 | OK | 15 | [128, 192] | Fuente image_gen documentada: diseno/arte_hd2d/acto3/manifest.json; aprobación final no presumida. |
| 219 | Pictures/retrato_elena_neutral | 0 | OK | 15 | [240, 340] | Fuente image_gen documentada: diseno/arte_hd2d/acto3/manifest.json; aprobación final no presumida. |
| 220 | Characters/vacas_alcantarilla | 0 | OK | 15, 17, 18, 19, 20, 21 | [128, 256] | Fuente image_gen documentada: diseno/arte_hd2d/acto4/manifest.json; aprobación final no presumida. |
| 221 | Tilesets/revision_mapa15 | 0 | OK | 15 | [256, 928] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 222 | Pictures/retrato_lucy_quiebre | 0 | OK | 16 | [240, 340] | Fuente image_gen documentada: diseno/arte_hd2d/acto3/manifest.json; aprobación final no presumida. |
| 223 | Pictures/screamer_9 | 0 | OK | 16 | [640, 480] | Fuente image_gen documentada: diseno/arte_hd2d/acto3/manifest.json; aprobación final no presumida. |
| 224 | Tilesets/revision_mapa16 | 0 | OK | 16 | [256, 864] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 225 | Tilesets/acto4_alcantarillas | 0 | OK | 17, 18, 19, 20, 21 | [256, 64] | Fuente image_gen documentada: diseno/arte_hd2d/acto4/manifest.json; aprobación final no presumida. |
| 226 | Battlebacks/mente_tunel | 0 | OK | 17, 18, 19, 20, 21 | [640, 480] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 227 | Characters/vacas_muesca | 0 | OK | 18, 19, 20, 23, 27, 28 | [192, 192] | Fuente image_gen documentada: diseno/arte_hd2d/acto4/manifest.json; aprobación final no presumida. |
| 228 | Pictures/retrato_muesca_neutral | 0 | OK | 18, 20, 23, 27, 28, 32 | [240, 340] | Fuente image_gen documentada: diseno/arte_hd2d/acto4/manifest.json; aprobación final no presumida. |
| 229 | Pictures/screamer_10 | 0 | OK | 18 | [640, 480] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 230 | Characters/vacas_junco | 0 | OK | 19, 20, 23, 27 | [192, 192] | Fuente image_gen documentada: diseno/arte_hd2d/acto4/manifest.json; aprobación final no presumida. |
| 231 | Pictures/retrato_junco_neutral | 0 | OK | 19, 20, 23, 27 | [240, 340] | Fuente image_gen documentada: diseno/arte_hd2d/acto4/manifest.json; aprobación final no presumida. |
| 232 | Pictures/screamer_11 | 0 | OK | 19 | [640, 480] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 233 | Characters/vacas_guernsey4 | 0 | OK | 20, 26, 27, 29, 32 | [192, 192] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 234 | Tilesets/acto5_matanza | 0 | OK | 22, 23, 24, 25, 26, 27 | [256, 2656] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 235 | Pictures/screamer_12 | 0 | OK | 25 | [640, 480] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 236 | Pictures/screamer_13 | 0 | OK | 25 | [640, 480] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 237 | Tilesets/acto6_reydios | 0 | OK | 28, 29, 30, 31, 32 | [256, 992] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 238 | Pictures/retrato_madre_envejecida_neutral | 0 | OK | 30 | [240, 340] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 239 | Icons/045-Skill02 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 240 | Icons/044-Skill01 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 241 | Icons/046-Skill03 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 242 | Icons/047-Skill04 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 243 | Icons/048-Skill05 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 244 | Icons/050-Skill07 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 245 | Icons/vacas_habilidad_61 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 246 | Icons/vacas_habilidad_62 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 247 | Icons/vacas_habilidad_63 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 248 | Icons/vacas_habilidad_64 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 249 | Icons/vacas_habilidad_65 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 250 | Icons/vacas_habilidad_66 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 251 | Icons/vacas_habilidad_67 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 252 | Icons/vacas_habilidad_68 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 253 | Icons/vacas_habilidad_69 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 254 | Icons/vacas_habilidad_70 | 0 | OK | BD/scripts | [24, 24] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 255 | Gameovers/vacas_gameover | 0 | OK | BD/scripts | [640, 480] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 256 | Titles/vacas_titulo | 0 | OK | BD/scripts | [640, 480] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 257 | Windowskins/ui_windowskin | 0 | OK | BD/scripts | [192, 128] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 258 | Battlebacks/mente_matadero | 0 | OK | BD/scripts | [640, 480] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 259 | Autotiles/001-G_Water01 | 0 | PLACEHOLDER o RTP | BD/scripts | [384, 128] | RTP genérico; existencia no acredita autoría propia. |
| 260 | Autotiles/040-Ground01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 261 | Autotiles/041-Grass01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 262 | Autotiles/007-G_Undulation01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 263 | Autotiles/008-G_Undulation02 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 264 | Battlebacks/001-Grassland01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 265 | Tilesets/001-Grassland01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 576] | RTP genérico; existencia no acredita autoría propia. |
| 266 | Autotiles/043-Grass02 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 267 | Autotiles/036-Tree01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 268 | Autotiles/037-Tree02 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 269 | Battlebacks/002-Woods01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 270 | Tilesets/002-Woods01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 800] | RTP genérico; existencia no acredita autoría propia. |
| 271 | Autotiles/009-G2_Water01 | 0 | PLACEHOLDER o RTP | BD/scripts | [384, 128] | RTP genérico; existencia no acredita autoría propia. |
| 272 | Autotiles/010-G2_Ground01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 273 | Autotiles/011-G2_Ground02 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 274 | Autotiles/042-Ground02 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 275 | Autotiles/038-Tree03 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 276 | Autotiles/039-Tree04 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 277 | Battlebacks/003-Forest01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 278 | Tilesets/003-Forest01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 608] | RTP genérico; existencia no acredita autoría propia. |
| 279 | Panoramas/006-Mountains01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 640] | RTP genérico; existencia no acredita autoría propia. |
| 280 | Autotiles/033-Waterfall01 | 0 | PLACEHOLDER o RTP | BD/scripts | [384, 128] | RTP genérico; existencia no acredita autoría propia. |
| 281 | Autotiles/034-Waterfall02 | 0 | PLACEHOLDER o RTP | BD/scripts | [384, 128] | RTP genérico; existencia no acredita autoría propia. |
| 282 | Autotiles/035-Waterfall03 | 0 | PLACEHOLDER o RTP | BD/scripts | [384, 128] | RTP genérico; existencia no acredita autoría propia. |
| 283 | Battlebacks/004-Mountain01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 284 | Tilesets/004-Mountain01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 896] | RTP genérico; existencia no acredita autoría propia. |
| 285 | Autotiles/024-Ocean01 | 0 | PLACEHOLDER o RTP | BD/scripts | [384, 128] | RTP genérico; existencia no acredita autoría propia. |
| 286 | Autotiles/025-Ocean02 | 0 | PLACEHOLDER o RTP | BD/scripts | [384, 128] | RTP genérico; existencia no acredita autoría propia. |
| 287 | Autotiles/026-Ocean03 | 0 | PLACEHOLDER o RTP | BD/scripts | [384, 128] | RTP genérico; existencia no acredita autoría propia. |
| 288 | Autotiles/027-Ocean04 | 0 | PLACEHOLDER o RTP | BD/scripts | [384, 128] | RTP genérico; existencia no acredita autoría propia. |
| 289 | Autotiles/016-Sa_Shadow01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 290 | Autotiles/017-Sa_Grass01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 291 | Autotiles/045-Road02 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 292 | Battlebacks/005-Beach01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 293 | Tilesets/005-Beach01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 544] | RTP genérico; existencia no acredita autoría propia. |
| 294 | Autotiles/015-Sa_Water01 | 0 | PLACEHOLDER o RTP | BD/scripts | [384, 128] | RTP genérico; existencia no acredita autoría propia. |
| 295 | Autotiles/018-Sa_Ground01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 296 | Autotiles/019-Sa_Grass02 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 297 | Autotiles/020-Sa_Grass03 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 298 | Autotiles/023-Sa_Undulation01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 299 | Battlebacks/006-Desert01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 300 | Tilesets/006-Desert01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 608] | RTP genérico; existencia no acredita autoría propia. |
| 301 | Autotiles/012-G2_Swamp01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 302 | Autotiles/013-G2_Swamp02 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 303 | Autotiles/014-G2_Swamp03 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 304 | Battlebacks/007-Swamp01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 305 | Tilesets/007-Swamp01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 448] | RTP genérico; existencia no acredita autoría propia. |
| 306 | Autotiles/028-Sn_Water01 | 0 | PLACEHOLDER o RTP | BD/scripts | [384, 128] | RTP genérico; existencia no acredita autoría propia. |
| 307 | Autotiles/029-Sn_Shadow01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 308 | Autotiles/030-Sn_Ground01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 309 | Autotiles/044-Road01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 310 | Autotiles/031-Sn_Undulation01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 311 | Battlebacks/008-Snowfield01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 312 | Tilesets/008-Snowfield01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 864] | RTP genérico; existencia no acredita autoría propia. |
| 313 | Battlebacks/009-CastleTown01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 314 | Tilesets/009-CastleTown01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 960] | RTP genérico; existencia no acredita autoría propia. |
| 315 | Autotiles/054-Wall02 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 316 | Autotiles/051-Carpet01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 317 | Battlebacks/010-CastleTown02 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 318 | Tilesets/010-CastleTown02 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 736] | RTP genérico; existencia no acredita autoría propia. |
| 319 | Autotiles/032-T_Ocean01 | 0 | PLACEHOLDER o RTP | BD/scripts | [384, 128] | RTP genérico; existencia no acredita autoría propia. |
| 320 | Autotiles/004-G_Ground02 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 321 | Battlebacks/011-PortTown01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 322 | Tilesets/011-PortTown01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 1024] | RTP genérico; existencia no acredita autoría propia. |
| 323 | Battlebacks/012-PortTown02 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 324 | Tilesets/012-PortTown02 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 672] | RTP genérico; existencia no acredita autoría propia. |
| 325 | Battlebacks/013-PostTown01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 326 | Tilesets/013-PostTown01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 960] | RTP genérico; existencia no acredita autoría propia. |
| 327 | Battlebacks/014-PostTown02 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 328 | Tilesets/014-PostTown02 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 704] | RTP genérico; existencia no acredita autoría propia. |
| 329 | Battlebacks/015-ForestTown01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 330 | Tilesets/015-ForestTown01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 1056] | RTP genérico; existencia no acredita autoría propia. |
| 331 | Battlebacks/016-ForestTown02 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 332 | Tilesets/016-ForestTown02 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 800] | RTP genérico; existencia no acredita autoría propia. |
| 333 | Battlebacks/017-MineTown01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 334 | Tilesets/017-MineTown01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 1216] | RTP genérico; existencia no acredita autoría propia. |
| 335 | Battlebacks/018-MineTown02 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 336 | Tilesets/018-MineTown02 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 832] | RTP genérico; existencia no acredita autoría propia. |
| 337 | Autotiles/021-Sa_Road01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 338 | Autotiles/022-Roof01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 339 | Battlebacks/019-DesertTown01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 340 | Tilesets/019-DesertTown01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 704] | RTP genérico; existencia no acredita autoría propia. |
| 341 | Autotiles/055-Wall03 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 342 | Battlebacks/020-DesertTown02 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 343 | Tilesets/020-DesertTown02 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 736] | RTP genérico; existencia no acredita autoría propia. |
| 344 | Battlebacks/021-SnowTown01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 345 | Tilesets/021-SnowTown01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 1280] | RTP genérico; existencia no acredita autoría propia. |
| 346 | Battlebacks/022-SnowTown02 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 347 | Tilesets/022-SnowTown02 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 736] | RTP genérico; existencia no acredita autoría propia. |
| 348 | Battlebacks/023-FarmVillage01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 349 | Tilesets/023-FarmVillage01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 1024] | RTP genérico; existencia no acredita autoría propia. |
| 350 | Battlebacks/024-FarmVillage02 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 351 | Tilesets/024-FarmVillage02 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 736] | RTP genérico; existencia no acredita autoría propia. |
| 352 | Autotiles/047-Flower01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 353 | Battlebacks/025-Castle01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 354 | Tilesets/025-Castle01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 896] | RTP genérico; existencia no acredita autoría propia. |
| 355 | Autotiles/049-St_Shadow01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 356 | Battlebacks/026-Castle02 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 357 | Tilesets/026-Castle02 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 800] | RTP genérico; existencia no acredita autoría propia. |
| 358 | Battlebacks/027-Castle03 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 359 | Tilesets/027-Castle03 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 800] | RTP genérico; existencia no acredita autoría propia. |
| 360 | Battlebacks/028-Church01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 361 | Tilesets/028-Church01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 1088] | RTP genérico; existencia no acredita autoría propia. |
| 362 | Battlebacks/029-Church02 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 363 | Tilesets/029-Church02 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 1056] | RTP genérico; existencia no acredita autoría propia. |
| 364 | Autotiles/046-Road03 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 365 | Battlebacks/030-Ship01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 366 | Tilesets/030-Ship01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 1184] | RTP genérico; existencia no acredita autoría propia. |
| 367 | Battlebacks/031-Ship02 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 368 | Tilesets/031-Ship02 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 928] | RTP genérico; existencia no acredita autoría propia. |
| 369 | Panoramas/001-Sky01 | 0 | PLACEHOLDER o RTP | BD/scripts | [480, 480] | RTP genérico; existencia no acredita autoría propia. |
| 370 | Battlebacks/032-Heaven01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 371 | Tilesets/032-Heaven01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 1024] | RTP genérico; existencia no acredita autoría propia. |
| 372 | Battlebacks/033-Heaven02 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 373 | Tilesets/033-Heaven02 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 928] | RTP genérico; existencia no acredita autoría propia. |
| 374 | Battlebacks/034-Bridge01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 375 | Tilesets/034-Bridge01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 960] | RTP genérico; existencia no acredita autoría propia. |
| 376 | Tilesets/035-Ruins01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 896] | RTP genérico; existencia no acredita autoría propia. |
| 377 | Battlebacks/035-Ruins01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 378 | Battlebacks/036-Shop01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 379 | Tilesets/036-Shop01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 1248] | RTP genérico; existencia no acredita autoría propia. |
| 380 | Battlebacks/037-Fort01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 381 | Tilesets/037-Fort01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 960] | RTP genérico; existencia no acredita autoría propia. |
| 382 | Battlebacks/038-Fort02 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 383 | Tilesets/038-Fort02 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 832] | RTP genérico; existencia no acredita autoría propia. |
| 384 | Battlebacks/039-Tower01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 385 | Tilesets/039-Tower01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 1056] | RTP genérico; existencia no acredita autoría propia. |
| 386 | Battlebacks/040-Tower02 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 387 | Tilesets/040-Tower02 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 960] | RTP genérico; existencia no acredita autoría propia. |
| 388 | Battlebacks/041-EvilCastle01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 389 | Tilesets/041-EvilCastle01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 960] | RTP genérico; existencia no acredita autoría propia. |
| 390 | Battlebacks/042-EvilCastle02 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 391 | Tilesets/042-EvilCastle02 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 832] | RTP genérico; existencia no acredita autoría propia. |
| 392 | Autotiles/056-CE_Water01 | 0 | PLACEHOLDER o RTP | BD/scripts | [384, 128] | RTP genérico; existencia no acredita autoría propia. |
| 393 | Autotiles/057-CE_Shadow01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 394 | Autotiles/058-CE_Ground01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 395 | Autotiles/059-CE_Ground02 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 396 | Autotiles/060-CE_Grass01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 397 | Autotiles/061-CE_Road01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 398 | Battlebacks/043-Cave01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 399 | Tilesets/043-Cave01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 1056] | RTP genérico; existencia no acredita autoría propia. |
| 400 | Autotiles/062-CF_Lava01 | 0 | PLACEHOLDER o RTP | BD/scripts | [384, 128] | RTP genérico; existencia no acredita autoría propia. |
| 401 | Autotiles/063-CF_Shadow01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 402 | Autotiles/064-CF_Ground01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 403 | Autotiles/065-CF_Ground02 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 404 | Autotiles/066-CF_Ground03 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 405 | Autotiles/067-CF_Ground04 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 406 | Tilesets/044-Cave02 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 1056] | RTP genérico; existencia no acredita autoría propia. |
| 407 | Battlebacks/044-Cave02 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 408 | Autotiles/068-CI_Water01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 409 | Autotiles/069-CI_Shadow01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 410 | Autotiles/070-CI_Snow01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 411 | Autotiles/071-CI_Ground01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 412 | Autotiles/072-CI_Ice01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 413 | Autotiles/073-CI_Ground02 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 414 | Tilesets/045-Cave03 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 1056] | RTP genérico; existencia no acredita autoría propia. |
| 415 | Battlebacks/045-Cave03 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 416 | Autotiles/074-CW_Water01 | 0 | PLACEHOLDER o RTP | BD/scripts | [384, 128] | RTP genérico; existencia no acredita autoría propia. |
| 417 | Autotiles/075-CW_Shadow01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 418 | Autotiles/076-CW_Grass01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 419 | Autotiles/077-CW_Grass02 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 420 | Autotiles/078-CW_Ground01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 421 | Autotiles/079-CW_Grass03 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 422 | Tilesets/046-Cave04 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 1056] | RTP genérico; existencia no acredita autoría propia. |
| 423 | Battlebacks/046-Cave04 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 424 | Battlebacks/047-Mine01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 425 | Tilesets/047-Mine01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 864] | RTP genérico; existencia no acredita autoría propia. |
| 426 | Battlebacks/048-Sewer01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 427 | Tilesets/048-Sewer01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 768] | RTP genérico; existencia no acredita autoría propia. |
| 428 | Autotiles/080-B_Ground01 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 429 | Autotiles/081-B_Ground02 | 0 | PLACEHOLDER o RTP | BD/scripts | [96, 128] | RTP genérico; existencia no acredita autoría propia. |
| 430 | Battlebacks/049-InnerBody01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 431 | Tilesets/049-InnerBody01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 672] | RTP genérico; existencia no acredita autoría propia. |
| 432 | Panoramas/003-StarlitSky01 | 0 | PLACEHOLDER o RTP | BD/scripts | [480, 480] | RTP genérico; existencia no acredita autoría propia. |
| 433 | Battlebacks/050-DarkSpace01 | 0 | PLACEHOLDER o RTP | BD/scripts | [640, 320] | RTP genérico; existencia no acredita autoría propia. |
| 434 | Tilesets/050-DarkSpace01 | 0 | PLACEHOLDER o RTP | BD/scripts | [256, 640] | RTP genérico; existencia no acredita autoría propia. |
| 435 | Tilesets/vacas_matadero | 0 | OK | BD/scripts | [256, 256] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 436 | Icons/001-Weapon01 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 437 | Icons/002-Weapon02 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 438 | Icons/003-Weapon03 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 439 | Icons/004-Weapon04 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 440 | Icons/005-Weapon05 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 441 | Icons/006-Weapon06 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 442 | Icons/007-Weapon07 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 443 | Icons/008-Weapon08 | 0 | PLACEHOLDER o RTP | BD/scripts | [24, 24] | RTP genérico; existencia no acredita autoría propia. |
| 444 | Windowskins/vacas_ventana | 0 | OK | BD/scripts | [192, 128] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 445 | Characters/vacas_steven_mono | 0 | OK | BD/scripts | [128, 192] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 446 | Pictures/ui_cursor | 0 | OK | BD/scripts | [16, 16] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 447 | Pictures/ui_fog | 0 | OK | BD/scripts | [256, 256] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 448 | Icons/ui_nota | 0 | OK | BD/scripts | [24, 24] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 449 | Icons/ui_objeto | 0 | OK | BD/scripts | [24, 24] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 450 | Icons/ui_bateria | 0 | OK | BD/scripts | [24, 24] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 451 | Icons/ui_estado_2 | 0 | OK | BD/scripts | [24, 24] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 452 | Pictures/ui_avance | 0 | OK | BD/scripts | [14, 14] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 453 | Pictures/ui_target | 0 | OK | BD/scripts | [32, 32] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 454 | Pictures/feka_halo | 0 | PLACEHOLDER o RTP | BD/scripts | [512, 256] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 455 | Pictures/feka_logo | 0 | PLACEHOLDER o RTP | BD/scripts | [368, 146] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 456 | Pictures/feka_linea | 0 | PLACEHOLDER o RTP | BD/scripts | [368, 13] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 457 | Pictures/feka_presenta | 0 | PLACEHOLDER o RTP | BD/scripts | [141, 28] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 458 | Pictures/feka_gota | 0 | PLACEHOLDER o RTP | BD/scripts | [16, 16] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 459 | Pictures/cine_piso | 0 | OK | BD/scripts | [640, 480] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 460 | Pictures/cine_matadero | 0 | OK | BD/scripts | [640, 480] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 461 | Pictures/cine_altar | 0 | OK | BD/scripts | [640, 480] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 462 | Pictures/cine_ciudad | 0 | OK | BD/scripts | [640, 480] | Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva. |
| 463 | Pictures/revision_luz01 | 0 | PLACEHOLDER o RTP | 1 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 464 | Pictures/revision_luz02 | 0 | PLACEHOLDER o RTP | 2 | [960, 704] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 465 | Pictures/revision_luz03 | 0 | PLACEHOLDER o RTP | 3 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 466 | Pictures/revision_luz04 | 0 | PLACEHOLDER o RTP | 4 | [1280, 640] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 467 | Pictures/revision_luz05 | 0 | PLACEHOLDER o RTP | 5 | [960, 704] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 468 | Pictures/revision_luz06 | 0 | PLACEHOLDER o RTP | 6 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 469 | Pictures/revision_luz07 | 0 | PLACEHOLDER o RTP | 7 | [960, 640] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 470 | Pictures/revision_luz08 | 0 | PLACEHOLDER o RTP | 8 | [1280, 768] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 471 | Pictures/revision_luz09 | 0 | PLACEHOLDER o RTP | 9 | [960, 640] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 472 | Pictures/revision_luz10 | 0 | PLACEHOLDER o RTP | 10 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 473 | Pictures/revision_luz11 | 0 | PLACEHOLDER o RTP | 11 | [960, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 474 | Pictures/revision_luz12 | 0 | PLACEHOLDER o RTP | 12 | [800, 640] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 475 | Pictures/revision_luz13 | 0 | PLACEHOLDER o RTP | 13 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 476 | Pictures/revision_luz14 | 0 | PLACEHOLDER o RTP | 14 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 477 | Pictures/revision_luz15 | 0 | PLACEHOLDER o RTP | 15 | [800, 640] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 478 | Pictures/revision_luz16 | 0 | PLACEHOLDER o RTP | 16 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 479 | Pictures/acto5_luz22 | 0 | PLACEHOLDER o RTP | 22 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 480 | Pictures/acto5_luz23 | 0 | PLACEHOLDER o RTP | 23 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 481 | Pictures/acto5_luz24 | 0 | PLACEHOLDER o RTP | 24 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 482 | Pictures/acto5_luz25 | 0 | PLACEHOLDER o RTP | 25 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 483 | Pictures/acto5_luz26 | 0 | PLACEHOLDER o RTP | 26 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 484 | Pictures/acto5_luz27 | 0 | PLACEHOLDER o RTP | 27 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 485 | Pictures/acto6_luz28 | 0 | PLACEHOLDER o RTP | 28 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 486 | Pictures/acto6_luz29 | 0 | PLACEHOLDER o RTP | 29 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 487 | Pictures/acto6_luz30 | 0 | PLACEHOLDER o RTP | 30 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 488 | Pictures/acto6_luz31 | 0 | PLACEHOLDER o RTP | 31 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 489 | Pictures/acto6_luz32 | 0 | PLACEHOLDER o RTP | 32 | [640, 480] | Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada. |
| 490 | Battlebacks/mente_piso | 0 | OK | BD/scripts | [640, 480] | Inventario aprobado fase 1/2; tamaño actual revisado por separado. |
| 491 | Pictures/ui_bar_cordura | 0 | OK | BD/scripts | [256, 8] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 492 | Pictures/ui_bar_vida | 0 | OK | BD/scripts | [256, 8] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 493 | Pictures/ui_gameover | 0 | OK | BD/scripts | [640, 480] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 494 | Pictures/ui_menu | 0 | OK | BD/scripts | [640, 480] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 495 | Pictures/ui_titulo | 0 | OK | BD/scripts | [640, 480] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 496 | Icons/ui_estado_3 | 0 | OK | BD/scripts | [24, 24] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 497 | Icons/ui_estado_4 | 0 | OK | BD/scripts | [24, 24] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 498 | Battlebacks/ui_alcantarillas | 0 | OK | 17, 18, 19, 28, 31 | [640, 480] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 499 | Battlebacks/ui_camaras | 0 | OK | 9, 25 | [640, 480] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 500 | Battlebacks/ui_laboratorio | 0 | OK | 12, 13, 14, 15, 16 | [640, 480] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 501 | Battlebacks/ui_manada | 0 | OK | 20, 21, 32 | [640, 480] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |
| 502 | Battlebacks/ui_matadero | 0 | OK | 5, 6, 7, 8, 10, 11, 22, 23, 24, 26, 27, 29 | [640, 480] | Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y diseno/arte_hd2d/interfaz/manifest.json |

## Por mapa y acto

### Mapa 01 — Acto I — MAP001

- #139 Pictures/retrato_dog_neutral, hue 0: **OK**.
- #140 Tilesets/revision_mapa01, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #156 Battlebacks/ui_piso, hue 0: **OK**.
- #463 Pictures/revision_luz01, hue 0: **PLACEHOLDER o RTP**.
### Mapa 02 — Acto I — El piso

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #139 Pictures/retrato_dog_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #144 Characters/vacas_madre, hue 0: **OK**.
- #145 Pictures/retrato_madre_ira, hue 0: **OK**.
- #146 Pictures/retrato_madre_neutral, hue 0: **OK**.
- #147 Pictures/screamer_7, hue 0: **OK**.
- #148 Characters/vacas_muebles, hue 0: **OK**.
- #149 Pictures/screamer_1, hue 0: **OK**.
- #150 Characters/vacas_cosas, hue 0: **OK**.
- #151 Pictures/screamer_2, hue 0: **OK**.
- #152 Characters/vacas_perro, hue 0: **OK**.
- #153 Pictures/retrato_dog_miedo, hue 0: **OK**.
- #154 Characters/vacas_vacio, hue 0: **OK**.
- #155 Autotiles/052-Carpet02, hue 0: **OK**.
- #156 Battlebacks/ui_piso, hue 0: **OK**.
- #157 Tilesets/revision_mapa02, hue 0: **OK**.
- #464 Pictures/revision_luz02, hue 0: **PLACEHOLDER o RTP**.
### Mapa 03 — Acto I — La escalera

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #150 Characters/vacas_cosas, hue 0: **OK**.
- #155 Autotiles/052-Carpet02, hue 0: **OK**.
- #156 Battlebacks/ui_piso, hue 0: **OK**.
- #158 Characters/vacas_puerta, hue 0: **OK**.
- #159 Characters/vacas_remedios, hue 0: **OK**.
- #160 Pictures/retrato_remedios_neutral, hue 0: **OK**.
- #161 Characters/vacas_anselmo, hue 0: **OK**.
- #162 Pictures/retrato_anselmo_neutral, hue 0: **OK**.
- #163 Characters/185-Light02, hue 0: **OK**.
- #164 Characters/vacas_lucy, hue 0: **OK**.
- #165 Pictures/retrato_lucy_susurro, hue 0: **OK**.
- #166 Tilesets/revision_mapa03, hue 0: **OK**.
- #465 Pictures/revision_luz03, hue 0: **PLACEHOLDER o RTP**.
### Mapa 04 — Acto I — La calle

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #139 Pictures/retrato_dog_neutral, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #150 Characters/vacas_cosas, hue 0: **OK**.
- #154 Characters/vacas_vacio, hue 0: **OK**.
- #156 Battlebacks/ui_piso, hue 0: **OK**.
- #158 Characters/vacas_puerta, hue 0: **OK**.
- #167 Characters/vacas_tablon, hue 0: **OK**.
- #168 Pictures/retrato_molina_neutral, hue 0: **OK**.
- #169 Characters/vacas_carnicero, hue 0: **OK**.
- #170 Characters/vacas_borracho, hue 0: **OK**.
- #171 Pictures/retrato_borracho_neutral, hue 0: **OK**.
- #172 Characters/vacas_transeunte, hue 0: **OK**.
- #173 Characters/vacas_furgoneta, hue 0: **OK**.
- #174 Characters/vacas_reclutador, hue 0: **OK**.
- #175 Pictures/retrato_reclutador_neutral, hue 0: **OK**.
- #176 Autotiles/048-Water01, hue 0: **OK**.
- #177 Autotiles/002-G_Shadow01, hue 0: **OK**.
- #178 Autotiles/003-G_Ground01, hue 0: **OK**.
- #179 Autotiles/005-G_Road01, hue 0: **OK**.
- #180 Autotiles/006-G_Road02, hue 0: **OK**.
- #181 Autotiles/050-Roof02, hue 0: **OK**.
- #182 Tilesets/revision_mapa04, hue 0: **OK**.
- #466 Pictures/revision_luz04, hue 0: **PLACEHOLDER o RTP**.
### Mapa 05 — Acto II — Matadero: entrada

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #139 Pictures/retrato_dog_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #154 Characters/vacas_vacio, hue 0: **OK**.
- #167 Characters/vacas_tablon, hue 0: **OK**.
- #173 Characters/vacas_furgoneta, hue 0: **OK**.
- #183 Pictures/retrato_steven_miedo, hue 0: **OK**.
- #184 Pictures/screamer_3, hue 0: **OK**.
- #185 Characters/vacas_obrero1, hue 0: **OK**.
- #186 Pictures/retrato_benito_neutral, hue 0: **OK**.
- #187 Characters/vacas_cripps, hue 0: **OK**.
- #188 Pictures/retrato_cripps_neutral, hue 0: **OK**.
- #189 Characters/vacas_matadero, hue 0: **OK**.
- #190 Tilesets/revision_mapa05, hue 0: **OK**.
- #467 Pictures/revision_luz05, hue 0: **PLACEHOLDER o RTP**.
- #502 Battlebacks/ui_matadero, hue 0: **OK**.
### Mapa 06 — Acto II — Matadero: vestuario

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #191 Pictures/screamer_4, hue 0: **OK**.
- #192 Characters/vacas_obrero3, hue 0: **OK**.
- #193 Pictures/retrato_encarna_neutral, hue 0: **OK**.
- #194 Characters/vacas_obrero4, hue 0: **OK**.
- #195 Pictures/retrato_chato_neutral, hue 0: **OK**.
- #196 Tilesets/revision_mapa06, hue 0: **OK**.
- #468 Pictures/revision_luz06, hue 0: **PLACEHOLDER o RTP**.
- #502 Battlebacks/ui_matadero, hue 0: **OK**.
### Mapa 07 — Acto II — Matadero: corrales

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #139 Pictures/retrato_dog_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #183 Pictures/retrato_steven_miedo, hue 0: **OK**.
- #197 Characters/vacas_vaca, hue 0: **OK**.
- #198 Characters/vacas_vaca_canela, hue 0: **OK**.
- #199 Characters/vacas_obrero2, hue 0: **OK**.
- #200 Pictures/retrato_rubio_neutral, hue 0: **OK**.
- #201 Tilesets/revision_mapa07, hue 0: **OK**.
- #469 Pictures/revision_luz07, hue 0: **PLACEHOLDER o RTP**.
- #502 Battlebacks/ui_matadero, hue 0: **OK**.
### Mapa 08 — Acto II — Matadero: la cadena

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #185 Characters/vacas_obrero1, hue 0: **OK**.
- #186 Pictures/retrato_benito_neutral, hue 0: **OK**.
- #187 Characters/vacas_cripps, hue 0: **OK**.
- #188 Pictures/retrato_cripps_neutral, hue 0: **OK**.
- #189 Characters/vacas_matadero, hue 0: **OK**.
- #192 Characters/vacas_obrero3, hue 0: **OK**.
- #193 Pictures/retrato_encarna_neutral, hue 0: **OK**.
- #198 Characters/vacas_vaca_canela, hue 0: **OK**.
- #199 Characters/vacas_obrero2, hue 0: **OK**.
- #202 Pictures/retrato_cripps_ira, hue 0: **OK**.
- #203 Pictures/retrato_sierra_neutral, hue 0: **OK**.
- #204 Tilesets/revision_mapa08, hue 0: **OK**.
- #470 Pictures/revision_luz08, hue 0: **PLACEHOLDER o RTP**.
- #502 Battlebacks/ui_matadero, hue 0: **OK**.
### Mapa 09 — Acto II — Matadero: cámaras frías

- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #187 Characters/vacas_cripps, hue 0: **OK**.
- #188 Pictures/retrato_cripps_neutral, hue 0: **OK**.
- #189 Characters/vacas_matadero, hue 0: **OK**.
- #202 Pictures/retrato_cripps_ira, hue 0: **OK**.
- #205 Pictures/screamer_6, hue 0: **OK**.
- #206 Tilesets/revision_mapa09, hue 0: **OK**.
- #471 Pictures/revision_luz09, hue 0: **PLACEHOLDER o RTP**.
- #499 Battlebacks/ui_camaras, hue 0: **OK**.
### Mapa 10 — Acto II — Matadero: oficina de Cripps

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #187 Characters/vacas_cripps, hue 0: **OK**.
- #188 Pictures/retrato_cripps_neutral, hue 0: **OK**.
- #189 Characters/vacas_matadero, hue 0: **OK**.
- #202 Pictures/retrato_cripps_ira, hue 0: **OK**.
- #205 Pictures/screamer_6, hue 0: **OK**.
- #207 Tilesets/revision_mapa10, hue 0: **OK**.
- #472 Pictures/revision_luz10, hue 0: **PLACEHOLDER o RTP**.
- #502 Battlebacks/ui_matadero, hue 0: **OK**.
### Mapa 11 — Acto II — Matadero: pasillo de mantenimiento

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #189 Characters/vacas_matadero, hue 0: **OK**.
- #208 Pictures/screamer_5, hue 0: **OK**.
- #209 Pictures/retrato_guernsey_susurro, hue 0: **OK**.
- #210 Tilesets/revision_mapa11, hue 0: **OK**.
- #473 Pictures/revision_luz11, hue 0: **PLACEHOLDER o RTP**.
- #502 Battlebacks/ui_matadero, hue 0: **OK**.
### Mapa 12 — Acto III — Lucy: el piso de arriba

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #148 Characters/vacas_muebles, hue 0: **OK**.
- #164 Characters/vacas_lucy, hue 0: **OK**.
- #183 Pictures/retrato_steven_miedo, hue 0: **OK**.
- #211 Pictures/retrato_lucy_neutral, hue 0: **OK**.
- #212 Characters/vacas_laboratorio, hue 0: **OK**.
- #213 Pictures/retrato_lucy_calma, hue 0: **OK**.
- #214 Tilesets/revision_mapa12, hue 0: **OK**.
- #474 Pictures/revision_luz12, hue 0: **PLACEHOLDER o RTP**.
- #500 Battlebacks/ui_laboratorio, hue 0: **OK**.
### Mapa 13 — Acto III — Carnicería Molina

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #168 Pictures/retrato_molina_neutral, hue 0: **OK**.
- #169 Characters/vacas_carnicero, hue 0: **OK**.
- #212 Characters/vacas_laboratorio, hue 0: **OK**.
- #215 Tilesets/revision_mapa13, hue 0: **OK**.
- #475 Pictures/revision_luz13, hue 0: **PLACEHOLDER o RTP**.
- #500 Battlebacks/ui_laboratorio, hue 0: **OK**.
### Mapa 14 — Acto III — Carnicería cerrada: depósito

- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #183 Pictures/retrato_steven_miedo, hue 0: **OK**.
- #187 Characters/vacas_cripps, hue 0: **OK**.
- #212 Characters/vacas_laboratorio, hue 0: **OK**.
- #216 Pictures/screamer_8, hue 0: **OK**.
- #217 Tilesets/revision_mapa14, hue 0: **OK**.
- #476 Pictures/revision_luz14, hue 0: **PLACEHOLDER o RTP**.
- #500 Battlebacks/ui_laboratorio, hue 0: **OK**.
### Mapa 15 — Acto III — Hospital cerrado: curas

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #212 Characters/vacas_laboratorio, hue 0: **OK**.
- #218 Characters/vacas_elena, hue 0: **OK**.
- #219 Pictures/retrato_elena_neutral, hue 0: **OK**.
- #220 Characters/vacas_alcantarilla, hue 0: **OK**.
- #221 Tilesets/revision_mapa15, hue 0: **OK**.
- #477 Pictures/revision_luz15, hue 0: **PLACEHOLDER o RTP**.
- #500 Battlebacks/ui_laboratorio, hue 0: **OK**.
### Mapa 16 — Acto III — Lucy: laboratorio improvisado

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #164 Characters/vacas_lucy, hue 0: **OK**.
- #183 Pictures/retrato_steven_miedo, hue 0: **OK**.
- #209 Pictures/retrato_guernsey_susurro, hue 0: **OK**.
- #211 Pictures/retrato_lucy_neutral, hue 0: **OK**.
- #212 Characters/vacas_laboratorio, hue 0: **OK**.
- #213 Pictures/retrato_lucy_calma, hue 0: **OK**.
- #222 Pictures/retrato_lucy_quiebre, hue 0: **OK**.
- #223 Pictures/screamer_9, hue 0: **OK**.
- #224 Tilesets/revision_mapa16, hue 0: **OK**.
- #478 Pictures/revision_luz16, hue 0: **PLACEHOLDER o RTP**.
- #500 Battlebacks/ui_laboratorio, hue 0: **OK**.
### Mapa 17 — Acto IV — Colector: la ultima escalera

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #183 Pictures/retrato_steven_miedo, hue 0: **OK**.
- #209 Pictures/retrato_guernsey_susurro, hue 0: **OK**.
- #220 Characters/vacas_alcantarilla, hue 0: **OK**.
- #225 Tilesets/acto4_alcantarillas, hue 0: **OK**.
- #226 Battlebacks/mente_tunel, hue 0: **OK**.
- #498 Battlebacks/ui_alcantarillas, hue 0: **OK**.
### Mapa 18 — Acto IV — Tuneles: nombres sin collar

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #220 Characters/vacas_alcantarilla, hue 0: **OK**.
- #225 Tilesets/acto4_alcantarillas, hue 0: **OK**.
- #226 Battlebacks/mente_tunel, hue 0: **OK**.
- #227 Characters/vacas_muesca, hue 0: **OK**.
- #228 Pictures/retrato_muesca_neutral, hue 0: **OK**.
- #229 Pictures/screamer_10, hue 0: **OK**.
- #498 Battlebacks/ui_alcantarillas, hue 0: **OK**.
### Mapa 19 — Acto IV — Canal de retorno

- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #220 Characters/vacas_alcantarilla, hue 0: **OK**.
- #225 Tilesets/acto4_alcantarillas, hue 0: **OK**.
- #226 Battlebacks/mente_tunel, hue 0: **OK**.
- #227 Characters/vacas_muesca, hue 0: **OK**.
- #230 Characters/vacas_junco, hue 0: **OK**.
- #231 Pictures/retrato_junco_neutral, hue 0: **OK**.
- #232 Pictures/screamer_11, hue 0: **OK**.
- #498 Battlebacks/ui_alcantarillas, hue 0: **OK**.
### Mapa 20 — Acto IV — La camara de la manada

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #209 Pictures/retrato_guernsey_susurro, hue 0: **OK**.
- #220 Characters/vacas_alcantarilla, hue 0: **OK**.
- #225 Tilesets/acto4_alcantarillas, hue 0: **OK**.
- #226 Battlebacks/mente_tunel, hue 0: **OK**.
- #227 Characters/vacas_muesca, hue 0: **OK**.
- #228 Pictures/retrato_muesca_neutral, hue 0: **OK**.
- #230 Characters/vacas_junco, hue 0: **OK**.
- #231 Pictures/retrato_junco_neutral, hue 0: **OK**.
- #233 Characters/vacas_guernsey4, hue 0: **OK**.
- #501 Battlebacks/ui_manada, hue 0: **OK**.
### Mapa 21 — Acto IV — Altar de las cosas salvadas

- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #220 Characters/vacas_alcantarilla, hue 0: **OK**.
- #225 Tilesets/acto4_alcantarillas, hue 0: **OK**.
- #226 Battlebacks/mente_tunel, hue 0: **OK**.
- #501 Battlebacks/ui_manada, hue 0: **OK**.
### Mapa 22 — Acto V — Matanza: muelle de carga

- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #183 Pictures/retrato_steven_miedo, hue 0: **OK**.
- #185 Characters/vacas_obrero1, hue 0: **OK**.
- #186 Pictures/retrato_benito_neutral, hue 0: **OK**.
- #209 Pictures/retrato_guernsey_susurro, hue 0: **OK**.
- #234 Tilesets/acto5_matanza, hue 0: **OK**.
- #479 Pictures/acto5_luz22, hue 0: **PLACEHOLDER o RTP**.
- #502 Battlebacks/ui_matadero, hue 0: **OK**.
### Mapa 23 — Acto V — Matanza: corrales de espera

- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #183 Pictures/retrato_steven_miedo, hue 0: **OK**.
- #197 Characters/vacas_vaca, hue 0: **OK**.
- #198 Characters/vacas_vaca_canela, hue 0: **OK**.
- #199 Characters/vacas_obrero2, hue 0: **OK**.
- #203 Pictures/retrato_sierra_neutral, hue 0: **OK**.
- #209 Pictures/retrato_guernsey_susurro, hue 0: **OK**.
- #227 Characters/vacas_muesca, hue 0: **OK**.
- #228 Pictures/retrato_muesca_neutral, hue 0: **OK**.
- #230 Characters/vacas_junco, hue 0: **OK**.
- #231 Pictures/retrato_junco_neutral, hue 0: **OK**.
- #234 Tilesets/acto5_matanza, hue 0: **OK**.
- #480 Pictures/acto5_luz23, hue 0: **PLACEHOLDER o RTP**.
- #502 Battlebacks/ui_matadero, hue 0: **OK**.
### Mapa 24 — Acto V — Matanza: sala de matanza

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #183 Pictures/retrato_steven_miedo, hue 0: **OK**.
- #192 Characters/vacas_obrero3, hue 0: **OK**.
- #194 Characters/vacas_obrero4, hue 0: **OK**.
- #195 Pictures/retrato_chato_neutral, hue 0: **OK**.
- #200 Pictures/retrato_rubio_neutral, hue 0: **OK**.
- #234 Tilesets/acto5_matanza, hue 0: **OK**.
- #481 Pictures/acto5_luz24, hue 0: **PLACEHOLDER o RTP**.
- #502 Battlebacks/ui_matadero, hue 0: **OK**.
### Mapa 25 — Acto V — Matanza: camara de sangrado

- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #183 Pictures/retrato_steven_miedo, hue 0: **OK**.
- #187 Characters/vacas_cripps, hue 0: **OK**.
- #202 Pictures/retrato_cripps_ira, hue 0: **OK**.
- #209 Pictures/retrato_guernsey_susurro, hue 0: **OK**.
- #234 Tilesets/acto5_matanza, hue 0: **OK**.
- #235 Pictures/screamer_12, hue 0: **OK**.
- #236 Pictures/screamer_13, hue 0: **OK**.
- #482 Pictures/acto5_luz25, hue 0: **PLACEHOLDER o RTP**.
- #499 Battlebacks/ui_camaras, hue 0: **OK**.
### Mapa 26 — Acto V — Matanza: oficina alta

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #183 Pictures/retrato_steven_miedo, hue 0: **OK**.
- #187 Characters/vacas_cripps, hue 0: **OK**.
- #188 Pictures/retrato_cripps_neutral, hue 0: **OK**.
- #202 Pictures/retrato_cripps_ira, hue 0: **OK**.
- #209 Pictures/retrato_guernsey_susurro, hue 0: **OK**.
- #233 Characters/vacas_guernsey4, hue 0: **OK**.
- #234 Tilesets/acto5_matanza, hue 0: **OK**.
- #483 Pictures/acto5_luz26, hue 0: **PLACEHOLDER o RTP**.
- #502 Battlebacks/ui_matadero, hue 0: **OK**.
### Mapa 27 — Acto V — Matanza: patio del alba

- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #183 Pictures/retrato_steven_miedo, hue 0: **OK**.
- #192 Characters/vacas_obrero3, hue 0: **OK**.
- #194 Characters/vacas_obrero4, hue 0: **OK**.
- #195 Pictures/retrato_chato_neutral, hue 0: **OK**.
- #197 Characters/vacas_vaca, hue 0: **OK**.
- #198 Characters/vacas_vaca_canela, hue 0: **OK**.
- #200 Pictures/retrato_rubio_neutral, hue 0: **OK**.
- #209 Pictures/retrato_guernsey_susurro, hue 0: **OK**.
- #227 Characters/vacas_muesca, hue 0: **OK**.
- #228 Pictures/retrato_muesca_neutral, hue 0: **OK**.
- #230 Characters/vacas_junco, hue 0: **OK**.
- #231 Pictures/retrato_junco_neutral, hue 0: **OK**.
- #233 Characters/vacas_guernsey4, hue 0: **OK**.
- #234 Tilesets/acto5_matanza, hue 0: **OK**.
- #484 Pictures/acto5_luz27, hue 0: **PLACEHOLDER o RTP**.
- #502 Battlebacks/ui_matadero, hue 0: **OK**.
### Mapa 28 — Acto VI — Túneles profundos: la raíz

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #209 Pictures/retrato_guernsey_susurro, hue 0: **OK**.
- #211 Pictures/retrato_lucy_neutral, hue 0: **OK**.
- #213 Pictures/retrato_lucy_calma, hue 0: **OK**.
- #227 Characters/vacas_muesca, hue 0: **OK**.
- #228 Pictures/retrato_muesca_neutral, hue 0: **OK**.
- #237 Tilesets/acto6_reydios, hue 0: **OK**.
- #485 Pictures/acto6_luz28, hue 0: **PLACEHOLDER o RTP**.
- #498 Battlebacks/ui_alcantarillas, hue 0: **OK**.
### Mapa 29 — Acto VI — Ciudad tomada: el nuevo turno

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #139 Pictures/retrato_dog_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #185 Characters/vacas_obrero1, hue 0: **OK**.
- #192 Characters/vacas_obrero3, hue 0: **OK**.
- #197 Characters/vacas_vaca, hue 0: **OK**.
- #200 Pictures/retrato_rubio_neutral, hue 0: **OK**.
- #209 Pictures/retrato_guernsey_susurro, hue 0: **OK**.
- #233 Characters/vacas_guernsey4, hue 0: **OK**.
- #237 Tilesets/acto6_reydios, hue 0: **OK**.
- #486 Pictures/acto6_luz29, hue 0: **PLACEHOLDER o RTP**.
- #502 Battlebacks/ui_matadero, hue 0: **OK**.
### Mapa 30 — Acto VI — El piso: la última cena

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #139 Pictures/retrato_dog_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #144 Characters/vacas_madre, hue 0: **OK**.
- #145 Pictures/retrato_madre_ira, hue 0: **OK**.
- #152 Characters/vacas_perro, hue 0: **OK**.
- #156 Battlebacks/ui_piso, hue 0: **OK**.
- #237 Tilesets/acto6_reydios, hue 0: **OK**.
- #238 Pictures/retrato_madre_envejecida_neutral, hue 0: **OK**.
- #487 Pictures/acto6_luz30, hue 0: **PLACEHOLDER o RTP**.
### Mapa 31 — Acto VI — Galería de compuertas

- #139 Pictures/retrato_dog_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #200 Pictures/retrato_rubio_neutral, hue 0: **OK**.
- #237 Tilesets/acto6_reydios, hue 0: **OK**.
- #488 Pictures/acto6_luz31, hue 0: **PLACEHOLDER o RTP**.
- #498 Battlebacks/ui_alcantarillas, hue 0: **OK**.
### Mapa 32 — Acto VI — Rey-dios: el altar

- #61 Pictures/retrato_steven_neutral, hue 0: **OK**.
- #139 Pictures/retrato_dog_neutral, hue 0: **OK**.
- #141 Autotiles/053-Wall01, hue 0: **OK**.
- #142 Autotiles/vacas_canal, hue 0: **OK**.
- #143 Fogs/002-Clouds01, hue 0: **OK**.
- #152 Characters/vacas_perro, hue 0: **OK**.
- #209 Pictures/retrato_guernsey_susurro, hue 0: **OK**.
- #228 Pictures/retrato_muesca_neutral, hue 0: **OK**.
- #233 Characters/vacas_guernsey4, hue 0: **OK**.
- #237 Tilesets/acto6_reydios, hue 0: **OK**.
- #489 Pictures/acto6_luz32, hue 0: **PLACEHOLDER o RTP**.
- #501 Battlebacks/ui_manada, hue 0: **OK**.

## Cada referencia en Data/scripts

Rutas exactas de objeto: evento/página/comando, enemigo y tropa. El JSON permite filtrar todas las ocurrencias.

### #1 Characters/vacas_steven — OK

- `Actors[1].character_name`
- `Scripts[89] Vacas_Nucleo:131`
- `Scripts[97] Vacas_Lucy:12`
### #2 Battlers/steven_mente — OK

- `Actors[1].battler_name`
- `System.battler_name`
- `Scripts[95] Vacas_Mente:11`
- `Scripts[97] Vacas_Lucy:12`
### #3 Characters/010-Lancer02 — PLACEHOLDER o RTP

- `Actors[2].character_name`
### #4 Battlers/010-Lancer02 — PLACEHOLDER o RTP

- `Actors[2].battler_name`
### #5 Characters/013-Warrior01 — PLACEHOLDER o RTP

- `Actors[3].character_name`
### #6 Battlers/013-Warrior01 — PLACEHOLDER o RTP

- `Actors[3].battler_name`
### #7 Characters/019-Thief04 — PLACEHOLDER o RTP

- `Actors[4].character_name`
### #8 Battlers/019-Thief04 — PLACEHOLDER o RTP

- `Actors[4].battler_name`
### #9 Characters/022-Hunter03 — PLACEHOLDER o RTP

- `Actors[5].character_name`
### #10 Battlers/022-Hunter03 — PLACEHOLDER o RTP

- `Actors[5].battler_name`
### #11 Characters/023-Gunner01 — PLACEHOLDER o RTP

- `Actors[6].character_name`
### #12 Battlers/023-Gunner01 — PLACEHOLDER o RTP

- `Actors[6].battler_name`
### #13 Characters/029-Cleric05 — PLACEHOLDER o RTP

- `Actors[7].character_name`
### #14 Battlers/029-Cleric05 — PLACEHOLDER o RTP

- `Actors[7].battler_name`
### #15 Characters/038-Mage06 — PLACEHOLDER o RTP

- `Actors[8].character_name`
### #16 Battlers/038-Mage06 — PLACEHOLDER o RTP

- `Actors[8].battler_name`
### #17 Animations/001-Action01 — PLACEHOLDER o RTP

- `Animations[1].animation_name`
- `Animations[2].animation_name`
### #18 Animations/002-Action02 — PLACEHOLDER o RTP

- `Animations[3].animation_name`
### #19 Animations/003-Attack01 — PLACEHOLDER o RTP

- `Animations[4].animation_name`
- `Animations[13].animation_name`
- `Animations[14].animation_name`
### #20 Animations/004-Attack02 — PLACEHOLDER o RTP

- `Animations[5].animation_name`
### #21 Animations/005-Attack03 — PLACEHOLDER o RTP

- `Animations[6].animation_name`
### #22 Animations/006-Weapon01 — PLACEHOLDER o RTP

- `Animations[7].animation_name`
- `Animations[67].animation_name`
- `Animations[68].animation_name`
- `Animations[69].animation_name`
- `Animations[70].animation_name`
### #23 Animations/007-Weapon02 — PLACEHOLDER o RTP

- `Animations[8].animation_name`
- `Animations[71].animation_name`
- `Animations[72].animation_name`
- `Animations[73].animation_name`
- `Animations[74].animation_name`
### #24 Animations/008-Weapon03 — PLACEHOLDER o RTP

- `Animations[9].animation_name`
- `Animations[75].animation_name`
- `Animations[77].animation_name`
- `Animations[78].animation_name`
### #25 Animations/009-Weapon04 — PLACEHOLDER o RTP

- `Animations[10].animation_name`
- `Animations[79].animation_name`
- `Animations[80].animation_name`
- `Animations[81].animation_name`
- `Animations[82].animation_name`
### #26 Animations/010-Weapon05 — PLACEHOLDER o RTP

- `Animations[11].animation_name`
- `Animations[83].animation_name`
- `Animations[84].animation_name`
- `Animations[85].animation_name`
- `Animations[86].animation_name`
### #27 Animations/011-Weapon06 — PLACEHOLDER o RTP

- `Animations[12].animation_name`
- `Animations[88].animation_name`
- `Animations[90].animation_name`
### #28 Animations/012-Heal01 — PLACEHOLDER o RTP

- `Animations[15].animation_name`
- `Animations[16].animation_name`
- `Animations[17].animation_name`
### #29 Animations/013-Heal02 — PLACEHOLDER o RTP

- `Animations[18].animation_name`
- `Animations[19].animation_name`
- `Animations[20].animation_name`
- `Animations[21].animation_name`
- `Animations[22].animation_name`
### #30 Animations/014-Heal03 — PLACEHOLDER o RTP

- `Animations[23].animation_name`
- `Animations[24].animation_name`
- `Animations[25].animation_name`
- `Animations[26].animation_name`
### #31 Animations/015-Fire01 — PLACEHOLDER o RTP

- `Animations[27].animation_name`
- `Animations[28].animation_name`
- `Animations[29].animation_name`
### #32 Animations/016-Ice01 — PLACEHOLDER o RTP

- `Animations[30].animation_name`
- `Animations[31].animation_name`
- `Animations[32].animation_name`
### #33 Animations/017-Thunder01 — PLACEHOLDER o RTP

- `Animations[33].animation_name`
- `Animations[34].animation_name`
- `Animations[35].animation_name`
### #34 Animations/018-Water01 — PLACEHOLDER o RTP

- `Animations[36].animation_name`
- `Animations[37].animation_name`
- `Animations[38].animation_name`
### #35 Animations/019-Earth01 — PLACEHOLDER o RTP

- `Animations[39].animation_name`
- `Animations[40].animation_name`
- `Animations[41].animation_name`
### #36 Animations/020-Wind01 — PLACEHOLDER o RTP

- `Animations[42].animation_name`
- `Animations[43].animation_name`
- `Animations[44].animation_name`
### #37 Animations/021-Light01 — PLACEHOLDER o RTP

- `Animations[45].animation_name`
- `Animations[46].animation_name`
- `Animations[47].animation_name`
### #38 Animations/022-Darkness01 — PLACEHOLDER o RTP

- `Animations[48].animation_name`
- `Animations[49].animation_name`
- `Animations[50].animation_name`
### #39 Animations/023-Burst01 — PLACEHOLDER o RTP

- `Animations[51].animation_name`
- `Animations[52].animation_name`
### #40 Animations/024-Support01 — PLACEHOLDER o RTP

- `Animations[53].animation_name`
- `Animations[54].animation_name`
- `Animations[55].animation_name`
### #41 Animations/025-Support02 — PLACEHOLDER o RTP

- `Animations[56].animation_name`
- `Animations[57].animation_name`
- `Animations[58].animation_name`
### #42 Animations/026-Support03 — PLACEHOLDER o RTP

- `Animations[59].animation_name`
### #43 Animations/026-Support03 — PLACEHOLDER o RTP

- `Animations[60].animation_name`
### #44 Animations/026-Support03 — PLACEHOLDER o RTP

- `Animations[61].animation_name`
### #45 Animations/026-Support03 — PLACEHOLDER o RTP

- `Animations[62].animation_name`
### #46 Animations/027-Support04 — PLACEHOLDER o RTP

- `Animations[63].animation_name`
- `Animations[64].animation_name`
- `Animations[65].animation_name`
### #47 Animations/027-Support04 — PLACEHOLDER o RTP

- `Animations[66].animation_name`
### #48 Animations/008-Weapon03 — PLACEHOLDER o RTP

- `Animations[76].animation_name`
### #49 Animations/011-Weapon06 — PLACEHOLDER o RTP

- `Animations[87].animation_name`
### #50 Animations/011-Weapon06 — PLACEHOLDER o RTP

- `Animations[89].animation_name`
### #51 Animations/028-State01 — PLACEHOLDER o RTP

- `Animations[91].animation_name`
- `Animations[92].animation_name`
- `Animations[93].animation_name`
- `Animations[94].animation_name`
- `Animations[95].animation_name`
- `Animations[96].animation_name`
### #52 Animations/029-Emotion01 — PLACEHOLDER o RTP

- `Animations[97].animation_name`
- `Animations[98].animation_name`
### #53 Animations/030-Explosion01 — PLACEHOLDER o RTP

- `Animations[99].animation_name`
- `Animations[100].animation_name`
### #54 Icons/009-Shield01 — PLACEHOLDER o RTP

- `Armors[1].icon_name`
- `Armors[2].icon_name`
- `Armors[3].icon_name`
- `Armors[4].icon_name`
### #55 Icons/010-Head01 — PLACEHOLDER o RTP

- `Armors[5].icon_name`
- `Armors[6].icon_name`
- `Armors[7].icon_name`
- `Armors[8].icon_name`
### #56 Icons/011-Head02 — PLACEHOLDER o RTP

- `Armors[9].icon_name`
- `Armors[10].icon_name`
- `Armors[11].icon_name`
- `Armors[12].icon_name`
### #57 Icons/013-Body01 — PLACEHOLDER o RTP

- `Armors[13].icon_name`
- `Armors[14].icon_name`
- `Armors[15].icon_name`
- `Armors[16].icon_name`
### #58 Icons/014-Body02 — PLACEHOLDER o RTP

- `Armors[17].icon_name`
- `Armors[18].icon_name`
- `Armors[19].icon_name`
- `Armors[20].icon_name`
### #59 Icons/015-Body03 — PLACEHOLDER o RTP

- `Armors[21].icon_name`
- `Armors[22].icon_name`
- `Armors[23].icon_name`
- `Armors[24].icon_name`
### #60 Icons/016-Accessory01 — PLACEHOLDER o RTP

- `Armors[25].icon_name`
- `Armors[26].icon_name`
- `Armors[27].icon_name`
- `Armors[28].icon_name`
- `Armors[29].icon_name`
- `Armors[30].icon_name`
- `Armors[31].icon_name`
- `Armors[32].icon_name`
### #61 Pictures/retrato_steven_neutral — OK

- `CommonEvents[1].list[24].parameters[0]`
- `Map002.events.3.pages[0].list[5].parameters[0]`
- `Map002.events.3.pages[0].list[15].parameters[0]`
- `Map002.events.4.pages[1].list[52].parameters[0]`
- `Map002.events.4.pages[4].list[25].parameters[0]`
- `Map002.events.4.pages[5].list[25].parameters[0]`
- `Map002.events.5.pages[1].list[52].parameters[0]`
- `Map002.events.5.pages[4].list[25].parameters[0]`
- `Map002.events.5.pages[5].list[25].parameters[0]`
- `Map002.events.8.pages[0].list[3].parameters[0]`
- `Map002.events.14.pages[0].list[59].parameters[0]`
- `Map002.events.14.pages[0].list[133].parameters[0]`
- `Map002.events.14.pages[4].list[93].parameters[0]`
- `Map002.events.14.pages[5].list[6].parameters[0]`
- `Map002.events.15.pages[1].list[8].parameters[0]`
- `Map002.events.31.pages[0].list[116].parameters[0]`
- `Map002.events.34.pages[0].list[38].parameters[0]`
- `Map002.events.34.pages[0].list[45].parameters[0]`
- `Map002.events.34.pages[2].list[38].parameters[0]`
- `Map002.events.34.pages[2].list[45].parameters[0]`
- `Map002.events.39.pages[1].list[11].parameters[0]`
- `Map003.events.7.pages[0].list[4].parameters[0]`
- `Map003.events.7.pages[1].list[3].parameters[0]`
- `Map003.events.15.pages[1].list[46].parameters[0]`
- `Map004.events.3.pages[0].list[9].parameters[0]`
- `Map005.events.2.pages[0].list[17].parameters[0]`
- `Map006.events.5.pages[0].list[9].parameters[0]`
- `Map006.events.9.pages[0].list[4].parameters[0]`
- `Map007.events.11.pages[0].list[6].parameters[0]`
- `Map007.events.14.pages[0].list[9].parameters[0]`
- `Map008.events.53.pages[0].list[33].parameters[0]`
- `Map008.events.58.pages[0].list[9].parameters[0]`
- `Map008.events.59.pages[1].list[69].parameters[0]`
- `Map008.events.59.pages[1].list[79].parameters[0]`
- `Map010.events.1.pages[0].list[12].parameters[0]`
- `Map011.events.1.pages[0].list[10].parameters[0]`
- `Map011.events.1.pages[0].list[15].parameters[0]`
- `Map011.events.1.pages[0].list[138].parameters[0]`
- `Map011.events.1.pages[0].list[150].parameters[0]`
- `Map011.events.4.pages[0].list[16].parameters[0]`
- `Map012.events.4.pages[0].list[4].parameters[0]`
- `Map012.events.6.pages[0].list[5].parameters[0]`
- `Map013.events.3.pages[0].list[5].parameters[0]`
- `Map015.events.3.pages[0].list[6].parameters[0]`
- `Map016.events.7.pages[0].list[6].parameters[0]`
- `Map016.events.7.pages[0].list[14].parameters[0]`
- `Map016.events.7.pages[0].list[18].parameters[0]`
- `Map016.events.8.pages[0].list[64].parameters[0]`
- `Map016.events.8.pages[0].list[84].parameters[0]`
- `Map017.events.2.pages[0].list[7].parameters[0]`
- `Map018.events.5.pages[0].list[5].parameters[0]`
- `Map018.events.5.pages[0].list[11].parameters[0]`
- `Map020.events.4.pages[0].list[82].parameters[0]`
- `Map020.events.4.pages[0].list[98].parameters[0]`
- `Map024.events.3.pages[0].list[12].parameters[0]`
- `Map024.events.4.pages[0].list[12].parameters[0]`
- `Map026.events.9.pages[1].list[83].parameters[0]`
- `Map026.events.9.pages[1].list[137].parameters[0]`
- `Map028.events.2.pages[0].list[22].parameters[0]`
- `Map029.events.4.pages[1].list[2].parameters[0]`
- `Map030.events.2.pages[0].list[5].parameters[0]`
- `Map030.events.5.pages[0].list[2].parameters[0]`
- `Map030.events.5.pages[0].list[25].parameters[0]`
- `Map030.events.5.pages[0].list[28].parameters[0]`
- `Map030.events.5.pages[0].list[34].parameters[0]`
- `Map030.events.5.pages[0].list[39].parameters[0]`
- `Map030.events.5.pages[0].list[47].parameters[0]`
- `Map030.events.5.pages[0].list[51].parameters[0]`
- `Map030.events.5.pages[0].list[83].parameters[0]`
- `Map032.events.2.pages[0].list[7].parameters[0]`
- `Map032.events.7.pages[0].list[43].parameters[0]`
- `Map032.events.7.pages[0].list[47].parameters[0]`
- `Map032.events.7.pages[0].list[153].parameters[0]`
- `Map032.events.7.pages[0].list[262].parameters[0]`
- `Map032.events.7.pages[0].list[266].parameters[0]`
- `Scripts[104] Vacas_Cinematicas:5`
### #62 Battlers/enemigo_vaca — OK

- `Enemies[1].battler_name`
- `DB.Troops[1].Enemies[1].battler_name`
### #63 Battlers/enemigo_madre — OK

- `Enemies[2].battler_name`
- `DB.Troops[2].Enemies[2].battler_name`
### #64 Battlers/enemigo_tunel — OK

- `Enemies[3].battler_name`
- `DB.Troops[3].Enemies[3].battler_name`
### #65 Battlers/enemigo_sombra_cripps — OK

- `Enemies[4].battler_name`
- `DB.Troops[4].Enemies[4].battler_name`
### #66 Battlers/enemigo_moscas — OK

- `Enemies[5].battler_name`
- `DB.Troops[5].Enemies[5].battler_name`
### #67 Battlers/enemigo_guernsey — OK

- `Enemies[6].battler_name`
- `DB.Troops[6].Enemies[6].battler_name`
### #68 Battlers/enemigo_canal — OK

- `Enemies[7].battler_name`
- `DB.Troops[7].Enemies[7].battler_name`
### #69 Battlers/enemigo_televisor — OK

- `Enemies[8].battler_name`
- `DB.Troops[8].Enemies[8].battler_name`
### #70 Battlers/enemigo_rey — OK

- `Enemies[9].battler_name`
- `DB.Troops[9].Enemies[9].battler_name`
### #71 Battlers/enemigo_tarro — OK

- `Enemies[10].battler_name`
- `DB.Troops[10].Enemies[10].battler_name`
### #72 Battlers/enemigo_factura — OK

- `Enemies[11].battler_name`
- `DB.Troops[11].Enemies[11].battler_name`
- `DB.Troops[22].Enemies[11].battler_name`
### #73 Battlers/enemigo_camilla — OK

- `Enemies[12].battler_name`
- `DB.Troops[12].Enemies[12].battler_name`
- `DB.Troops[23].Enemies[12].battler_name`
- `DB.Troops[24].Enemies[12].battler_name`
### #74 Battlers/enemigo_diagnostico — OK

- `Enemies[13].battler_name`
- `DB.Troops[13].Enemies[13].battler_name`
- `DB.Troops[25].Enemies[13].battler_name`
- `DB.Troops[26].Enemies[13].battler_name`
### #75 Battlers/enemigo_coro — OK

- `Enemies[14].battler_name`
- `DB.Troops[14].Enemies[14].battler_name`
- `DB.Troops[27].Enemies[14].battler_name`
- `DB.Troops[28].Enemies[14].battler_name`
### #76 Battlers/enemigo_pulmon — OK

- `Enemies[15].battler_name`
- `DB.Troops[15].Enemies[15].battler_name`
- `DB.Troops[29].Enemies[15].battler_name`
- `DB.Troops[30].Enemies[15].battler_name`
### #77 Battlers/enemigo_cencerro — OK

- `Enemies[16].battler_name`
- `DB.Troops[16].Enemies[16].battler_name`
- `DB.Troops[31].Enemies[16].battler_name`
- `DB.Troops[32].Enemies[16].battler_name`
### #78 Battlers/enemigo_pastor — OK

- `Enemies[17].battler_name`
- `DB.Troops[17].Enemies[17].battler_name`
### #79 Battlers/enemigo_turno_noche — OK

- `Enemies[18].battler_name`
- `DB.Troops[18].Enemies[18].battler_name`
### #80 Battlers/enemigo_res_cuenta — OK

- `Enemies[19].battler_name`
- `DB.Troops[19].Enemies[19].battler_name`
### #81 Battlers/enemigo_gancho_respira — OK

- `Enemies[20].battler_name`
- `DB.Troops[20].Enemies[20].battler_name`
### #82 Battlers/enemigo_cripps_matarife — OK

- `Enemies[21].battler_name`
- `DB.Troops[21].Enemies[21].battler_name`
### #83 Battlers/073-Bird03 — PLACEHOLDER o RTP

- `Enemies[22].battler_name`
### #84 Battlers/077-Devil03 — PLACEHOLDER o RTP

- `Enemies[23].battler_name`
### #85 Battlers/081-Angel03 — PLACEHOLDER o RTP

- `Enemies[24].battler_name`
### #86 Battlers/054-Undead04 — PLACEHOLDER o RTP

- `Enemies[25].battler_name`
### #87 Battlers/058-Snake04 — PLACEHOLDER o RTP

- `Enemies[26].battler_name`
### #88 Battlers/062-Aquatic04 — PLACEHOLDER o RTP

- `Enemies[27].battler_name`
### #89 Battlers/066-Beast04 — PLACEHOLDER o RTP

- `Enemies[28].battler_name`
### #90 Battlers/070-Goblin04 — PLACEHOLDER o RTP

- `Enemies[29].battler_name`
### #91 Battlers/074-Bird04 — PLACEHOLDER o RTP

- `Enemies[30].battler_name`
### #92 Battlers/078-Devil04 — PLACEHOLDER o RTP

- `Enemies[31].battler_name`
### #93 Battlers/082-Angel04 — PLACEHOLDER o RTP

- `Enemies[32].battler_name`
### #94 Battlers/enemigo_censo_bocas — OK

- `Enemies[33].battler_name`
- `DB.Troops[33].Enemies[33].battler_name`
### #95 Battlers/enemigo_mesa_exige — OK

- `Enemies[34].battler_name`
- `DB.Troops[34].Enemies[34].battler_name`
### #96 Battlers/enemigo_rey_sin_rostro — OK

- `Enemies[35].battler_name`
- `DB.Troops[35].Enemies[35].battler_name`
### #97 Battlers/enemigo_numero_cadena — OK

- `Enemies[36].battler_name`
- `DB.Troops[36].Enemies[36].battler_name`
### #98 Battlers/enemigo_puerta_muerde — OK

- `Enemies[37].battler_name`
- `DB.Troops[37].Enemies[37].battler_name`
### #99 Icons/vacas_item_01 — OK

- `Items[1].icon_name`
### #100 Icons/vacas_item_02 — OK

- `Items[2].icon_name`
### #101 Icons/vacas_item_03 — OK

- `Items[3].icon_name`
### #102 Icons/vacas_item_04 — OK

- `Items[4].icon_name`
### #103 Icons/vacas_item_05 — OK

- `Items[5].icon_name`
### #104 Icons/vacas_item_06 — OK

- `Items[6].icon_name`
### #105 Icons/vacas_item_07 — OK

- `Items[7].icon_name`
### #106 Icons/vacas_item_08 — OK

- `Items[8].icon_name`
### #107 Icons/vacas_item_09 — OK

- `Items[9].icon_name`
### #108 Icons/vacas_item_10 — OK

- `Items[10].icon_name`
### #109 Icons/vacas_item_11 — OK

- `Items[11].icon_name`
### #110 Icons/vacas_item_12 — OK

- `Items[12].icon_name`
### #111 Icons/vacas_item_13 — OK

- `Items[13].icon_name`
### #112 Icons/vacas_item_14 — OK

- `Items[14].icon_name`
### #113 Icons/vacas_item_15 — OK

- `Items[15].icon_name`
### #114 Icons/vacas_item_16 — OK

- `Items[16].icon_name`
### #115 Icons/vacas_item_17 — OK

- `Items[17].icon_name`
### #116 Icons/vacas_item_18 — OK

- `Items[18].icon_name`
### #117 Icons/vacas_item_19 — OK

- `Items[19].icon_name`
### #118 Icons/vacas_item_20 — OK

- `Items[20].icon_name`
### #119 Icons/vacas_item_21 — OK

- `Items[21].icon_name`
### #120 Icons/vacas_item_22 — OK

- `Items[22].icon_name`
### #121 Icons/vacas_item_23 — OK

- `Items[23].icon_name`
### #122 Icons/vacas_item_24 — OK

- `Items[24].icon_name`
### #123 Icons/vacas_item_25 — OK

- `Items[25].icon_name`
### #124 Icons/vacas_item_26 — OK

- `Items[26].icon_name`
### #125 Icons/vacas_item_27 — OK

- `Items[27].icon_name`
### #126 Icons/vacas_item_28 — OK

- `Items[28].icon_name`
### #127 Icons/vacas_item_29 — OK

- `Items[29].icon_name`
### #128 Icons/vacas_item_30 — OK

- `Items[30].icon_name`
### #129 Icons/vacas_item_31 — OK

- `Items[31].icon_name`
### #130 Icons/vacas_item_32 — OK

- `Items[32].icon_name`
### #131 Icons/vacas_item_33 — OK

- `Items[33].icon_name`
### #132 Icons/vacas_item_34 — OK

- `Items[34].icon_name`
### #133 Icons/vacas_item_35 — OK

- `Items[35].icon_name`
### #134 Icons/vacas_item_36 — OK

- `Items[36].icon_name`
### #135 Icons/vacas_item_37 — OK

- `Items[37].icon_name`
### #136 Icons/vacas_item_38 — OK

- `Items[38].icon_name`
### #137 Icons/vacas_item_39 — OK

- `Items[39].icon_name`
### #138 Icons/vacas_item_40 — OK

- `Items[40].icon_name`
### #139 Pictures/retrato_dog_neutral — OK

- `Map001.events.1.pages[0].list[13].parameters[0]`
- `Map001.events.1.pages[0].list[21].parameters[0]`
- `Map002.events.1.pages[1].list[52].parameters[0]`
- `Map002.events.4.pages[2].list[10].parameters[0]`
- `Map002.events.4.pages[2].list[82].parameters[0]`
- `Map002.events.4.pages[4].list[62].parameters[0]`
- `Map002.events.4.pages[4].list[97].parameters[0]`
- `Map002.events.4.pages[4].list[196].parameters[0]`
- `Map002.events.4.pages[5].list[62].parameters[0]`
- `Map002.events.4.pages[5].list[97].parameters[0]`
- `Map002.events.4.pages[5].list[196].parameters[0]`
- `Map002.events.5.pages[2].list[10].parameters[0]`
- `Map002.events.5.pages[2].list[82].parameters[0]`
- `Map002.events.5.pages[4].list[62].parameters[0]`
- `Map002.events.5.pages[4].list[97].parameters[0]`
- `Map002.events.5.pages[4].list[196].parameters[0]`
- `Map002.events.5.pages[5].list[62].parameters[0]`
- `Map002.events.5.pages[5].list[97].parameters[0]`
- `Map002.events.5.pages[5].list[196].parameters[0]`
- `Map002.events.6.pages[1].list[84].parameters[0]`
- `Map002.events.6.pages[1].list[162].parameters[0]`
- `Map002.events.8.pages[0].list[6].parameters[0]`
- `Map002.events.12.pages[1].list[79].parameters[0]`
- `Map002.events.12.pages[1].list[157].parameters[0]`
- `Map002.events.34.pages[0].list[2].parameters[0]`
- `Map002.events.34.pages[0].list[13].parameters[0]`
- `Map002.events.34.pages[0].list[31].parameters[0]`
- `Map002.events.34.pages[0].list[51].parameters[0]`
- `Map002.events.34.pages[2].list[2].parameters[0]`
- `Map002.events.34.pages[2].list[13].parameters[0]`
- `Map002.events.34.pages[2].list[31].parameters[0]`
- `Map002.events.34.pages[2].list[51].parameters[0]`
- `Map002.events.34.pages[3].list[1].parameters[0]`
- `Map002.events.34.pages[3].list[8].parameters[0]`
- `Map002.events.34.pages[3].list[21].parameters[0]`
- `Map002.events.34.pages[4].list[0].parameters[0]`
- `Map002.events.35.pages[0].list[0].parameters[0]`
- `Map002.events.36.pages[0].list[0].parameters[0]`
- `Map002.events.36.pages[1].list[0].parameters[0]`
- `Map002.events.39.pages[1].list[5].parameters[0]`
- `Map002.events.48.pages[1].list[56].parameters[0]`
- `Map004.events.19.pages[1].list[61].parameters[0]`
- `Map005.events.2.pages[0].list[3].parameters[0]`
- `Map007.events.14.pages[0].list[6].parameters[0]`
- `Map029.events.5.pages[1].list[0].parameters[0]`
- `Map030.events.2.pages[0].list[0].parameters[0]`
- `Map030.events.4.pages[0].list[0].parameters[0]`
- `Map030.events.5.pages[0].list[65].parameters[0]`
- `Map030.events.8.pages[0].list[0].parameters[0]`
- `Map030.events.9.pages[0].list[4].parameters[0]`
- `Map030.events.10.pages[0].list[4].parameters[0]`
- `Map031.events.2.pages[0].list[0].parameters[0]`
- `Map032.events.4.pages[0].list[0].parameters[0]`
- `Map032.events.7.pages[0].list[36].parameters[0]`
- `Map032.events.7.pages[0].list[93].parameters[0]`
- `Map032.events.7.pages[0].list[99].parameters[0]`
- `Map032.events.7.pages[0].list[146].parameters[0]`
- `Map032.events.7.pages[0].list[161].parameters[0]`
- `Map032.events.7.pages[0].list[167].parameters[0]`
- `Map032.events.7.pages[0].list[205].parameters[0]`
- `Map032.events.7.pages[0].list[210].parameters[0]`
- `Map032.events.7.pages[0].list[257].parameters[0]`
- `Map032.events.7.pages[0].list[274].parameters[0]`
- `Map032.events.7.pages[0].list[322].parameters[0]`
- `Map032.events.7.pages[0].list[328].parameters[0]`
- `Map032.events.7.pages[0].list[335].parameters[0]`
- `Map032.events.7.pages[0].list[346].parameters[0]`
- `Scripts[104] Vacas_Cinematicas:40`
### #140 Tilesets/revision_mapa01 — OK

- `Map001.Tilesets[52].tileset_name`
- `Tilesets[52].tileset_name`
### #141 Autotiles/053-Wall01 — OK

- `Map001.Tilesets[52].autotile_names[0]`
- `Map002.Tilesets[53].autotile_names[0]`
- `Map003.Tilesets[54].autotile_names[0]`
- `Map005.Tilesets[56].autotile_names[0]`
- `Map006.Tilesets[57].autotile_names[0]`
- `Map007.Tilesets[58].autotile_names[0]`
- `Map008.Tilesets[59].autotile_names[0]`
- `Map009.Tilesets[60].autotile_names[0]`
- `Map010.Tilesets[61].autotile_names[0]`
- `Map011.Tilesets[62].autotile_names[0]`
- `Map012.Tilesets[63].autotile_names[0]`
- `Map013.Tilesets[64].autotile_names[0]`
- `Map014.Tilesets[65].autotile_names[0]`
- `Map015.Tilesets[66].autotile_names[0]`
- `Map016.Tilesets[67].autotile_names[0]`
- `Map022.Tilesets[69].autotile_names[0]`
- `Map023.Tilesets[69].autotile_names[0]`
- `Map024.Tilesets[69].autotile_names[0]`
- `Map025.Tilesets[69].autotile_names[0]`
- `Map026.Tilesets[69].autotile_names[0]`
- `Map027.Tilesets[69].autotile_names[0]`
- `Map028.Tilesets[70].autotile_names[0]`
- `Map029.Tilesets[70].autotile_names[0]`
- `Map030.Tilesets[70].autotile_names[0]`
- `Map031.Tilesets[70].autotile_names[0]`
- `Map032.Tilesets[70].autotile_names[0]`
- `Tilesets[12].autotile_names[0]`
- `Tilesets[18].autotile_names[0]`
- `Tilesets[26].autotile_names[0]`
- `Tilesets[27].autotile_names[0]`
- `Tilesets[33].autotile_names[0]`
- `Tilesets[36].autotile_names[0]`
- `Tilesets[40].autotile_names[0]`
- `Tilesets[48].autotile_names[0]`
- `Tilesets[51].autotile_names[0]`
- `Tilesets[52].autotile_names[0]`
- `Tilesets[53].autotile_names[0]`
- `Tilesets[54].autotile_names[0]`
- `Tilesets[56].autotile_names[0]`
- `Tilesets[57].autotile_names[0]`
- `Tilesets[58].autotile_names[0]`
- `Tilesets[59].autotile_names[0]`
- `Tilesets[60].autotile_names[0]`
- `Tilesets[61].autotile_names[0]`
- `Tilesets[62].autotile_names[0]`
- `Tilesets[63].autotile_names[0]`
- `Tilesets[64].autotile_names[0]`
- `Tilesets[65].autotile_names[0]`
- `Tilesets[66].autotile_names[0]`
- `Tilesets[67].autotile_names[0]`
- `Tilesets[69].autotile_names[0]`
- `Tilesets[70].autotile_names[0]`
### #142 Autotiles/vacas_canal — OK

- `Map001.Tilesets[52].autotile_names[1]`
- `Map005.Tilesets[56].autotile_names[1]`
- `Map006.Tilesets[57].autotile_names[1]`
- `Map007.Tilesets[58].autotile_names[1]`
- `Map008.Tilesets[59].autotile_names[1]`
- `Map009.Tilesets[60].autotile_names[1]`
- `Map010.Tilesets[61].autotile_names[1]`
- `Map011.Tilesets[62].autotile_names[1]`
- `Map012.Tilesets[63].autotile_names[1]`
- `Map013.Tilesets[64].autotile_names[1]`
- `Map014.Tilesets[65].autotile_names[1]`
- `Map015.Tilesets[66].autotile_names[1]`
- `Map016.Tilesets[67].autotile_names[1]`
- `Map022.Tilesets[69].autotile_names[1]`
- `Map023.Tilesets[69].autotile_names[1]`
- `Map024.Tilesets[69].autotile_names[1]`
- `Map025.Tilesets[69].autotile_names[1]`
- `Map026.Tilesets[69].autotile_names[1]`
- `Map027.Tilesets[69].autotile_names[1]`
- `Map028.Tilesets[70].autotile_names[1]`
- `Map029.Tilesets[70].autotile_names[1]`
- `Map030.Tilesets[70].autotile_names[1]`
- `Map031.Tilesets[70].autotile_names[1]`
- `Map032.Tilesets[70].autotile_names[1]`
- `Tilesets[51].autotile_names[1]`
- `Tilesets[52].autotile_names[1]`
- `Tilesets[56].autotile_names[1]`
- `Tilesets[57].autotile_names[1]`
- `Tilesets[58].autotile_names[1]`
- `Tilesets[59].autotile_names[1]`
- `Tilesets[60].autotile_names[1]`
- `Tilesets[61].autotile_names[1]`
- `Tilesets[62].autotile_names[1]`
- `Tilesets[63].autotile_names[1]`
- `Tilesets[64].autotile_names[1]`
- `Tilesets[65].autotile_names[1]`
- `Tilesets[66].autotile_names[1]`
- `Tilesets[67].autotile_names[1]`
- `Tilesets[69].autotile_names[1]`
- `Tilesets[70].autotile_names[1]`
### #143 Fogs/002-Clouds01 — OK

- `Map001.Tilesets[52].fog_name`
- `Map002.events.2.pages[0].list[31].map_setting`
- `Map003.events.1.pages[0].list[9].map_setting`
- `Map004.events.1.pages[0].list[10].map_setting`
- `Map005.events.1.pages[0].list[15].map_setting`
- `Map005.Tilesets[56].fog_name`
- `Map006.events.1.pages[0].list[2].map_setting`
- `Map006.Tilesets[57].fog_name`
- `Map007.events.1.pages[0].list[2].map_setting`
- `Map007.Tilesets[58].fog_name`
- `Map008.events.3.pages[0].list[2].map_setting`
- `Map008.Tilesets[59].fog_name`
- `Map009.events.1.pages[0].list[2].map_setting`
- `Map009.Tilesets[60].fog_name`
- `Map010.events.1.pages[0].list[2].map_setting`
- `Map010.Tilesets[61].fog_name`
- `Map011.events.2.pages[0].list[2].map_setting`
- `Map011.Tilesets[62].fog_name`
- `Map012.Tilesets[63].fog_name`
- `Map013.Tilesets[64].fog_name`
- `Map014.Tilesets[65].fog_name`
- `Map015.Tilesets[66].fog_name`
- `Map016.Tilesets[67].fog_name`
- `Map017.Tilesets[68].fog_name`
- `Map018.Tilesets[68].fog_name`
- `Map019.Tilesets[68].fog_name`
- `Map020.Tilesets[68].fog_name`
- `Map021.Tilesets[68].fog_name`
- `Map022.Tilesets[69].fog_name`
- `Map023.Tilesets[69].fog_name`
- `Map024.Tilesets[69].fog_name`
- `Map025.Tilesets[69].fog_name`
- `Map026.Tilesets[69].fog_name`
- `Map027.Tilesets[69].fog_name`
- `Map028.Tilesets[70].fog_name`
- `Map029.Tilesets[70].fog_name`
- `Map030.Tilesets[70].fog_name`
- `Map031.Tilesets[70].fog_name`
- `Map032.Tilesets[70].fog_name`
- `Tilesets[51].fog_name`
- `Tilesets[52].fog_name`
- `Tilesets[56].fog_name`
- `Tilesets[57].fog_name`
- `Tilesets[58].fog_name`
- `Tilesets[59].fog_name`
- `Tilesets[60].fog_name`
- `Tilesets[61].fog_name`
- `Tilesets[62].fog_name`
- `Tilesets[63].fog_name`
- `Tilesets[64].fog_name`
- `Tilesets[65].fog_name`
- `Tilesets[66].fog_name`
- `Tilesets[67].fog_name`
- `Tilesets[68].fog_name`
- `Tilesets[69].fog_name`
- `Tilesets[70].fog_name`
### #144 Characters/vacas_madre — OK

- `Map002.events.1.pages[1].graphic.character_name`
- `Map002.events.1.pages[2].graphic.character_name`
- `Map002.events.14.pages[0].graphic.character_name`
- `Map002.events.14.pages[1].graphic.character_name`
- `Map002.events.14.pages[4].graphic.character_name`
- `Map002.events.14.pages[5].graphic.character_name`
- `Map002.events.46.pages[1].graphic.character_name`
- `Map030.events.5.pages[0].graphic.character_name`
- `Map030.events.5.pages[1].graphic.character_name`
### #145 Pictures/retrato_madre_ira — OK

- `Map002.events.1.pages[1].list[6].parameters[0]`
- `Map002.events.1.pages[1].list[16].parameters[0]`
- `Map002.events.3.pages[0].list[10].parameters[0]`
- `Map002.events.3.pages[0].list[11].parameters[0]`
- `Map002.events.4.pages[1].list[48].parameters[0]`
- `Map002.events.4.pages[2].list[36].parameters[0]`
- `Map002.events.4.pages[2].list[46].parameters[0]`
- `Map002.events.4.pages[4].list[195].parameters[0]`
- `Map002.events.4.pages[5].list[195].parameters[0]`
- `Map002.events.5.pages[1].list[48].parameters[0]`
- `Map002.events.5.pages[2].list[36].parameters[0]`
- `Map002.events.5.pages[2].list[46].parameters[0]`
- `Map002.events.5.pages[4].list[195].parameters[0]`
- `Map002.events.5.pages[5].list[195].parameters[0]`
- `Map002.events.6.pages[1].list[116].parameters[0]`
- `Map002.events.6.pages[1].list[126].parameters[0]`
- `Map002.events.12.pages[1].list[111].parameters[0]`
- `Map002.events.12.pages[1].list[121].parameters[0]`
- `Map002.events.14.pages[0].list[152].parameters[0]`
- `Map002.events.14.pages[4].list[24].parameters[0]`
- `Map002.events.31.pages[0].list[121].parameters[0]`
- `Map002.events.48.pages[1].list[10].parameters[0]`
- `Map002.events.48.pages[1].list[20].parameters[0]`
- `Map030.events.5.pages[0].list[4].parameters[0]`
### #146 Pictures/retrato_madre_neutral — OK

- `Map002.events.1.pages[1].list[68].parameters[0]`
- `Map002.events.1.pages[1].list[70].parameters[0]`
- `Map002.events.4.pages[1].list[49].parameters[0]`
- `Map002.events.4.pages[2].list[26].parameters[0]`
- `Map002.events.4.pages[2].list[98].parameters[0]`
- `Map002.events.4.pages[2].list[100].parameters[0]`
- `Map002.events.5.pages[1].list[49].parameters[0]`
- `Map002.events.5.pages[2].list[26].parameters[0]`
- `Map002.events.5.pages[2].list[98].parameters[0]`
- `Map002.events.5.pages[2].list[100].parameters[0]`
- `Map002.events.6.pages[1].list[29].parameters[0]`
- `Map002.events.6.pages[1].list[41].parameters[0]`
- `Map002.events.6.pages[1].list[100].parameters[0]`
- `Map002.events.6.pages[1].list[102].parameters[0]`
- `Map002.events.6.pages[1].list[178].parameters[0]`
- `Map002.events.6.pages[1].list[180].parameters[0]`
- `Map002.events.12.pages[1].list[27].parameters[0]`
- `Map002.events.12.pages[1].list[38].parameters[0]`
- `Map002.events.12.pages[1].list[95].parameters[0]`
- `Map002.events.12.pages[1].list[97].parameters[0]`
- `Map002.events.12.pages[1].list[173].parameters[0]`
- `Map002.events.12.pages[1].list[175].parameters[0]`
- `Map002.events.14.pages[0].list[5].parameters[0]`
- `Map002.events.14.pages[0].list[7].parameters[0]`
- `Map002.events.14.pages[0].list[16].parameters[0]`
- `Map002.events.14.pages[0].list[23].parameters[0]`
- `Map002.events.14.pages[0].list[34].parameters[0]`
- `Map002.events.14.pages[0].list[41].parameters[0]`
- `Map002.events.14.pages[0].list[46].parameters[0]`
- `Map002.events.14.pages[0].list[48].parameters[0]`
- `Map002.events.14.pages[0].list[75].parameters[0]`
- `Map002.events.14.pages[0].list[79].parameters[0]`
- `Map002.events.14.pages[0].list[93].parameters[0]`
- `Map002.events.14.pages[0].list[94].parameters[0]`
- `Map002.events.14.pages[0].list[108].parameters[0]`
- `Map002.events.14.pages[0].list[113].parameters[0]`
- `Map002.events.14.pages[0].list[118].parameters[0]`
- `Map002.events.14.pages[0].list[122].parameters[0]`
- `Map002.events.14.pages[0].list[130].parameters[0]`
- `Map002.events.14.pages[0].list[135].parameters[0]`
- `Map002.events.14.pages[0].list[136].parameters[0]`
- `Map002.events.14.pages[0].list[139].parameters[0]`
- `Map002.events.14.pages[0].list[142].parameters[0]`
- `Map002.events.14.pages[0].list[150].parameters[0]`
- `Map002.events.14.pages[0].list[155].parameters[0]`
- `Map002.events.14.pages[4].list[2].parameters[0]`
- `Map002.events.14.pages[4].list[6].parameters[0]`
- `Map002.events.14.pages[4].list[17].parameters[0]`
- `Map002.events.14.pages[4].list[20].parameters[0]`
- `Map002.events.14.pages[4].list[33].parameters[0]`
- `Map002.events.14.pages[4].list[36].parameters[0]`
- `Map002.events.14.pages[4].list[40].parameters[0]`
- `Map002.events.14.pages[4].list[51].parameters[0]`
- `Map002.events.14.pages[4].list[66].parameters[0]`
- `Map002.events.14.pages[4].list[84].parameters[0]`
- `Map002.events.14.pages[5].list[0].parameters[0]`
- `Map002.events.14.pages[5].list[11].parameters[0]`
- `Map002.events.15.pages[1].list[7].parameters[0]`
- `Map002.events.15.pages[1].list[9].parameters[0]`
- `Map002.events.15.pages[1].list[17].parameters[0]`
- `Map002.events.15.pages[1].list[28].parameters[0]`
- `Map002.events.46.pages[1].list[2].parameters[0]`
- `Map002.events.46.pages[1].list[5].parameters[0]`
- `Map002.events.46.pages[1].list[7].parameters[0]`
- `Map002.events.48.pages[1].list[72].parameters[0]`
- `Map002.events.48.pages[1].list[74].parameters[0]`
- `Scripts[104] Vacas_Cinematicas:11`
### #147 Pictures/screamer_7 — OK

- `Map002.events.4.pages[4].list[32].parameters[0]`
- `Map002.events.4.pages[4].list[67].parameters[0]`
- `Map002.events.4.pages[5].list[32].parameters[0]`
- `Map002.events.4.pages[5].list[67].parameters[0]`
- `Map002.events.5.pages[4].list[32].parameters[0]`
- `Map002.events.5.pages[4].list[67].parameters[0]`
- `Map002.events.5.pages[5].list[32].parameters[0]`
- `Map002.events.5.pages[5].list[67].parameters[0]`
### #148 Characters/vacas_muebles — OK

- `Map002.events.6.pages[0].graphic.character_name`
- `Map002.events.6.pages[1].graphic.character_name`
- `Map002.events.6.pages[2].graphic.character_name`
- `Map002.events.10.pages[0].graphic.character_name`
- `Map002.events.11.pages[0].graphic.character_name`
- `Map002.events.11.pages[1].graphic.character_name`
- `Map002.events.12.pages[0].graphic.character_name`
- `Map002.events.12.pages[1].graphic.character_name`
- `Map002.events.13.pages[0].graphic.character_name`
- `Map002.events.31.pages[0].graphic.character_name`
- `Map002.events.31.pages[0].list[17].parameters[1].list[0].change_graphic`
- `Map002.events.31.pages[0].list[18].parameters[0].change_graphic`
- `Map002.events.31.pages[0].list[22].parameters[1].list[0].change_graphic`
- `Map002.events.31.pages[0].list[23].parameters[0].change_graphic`
- `Map002.events.31.pages[0].list[62].parameters[1].list[0].change_graphic`
- `Map002.events.31.pages[0].list[63].parameters[0].change_graphic`
- `Map002.events.31.pages[0].list[73].parameters[1].list[0].change_graphic`
- `Map002.events.31.pages[0].list[74].parameters[0].change_graphic`
- `Map002.events.31.pages[0].list[83].parameters[1].list[0].change_graphic`
- `Map002.events.31.pages[0].list[84].parameters[0].change_graphic`
- `Map002.events.31.pages[0].list[94].parameters[1].list[0].change_graphic`
- `Map002.events.31.pages[0].list[95].parameters[0].change_graphic`
- `Map002.events.31.pages[0].list[103].parameters[1].list[0].change_graphic`
- `Map002.events.31.pages[0].list[104].parameters[0].change_graphic`
- `Map002.events.31.pages[0].list[127].parameters[1].list[0].change_graphic`
- `Map002.events.31.pages[0].list[128].parameters[0].change_graphic`
- `Map002.events.31.pages[0].list[133].parameters[1].list[0].change_graphic`
- `Map002.events.31.pages[0].list[134].parameters[0].change_graphic`
- `Map002.events.31.pages[0].list[140].parameters[1].list[0].change_graphic`
- `Map002.events.31.pages[0].list[141].parameters[0].change_graphic`
- `Map002.events.31.pages[1].graphic.character_name`
- `Map002.events.33.pages[0].graphic.character_name`
- `Map002.events.33.pages[1].graphic.character_name`
- `Map002.events.33.pages[2].graphic.character_name`
- `Map002.events.42.pages[0].graphic.character_name`
- `Map002.events.42.pages[1].graphic.character_name`
- `Map012.events.5.pages[0].graphic.character_name`
### #149 Pictures/screamer_1 — OK

- `Map002.events.11.pages[0].list[4].parameters[0]`
### #150 Characters/vacas_cosas — OK

- `Map002.events.19.pages[0].graphic.character_name`
- `Map002.events.20.pages[0].graphic.character_name`
- `Map002.events.26.pages[0].graphic.character_name`
- `Map002.events.27.pages[0].graphic.character_name`
- `Map002.events.28.pages[0].graphic.character_name`
- `Map002.events.35.pages[0].graphic.character_name`
- `Map002.events.36.pages[0].graphic.character_name`
- `Map002.events.36.pages[1].graphic.character_name`
- `Map002.events.44.pages[1].graphic.character_name`
- `Map003.events.12.pages[0].graphic.character_name`
- `Map003.events.13.pages[0].graphic.character_name`
- `Map003.events.14.pages[0].graphic.character_name`
- `Map004.events.4.pages[0].graphic.character_name`
- `Map004.events.9.pages[0].graphic.character_name`
- `Map004.events.13.pages[0].graphic.character_name`
- `Map004.events.14.pages[0].graphic.character_name`
- `Map004.events.15.pages[0].graphic.character_name`
- `Map004.events.16.pages[0].graphic.character_name`
- `Map004.events.17.pages[0].graphic.character_name`
- `Map004.events.18.pages[0].graphic.character_name`
### #151 Pictures/screamer_2 — OK

- `Map002.events.31.pages[0].list[30].parameters[0]`
### #152 Characters/vacas_perro — OK

- `Map002.events.34.pages[0].graphic.character_name`
- `Map002.events.34.pages[1].graphic.character_name`
- `Map002.events.34.pages[2].graphic.character_name`
- `Map002.events.34.pages[3].graphic.character_name`
- `Map002.events.34.pages[4].graphic.character_name`
- `Map030.events.4.pages[0].graphic.character_name`
- `Map032.events.4.pages[0].graphic.character_name`
### #153 Pictures/retrato_dog_miedo — OK

- `Map002.events.34.pages[0].list[43].parameters[0]`
- `Map002.events.34.pages[1].list[0].parameters[0]`
- `Map002.events.34.pages[2].list[43].parameters[0]`
- `Map002.events.34.pages[3].list[16].parameters[0]`
### #154 Characters/vacas_vacio — OK

- `Map002.events.49.pages[0].graphic.character_name`
- `Map004.events.11.pages[1].graphic.character_name`
- `Map004.events.12.pages[1].graphic.character_name`
- `Map005.events.4.pages[0].graphic.character_name`
- `Map005.events.5.pages[0].graphic.character_name`
- `Map005.events.7.pages[0].graphic.character_name`
- `Map005.events.8.pages[0].graphic.character_name`
### #155 Autotiles/052-Carpet02 — OK

- `Map002.Tilesets[53].autotile_names[1]`
- `Map003.Tilesets[54].autotile_names[1]`
- `Tilesets[12].autotile_names[1]`
- `Tilesets[14].autotile_names[1]`
- `Tilesets[16].autotile_names[1]`
- `Tilesets[18].autotile_names[1]`
- `Tilesets[20].autotile_names[1]`
- `Tilesets[22].autotile_names[1]`
- `Tilesets[24].autotile_names[1]`
- `Tilesets[26].autotile_names[4]`
- `Tilesets[27].autotile_names[4]`
- `Tilesets[29].autotile_names[2]`
- `Tilesets[31].autotile_names[1]`
- `Tilesets[33].autotile_names[4]`
- `Tilesets[36].autotile_names[5]`
- `Tilesets[38].autotile_names[2]`
- `Tilesets[40].autotile_names[3]`
- `Tilesets[53].autotile_names[1]`
- `Tilesets[54].autotile_names[1]`
### #156 Battlebacks/ui_piso — OK

- `Map002.Tilesets[53].battleback_name`
- `Map003.Tilesets[54].battleback_name`
- `Map004.Tilesets[55].battleback_name`
- `Tilesets[53].battleback_name`
- `Tilesets[54].battleback_name`
- `Tilesets[55].battleback_name`
- `Scripts: Vacas_Interfaz familia dinámica`
- `Scripts: Scene_Battle fondo por MAP_AUDIO`
### #157 Tilesets/revision_mapa02 — OK

- `Map002.Tilesets[53].tileset_name`
- `Tilesets[53].tileset_name`
### #158 Characters/vacas_puerta — OK

- `Map003.events.2.pages[0].graphic.character_name`
- `Map003.events.3.pages[0].graphic.character_name`
- `Map003.events.4.pages[0].graphic.character_name`
- `Map004.events.2.pages[0].graphic.character_name`
### #159 Characters/vacas_remedios — OK

- `Map003.events.5.pages[0].graphic.character_name`
- `Map003.events.5.pages[1].graphic.character_name`
### #160 Pictures/retrato_remedios_neutral — OK

- `Map003.events.5.pages[0].list[1].parameters[0]`
- `Map003.events.5.pages[0].list[3].parameters[0]`
- `Map003.events.5.pages[0].list[9].parameters[0]`
- `Map003.events.5.pages[1].list[0].parameters[0]`
- `Map003.events.5.pages[1].list[3].parameters[0]`
### #161 Characters/vacas_anselmo — OK

- `Map003.events.6.pages[0].graphic.character_name`
- `Map003.events.6.pages[1].graphic.character_name`
- `Map003.events.6.pages[2].graphic.character_name`
### #162 Pictures/retrato_anselmo_neutral — OK

- `Map003.events.6.pages[0].list[1].parameters[0]`
- `Map003.events.6.pages[0].list[3].parameters[0]`
- `Map003.events.6.pages[0].list[9].parameters[0]`
- `Map003.events.6.pages[1].list[0].parameters[0]`
- `Map003.events.6.pages[1].list[3].parameters[0]`
- `Map003.events.6.pages[2].list[3].parameters[0]`
- `Map003.events.6.pages[2].list[9].parameters[0]`
### #163 Characters/185-Light02 — OK

- `Map003.events.11.pages[0].graphic.character_name`
### #164 Characters/vacas_lucy — OK

- `Map003.events.15.pages[1].graphic.character_name`
- `Map012.events.4.pages[0].graphic.character_name`
- `Map012.events.4.pages[1].graphic.character_name`
- `Map016.events.8.pages[0].graphic.character_name`
- `Map016.events.8.pages[1].graphic.character_name`
### #165 Pictures/retrato_lucy_susurro — OK

- `Map003.events.15.pages[1].list[36].parameters[0]`
- `Map003.events.15.pages[1].list[41].parameters[0]`
- `Map003.events.15.pages[1].list[47].parameters[0]`
- `Map003.events.15.pages[1].list[53].parameters[0]`
- `Map003.events.15.pages[1].list[58].parameters[0]`
- `Map003.events.15.pages[1].list[62].parameters[0]`
- `Map003.events.15.pages[1].list[68].parameters[0]`
- `Map003.events.15.pages[1].list[74].parameters[0]`
- `Map003.events.15.pages[1].list[84].parameters[0]`
### #166 Tilesets/revision_mapa03 — OK

- `Map003.Tilesets[54].tileset_name`
- `Tilesets[54].tileset_name`
### #167 Characters/vacas_tablon — OK

- `Map004.events.3.pages[0].graphic.character_name`
- `Map005.events.16.pages[0].graphic.character_name`
### #168 Pictures/retrato_molina_neutral — OK

- `Map004.events.4.pages[0].list[1].parameters[0]`
- `Map004.events.4.pages[0].list[3].parameters[0]`
- `Map004.events.4.pages[0].list[9].parameters[0]`
- `Map004.events.4.pages[0].list[13].parameters[0]`
- `Map004.events.4.pages[0].list[23].parameters[0]`
- `Map004.events.4.pages[0].list[26].parameters[0]`
- `Map004.events.4.pages[0].list[31].parameters[0]`
- `Map004.events.4.pages[0].list[38].parameters[0]`
- `Map013.events.3.pages[0].list[2].parameters[0]`
- `Map013.events.3.pages[0].list[6].parameters[0]`
- `Map013.events.3.pages[0].list[23].parameters[0]`
- `Map013.events.3.pages[0].list[31].parameters[0]`
### #169 Characters/vacas_carnicero — OK

- `Map004.events.5.pages[0].graphic.character_name`
- `Map013.events.3.pages[0].graphic.character_name`
### #170 Characters/vacas_borracho — OK

- `Map004.events.7.pages[0].graphic.character_name`
- `Map004.events.7.pages[1].graphic.character_name`
### #171 Pictures/retrato_borracho_neutral — OK

- `Map004.events.7.pages[0].list[1].parameters[0]`
- `Map004.events.7.pages[0].list[2].parameters[0]`
- `Map004.events.7.pages[0].list[4].parameters[0]`
- `Map004.events.7.pages[0].list[11].parameters[0]`
### #172 Characters/vacas_transeunte — OK

- `Map004.events.8.pages[0].graphic.character_name`
### #173 Characters/vacas_furgoneta — OK

- `Map004.events.10.pages[1].graphic.character_name`
- `Map005.events.3.pages[0].graphic.character_name`
- `Map005.events.6.pages[0].graphic.character_name`
### #174 Characters/vacas_reclutador — OK

- `Map004.events.19.pages[1].graphic.character_name`
- `Map004.events.19.pages[2].graphic.character_name`
### #175 Pictures/retrato_reclutador_neutral — OK

- `Map004.events.19.pages[1].list[0].parameters[0]`
- `Map004.events.19.pages[1].list[5].parameters[0]`
- `Map004.events.19.pages[1].list[9].parameters[0]`
- `Map004.events.19.pages[1].list[12].parameters[0]`
- `Map004.events.19.pages[1].list[16].parameters[0]`
- `Map004.events.19.pages[1].list[19].parameters[0]`
- `Map004.events.19.pages[1].list[24].parameters[0]`
- `Map004.events.19.pages[1].list[28].parameters[0]`
- `Map004.events.19.pages[1].list[31].parameters[0]`
- `Map004.events.19.pages[1].list[35].parameters[0]`
- `Map004.events.19.pages[1].list[38].parameters[0]`
- `Map004.events.19.pages[1].list[42].parameters[0]`
- `Map004.events.19.pages[1].list[46].parameters[0]`
### #176 Autotiles/048-Water01 — OK

- `Map004.Tilesets[55].autotile_names[0]`
- `Tilesets[9].autotile_names[0]`
- `Tilesets[17].autotile_names[0]`
- `Tilesets[24].autotile_names[0]`
- `Tilesets[25].autotile_names[0]`
- `Tilesets[26].autotile_names[1]`
- `Tilesets[27].autotile_names[1]`
- `Tilesets[28].autotile_names[0]`
- `Tilesets[29].autotile_names[0]`
- `Tilesets[33].autotile_names[1]`
- `Tilesets[36].autotile_names[3]`
- `Tilesets[38].autotile_names[0]`
- `Tilesets[40].autotile_names[1]`
- `Tilesets[42].autotile_names[0]`
- `Tilesets[48].autotile_names[1]`
- `Tilesets[55].autotile_names[0]`
### #177 Autotiles/002-G_Shadow01 — OK

- `Map004.Tilesets[55].autotile_names[1]`
- `Tilesets[1].autotile_names[1]`
- `Tilesets[2].autotile_names[1]`
- `Tilesets[4].autotile_names[1]`
- `Tilesets[9].autotile_names[1]`
- `Tilesets[11].autotile_names[1]`
- `Tilesets[13].autotile_names[1]`
- `Tilesets[15].autotile_names[1]`
- `Tilesets[23].autotile_names[1]`
- `Tilesets[25].autotile_names[1]`
- `Tilesets[28].autotile_names[1]`
- `Tilesets[32].autotile_names[1]`
- `Tilesets[34].autotile_names[1]`
- `Tilesets[35].autotile_names[1]`
- `Tilesets[37].autotile_names[1]`
- `Tilesets[39].autotile_names[1]`
- `Tilesets[55].autotile_names[1]`
### #178 Autotiles/003-G_Ground01 — OK

- `Map004.Tilesets[55].autotile_names[2]`
- `Tilesets[1].autotile_names[2]`
- `Tilesets[2].autotile_names[2]`
- `Tilesets[9].autotile_names[2]`
- `Tilesets[13].autotile_names[2]`
- `Tilesets[23].autotile_names[2]`
- `Tilesets[32].autotile_names[2]`
- `Tilesets[34].autotile_names[2]`
- `Tilesets[35].autotile_names[2]`
- `Tilesets[37].autotile_names[2]`
- `Tilesets[39].autotile_names[2]`
- `Tilesets[55].autotile_names[2]`
### #179 Autotiles/005-G_Road01 — OK

- `Map004.Tilesets[55].autotile_names[3]`
- `Tilesets[9].autotile_names[3]`
- `Tilesets[11].autotile_names[5]`
- `Tilesets[28].autotile_names[3]`
- `Tilesets[35].autotile_names[3]`
- `Tilesets[55].autotile_names[3]`
### #180 Autotiles/006-G_Road02 — OK

- `Map004.Tilesets[55].autotile_names[4]`
- `Tilesets[9].autotile_names[4]`
- `Tilesets[13].autotile_names[3]`
- `Tilesets[25].autotile_names[3]`
- `Tilesets[28].autotile_names[4]`
- `Tilesets[34].autotile_names[3]`
- `Tilesets[55].autotile_names[4]`
### #181 Autotiles/050-Roof02 — OK

- `Map004.Tilesets[55].autotile_names[5]`
- `Tilesets[9].autotile_names[5]`
- `Tilesets[11].autotile_names[6]`
- `Tilesets[25].autotile_names[5]`
- `Tilesets[28].autotile_names[6]`
- `Tilesets[30].autotile_names[0]`
- `Tilesets[34].autotile_names[6]`
- `Tilesets[35].autotile_names[4]`
- `Tilesets[39].autotile_names[6]`
- `Tilesets[55].autotile_names[5]`
### #182 Tilesets/revision_mapa04 — OK

- `Map004.Tilesets[55].tileset_name`
- `Tilesets[55].tileset_name`
### #183 Pictures/retrato_steven_miedo — OK

- `Map005.events.2.pages[0].list[28].parameters[0]`
- `Map005.events.2.pages[0].list[41].parameters[0]`
- `Map007.events.14.pages[0].list[20].parameters[0]`
- `Map012.events.2.pages[0].list[5].parameters[0]`
- `Map012.events.2.pages[0].list[11].parameters[0]`
- `Map014.events.2.pages[0].list[1].parameters[0]`
- `Map016.events.7.pages[0].list[31].parameters[0]`
- `Map017.events.2.pages[0].list[1].parameters[0]`
- `Map022.events.2.pages[0].list[19].parameters[0]`
- `Map023.events.2.pages[0].list[4].parameters[0]`
- `Map024.events.3.pages[0].list[25].parameters[0]`
- `Map024.events.4.pages[0].list[25].parameters[0]`
- `Map025.events.2.pages[0].list[5].parameters[0]`
- `Map026.events.9.pages[1].list[23].parameters[0]`
- `Map027.events.3.pages[0].list[28].parameters[0]`
- `Troops[1].pages[0].list[0].parameters[0]`
- `Troops[2].pages[0].list[0].parameters[0]`
- `Troops[3].pages[0].list[0].parameters[0]`
- `Troops[4].pages[0].list[0].parameters[0]`
- `Troops[5].pages[0].list[0].parameters[0]`
- `Troops[6].pages[0].list[0].parameters[0]`
- `Troops[7].pages[0].list[0].parameters[0]`
- `Troops[8].pages[0].list[0].parameters[0]`
- `Troops[9].pages[0].list[0].parameters[0]`
- `Troops[10].pages[0].list[0].parameters[0]`
- `Troops[11].pages[0].list[0].parameters[0]`
- `Troops[12].pages[0].list[0].parameters[0]`
- `Troops[13].pages[0].list[0].parameters[0]`
- `Troops[14].pages[0].list[0].parameters[0]`
- `Troops[15].pages[0].list[0].parameters[0]`
- `Troops[16].pages[0].list[0].parameters[0]`
- `Troops[17].pages[0].list[0].parameters[0]`
- `Troops[18].pages[0].list[0].parameters[0]`
- `Troops[19].pages[0].list[0].parameters[0]`
- `Troops[20].pages[0].list[0].parameters[0]`
- `Troops[21].pages[0].list[2].parameters[0]`
- `Troops[33].pages[0].list[0].parameters[0]`
- `Troops[34].pages[0].list[0].parameters[0]`
- `Troops[35].pages[0].list[0].parameters[0]`
- `Troops[36].pages[0].list[0].parameters[0]`
- `Troops[37].pages[0].list[0].parameters[0]`
- `DB.Troops[1].pages[0].list[0].parameters[0]`
- `DB.Troops[2].pages[0].list[0].parameters[0]`
- `DB.Troops[3].pages[0].list[0].parameters[0]`
- `DB.Troops[4].pages[0].list[0].parameters[0]`
- `DB.Troops[5].pages[0].list[0].parameters[0]`
- `DB.Troops[6].pages[0].list[0].parameters[0]`
- `DB.Troops[7].pages[0].list[0].parameters[0]`
- `DB.Troops[8].pages[0].list[0].parameters[0]`
- `DB.Troops[9].pages[0].list[0].parameters[0]`
- `DB.Troops[10].pages[0].list[0].parameters[0]`
- `DB.Troops[11].pages[0].list[0].parameters[0]`
- `DB.Troops[12].pages[0].list[0].parameters[0]`
- `DB.Troops[13].pages[0].list[0].parameters[0]`
- `DB.Troops[14].pages[0].list[0].parameters[0]`
- `DB.Troops[15].pages[0].list[0].parameters[0]`
- `DB.Troops[16].pages[0].list[0].parameters[0]`
- `DB.Troops[17].pages[0].list[0].parameters[0]`
- `DB.Troops[18].pages[0].list[0].parameters[0]`
- `DB.Troops[19].pages[0].list[0].parameters[0]`
- `DB.Troops[20].pages[0].list[0].parameters[0]`
- `DB.Troops[21].pages[0].list[2].parameters[0]`
- `DB.Troops[33].pages[0].list[0].parameters[0]`
- `DB.Troops[34].pages[0].list[0].parameters[0]`
- `DB.Troops[35].pages[0].list[0].parameters[0]`
- `DB.Troops[36].pages[0].list[0].parameters[0]`
- `DB.Troops[37].pages[0].list[0].parameters[0]`
### #184 Pictures/screamer_3 — OK

- `Map005.events.6.pages[0].list[9].parameters[0]`
### #185 Characters/vacas_obrero1 — OK

- `Map005.events.11.pages[0].graphic.character_name`
- `Map008.events.54.pages[0].graphic.character_name`
- `Map022.events.4.pages[0].graphic.character_name`
- `Map029.events.5.pages[0].graphic.character_name`
- `Map029.events.5.pages[1].graphic.character_name`
- `Map029.events.5.pages[2].graphic.character_name`
### #186 Pictures/retrato_benito_neutral — OK

- `Map005.events.11.pages[0].list[1].parameters[0]`
- `Map005.events.11.pages[0].list[7].parameters[0]`
- `Map005.events.11.pages[0].list[14].parameters[0]`
- `Map005.events.11.pages[0].list[19].parameters[0]`
- `Map005.events.11.pages[0].list[21].parameters[0]`
- `Map008.events.41.pages[0].list[5].parameters[0]`
- `Map008.events.41.pages[0].list[27].parameters[0]`
- `Map008.events.52.pages[0].list[5].parameters[0]`
- `Map008.events.54.pages[0].list[1].parameters[0]`
- `Map008.events.54.pages[0].list[6].parameters[0]`
- `Map008.events.54.pages[0].list[12].parameters[0]`
- `Map022.events.3.pages[1].list[0].parameters[0]`
### #187 Characters/vacas_cripps — OK

- `Map005.events.12.pages[1].graphic.character_name`
- `Map008.events.1.pages[1].graphic.character_name`
- `Map009.events.33.pages[1].graphic.character_name`
- `Map010.events.13.pages[1].graphic.character_name`
- `Map014.events.3.pages[1].graphic.character_name`
- `Map025.events.3.pages[1].graphic.character_name`
- `Map025.events.3.pages[2].graphic.character_name`
- `Map026.events.9.pages[0].graphic.character_name`
- `Map026.events.9.pages[1].graphic.character_name`
### #188 Pictures/retrato_cripps_neutral — OK

- `Map005.events.12.pages[1].list[1].parameters[0]`
- `Map005.events.12.pages[1].list[6].parameters[0]`
- `Map005.events.12.pages[1].list[8].parameters[0]`
- `Map005.events.12.pages[1].list[12].parameters[0]`
- `Map005.events.13.pages[0].list[37].parameters[0]`
- `Map005.events.13.pages[0].list[43].parameters[0]`
- `Map005.events.13.pages[0].list[46].parameters[0]`
- `Map005.events.13.pages[0].list[51].parameters[0]`
- `Map005.events.13.pages[0].list[55].parameters[0]`
- `Map005.events.13.pages[0].list[63].parameters[0]`
- `Map005.events.13.pages[0].list[69].parameters[0]`
- `Map008.events.1.pages[1].list[2].parameters[0]`
- `Map008.events.1.pages[1].list[7].parameters[0]`
- `Map008.events.1.pages[1].list[15].parameters[0]`
- `Map008.events.1.pages[1].list[18].parameters[0]`
- `Map008.events.1.pages[1].list[21].parameters[0]`
- `Map008.events.1.pages[1].list[26].parameters[0]`
- `Map008.events.1.pages[1].list[32].parameters[0]`
- `Map008.events.1.pages[1].list[41].parameters[0]`
- `Map008.events.1.pages[1].list[48].parameters[0]`
- `Map008.events.1.pages[1].list[53].parameters[0]`
- `Map008.events.1.pages[1].list[54].parameters[0]`
- `Map008.events.1.pages[1].list[59].parameters[0]`
- `Map008.events.1.pages[1].list[63].parameters[0]`
- `Map008.events.1.pages[1].list[75].parameters[0]`
- `Map008.events.1.pages[1].list[80].parameters[0]`
- `Map008.events.1.pages[1].list[83].parameters[0]`
- `Map008.events.1.pages[1].list[93].parameters[0]`
- `Map008.events.1.pages[1].list[100].parameters[0]`
- `Map008.events.52.pages[0].list[19].parameters[0]`
- `Map008.events.52.pages[0].list[27].parameters[0]`
- `Map008.events.52.pages[0].list[30].parameters[0]`
- `Map008.events.52.pages[0].list[34].parameters[0]`
- `Map008.events.59.pages[1].list[17].parameters[0]`
- `Map008.events.59.pages[1].list[20].parameters[0]`
- `Map008.events.59.pages[1].list[42].parameters[0]`
- `Map008.events.59.pages[1].list[65].parameters[0]`
- `Map008.events.59.pages[1].list[68].parameters[0]`
- `Map008.events.59.pages[1].list[84].parameters[0]`
- `Map008.events.59.pages[1].list[102].parameters[0]`
- `Map008.events.59.pages[1].list[104].parameters[0]`
- `Map009.events.2.pages[1].list[11].parameters[0]`
- `Map009.events.2.pages[1].list[18].parameters[0]`
- `Map010.events.2.pages[1].list[11].parameters[0]`
- `Map010.events.2.pages[1].list[18].parameters[0]`
- `Map026.events.9.pages[0].list[0].parameters[0]`
- `Map026.events.9.pages[1].list[0].parameters[0]`
- `Map026.events.9.pages[1].list[3].parameters[0]`
- `Map026.events.9.pages[1].list[7].parameters[0]`
- `Map026.events.9.pages[1].list[13].parameters[0]`
- `Map026.events.9.pages[1].list[18].parameters[0]`
- `Map026.events.9.pages[1].list[25].parameters[0]`
- `Map026.events.9.pages[1].list[139].parameters[0]`
### #189 Characters/vacas_matadero — OK

- `Map005.events.13.pages[0].graphic.character_name`
- `Map008.events.10.pages[0].graphic.character_name`
- `Map008.events.11.pages[0].graphic.character_name`
- `Map008.events.12.pages[0].graphic.character_name`
- `Map008.events.13.pages[0].graphic.character_name`
- `Map008.events.14.pages[0].graphic.character_name`
- `Map008.events.15.pages[0].graphic.character_name`
- `Map008.events.16.pages[0].graphic.character_name`
- `Map008.events.17.pages[0].graphic.character_name`
- `Map008.events.18.pages[0].graphic.character_name`
- `Map008.events.19.pages[0].graphic.character_name`
- `Map008.events.20.pages[0].graphic.character_name`
- `Map008.events.21.pages[0].graphic.character_name`
- `Map008.events.22.pages[0].graphic.character_name`
- `Map008.events.23.pages[0].graphic.character_name`
- `Map008.events.24.pages[0].graphic.character_name`
- `Map008.events.25.pages[0].graphic.character_name`
- `Map008.events.26.pages[0].graphic.character_name`
- `Map008.events.27.pages[0].graphic.character_name`
- `Map008.events.28.pages[0].graphic.character_name`
- `Map008.events.29.pages[0].graphic.character_name`
- `Map008.events.30.pages[0].graphic.character_name`
- `Map008.events.31.pages[0].graphic.character_name`
- `Map008.events.32.pages[0].graphic.character_name`
- `Map008.events.33.pages[0].graphic.character_name`
- `Map008.events.34.pages[0].graphic.character_name`
- `Map008.events.35.pages[0].graphic.character_name`
- `Map008.events.36.pages[0].graphic.character_name`
- `Map008.events.37.pages[0].graphic.character_name`
- `Map008.events.38.pages[0].graphic.character_name`
- `Map008.events.39.pages[0].graphic.character_name`
- `Map008.events.40.pages[0].graphic.character_name`
- `Map008.events.41.pages[0].graphic.character_name`
- `Map008.events.42.pages[0].graphic.character_name`
- `Map008.events.43.pages[0].graphic.character_name`
- `Map008.events.44.pages[0].graphic.character_name`
- `Map008.events.45.pages[0].graphic.character_name`
- `Map008.events.46.pages[0].graphic.character_name`
- `Map008.events.47.pages[0].graphic.character_name`
- `Map008.events.48.pages[0].graphic.character_name`
- `Map008.events.49.pages[0].graphic.character_name`
- `Map008.events.50.pages[0].graphic.character_name`
- `Map008.events.51.pages[0].graphic.character_name`
- `Map008.events.52.pages[0].graphic.character_name`
- `Map008.events.58.pages[0].graphic.character_name`
- `Map009.events.4.pages[0].graphic.character_name`
- `Map009.events.5.pages[0].graphic.character_name`
- `Map009.events.6.pages[0].graphic.character_name`
- `Map009.events.7.pages[0].graphic.character_name`
- `Map009.events.8.pages[0].graphic.character_name`
- `Map009.events.9.pages[0].graphic.character_name`
- `Map009.events.10.pages[0].graphic.character_name`
- `Map009.events.11.pages[0].graphic.character_name`
- `Map009.events.12.pages[0].graphic.character_name`
- `Map009.events.13.pages[0].graphic.character_name`
- `Map009.events.14.pages[0].graphic.character_name`
- `Map009.events.15.pages[0].graphic.character_name`
- `Map009.events.16.pages[0].graphic.character_name`
- `Map009.events.17.pages[0].graphic.character_name`
- `Map009.events.18.pages[0].graphic.character_name`
- `Map009.events.19.pages[0].graphic.character_name`
- `Map009.events.20.pages[0].graphic.character_name`
- `Map009.events.21.pages[0].graphic.character_name`
- `Map009.events.22.pages[0].graphic.character_name`
- `Map009.events.23.pages[0].graphic.character_name`
- `Map009.events.24.pages[0].graphic.character_name`
- `Map009.events.25.pages[0].graphic.character_name`
- `Map009.events.26.pages[0].graphic.character_name`
- `Map009.events.27.pages[0].graphic.character_name`
- `Map009.events.28.pages[0].graphic.character_name`
- `Map010.events.11.pages[0].graphic.character_name`
- `Map010.events.12.pages[0].graphic.character_name`
- `Map011.events.1.pages[0].graphic.character_name`
- `Map011.events.1.pages[0].list[1].parameters[1].list[0].change_graphic`
- `Map011.events.1.pages[0].list[2].parameters[0].change_graphic`
- `Map011.events.1.pages[0].list[25].parameters[1].list[0].change_graphic`
- `Map011.events.1.pages[0].list[26].parameters[0].change_graphic`
- `Map011.events.1.pages[0].list[39].parameters[1].list[0].change_graphic`
- `Map011.events.1.pages[0].list[40].parameters[0].change_graphic`
- `Map011.events.1.pages[0].list[59].parameters[1].list[0].change_graphic`
- `Map011.events.1.pages[0].list[60].parameters[0].change_graphic`
- `Map011.events.1.pages[0].list[91].parameters[1].list[0].change_graphic`
- `Map011.events.1.pages[0].list[92].parameters[0].change_graphic`
- `Map011.events.1.pages[0].list[106].parameters[1].list[0].change_graphic`
- `Map011.events.1.pages[0].list[107].parameters[0].change_graphic`
- `Map011.events.1.pages[0].list[116].parameters[1].list[0].change_graphic`
- `Map011.events.1.pages[0].list[117].parameters[0].change_graphic`
- `Map011.events.1.pages[0].list[135].parameters[1].list[0].change_graphic`
- `Map011.events.1.pages[0].list[136].parameters[0].change_graphic`
- `Map011.events.1.pages[0].list[162].parameters[1].list[0].change_graphic`
- `Map011.events.1.pages[0].list[163].parameters[0].change_graphic`
- `Map011.events.4.pages[0].list[18].parameters[1].list[0].change_graphic`
- `Map011.events.4.pages[0].list[19].parameters[0].change_graphic`
- `Map011.events.4.pages[0].list[21].parameters[1].list[0].change_graphic`
- `Map011.events.4.pages[0].list[22].parameters[0].change_graphic`
- `Map011.events.9.pages[1].list[10].parameters[1].list[0].change_graphic`
- `Map011.events.9.pages[1].list[11].parameters[0].change_graphic`
- `Map011.events.9.pages[1].list[49].parameters[1].list[0].change_graphic`
- `Map011.events.9.pages[1].list[50].parameters[0].change_graphic`
- `Scripts[100] Vacas_Interfaz:64`
### #190 Tilesets/revision_mapa05 — OK

- `Map005.Tilesets[56].tileset_name`
- `Tilesets[56].tileset_name`
### #191 Pictures/screamer_4 — OK

- `Map006.events.10.pages[0].list[10].parameters[0]`
### #192 Characters/vacas_obrero3 — OK

- `Map006.events.11.pages[0].graphic.character_name`
- `Map008.events.56.pages[0].graphic.character_name`
- `Map024.events.3.pages[0].graphic.character_name`
- `Map027.events.11.pages[1].graphic.character_name`
- `Map029.events.4.pages[1].graphic.character_name`
### #193 Pictures/retrato_encarna_neutral — OK

- `Map006.events.11.pages[0].list[1].parameters[0]`
- `Map006.events.11.pages[0].list[4].parameters[0]`
- `Map006.events.11.pages[0].list[10].parameters[0]`
- `Map006.events.11.pages[0].list[13].parameters[0]`
- `Map006.events.11.pages[0].list[20].parameters[0]`
- `Map006.events.11.pages[0].list[22].parameters[0]`
- `Map006.events.11.pages[0].list[26].parameters[0]`
- `Map006.events.11.pages[0].list[28].parameters[0]`
- `Map006.events.11.pages[0].list[35].parameters[0]`
- `Map008.events.56.pages[0].list[0].parameters[0]`
### #194 Characters/vacas_obrero4 — OK

- `Map006.events.12.pages[0].graphic.character_name`
- `Map024.events.4.pages[0].graphic.character_name`
- `Map027.events.12.pages[1].graphic.character_name`
### #195 Pictures/retrato_chato_neutral — OK

- `Map006.events.12.pages[0].list[4].parameters[0]`
- `Map006.events.12.pages[0].list[8].parameters[0]`
- `Map006.events.12.pages[0].list[13].parameters[0]`
- `Map024.events.3.pages[0].list[7].parameters[0]`
- `Map024.events.3.pages[0].list[15].parameters[0]`
- `Map024.events.3.pages[0].list[36].parameters[0]`
- `Map024.events.4.pages[0].list[7].parameters[0]`
- `Map024.events.4.pages[0].list[15].parameters[0]`
- `Map024.events.4.pages[0].list[36].parameters[0]`
- `Map027.events.12.pages[1].list[0].parameters[0]`
### #196 Tilesets/revision_mapa06 — OK

- `Map006.Tilesets[57].tileset_name`
- `Tilesets[57].tileset_name`
### #197 Characters/vacas_vaca — OK

- `Map007.events.5.pages[0].graphic.character_name`
- `Map007.events.6.pages[0].graphic.character_name`
- `Map007.events.7.pages[0].graphic.character_name`
- `Map007.events.8.pages[0].graphic.character_name`
- `Map007.events.9.pages[0].graphic.character_name`
- `Map007.events.10.pages[0].graphic.character_name`
- `Map023.events.15.pages[0].graphic.character_name`
- `Map023.events.18.pages[0].graphic.character_name`
- `Map023.events.19.pages[0].graphic.character_name`
- `Map023.events.20.pages[0].graphic.character_name`
- `Map023.events.22.pages[0].graphic.character_name`
- `Map023.events.23.pages[0].graphic.character_name`
- `Map023.events.24.pages[0].graphic.character_name`
- `Map023.events.25.pages[0].graphic.character_name`
- `Map027.events.6.pages[0].graphic.character_name`
- `Map027.events.8.pages[0].graphic.character_name`
- `Map027.events.10.pages[0].graphic.character_name`
- `Map029.events.7.pages[0].graphic.character_name`
- `Map029.events.8.pages[0].graphic.character_name`
- `Map029.events.9.pages[0].graphic.character_name`
- `Map029.events.10.pages[0].graphic.character_name`
### #198 Characters/vacas_vaca_canela — OK

- `Map007.events.11.pages[0].graphic.character_name`
- `Map008.events.2.pages[1].graphic.character_name`
- `Map023.events.16.pages[0].graphic.character_name`
- `Map023.events.17.pages[0].graphic.character_name`
- `Map023.events.21.pages[0].graphic.character_name`
- `Map027.events.7.pages[0].graphic.character_name`
- `Map027.events.9.pages[0].graphic.character_name`
### #199 Characters/vacas_obrero2 — OK

- `Map007.events.15.pages[0].graphic.character_name`
- `Map008.events.55.pages[0].graphic.character_name`
- `Map023.events.4.pages[0].graphic.character_name`
### #200 Pictures/retrato_rubio_neutral — OK

- `Map007.events.15.pages[0].list[1].parameters[0]`
- `Map007.events.15.pages[0].list[4].parameters[0]`
- `Map007.events.15.pages[0].list[9].parameters[0]`
- `Map007.events.15.pages[0].list[11].parameters[0]`
- `Map007.events.15.pages[0].list[18].parameters[0]`
- `Map007.events.15.pages[0].list[21].parameters[0]`
- `Map024.events.3.pages[0].list[1].parameters[0]`
- `Map024.events.3.pages[0].list[5].parameters[0]`
- `Map024.events.3.pages[0].list[14].parameters[0]`
- `Map024.events.3.pages[0].list[27].parameters[0]`
- `Map024.events.4.pages[0].list[1].parameters[0]`
- `Map024.events.4.pages[0].list[5].parameters[0]`
- `Map024.events.4.pages[0].list[14].parameters[0]`
- `Map024.events.4.pages[0].list[27].parameters[0]`
- `Map027.events.11.pages[1].list[0].parameters[0]`
- `Map029.events.4.pages[1].list[0].parameters[0]`
- `Map029.events.4.pages[1].list[3].parameters[0]`
- `Map031.events.2.pages[0].list[5].parameters[0]`
### #201 Tilesets/revision_mapa07 — OK

- `Map007.Tilesets[58].tileset_name`
- `Tilesets[58].tileset_name`
### #202 Pictures/retrato_cripps_ira — OK

- `Map008.events.1.pages[1].list[64].parameters[0]`
- `Map008.events.1.pages[1].list[104].parameters[0]`
- `Map008.events.41.pages[0].list[20].parameters[0]`
- `Map008.events.41.pages[0].list[32].parameters[0]`
- `Map009.events.2.pages[1].list[3].parameters[0]`
- `Map009.events.29.pages[0].list[17].parameters[0]`
- `Map009.events.30.pages[0].list[17].parameters[0]`
- `Map009.events.31.pages[0].list[17].parameters[0]`
- `Map010.events.2.pages[1].list[3].parameters[0]`
- `Map025.events.3.pages[1].list[3].parameters[0]`
- `Map025.events.3.pages[2].list[3].parameters[0]`
- `Map025.events.4.pages[1].list[4].parameters[0]`
- `Map025.events.4.pages[1].list[6].parameters[0]`
- `Map025.events.5.pages[1].list[32].parameters[0]`
- `Map026.events.9.pages[1].list[29].parameters[0]`
- `Troops[21].pages[0].list[0].parameters[0]`
- `DB.Troops[21].pages[0].list[0].parameters[0]`
### #203 Pictures/retrato_sierra_neutral — OK

- `Map008.events.55.pages[0].list[1].parameters[0]`
- `Map008.events.55.pages[0].list[6].parameters[0]`
- `Map008.events.55.pages[0].list[10].parameters[0]`
- `Map023.events.3.pages[1].list[0].parameters[0]`
### #204 Tilesets/revision_mapa08 — OK

- `Map008.Tilesets[59].tileset_name`
- `Tilesets[59].tileset_name`
### #205 Pictures/screamer_6 — OK

- `Map009.events.32.pages[0].list[10].parameters[0]`
- `Map010.events.9.pages[0].list[6].parameters[0]`
### #206 Tilesets/revision_mapa09 — OK

- `Map009.Tilesets[60].tileset_name`
- `Tilesets[60].tileset_name`
### #207 Tilesets/revision_mapa10 — OK

- `Map010.Tilesets[61].tileset_name`
- `Tilesets[61].tileset_name`
### #208 Pictures/screamer_5 — OK

- `Map011.events.1.pages[0].list[6].parameters[0]`
### #209 Pictures/retrato_guernsey_susurro — OK

- `Map011.events.1.pages[0].list[8].parameters[0]`
- `Map011.events.1.pages[0].list[16].parameters[0]`
- `Map011.events.1.pages[0].list[21].parameters[0]`
- `Map011.events.1.pages[0].list[34].parameters[0]`
- `Map011.events.1.pages[0].list[37].parameters[0]`
- `Map011.events.1.pages[0].list[62].parameters[0]`
- `Map011.events.1.pages[0].list[65].parameters[0]`
- `Map011.events.1.pages[0].list[67].parameters[0]`
- `Map011.events.1.pages[0].list[71].parameters[0]`
- `Map011.events.1.pages[0].list[75].parameters[0]`
- `Map011.events.1.pages[0].list[79].parameters[0]`
- `Map011.events.1.pages[0].list[82].parameters[0]`
- `Map011.events.1.pages[0].list[86].parameters[0]`
- `Map011.events.1.pages[0].list[89].parameters[0]`
- `Map011.events.1.pages[0].list[108].parameters[0]`
- `Map011.events.1.pages[0].list[118].parameters[0]`
- `Map011.events.1.pages[0].list[120].parameters[0]`
- `Map011.events.1.pages[0].list[123].parameters[0]`
- `Map011.events.1.pages[0].list[130].parameters[0]`
- `Map011.events.1.pages[0].list[137].parameters[0]`
- `Map011.events.1.pages[0].list[140].parameters[0]`
- `Map011.events.1.pages[0].list[144].parameters[0]`
- `Map011.events.1.pages[0].list[151].parameters[0]`
- `Map011.events.1.pages[0].list[157].parameters[0]`
- `Map011.events.9.pages[1].list[14].parameters[0]`
- `Map011.events.9.pages[1].list[17].parameters[0]`
- `Map011.events.9.pages[1].list[19].parameters[0]`
- `Map011.events.9.pages[1].list[26].parameters[0]`
- `Map011.events.9.pages[1].list[29].parameters[0]`
- `Map011.events.9.pages[1].list[36].parameters[0]`
- `Map011.events.9.pages[1].list[41].parameters[0]`
- `Map011.events.9.pages[1].list[46].parameters[0]`
- `Map016.events.8.pages[0].list[50].parameters[0]`
- `Map017.events.2.pages[0].list[3].parameters[0]`
- `Map017.events.2.pages[0].list[9].parameters[0]`
- `Map020.events.4.pages[0].list[1].parameters[0]`
- `Map020.events.4.pages[0].list[5].parameters[0]`
- `Map020.events.4.pages[0].list[10].parameters[0]`
- `Map020.events.4.pages[0].list[74].parameters[0]`
- `Map020.events.4.pages[0].list[84].parameters[0]`
- `Map020.events.4.pages[0].list[100].parameters[0]`
- `Map020.events.4.pages[0].list[117].parameters[0]`
- `Map022.events.2.pages[0].list[4].parameters[0]`
- `Map022.events.2.pages[0].list[9].parameters[0]`
- `Map022.events.2.pages[0].list[14].parameters[0]`
- `Map022.events.12.pages[0].list[1].parameters[0]`
- `Map022.events.12.pages[0].list[5].parameters[0]`
- `Map023.events.6.pages[0].list[0].parameters[0]`
- `Map023.events.6.pages[1].list[0].parameters[0]`
- `Map025.events.10.pages[0].list[1].parameters[0]`
- `Map025.events.10.pages[0].list[5].parameters[0]`
- `Map026.events.9.pages[1].list[71].parameters[0]`
- `Map026.events.9.pages[1].list[76].parameters[0]`
- `Map026.events.9.pages[1].list[131].parameters[0]`
- `Map026.events.9.pages[1].list[151].parameters[0]`
- `Map026.events.10.pages[1].list[1].parameters[0]`
- `Map026.events.10.pages[1].list[6].parameters[0]`
- `Map026.events.10.pages[1].list[10].parameters[0]`
- `Map027.events.3.pages[0].list[1].parameters[0]`
- `Map027.events.3.pages[0].list[7].parameters[0]`
- `Map027.events.3.pages[0].list[13].parameters[0]`
- `Map027.events.3.pages[0].list[18].parameters[0]`
- `Map027.events.3.pages[0].list[23].parameters[0]`
- `Map027.events.3.pages[0].list[29].parameters[0]`
- `Map027.events.3.pages[1].list[0].parameters[0]`
- `Map028.events.2.pages[0].list[3].parameters[0]`
- `Map028.events.2.pages[0].list[6].parameters[0]`
- `Map028.events.2.pages[0].list[11].parameters[0]`
- `Map028.events.2.pages[0].list[15].parameters[0]`
- `Map029.events.6.pages[0].list[1].parameters[0]`
- `Map029.events.6.pages[0].list[6].parameters[0]`
- `Map032.events.2.pages[0].list[5].parameters[0]`
- `Map032.events.7.pages[0].list[41].parameters[0]`
- `Map032.events.7.pages[0].list[44].parameters[0]`
- `Map032.events.7.pages[0].list[151].parameters[0]`
- `Map032.events.7.pages[0].list[154].parameters[0]`
- `Map032.events.7.pages[0].list[264].parameters[0]`
- `Scripts[104] Vacas_Cinematicas:27`
### #210 Tilesets/revision_mapa11 — OK

- `Map011.Tilesets[62].tileset_name`
- `Tilesets[62].tileset_name`
### #211 Pictures/retrato_lucy_neutral — OK

- `Map012.events.2.pages[0].list[2].parameters[0]`
- `Map012.events.2.pages[0].list[7].parameters[0]`
- `Map012.events.2.pages[0].list[13].parameters[0]`
- `Map012.events.2.pages[0].list[17].parameters[0]`
- `Map012.events.4.pages[0].list[1].parameters[0]`
- `Map012.events.4.pages[0].list[5].parameters[0]`
- `Map012.events.4.pages[0].list[17].parameters[0]`
- `Map012.events.4.pages[1].list[0].parameters[0]`
- `Map012.events.6.pages[0].list[1].parameters[0]`
- `Map012.events.6.pages[0].list[12].parameters[0]`
- `Map016.events.7.pages[0].list[11].parameters[0]`
- `Map016.events.8.pages[0].list[0].parameters[0]`
- `Map016.events.8.pages[0].list[45].parameters[0]`
- `Map016.events.8.pages[0].list[107].parameters[0]`
- `Map016.events.8.pages[1].list[0].parameters[0]`
- `Map028.events.8.pages[0].list[7].parameters[0]`
### #212 Characters/vacas_laboratorio — OK

- `Map012.events.6.pages[0].graphic.character_name`
- `Map012.events.9.pages[0].graphic.character_name`
- `Map012.events.10.pages[0].graphic.character_name`
- `Map012.events.11.pages[0].graphic.character_name`
- `Map013.events.7.pages[0].graphic.character_name`
- `Map014.events.5.pages[0].graphic.character_name`
- `Map014.events.6.pages[0].graphic.character_name`
- `Map014.events.9.pages[0].graphic.character_name`
- `Map015.events.4.pages[0].graphic.character_name`
- `Map015.events.6.pages[0].graphic.character_name`
- `Map015.events.7.pages[0].graphic.character_name`
- `Map016.events.3.pages[0].graphic.character_name`
- `Map016.events.4.pages[0].graphic.character_name`
- `Map016.events.5.pages[0].graphic.character_name`
- `Map016.events.7.pages[0].graphic.character_name`
- `Map016.events.9.pages[0].graphic.character_name`
- `Map016.events.10.pages[0].graphic.character_name`
- `Map016.events.11.pages[0].graphic.character_name`
- `Scripts[100] Vacas_Interfaz:66`
### #213 Pictures/retrato_lucy_calma — OK

- `Map012.events.6.pages[0].list[6].parameters[0]`
- `Map016.events.8.pages[0].list[66].parameters[0]`
- `Map028.events.8.pages[0].list[1].parameters[0]`
### #214 Tilesets/revision_mapa12 — OK

- `Map012.Tilesets[63].tileset_name`
- `Tilesets[63].tileset_name`
### #215 Tilesets/revision_mapa13 — OK

- `Map013.Tilesets[64].tileset_name`
- `Tilesets[64].tileset_name`
### #216 Pictures/screamer_8 — OK

- `Map014.events.2.pages[0].list[6].parameters[0]`
### #217 Tilesets/revision_mapa14 — OK

- `Map014.Tilesets[65].tileset_name`
- `Tilesets[65].tileset_name`
### #218 Characters/vacas_elena — OK

- `Map015.events.3.pages[0].graphic.character_name`
### #219 Pictures/retrato_elena_neutral — OK

- `Map015.events.3.pages[0].list[2].parameters[0]`
- `Map015.events.3.pages[0].list[8].parameters[0]`
- `Map015.events.3.pages[0].list[24].parameters[0]`
- `Map015.events.3.pages[0].list[32].parameters[0]`
### #220 Characters/vacas_alcantarilla — OK

- `Map015.events.8.pages[1].graphic.character_name`
- `Map017.events.3.pages[0].graphic.character_name`
- `Map017.events.4.pages[0].graphic.character_name`
- `Map017.events.5.pages[0].graphic.character_name`
- `Map017.events.6.pages[0].graphic.character_name`
- `Map017.events.6.pages[1].graphic.character_name`
- `Map017.events.7.pages[0].graphic.character_name`
- `Map017.events.8.pages[0].graphic.character_name`
- `Map018.events.2.pages[0].graphic.character_name`
- `Map018.events.3.pages[0].graphic.character_name`
- `Map018.events.4.pages[0].graphic.character_name`
- `Map018.events.9.pages[0].graphic.character_name`
- `Map018.events.10.pages[0].graphic.character_name`
- `Map018.events.11.pages[0].graphic.character_name`
- `Map018.events.12.pages[0].graphic.character_name`
- `Map019.events.2.pages[0].graphic.character_name`
- `Map019.events.3.pages[0].graphic.character_name`
- `Map019.events.5.pages[0].graphic.character_name`
- `Map019.events.6.pages[0].graphic.character_name`
- `Map019.events.10.pages[0].graphic.character_name`
- `Map019.events.11.pages[0].graphic.character_name`
- `Map019.events.12.pages[0].graphic.character_name`
- `Map020.events.2.pages[0].graphic.character_name`
- `Map020.events.3.pages[0].graphic.character_name`
- `Map020.events.7.pages[0].graphic.character_name`
- `Map021.events.2.pages[0].graphic.character_name`
- `Map021.events.3.pages[0].graphic.character_name`
- `Map021.events.4.pages[0].graphic.character_name`
- `Map021.events.5.pages[0].graphic.character_name`
- `Map021.events.6.pages[0].graphic.character_name`
- `Map021.events.7.pages[0].graphic.character_name`
- `Map021.events.8.pages[0].graphic.character_name`
### #221 Tilesets/revision_mapa15 — OK

- `Map015.Tilesets[66].tileset_name`
- `Tilesets[66].tileset_name`
### #222 Pictures/retrato_lucy_quiebre — OK

- `Map016.events.7.pages[0].list[26].parameters[0]`
- `Map016.events.8.pages[0].list[4].parameters[0]`
- `Map016.events.8.pages[0].list[41].parameters[0]`
- `Map016.events.8.pages[0].list[87].parameters[0]`
### #223 Pictures/screamer_9 — OK

- `Map016.events.7.pages[0].list[29].parameters[0]`
### #224 Tilesets/revision_mapa16 — OK

- `Map016.Tilesets[67].tileset_name`
- `Tilesets[67].tileset_name`
### #225 Tilesets/acto4_alcantarillas — OK

- `Map017.Tilesets[68].tileset_name`
- `Map018.Tilesets[68].tileset_name`
- `Map019.Tilesets[68].tileset_name`
- `Map020.Tilesets[68].tileset_name`
- `Map021.Tilesets[68].tileset_name`
- `Tilesets[68].tileset_name`
### #226 Battlebacks/mente_tunel — OK

- `Map017.Tilesets[68].battleback_name`
- `Map018.Tilesets[68].battleback_name`
- `Map019.Tilesets[68].battleback_name`
- `Map020.Tilesets[68].battleback_name`
- `Map021.Tilesets[68].battleback_name`
- `Tilesets[68].battleback_name`
- `Scripts: Vacas_Mente fondo dinámico`
### #227 Characters/vacas_muesca — OK

- `Map018.events.5.pages[0].graphic.character_name`
- `Map018.events.6.pages[1].graphic.character_name`
- `Map019.events.7.pages[1].graphic.character_name`
- `Map020.events.5.pages[0].graphic.character_name`
- `Map023.events.5.pages[1].graphic.character_name`
- `Map027.events.4.pages[0].graphic.character_name`
- `Map028.events.6.pages[0].graphic.character_name`
- `Map028.events.6.pages[1].graphic.character_name`
### #228 Pictures/retrato_muesca_neutral — OK

- `Map018.events.5.pages[0].list[1].parameters[0]`
- `Map018.events.5.pages[0].list[17].parameters[0]`
- `Map018.events.5.pages[0].list[27].parameters[0]`
- `Map018.events.5.pages[0].list[39].parameters[0]`
- `Map018.events.5.pages[0].list[46].parameters[0]`
- `Map018.events.5.pages[0].list[50].parameters[0]`
- `Map020.events.4.pages[0].list[19].parameters[0]`
- `Map020.events.5.pages[0].list[1].parameters[0]`
- `Map020.events.5.pages[0].list[4].parameters[0]`
- `Map023.events.5.pages[1].list[1].parameters[0]`
- `Map023.events.5.pages[1].list[5].parameters[0]`
- `Map027.events.4.pages[0].list[1].parameters[0]`
- `Map027.events.4.pages[0].list[5].parameters[0]`
- `Map028.events.6.pages[0].list[1].parameters[0]`
- `Map028.events.6.pages[0].list[8].parameters[0]`
- `Map028.events.6.pages[1].list[0].parameters[0]`
- `Map032.events.7.pages[0].list[164].parameters[0]`
- `Map032.events.7.pages[0].list[269].parameters[0]`
### #229 Pictures/screamer_10 — OK

- `Map018.events.5.pages[0].list[35].parameters[0]`
### #230 Characters/vacas_junco — OK

- `Map019.events.4.pages[0].graphic.character_name`
- `Map020.events.6.pages[0].graphic.character_name`
- `Map023.events.5.pages[2].graphic.character_name`
- `Map027.events.5.pages[1].graphic.character_name`
### #231 Pictures/retrato_junco_neutral — OK

- `Map019.events.4.pages[0].list[1].parameters[0]`
- `Map019.events.4.pages[0].list[7].parameters[0]`
- `Map019.events.4.pages[0].list[16].parameters[0]`
- `Map019.events.4.pages[0].list[22].parameters[0]`
- `Map020.events.4.pages[0].list[15].parameters[0]`
- `Map020.events.6.pages[0].list[1].parameters[0]`
- `Map020.events.6.pages[0].list[5].parameters[0]`
- `Map023.events.5.pages[2].list[1].parameters[0]`
- `Map023.events.5.pages[2].list[5].parameters[0]`
- `Map027.events.5.pages[1].list[0].parameters[0]`
### #232 Pictures/screamer_11 — OK

- `Map019.events.6.pages[0].list[18].parameters[0]`
### #233 Characters/vacas_guernsey4 — OK

- `Map020.events.4.pages[0].graphic.character_name`
- `Map026.events.10.pages[1].graphic.character_name`
- `Map027.events.3.pages[0].graphic.character_name`
- `Map027.events.3.pages[1].graphic.character_name`
- `Map029.events.6.pages[0].graphic.character_name`
- `Map032.events.7.pages[0].graphic.character_name`
### #234 Tilesets/acto5_matanza — OK

- `Map022.Tilesets[69].tileset_name`
- `Map023.Tilesets[69].tileset_name`
- `Map024.Tilesets[69].tileset_name`
- `Map025.Tilesets[69].tileset_name`
- `Map026.Tilesets[69].tileset_name`
- `Map027.Tilesets[69].tileset_name`
- `Tilesets[69].tileset_name`
### #235 Pictures/screamer_12 — OK

- `Map025.events.4.pages[1].list[8].parameters[0]`
### #236 Pictures/screamer_13 — OK

- `Map025.events.6.pages[0].list[11].parameters[0]`
- `Map025.events.7.pages[0].list[11].parameters[0]`
### #237 Tilesets/acto6_reydios — OK

- `Map028.Tilesets[70].tileset_name`
- `Map029.Tilesets[70].tileset_name`
- `Map030.Tilesets[70].tileset_name`
- `Map031.Tilesets[70].tileset_name`
- `Map032.Tilesets[70].tileset_name`
- `Tilesets[70].tileset_name`
### #238 Pictures/retrato_madre_envejecida_neutral — OK

- `Map030.events.2.pages[0].list[4].parameters[0]`
- `Map030.events.2.pages[0].list[6].parameters[0]`
- `Map030.events.5.pages[0].list[0].parameters[0]`
- `Map030.events.5.pages[0].list[50].parameters[0]`
- `Map030.events.5.pages[1].list[1].parameters[0]`
- `Map030.events.5.pages[1].list[5].parameters[0]`
### #239 Icons/045-Skill02 — PLACEHOLDER o RTP

- `Skills[1].icon_name`
- `Skills[2].icon_name`
- `Skills[3].icon_name`
- `Skills[4].icon_name`
- `Skills[5].icon_name`
- `Skills[6].icon_name`
### #240 Icons/044-Skill01 — PLACEHOLDER o RTP

- `Skills[7].icon_name`
- `Skills[8].icon_name`
- `Skills[9].icon_name`
- `Skills[10].icon_name`
- `Skills[11].icon_name`
- `Skills[12].icon_name`
- `Skills[13].icon_name`
- `Skills[14].icon_name`
- `Skills[15].icon_name`
- `Skills[16].icon_name`
- `Skills[17].icon_name`
- `Skills[18].icon_name`
- `Skills[19].icon_name`
- `Skills[20].icon_name`
- `Skills[21].icon_name`
- `Skills[22].icon_name`
- `Skills[23].icon_name`
- `Skills[24].icon_name`
- `Skills[25].icon_name`
- `Skills[26].icon_name`
- `Skills[27].icon_name`
- `Skills[28].icon_name`
- `Skills[29].icon_name`
- `Skills[30].icon_name`
- `Skills[31].icon_name`
- `Skills[32].icon_name`
### #241 Icons/046-Skill03 — PLACEHOLDER o RTP

- `Skills[33].icon_name`
- `Skills[34].icon_name`
- `Skills[35].icon_name`
- `Skills[36].icon_name`
- `Skills[37].icon_name`
- `Skills[38].icon_name`
- `Skills[39].icon_name`
- `Skills[40].icon_name`
- `Skills[41].icon_name`
- `Skills[42].icon_name`
- `Skills[43].icon_name`
- `Skills[44].icon_name`
### #242 Icons/047-Skill04 — PLACEHOLDER o RTP

- `Skills[45].icon_name`
- `Skills[46].icon_name`
- `Skills[47].icon_name`
- `Skills[48].icon_name`
- `Skills[49].icon_name`
- `Skills[50].icon_name`
- `Skills[51].icon_name`
- `Skills[52].icon_name`
### #243 Icons/048-Skill05 — PLACEHOLDER o RTP

- `Skills[53].icon_name`
- `Skills[54].icon_name`
- `Skills[55].icon_name`
- `Skills[56].icon_name`
### #244 Icons/050-Skill07 — PLACEHOLDER o RTP

- `Skills[57].icon_name`
- `Skills[58].icon_name`
- `Skills[59].icon_name`
- `Skills[60].icon_name`
- `Skills[71].icon_name`
- `Skills[72].icon_name`
- `Skills[73].icon_name`
- `Skills[74].icon_name`
- `Skills[75].icon_name`
- `Skills[76].icon_name`
- `Skills[77].icon_name`
- `Skills[78].icon_name`
- `Skills[79].icon_name`
- `Skills[80].icon_name`
### #245 Icons/vacas_habilidad_61 — OK

- `Skills[61].icon_name`
### #246 Icons/vacas_habilidad_62 — OK

- `Skills[62].icon_name`
### #247 Icons/vacas_habilidad_63 — OK

- `Skills[63].icon_name`
### #248 Icons/vacas_habilidad_64 — OK

- `Skills[64].icon_name`
### #249 Icons/vacas_habilidad_65 — OK

- `Skills[65].icon_name`
### #250 Icons/vacas_habilidad_66 — OK

- `Skills[66].icon_name`
### #251 Icons/vacas_habilidad_67 — OK

- `Skills[67].icon_name`
### #252 Icons/vacas_habilidad_68 — OK

- `Skills[68].icon_name`
### #253 Icons/vacas_habilidad_69 — OK

- `Skills[69].icon_name`
### #254 Icons/vacas_habilidad_70 — OK

- `Skills[70].icon_name`
### #255 Gameovers/vacas_gameover — OK

- `System.gameover_name`
- `Scripts[89] Vacas_Nucleo:45`
- `Scripts[100] Vacas_Interfaz:48`
### #256 Titles/vacas_titulo — OK

- `System.title_name`
- `Scripts[89] Vacas_Nucleo:44`
- `Scripts[100] Vacas_Interfaz:44`
### #257 Windowskins/ui_windowskin — OK

- `System.windowskin_name`
- `Scripts[100] Vacas_Interfaz:492`
- `Scripts[100] Vacas_Interfaz:498`
- `Scripts[100] Vacas_Interfaz:816`
### #258 Battlebacks/mente_matadero — OK

- `System.battleback_name`
- `Scripts: Vacas_Mente fondo dinámico`
### #259 Autotiles/001-G_Water01 — PLACEHOLDER o RTP

- `Tilesets[1].autotile_names[0]`
- `Tilesets[2].autotile_names[0]`
- `Tilesets[4].autotile_names[0]`
- `Tilesets[13].autotile_names[0]`
- `Tilesets[15].autotile_names[0]`
- `Tilesets[23].autotile_names[0]`
- `Tilesets[32].autotile_names[0]`
- `Tilesets[34].autotile_names[0]`
- `Tilesets[35].autotile_names[0]`
- `Tilesets[37].autotile_names[0]`
- `Tilesets[39].autotile_names[0]`
### #260 Autotiles/040-Ground01 — PLACEHOLDER o RTP

- `Tilesets[1].autotile_names[3]`
- `Tilesets[2].autotile_names[3]`
- `Tilesets[4].autotile_names[2]`
- `Tilesets[13].autotile_names[4]`
- `Tilesets[17].autotile_names[1]`
- `Tilesets[23].autotile_names[3]`
- `Tilesets[32].autotile_names[3]`
- `Tilesets[34].autotile_names[4]`
- `Tilesets[37].autotile_names[3]`
- `Tilesets[39].autotile_names[3]`
### #261 Autotiles/041-Grass01 — PLACEHOLDER o RTP

- `Tilesets[1].autotile_names[4]`
- `Tilesets[11].autotile_names[4]`
- `Tilesets[13].autotile_names[5]`
- `Tilesets[15].autotile_names[3]`
- `Tilesets[23].autotile_names[4]`
- `Tilesets[32].autotile_names[4]`
- `Tilesets[34].autotile_names[5]`
- `Tilesets[37].autotile_names[4]`
### #262 Autotiles/007-G_Undulation01 — PLACEHOLDER o RTP

- `Tilesets[1].autotile_names[5]`
- `Tilesets[4].autotile_names[3]`
- `Tilesets[23].autotile_names[6]`
### #263 Autotiles/008-G_Undulation02 — PLACEHOLDER o RTP

- `Tilesets[1].autotile_names[6]`
- `Tilesets[37].autotile_names[6]`
### #264 Battlebacks/001-Grassland01 — PLACEHOLDER o RTP

- `Tilesets[1].battleback_name`
### #265 Tilesets/001-Grassland01 — PLACEHOLDER o RTP

- `Tilesets[1].tileset_name`
### #266 Autotiles/043-Grass02 — PLACEHOLDER o RTP

- `Tilesets[2].autotile_names[4]`
- `Tilesets[35].autotile_names[5]`
- `Tilesets[39].autotile_names[4]`
### #267 Autotiles/036-Tree01 — PLACEHOLDER o RTP

- `Tilesets[2].autotile_names[5]`
- `Tilesets[15].autotile_names[5]`
### #268 Autotiles/037-Tree02 — PLACEHOLDER o RTP

- `Tilesets[2].autotile_names[6]`
- `Tilesets[15].autotile_names[6]`
### #269 Battlebacks/002-Woods01 — PLACEHOLDER o RTP

- `Tilesets[2].battleback_name`
### #270 Tilesets/002-Woods01 — PLACEHOLDER o RTP

- `Tilesets[2].tileset_name`
### #271 Autotiles/009-G2_Water01 — PLACEHOLDER o RTP

- `Tilesets[3].autotile_names[0]`
### #272 Autotiles/010-G2_Ground01 — PLACEHOLDER o RTP

- `Tilesets[3].autotile_names[1]`
- `Tilesets[7].autotile_names[0]`
### #273 Autotiles/011-G2_Ground02 — PLACEHOLDER o RTP

- `Tilesets[3].autotile_names[2]`
- `Tilesets[7].autotile_names[1]`
### #274 Autotiles/042-Ground02 — PLACEHOLDER o RTP

- `Tilesets[3].autotile_names[3]`
- `Tilesets[7].autotile_names[2]`
### #275 Autotiles/038-Tree03 — PLACEHOLDER o RTP

- `Tilesets[3].autotile_names[4]`
- `Tilesets[7].autotile_names[3]`
- `Tilesets[35].autotile_names[6]`
### #276 Autotiles/039-Tree04 — PLACEHOLDER o RTP

- `Tilesets[3].autotile_names[5]`
### #277 Battlebacks/003-Forest01 — PLACEHOLDER o RTP

- `Tilesets[3].battleback_name`
### #278 Tilesets/003-Forest01 — PLACEHOLDER o RTP

- `Tilesets[3].tileset_name`
### #279 Panoramas/006-Mountains01 — PLACEHOLDER o RTP

- `Tilesets[4].panorama_name`
- `Tilesets[34].panorama_name`
### #280 Autotiles/033-Waterfall01 — PLACEHOLDER o RTP

- `Tilesets[4].autotile_names[4]`
### #281 Autotiles/034-Waterfall02 — PLACEHOLDER o RTP

- `Tilesets[4].autotile_names[5]`
### #282 Autotiles/035-Waterfall03 — PLACEHOLDER o RTP

- `Tilesets[4].autotile_names[6]`
### #283 Battlebacks/004-Mountain01 — PLACEHOLDER o RTP

- `Tilesets[4].battleback_name`
### #284 Tilesets/004-Mountain01 — PLACEHOLDER o RTP

- `Tilesets[4].tileset_name`
### #285 Autotiles/024-Ocean01 — PLACEHOLDER o RTP

- `Tilesets[5].autotile_names[0]`
### #286 Autotiles/025-Ocean02 — PLACEHOLDER o RTP

- `Tilesets[5].autotile_names[1]`
### #287 Autotiles/026-Ocean03 — PLACEHOLDER o RTP

- `Tilesets[5].autotile_names[2]`
### #288 Autotiles/027-Ocean04 — PLACEHOLDER o RTP

- `Tilesets[5].autotile_names[3]`
### #289 Autotiles/016-Sa_Shadow01 — PLACEHOLDER o RTP

- `Tilesets[5].autotile_names[4]`
- `Tilesets[6].autotile_names[1]`
- `Tilesets[19].autotile_names[1]`
### #290 Autotiles/017-Sa_Grass01 — PLACEHOLDER o RTP

- `Tilesets[5].autotile_names[5]`
- `Tilesets[6].autotile_names[2]`
- `Tilesets[11].autotile_names[3]`
### #291 Autotiles/045-Road02 — PLACEHOLDER o RTP

- `Tilesets[5].autotile_names[6]`
- `Tilesets[32].autotile_names[6]`
### #292 Battlebacks/005-Beach01 — PLACEHOLDER o RTP

- `Tilesets[5].battleback_name`
### #293 Tilesets/005-Beach01 — PLACEHOLDER o RTP

- `Tilesets[5].tileset_name`
### #294 Autotiles/015-Sa_Water01 — PLACEHOLDER o RTP

- `Tilesets[6].autotile_names[0]`
- `Tilesets[19].autotile_names[0]`
### #295 Autotiles/018-Sa_Ground01 — PLACEHOLDER o RTP

- `Tilesets[6].autotile_names[3]`
- `Tilesets[19].autotile_names[2]`
### #296 Autotiles/019-Sa_Grass02 — PLACEHOLDER o RTP

- `Tilesets[6].autotile_names[4]`
- `Tilesets[19].autotile_names[3]`
### #297 Autotiles/020-Sa_Grass03 — PLACEHOLDER o RTP

- `Tilesets[6].autotile_names[5]`
- `Tilesets[19].autotile_names[4]`
### #298 Autotiles/023-Sa_Undulation01 — PLACEHOLDER o RTP

- `Tilesets[6].autotile_names[6]`
### #299 Battlebacks/006-Desert01 — PLACEHOLDER o RTP

- `Tilesets[6].battleback_name`
### #300 Tilesets/006-Desert01 — PLACEHOLDER o RTP

- `Tilesets[6].tileset_name`
### #301 Autotiles/012-G2_Swamp01 — PLACEHOLDER o RTP

- `Tilesets[7].autotile_names[4]`
### #302 Autotiles/013-G2_Swamp02 — PLACEHOLDER o RTP

- `Tilesets[7].autotile_names[5]`
### #303 Autotiles/014-G2_Swamp03 — PLACEHOLDER o RTP

- `Tilesets[7].autotile_names[6]`
### #304 Battlebacks/007-Swamp01 — PLACEHOLDER o RTP

- `Tilesets[7].battleback_name`
### #305 Tilesets/007-Swamp01 — PLACEHOLDER o RTP

- `Tilesets[7].tileset_name`
### #306 Autotiles/028-Sn_Water01 — PLACEHOLDER o RTP

- `Tilesets[8].autotile_names[0]`
- `Tilesets[21].autotile_names[0]`
### #307 Autotiles/029-Sn_Shadow01 — PLACEHOLDER o RTP

- `Tilesets[8].autotile_names[1]`
- `Tilesets[21].autotile_names[1]`
### #308 Autotiles/030-Sn_Ground01 — PLACEHOLDER o RTP

- `Tilesets[8].autotile_names[2]`
- `Tilesets[21].autotile_names[2]`
### #309 Autotiles/044-Road01 — PLACEHOLDER o RTP

- `Tilesets[8].autotile_names[3]`
- `Tilesets[13].autotile_names[6]`
- `Tilesets[15].autotile_names[4]`
- `Tilesets[17].autotile_names[2]`
- `Tilesets[21].autotile_names[3]`
- `Tilesets[23].autotile_names[5]`
- `Tilesets[37].autotile_names[5]`
- `Tilesets[39].autotile_names[5]`
### #310 Autotiles/031-Sn_Undulation01 — PLACEHOLDER o RTP

- `Tilesets[8].autotile_names[4]`
- `Tilesets[21].autotile_names[4]`
### #311 Battlebacks/008-Snowfield01 — PLACEHOLDER o RTP

- `Tilesets[8].battleback_name`
### #312 Tilesets/008-Snowfield01 — PLACEHOLDER o RTP

- `Tilesets[8].tileset_name`
### #313 Battlebacks/009-CastleTown01 — PLACEHOLDER o RTP

- `Tilesets[9].battleback_name`
### #314 Tilesets/009-CastleTown01 — PLACEHOLDER o RTP

- `Tilesets[9].tileset_name`
### #315 Autotiles/054-Wall02 — PLACEHOLDER o RTP

- `Tilesets[10].autotile_names[0]`
- `Tilesets[14].autotile_names[0]`
- `Tilesets[16].autotile_names[0]`
- `Tilesets[22].autotile_names[0]`
- `Tilesets[36].autotile_names[1]`
### #316 Autotiles/051-Carpet01 — PLACEHOLDER o RTP

- `Tilesets[10].autotile_names[1]`
- `Tilesets[26].autotile_names[3]`
- `Tilesets[27].autotile_names[3]`
- `Tilesets[29].autotile_names[1]`
- `Tilesets[31].autotile_names[0]`
- `Tilesets[33].autotile_names[3]`
- `Tilesets[38].autotile_names[1]`
- `Tilesets[42].autotile_names[1]`
### #317 Battlebacks/010-CastleTown02 — PLACEHOLDER o RTP

- `Tilesets[10].battleback_name`
### #318 Tilesets/010-CastleTown02 — PLACEHOLDER o RTP

- `Tilesets[10].tileset_name`
### #319 Autotiles/032-T_Ocean01 — PLACEHOLDER o RTP

- `Tilesets[11].autotile_names[0]`
- `Tilesets[30].autotile_names[1]`
### #320 Autotiles/004-G_Ground02 — PLACEHOLDER o RTP

- `Tilesets[11].autotile_names[2]`
- `Tilesets[15].autotile_names[2]`
- `Tilesets[25].autotile_names[2]`
- `Tilesets[28].autotile_names[2]`
### #321 Battlebacks/011-PortTown01 — PLACEHOLDER o RTP

- `Tilesets[11].battleback_name`
### #322 Tilesets/011-PortTown01 — PLACEHOLDER o RTP

- `Tilesets[11].tileset_name`
### #323 Battlebacks/012-PortTown02 — PLACEHOLDER o RTP

- `Tilesets[12].battleback_name`
### #324 Tilesets/012-PortTown02 — PLACEHOLDER o RTP

- `Tilesets[12].tileset_name`
### #325 Battlebacks/013-PostTown01 — PLACEHOLDER o RTP

- `Tilesets[13].battleback_name`
### #326 Tilesets/013-PostTown01 — PLACEHOLDER o RTP

- `Tilesets[13].tileset_name`
### #327 Battlebacks/014-PostTown02 — PLACEHOLDER o RTP

- `Tilesets[14].battleback_name`
### #328 Tilesets/014-PostTown02 — PLACEHOLDER o RTP

- `Tilesets[14].tileset_name`
### #329 Battlebacks/015-ForestTown01 — PLACEHOLDER o RTP

- `Tilesets[15].battleback_name`
### #330 Tilesets/015-ForestTown01 — PLACEHOLDER o RTP

- `Tilesets[15].tileset_name`
### #331 Battlebacks/016-ForestTown02 — PLACEHOLDER o RTP

- `Tilesets[16].battleback_name`
### #332 Tilesets/016-ForestTown02 — PLACEHOLDER o RTP

- `Tilesets[16].tileset_name`
### #333 Battlebacks/017-MineTown01 — PLACEHOLDER o RTP

- `Tilesets[17].battleback_name`
### #334 Tilesets/017-MineTown01 — PLACEHOLDER o RTP

- `Tilesets[17].tileset_name`
### #335 Battlebacks/018-MineTown02 — PLACEHOLDER o RTP

- `Tilesets[18].battleback_name`
### #336 Tilesets/018-MineTown02 — PLACEHOLDER o RTP

- `Tilesets[18].tileset_name`
### #337 Autotiles/021-Sa_Road01 — PLACEHOLDER o RTP

- `Tilesets[19].autotile_names[5]`
### #338 Autotiles/022-Roof01 — PLACEHOLDER o RTP

- `Tilesets[19].autotile_names[6]`
### #339 Battlebacks/019-DesertTown01 — PLACEHOLDER o RTP

- `Tilesets[19].battleback_name`
### #340 Tilesets/019-DesertTown01 — PLACEHOLDER o RTP

- `Tilesets[19].tileset_name`
### #341 Autotiles/055-Wall03 — PLACEHOLDER o RTP

- `Tilesets[20].autotile_names[0]`
- `Tilesets[36].autotile_names[2]`
### #342 Battlebacks/020-DesertTown02 — PLACEHOLDER o RTP

- `Tilesets[20].battleback_name`
### #343 Tilesets/020-DesertTown02 — PLACEHOLDER o RTP

- `Tilesets[20].tileset_name`
### #344 Battlebacks/021-SnowTown01 — PLACEHOLDER o RTP

- `Tilesets[21].battleback_name`
### #345 Tilesets/021-SnowTown01 — PLACEHOLDER o RTP

- `Tilesets[21].tileset_name`
### #346 Battlebacks/022-SnowTown02 — PLACEHOLDER o RTP

- `Tilesets[22].battleback_name`
### #347 Tilesets/022-SnowTown02 — PLACEHOLDER o RTP

- `Tilesets[22].tileset_name`
### #348 Battlebacks/023-FarmVillage01 — PLACEHOLDER o RTP

- `Tilesets[23].battleback_name`
### #349 Tilesets/023-FarmVillage01 — PLACEHOLDER o RTP

- `Tilesets[23].tileset_name`
### #350 Battlebacks/024-FarmVillage02 — PLACEHOLDER o RTP

- `Tilesets[24].battleback_name`
### #351 Tilesets/024-FarmVillage02 — PLACEHOLDER o RTP

- `Tilesets[24].tileset_name`
### #352 Autotiles/047-Flower01 — PLACEHOLDER o RTP

- `Tilesets[25].autotile_names[4]`
- `Tilesets[28].autotile_names[5]`
- `Tilesets[32].autotile_names[5]`
### #353 Battlebacks/025-Castle01 — PLACEHOLDER o RTP

- `Tilesets[25].battleback_name`
### #354 Tilesets/025-Castle01 — PLACEHOLDER o RTP

- `Tilesets[25].tileset_name`
### #355 Autotiles/049-St_Shadow01 — PLACEHOLDER o RTP

- `Tilesets[26].autotile_names[2]`
- `Tilesets[27].autotile_names[2]`
- `Tilesets[33].autotile_names[2]`
- `Tilesets[36].autotile_names[4]`
- `Tilesets[40].autotile_names[2]`
- `Tilesets[48].autotile_names[2]`
### #356 Battlebacks/026-Castle02 — PLACEHOLDER o RTP

- `Tilesets[26].battleback_name`
### #357 Tilesets/026-Castle02 — PLACEHOLDER o RTP

- `Tilesets[26].tileset_name`
### #358 Battlebacks/027-Castle03 — PLACEHOLDER o RTP

- `Tilesets[27].battleback_name`
### #359 Tilesets/027-Castle03 — PLACEHOLDER o RTP

- `Tilesets[27].tileset_name`
### #360 Battlebacks/028-Church01 — PLACEHOLDER o RTP

- `Tilesets[28].battleback_name`
### #361 Tilesets/028-Church01 — PLACEHOLDER o RTP

- `Tilesets[28].tileset_name`
### #362 Battlebacks/029-Church02 — PLACEHOLDER o RTP

- `Tilesets[29].battleback_name`
### #363 Tilesets/029-Church02 — PLACEHOLDER o RTP

- `Tilesets[29].tileset_name`
### #364 Autotiles/046-Road03 — PLACEHOLDER o RTP

- `Tilesets[30].autotile_names[2]`
### #365 Battlebacks/030-Ship01 — PLACEHOLDER o RTP

- `Tilesets[30].battleback_name`
### #366 Tilesets/030-Ship01 — PLACEHOLDER o RTP

- `Tilesets[30].tileset_name`
### #367 Battlebacks/031-Ship02 — PLACEHOLDER o RTP

- `Tilesets[31].battleback_name`
### #368 Tilesets/031-Ship02 — PLACEHOLDER o RTP

- `Tilesets[31].tileset_name`
### #369 Panoramas/001-Sky01 — PLACEHOLDER o RTP

- `Tilesets[32].panorama_name`
- `Tilesets[33].panorama_name`
### #370 Battlebacks/032-Heaven01 — PLACEHOLDER o RTP

- `Tilesets[32].battleback_name`
### #371 Tilesets/032-Heaven01 — PLACEHOLDER o RTP

- `Tilesets[32].tileset_name`
### #372 Battlebacks/033-Heaven02 — PLACEHOLDER o RTP

- `Tilesets[33].battleback_name`
### #373 Tilesets/033-Heaven02 — PLACEHOLDER o RTP

- `Tilesets[33].tileset_name`
### #374 Battlebacks/034-Bridge01 — PLACEHOLDER o RTP

- `Tilesets[34].battleback_name`
### #375 Tilesets/034-Bridge01 — PLACEHOLDER o RTP

- `Tilesets[34].tileset_name`
### #376 Tilesets/035-Ruins01 — PLACEHOLDER o RTP

- `Tilesets[35].tileset_name`
### #377 Battlebacks/035-Ruins01 — PLACEHOLDER o RTP

- `Tilesets[35].battleback_name`
### #378 Battlebacks/036-Shop01 — PLACEHOLDER o RTP

- `Tilesets[36].battleback_name`
### #379 Tilesets/036-Shop01 — PLACEHOLDER o RTP

- `Tilesets[36].tileset_name`
### #380 Battlebacks/037-Fort01 — PLACEHOLDER o RTP

- `Tilesets[37].battleback_name`
### #381 Tilesets/037-Fort01 — PLACEHOLDER o RTP

- `Tilesets[37].tileset_name`
### #382 Battlebacks/038-Fort02 — PLACEHOLDER o RTP

- `Tilesets[38].battleback_name`
### #383 Tilesets/038-Fort02 — PLACEHOLDER o RTP

- `Tilesets[38].tileset_name`
### #384 Battlebacks/039-Tower01 — PLACEHOLDER o RTP

- `Tilesets[39].battleback_name`
### #385 Tilesets/039-Tower01 — PLACEHOLDER o RTP

- `Tilesets[39].tileset_name`
### #386 Battlebacks/040-Tower02 — PLACEHOLDER o RTP

- `Tilesets[40].battleback_name`
### #387 Tilesets/040-Tower02 — PLACEHOLDER o RTP

- `Tilesets[40].tileset_name`
### #388 Battlebacks/041-EvilCastle01 — PLACEHOLDER o RTP

- `Tilesets[41].battleback_name`
### #389 Tilesets/041-EvilCastle01 — PLACEHOLDER o RTP

- `Tilesets[41].tileset_name`
### #390 Battlebacks/042-EvilCastle02 — PLACEHOLDER o RTP

- `Tilesets[42].battleback_name`
### #391 Tilesets/042-EvilCastle02 — PLACEHOLDER o RTP

- `Tilesets[42].tileset_name`
### #392 Autotiles/056-CE_Water01 — PLACEHOLDER o RTP

- `Tilesets[43].autotile_names[0]`
### #393 Autotiles/057-CE_Shadow01 — PLACEHOLDER o RTP

- `Tilesets[43].autotile_names[1]`
### #394 Autotiles/058-CE_Ground01 — PLACEHOLDER o RTP

- `Tilesets[43].autotile_names[2]`
### #395 Autotiles/059-CE_Ground02 — PLACEHOLDER o RTP

- `Tilesets[43].autotile_names[3]`
### #396 Autotiles/060-CE_Grass01 — PLACEHOLDER o RTP

- `Tilesets[43].autotile_names[4]`
### #397 Autotiles/061-CE_Road01 — PLACEHOLDER o RTP

- `Tilesets[43].autotile_names[5]`
### #398 Battlebacks/043-Cave01 — PLACEHOLDER o RTP

- `Tilesets[43].battleback_name`
### #399 Tilesets/043-Cave01 — PLACEHOLDER o RTP

- `Tilesets[43].tileset_name`
### #400 Autotiles/062-CF_Lava01 — PLACEHOLDER o RTP

- `Tilesets[44].autotile_names[0]`
### #401 Autotiles/063-CF_Shadow01 — PLACEHOLDER o RTP

- `Tilesets[44].autotile_names[1]`
### #402 Autotiles/064-CF_Ground01 — PLACEHOLDER o RTP

- `Tilesets[44].autotile_names[2]`
### #403 Autotiles/065-CF_Ground02 — PLACEHOLDER o RTP

- `Tilesets[44].autotile_names[3]`
### #404 Autotiles/066-CF_Ground03 — PLACEHOLDER o RTP

- `Tilesets[44].autotile_names[4]`
### #405 Autotiles/067-CF_Ground04 — PLACEHOLDER o RTP

- `Tilesets[44].autotile_names[5]`
### #406 Tilesets/044-Cave02 — PLACEHOLDER o RTP

- `Tilesets[44].tileset_name`
### #407 Battlebacks/044-Cave02 — PLACEHOLDER o RTP

- `Tilesets[44].battleback_name`
### #408 Autotiles/068-CI_Water01 — PLACEHOLDER o RTP

- `Tilesets[45].autotile_names[0]`
### #409 Autotiles/069-CI_Shadow01 — PLACEHOLDER o RTP

- `Tilesets[45].autotile_names[1]`
### #410 Autotiles/070-CI_Snow01 — PLACEHOLDER o RTP

- `Tilesets[45].autotile_names[2]`
### #411 Autotiles/071-CI_Ground01 — PLACEHOLDER o RTP

- `Tilesets[45].autotile_names[3]`
### #412 Autotiles/072-CI_Ice01 — PLACEHOLDER o RTP

- `Tilesets[45].autotile_names[4]`
### #413 Autotiles/073-CI_Ground02 — PLACEHOLDER o RTP

- `Tilesets[45].autotile_names[5]`
### #414 Tilesets/045-Cave03 — PLACEHOLDER o RTP

- `Tilesets[45].tileset_name`
### #415 Battlebacks/045-Cave03 — PLACEHOLDER o RTP

- `Tilesets[45].battleback_name`
### #416 Autotiles/074-CW_Water01 — PLACEHOLDER o RTP

- `Tilesets[46].autotile_names[0]`
### #417 Autotiles/075-CW_Shadow01 — PLACEHOLDER o RTP

- `Tilesets[46].autotile_names[1]`
### #418 Autotiles/076-CW_Grass01 — PLACEHOLDER o RTP

- `Tilesets[46].autotile_names[2]`
### #419 Autotiles/077-CW_Grass02 — PLACEHOLDER o RTP

- `Tilesets[46].autotile_names[3]`
### #420 Autotiles/078-CW_Ground01 — PLACEHOLDER o RTP

- `Tilesets[46].autotile_names[4]`
### #421 Autotiles/079-CW_Grass03 — PLACEHOLDER o RTP

- `Tilesets[46].autotile_names[5]`
### #422 Tilesets/046-Cave04 — PLACEHOLDER o RTP

- `Tilesets[46].tileset_name`
### #423 Battlebacks/046-Cave04 — PLACEHOLDER o RTP

- `Tilesets[46].battleback_name`
### #424 Battlebacks/047-Mine01 — PLACEHOLDER o RTP

- `Tilesets[47].battleback_name`
### #425 Tilesets/047-Mine01 — PLACEHOLDER o RTP

- `Tilesets[47].tileset_name`
### #426 Battlebacks/048-Sewer01 — PLACEHOLDER o RTP

- `Tilesets[48].battleback_name`
### #427 Tilesets/048-Sewer01 — PLACEHOLDER o RTP

- `Tilesets[48].tileset_name`
### #428 Autotiles/080-B_Ground01 — PLACEHOLDER o RTP

- `Tilesets[49].autotile_names[0]`
### #429 Autotiles/081-B_Ground02 — PLACEHOLDER o RTP

- `Tilesets[49].autotile_names[1]`
### #430 Battlebacks/049-InnerBody01 — PLACEHOLDER o RTP

- `Tilesets[49].battleback_name`
### #431 Tilesets/049-InnerBody01 — PLACEHOLDER o RTP

- `Tilesets[49].tileset_name`
### #432 Panoramas/003-StarlitSky01 — PLACEHOLDER o RTP

- `Tilesets[50].panorama_name`
### #433 Battlebacks/050-DarkSpace01 — PLACEHOLDER o RTP

- `Tilesets[50].battleback_name`
### #434 Tilesets/050-DarkSpace01 — PLACEHOLDER o RTP

- `Tilesets[50].tileset_name`
### #435 Tilesets/vacas_matadero — OK

- `Tilesets[51].tileset_name`
- `Scripts[100] Vacas_Interfaz:64`
### #436 Icons/001-Weapon01 — PLACEHOLDER o RTP

- `Weapons[1].icon_name`
- `Weapons[2].icon_name`
- `Weapons[3].icon_name`
- `Weapons[4].icon_name`
### #437 Icons/002-Weapon02 — PLACEHOLDER o RTP

- `Weapons[5].icon_name`
- `Weapons[6].icon_name`
- `Weapons[7].icon_name`
- `Weapons[8].icon_name`
### #438 Icons/003-Weapon03 — PLACEHOLDER o RTP

- `Weapons[9].icon_name`
- `Weapons[10].icon_name`
- `Weapons[11].icon_name`
- `Weapons[12].icon_name`
### #439 Icons/004-Weapon04 — PLACEHOLDER o RTP

- `Weapons[13].icon_name`
- `Weapons[14].icon_name`
- `Weapons[15].icon_name`
- `Weapons[16].icon_name`
### #440 Icons/005-Weapon05 — PLACEHOLDER o RTP

- `Weapons[17].icon_name`
- `Weapons[18].icon_name`
- `Weapons[19].icon_name`
- `Weapons[20].icon_name`
### #441 Icons/006-Weapon06 — PLACEHOLDER o RTP

- `Weapons[21].icon_name`
- `Weapons[22].icon_name`
- `Weapons[23].icon_name`
- `Weapons[24].icon_name`
### #442 Icons/007-Weapon07 — PLACEHOLDER o RTP

- `Weapons[25].icon_name`
- `Weapons[26].icon_name`
- `Weapons[27].icon_name`
- `Weapons[28].icon_name`
### #443 Icons/008-Weapon08 — PLACEHOLDER o RTP

- `Weapons[29].icon_name`
- `Weapons[30].icon_name`
- `Weapons[31].icon_name`
- `Weapons[32].icon_name`
### #444 Windowskins/vacas_ventana — OK

- `Scripts[89] Vacas_Nucleo:43`
### #445 Characters/vacas_steven_mono — OK

- `Scripts[89] Vacas_Nucleo:131`
### #446 Pictures/ui_cursor — OK

- `Scripts[100] Vacas_Interfaz:93`
- `Scripts[100] Vacas_Interfaz:557`
- `Scripts: Vacas_Interfaz familia dinámica`
### #447 Pictures/ui_fog — OK

- `Scripts[100] Vacas_Interfaz:471`
- `Scripts: Vacas_Interfaz familia dinámica`
### #448 Icons/ui_nota — OK

- `Scripts[100] Vacas_Interfaz:824`
### #449 Icons/ui_objeto — OK

- `Scripts[100] Vacas_Interfaz:824`
- `Scripts[100] Vacas_Interfaz:875`
### #450 Icons/ui_bateria — OK

- `Scripts[100] Vacas_Interfaz:825`
### #451 Icons/ui_estado_2 — OK

- `Scripts[100] Vacas_Interfaz:828`
- `Scripts: Vacas_Interfaz familia dinámica`
### #452 Pictures/ui_avance — OK

- `Scripts[100] Vacas_Interfaz:1010`
- `Scripts: Vacas_Interfaz familia dinámica`
### #453 Pictures/ui_target — OK

- `Scripts[100] Vacas_Interfaz:1096`
- `Scripts: Vacas_Interfaz familia dinámica`
### #454 Pictures/feka_halo — PLACEHOLDER o RTP

- `Scripts[101] Vacas_IntroFeka:68`
- `Scripts[101] Vacas_IntroFeka:78`
### #455 Pictures/feka_logo — PLACEHOLDER o RTP

- `Scripts[101] Vacas_IntroFeka:69`
- `Scripts[101] Vacas_IntroFeka:72`
- `Scripts[101] Vacas_IntroFeka:73`
- `Scripts[101] Vacas_IntroFeka:74`
### #456 Pictures/feka_linea — PLACEHOLDER o RTP

- `Scripts[101] Vacas_IntroFeka:75`
### #457 Pictures/feka_presenta — PLACEHOLDER o RTP

- `Scripts[101] Vacas_IntroFeka:76`
### #458 Pictures/feka_gota — PLACEHOLDER o RTP

- `Scripts[101] Vacas_IntroFeka:81`
- `Scripts[101] Vacas_IntroFeka:84`
### #459 Pictures/cine_piso — OK

- `Scripts[104] Vacas_Cinematicas:5`
- `Scripts[104] Vacas_Cinematicas:8`
- `Scripts[104] Vacas_Cinematicas:11`
### #460 Pictures/cine_matadero — OK

- `Scripts[104] Vacas_Cinematicas:14`
- `Scripts[104] Vacas_Cinematicas:34`
### #461 Pictures/cine_altar — OK

- `Scripts[104] Vacas_Cinematicas:27`
### #462 Pictures/cine_ciudad — OK

- `Scripts[104] Vacas_Cinematicas:30`
- `Scripts[104] Vacas_Cinematicas:40`
- `Scripts[104] Vacas_Cinematicas:43`
### #463 Pictures/revision_luz01 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #464 Pictures/revision_luz02 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #465 Pictures/revision_luz03 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #466 Pictures/revision_luz04 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #467 Pictures/revision_luz05 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #468 Pictures/revision_luz06 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #469 Pictures/revision_luz07 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #470 Pictures/revision_luz08 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #471 Pictures/revision_luz09 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #472 Pictures/revision_luz10 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #473 Pictures/revision_luz11 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #474 Pictures/revision_luz12 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #475 Pictures/revision_luz13 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #476 Pictures/revision_luz14 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #477 Pictures/revision_luz15 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #478 Pictures/revision_luz16 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #479 Pictures/acto5_luz22 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #480 Pictures/acto5_luz23 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #481 Pictures/acto5_luz24 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #482 Pictures/acto5_luz25 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #483 Pictures/acto5_luz26 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #484 Pictures/acto5_luz27 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #485 Pictures/acto6_luz28 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #486 Pictures/acto6_luz29 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #487 Pictures/acto6_luz30 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #488 Pictures/acto6_luz31 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #489 Pictures/acto6_luz32 — PLACEHOLDER o RTP

- `Scripts: máscara del mapa`
### #490 Battlebacks/mente_piso — OK

- `Scripts: Vacas_Mente fondo dinámico`
### #491 Pictures/ui_bar_cordura — OK

- `Scripts: Vacas_Interfaz familia dinámica`
### #492 Pictures/ui_bar_vida — OK

- `Scripts: Vacas_Interfaz familia dinámica`
### #493 Pictures/ui_gameover — OK

- `Scripts: Vacas_Interfaz familia dinámica`
### #494 Pictures/ui_menu — OK

- `Scripts: Vacas_Interfaz familia dinámica`
### #495 Pictures/ui_titulo — OK

- `Scripts: Vacas_Interfaz familia dinámica`
### #496 Icons/ui_estado_3 — OK

- `Scripts: Vacas_Interfaz familia dinámica`
### #497 Icons/ui_estado_4 — OK

- `Scripts: Vacas_Interfaz familia dinámica`
### #498 Battlebacks/ui_alcantarillas — OK

- `Scripts: Vacas_Interfaz familia dinámica`
- `Scripts: Scene_Battle fondo por MAP_AUDIO`
### #499 Battlebacks/ui_camaras — OK

- `Scripts: Vacas_Interfaz familia dinámica`
- `Scripts: Scene_Battle fondo por MAP_AUDIO`
### #500 Battlebacks/ui_laboratorio — OK

- `Scripts: Vacas_Interfaz familia dinámica`
- `Scripts: Scene_Battle fondo por MAP_AUDIO`
### #501 Battlebacks/ui_manada — OK

- `Scripts: Vacas_Interfaz familia dinámica`
- `Scripts: Scene_Battle fondo por MAP_AUDIO`
### #502 Battlebacks/ui_matadero — OK

- `Scripts: Vacas_Interfaz familia dinámica`
- `Scripts: Scene_Battle fondo por MAP_AUDIO`

## Tamaños y límites

61 variantes difieren del estándar general: detalle en size_findings del JSON. Objetos, retratos 240×340 y componentes UI tienen excepciones. Madre/Cripps humanos no estándar requieren ajuste a 48 px.

Existir en RTP local no garantiza distribución autónoma. La inspección estática no prueba todas las ramas ni tiempos de animación; puntos de carga dinámica en dynamic_script_sites.
