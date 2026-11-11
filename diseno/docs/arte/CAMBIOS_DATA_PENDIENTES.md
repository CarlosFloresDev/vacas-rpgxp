# Cambios de Data pendientes — coherencia de arte

Lectura del estado actual; esta herramienta no modifica Data ni diseno/scripts. Índices de páginas/comandos entre corchetes desde cero; eventos y registros conservan su ID real.

## Integración de anclas: comprobar primero

Los PNG corregidos conservan su apoyo original: vacas 76/80, furgoneta 61/64 y muebles según índice. **No deben sumar una compensación adicional en Sprite_Character.**

No se detecta el bloque de compensaciones antiguo en la fuente actual. El verificador final comprueba los PNG directamente.

## Actores RTP de reserva

No aparecen como gráficos de eventos de mapa. Se prepararon hojas civiles propias y battlers con otros nombres. No se ha cambiado la identidad de un NPC del guion. System.party_members todavía contiene 1,2,7,8; el evento 1 del mapa 1 retira 2,7,8 con comandos129. Al limpiar las reservas, revisar también esta inicialización.

| Registro (mapa/evento: ninguno) | Original | Sustituto preparado para character_name y battler_name | Contexto visual |
|---|---|---|---|
| Actors[2] | 010-Lancer02 / 010-Lancer02 | vacas_reserva_actor02 (ambas carpetas) | obrero veterano |
| Actors[3] | 013-Warrior01 / 013-Warrior01 | vacas_reserva_actor03 (ambas carpetas) | obrero bajo |
| Actors[4] | 019-Thief04 / 019-Thief04 | vacas_reserva_actor04 (ambas carpetas) | obrera |
| Actors[5] | 022-Hunter03 / 022-Hunter03 | vacas_reserva_actor05 (ambas carpetas) | transeúnte |
| Actors[6] | 023-Gunner01 / 023-Gunner01 | vacas_reserva_actor06 (ambas carpetas) | reclutador |
| Actors[7] | 029-Cleric05 / 029-Cleric05 | vacas_reserva_actor07 (ambas carpetas) | Lucy (reserva) |
| Actors[8] | 038-Mage06 / 038-Mage06 | vacas_reserva_actor08 (ambas carpetas) | Remedios (reserva) |

Cambiar ambos campos al nombre indicado; character_hue/battler_hue deben ser0. Estos recursos están preparados; las referencias originales siguen visibles en la auditoría hasta que otra tarea integre Data.

## Bovinos: escala adulta que exige cambiar la hoja asignada

Guernsey, Junco y Muesca usan celdas48×48: una longitud adulta de62px no cabe sin cambiar la geometría. Las hojas originales conservan tamaño; variantes320×320/celdas80×80 preparadas con sufijo `_80`. Al asignarlas, conservar dirección, patrón y resto de propiedades; revisar pasos estrechos/solapes en el motor. No cambia automáticamente la colisión de un evento XP.

| Mapa | Evento | Página (editor, desde1) | Campo exacto | Sustituto |
|---|---|---|---|---|
| 18 | 5 | 1 | graphic.character_name (vacas_muesca) | vacas_muesca_80 |
| 18 | 6 | 2 | graphic.character_name (vacas_muesca) | vacas_muesca_80 |
| 19 | 4 | 1 | graphic.character_name (vacas_junco) | vacas_junco_80 |
| 19 | 7 | 2 | graphic.character_name (vacas_muesca) | vacas_muesca_80 |
| 20 | 4 | 1 | graphic.character_name (vacas_guernsey4) | vacas_guernsey4_80 |
| 20 | 5 | 1 | graphic.character_name (vacas_muesca) | vacas_muesca_80 |
| 20 | 6 | 1 | graphic.character_name (vacas_junco) | vacas_junco_80 |
| 23 | 5 | 2 | graphic.character_name (vacas_muesca) | vacas_muesca_80 |
| 23 | 5 | 3 | graphic.character_name (vacas_junco) | vacas_junco_80 |
| 26 | 10 | 2 | graphic.character_name (vacas_guernsey4) | vacas_guernsey4_80 |
| 27 | 3 | 1 | graphic.character_name (vacas_guernsey4) | vacas_guernsey4_80 |
| 27 | 3 | 2 | graphic.character_name (vacas_guernsey4) | vacas_guernsey4_80 |
| 27 | 4 | 1 | graphic.character_name (vacas_muesca) | vacas_muesca_80 |
| 27 | 5 | 2 | graphic.character_name (vacas_junco) | vacas_junco_80 |
| 28 | 6 | 1 | graphic.character_name (vacas_muesca) | vacas_muesca_80 |
| 28 | 6 | 2 | graphic.character_name (vacas_muesca) | vacas_muesca_80 |
| 29 | 6 | 1 | graphic.character_name (vacas_guernsey4) | vacas_guernsey4_80 |
| 32 | 7 | 1 | graphic.character_name (vacas_guernsey4) | vacas_guernsey4_80 |

Guernsey tras barrotes de vacas_matadero conserva su celda indexada; no sustituir toda esa hoja por un ciclo de marcha.

## Animaciones con geometría heredada

| Archivo original | Registros que lo referencian | Hoja preparada | Acción |
|---|---|---|---|
| 016-Ice01 | Animations[30].animation_name; Animations[31].animation_name; Animations[32].animation_name | vacas_rejilla_016-Ice01 | Cambiar animation_name; mantiene celdas192 y añade ancho transparente hasta960. Sigue siendo arte RTP: no considerarlo regeneración. |
| 024-Support01 | Animations[53].animation_name; Animations[54].animation_name; Animations[55].animation_name | vacas_rejilla_024-Support01 | Cambiar animation_name; mantiene celdas192 y añade ancho transparente hasta960. Sigue siendo arte RTP: no considerarlo regeneración. |

## Restricción compartida Rubio / Sierra

Map007 evento15, Map008 evento55 y Map023 evento4 comparten vacas_obrero2. Se conserva el equipo protector compatible con ambos retratos de la Biblia. Si se exige distinguirlos, preparar otra hoja de32×48 y cambiar solo graphic.character_name en las páginas del obrero de la sierra tras confirmar el rol narrativo. No se ha inventado una asignación.

## Catálogo RTP: incidencias conservadas, no aprobadas

La tabla enumera todos los PNG RTP locales con avisos y sus referencias exactas. Un registro de Tilesets/Animations/Armors no demuestra que sea alcanzable durante la partida. Los mapas actuales usan tilesets52–70, propios; no se sustituyen cincuenta atlas ajenos sin uso de mapa para silenciar el informe. Los avisos de alpha/saturación y las dos geometrías heredadas siguen pendientes en este catálogo. Antes de usar una reserva, sustituirla por arte del juego o retirar su referencia; no borrar archivos de forma indiscriminada.

| PNG | Avisos | Referencias de solo lectura |
|---|---|---|
| Graphics/Animations/001-Action01.png | RTP_original | Animations[1].animation_name; Animations[2].animation_name |
| Graphics/Animations/002-Action02.png | RTP_original | Animations[3].animation_name |
| Graphics/Animations/003-Attack01.png | RTP_original | Animations[4].animation_name; Animations[13].animation_name; Animations[14].animation_name |
| Graphics/Animations/004-Attack02.png | RTP_original | Animations[5].animation_name |
| Graphics/Animations/005-Attack03.png | RTP_original | Animations[6].animation_name |
| Graphics/Animations/006-Weapon01.png | RTP_original | Animations[7].animation_name; Animations[67].animation_name; Animations[68].animation_name; Animations[69].animation_name; Animations[70].animation_name |
| Graphics/Animations/007-Weapon02.png | RTP_original | Animations[8].animation_name; Animations[71].animation_name; Animations[72].animation_name; Animations[73].animation_name; Animations[74].animation_name |
| Graphics/Animations/008-Weapon03.png | RTP_original | Animations[9].animation_name; Animations[75].animation_name; Animations[76].animation_name; Animations[77].animation_name; Animations[78].animation_name |
| Graphics/Animations/009-Weapon04.png | RTP_original | Animations[10].animation_name; Animations[79].animation_name; Animations[80].animation_name; Animations[81].animation_name; Animations[82].animation_name |
| Graphics/Animations/010-Weapon05.png | RTP_original | Animations[11].animation_name; Animations[83].animation_name; Animations[84].animation_name; Animations[85].animation_name; Animations[86].animation_name |
| Graphics/Animations/011-Weapon06.png | RTP_original | Animations[12].animation_name; Animations[87].animation_name; Animations[88].animation_name; Animations[89].animation_name; Animations[90].animation_name |
| Graphics/Animations/012-Heal01.png | RTP_original | Animations[15].animation_name; Animations[16].animation_name; Animations[17].animation_name |
| Graphics/Animations/013-Heal02.png | RTP_original | Animations[18].animation_name; Animations[19].animation_name; Animations[20].animation_name; Animations[21].animation_name; Animations[22].animation_name |
| Graphics/Animations/014-Heal03.png | RTP_original | Animations[23].animation_name; Animations[24].animation_name; Animations[25].animation_name; Animations[26].animation_name |
| Graphics/Animations/015-Fire01.png | RTP_original | Animations[27].animation_name; Animations[28].animation_name; Animations[29].animation_name |
| Graphics/Animations/016-Ice01.png | rejilla_no_entera, geometria_animacion, RTP_original | Animations[30].animation_name; Animations[31].animation_name; Animations[32].animation_name |
| Graphics/Animations/017-Thunder01.png | RTP_original | Animations[33].animation_name; Animations[34].animation_name; Animations[35].animation_name |
| Graphics/Animations/018-Water01.png | RTP_original | Animations[36].animation_name; Animations[37].animation_name; Animations[38].animation_name |
| Graphics/Animations/019-Earth01.png | RTP_original | Animations[39].animation_name; Animations[40].animation_name; Animations[41].animation_name |
| Graphics/Animations/020-Wind01.png | RTP_original | Animations[42].animation_name; Animations[43].animation_name; Animations[44].animation_name |
| Graphics/Animations/021-Light01.png | RTP_original | Animations[45].animation_name; Animations[46].animation_name; Animations[47].animation_name |
| Graphics/Animations/022-Darkness01.png | RTP_original | Animations[48].animation_name; Animations[49].animation_name; Animations[50].animation_name |
| Graphics/Animations/023-Burst01.png | RTP_original | Animations[51].animation_name; Animations[52].animation_name |
| Graphics/Animations/024-Support01.png | rejilla_no_entera, geometria_animacion, RTP_original | Animations[53].animation_name; Animations[54].animation_name; Animations[55].animation_name |
| Graphics/Animations/025-Support02.png | RTP_original | Animations[56].animation_name; Animations[57].animation_name; Animations[58].animation_name |
| Graphics/Animations/026-Support03.png | RTP_original | Animations[59].animation_name; Animations[60].animation_name; Animations[61].animation_name; Animations[62].animation_name |
| Graphics/Animations/027-Support04.png | RTP_original | Animations[63].animation_name; Animations[64].animation_name; Animations[65].animation_name; Animations[66].animation_name |
| Graphics/Animations/028-State01.png | RTP_original | Animations[91].animation_name; Animations[92].animation_name; Animations[93].animation_name; Animations[94].animation_name; Animations[95].animation_name; Animations[96].animation_name |
| Graphics/Animations/029-Emotion01.png | RTP_original | Animations[97].animation_name; Animations[98].animation_name |
| Graphics/Animations/030-Explosion01.png | RTP_original | Animations[99].animation_name; Animations[100].animation_name |
| Graphics/Autotiles/001-G_Water01.png | RTP_original | Tilesets[1].autotile_names[0]; Tilesets[2].autotile_names[0]; Tilesets[4].autotile_names[0]; Tilesets[13].autotile_names[0]; Tilesets[15].autotile_names[0]; Tilesets[23].autotile_names[0]; Tilesets[32].autotile_names[0]; Tilesets[34].autotile_names[0]; Tilesets[35].autotile_names[0]; Tilesets[37].autotile_names[0]; Tilesets[39].autotile_names[0] |
| Graphics/Autotiles/004-G_Ground02.png | RTP_original | Tilesets[11].autotile_names[2]; Tilesets[15].autotile_names[2]; Tilesets[25].autotile_names[2]; Tilesets[28].autotile_names[2] |
| Graphics/Autotiles/007-G_Undulation01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[1].autotile_names[5]; Tilesets[4].autotile_names[3]; Tilesets[23].autotile_names[6] |
| Graphics/Autotiles/008-G_Undulation02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[1].autotile_names[6]; Tilesets[37].autotile_names[6] |
| Graphics/Autotiles/009-G2_Water01.png | RTP_original | Tilesets[3].autotile_names[0] |
| Graphics/Autotiles/010-G2_Ground01.png | RTP_original | Tilesets[3].autotile_names[1]; Tilesets[7].autotile_names[0] |
| Graphics/Autotiles/011-G2_Ground02.png | RTP_original | Tilesets[3].autotile_names[2]; Tilesets[7].autotile_names[1] |
| Graphics/Autotiles/012-G2_Swamp01.png | RTP_original | Tilesets[7].autotile_names[4] |
| Graphics/Autotiles/013-G2_Swamp02.png | RTP_original | Tilesets[7].autotile_names[5] |
| Graphics/Autotiles/014-G2_Swamp03.png | RTP_original | Tilesets[7].autotile_names[6] |
| Graphics/Autotiles/015-Sa_Water01.png | RTP_original | Tilesets[6].autotile_names[0]; Tilesets[19].autotile_names[0] |
| Graphics/Autotiles/016-Sa_Shadow01.png | RTP_original | Tilesets[5].autotile_names[4]; Tilesets[6].autotile_names[1]; Tilesets[19].autotile_names[1] |
| Graphics/Autotiles/017-Sa_Grass01.png | RTP_original | Tilesets[5].autotile_names[5]; Tilesets[6].autotile_names[2]; Tilesets[11].autotile_names[3] |
| Graphics/Autotiles/018-Sa_Ground01.png | RTP_original | Tilesets[6].autotile_names[3]; Tilesets[19].autotile_names[2] |
| Graphics/Autotiles/019-Sa_Grass02.png | RTP_original | Tilesets[6].autotile_names[4]; Tilesets[19].autotile_names[3] |
| Graphics/Autotiles/020-Sa_Grass03.png | RTP_original | Tilesets[6].autotile_names[5]; Tilesets[19].autotile_names[4] |
| Graphics/Autotiles/021-Sa_Road01.png | RTP_original | Tilesets[19].autotile_names[5] |
| Graphics/Autotiles/022-Roof01.png | RTP_original | Tilesets[19].autotile_names[6] |
| Graphics/Autotiles/023-Sa_Undulation01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[6].autotile_names[6] |
| Graphics/Autotiles/024-Ocean01.png | RTP_original | Tilesets[5].autotile_names[0] |
| Graphics/Autotiles/025-Ocean02.png | RTP_original | Tilesets[5].autotile_names[1] |
| Graphics/Autotiles/026-Ocean03.png | RTP_original | Tilesets[5].autotile_names[2] |
| Graphics/Autotiles/027-Ocean04.png | RTP_original | Tilesets[5].autotile_names[3] |
| Graphics/Autotiles/028-Sn_Water01.png | RTP_original | Tilesets[8].autotile_names[0]; Tilesets[21].autotile_names[0] |
| Graphics/Autotiles/029-Sn_Shadow01.png | RTP_original | Tilesets[8].autotile_names[1]; Tilesets[21].autotile_names[1] |
| Graphics/Autotiles/030-Sn_Ground01.png | RTP_original | Tilesets[8].autotile_names[2]; Tilesets[21].autotile_names[2] |
| Graphics/Autotiles/031-Sn_Undulation01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[8].autotile_names[4]; Tilesets[21].autotile_names[4] |
| Graphics/Autotiles/032-T_Ocean01.png | saturacion_media_mayor_055, RTP_original | Tilesets[11].autotile_names[0]; Tilesets[30].autotile_names[1] |
| Graphics/Autotiles/033-Waterfall01.png | RTP_original | Tilesets[4].autotile_names[4] |
| Graphics/Autotiles/034-Waterfall02.png | RTP_original | Tilesets[4].autotile_names[5] |
| Graphics/Autotiles/035-Waterfall03.png | RTP_original | Tilesets[4].autotile_names[6] |
| Graphics/Autotiles/036-Tree01.png | RTP_original | Tilesets[2].autotile_names[5]; Tilesets[15].autotile_names[5] |
| Graphics/Autotiles/037-Tree02.png | saturacion_media_mayor_055, RTP_original | Tilesets[2].autotile_names[6]; Tilesets[15].autotile_names[6] |
| Graphics/Autotiles/038-Tree03.png | RTP_original | Tilesets[3].autotile_names[4]; Tilesets[7].autotile_names[3]; Tilesets[35].autotile_names[6] |
| Graphics/Autotiles/039-Tree04.png | RTP_original | Tilesets[3].autotile_names[5] |
| Graphics/Autotiles/040-Ground01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[1].autotile_names[3]; Tilesets[2].autotile_names[3]; Tilesets[4].autotile_names[2]; Tilesets[13].autotile_names[4]; Tilesets[17].autotile_names[1]; Tilesets[23].autotile_names[3]; Tilesets[32].autotile_names[3]; Tilesets[34].autotile_names[4]; Tilesets[37].autotile_names[3]; Tilesets[39].autotile_names[3] |
| Graphics/Autotiles/041-Grass01.png | RTP_original | Tilesets[1].autotile_names[4]; Tilesets[11].autotile_names[4]; Tilesets[13].autotile_names[5]; Tilesets[15].autotile_names[3]; Tilesets[23].autotile_names[4]; Tilesets[32].autotile_names[4]; Tilesets[34].autotile_names[5]; Tilesets[37].autotile_names[4] |
| Graphics/Autotiles/042-Ground02.png | RTP_original | Tilesets[3].autotile_names[3]; Tilesets[7].autotile_names[2] |
| Graphics/Autotiles/043-Grass02.png | RTP_original | Tilesets[2].autotile_names[4]; Tilesets[35].autotile_names[5]; Tilesets[39].autotile_names[4] |
| Graphics/Autotiles/044-Road01.png | RTP_original | Tilesets[8].autotile_names[3]; Tilesets[13].autotile_names[6]; Tilesets[15].autotile_names[4]; Tilesets[17].autotile_names[2]; Tilesets[21].autotile_names[3]; Tilesets[23].autotile_names[5]; Tilesets[37].autotile_names[5]; Tilesets[39].autotile_names[5] |
| Graphics/Autotiles/045-Road02.png | RTP_original | Tilesets[5].autotile_names[6]; Tilesets[32].autotile_names[6] |
| Graphics/Autotiles/046-Road03.png | RTP_original | Tilesets[30].autotile_names[2] |
| Graphics/Autotiles/047-Flower01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[25].autotile_names[4]; Tilesets[28].autotile_names[5]; Tilesets[32].autotile_names[5] |
| Graphics/Autotiles/049-St_Shadow01.png | RTP_original | Tilesets[26].autotile_names[2]; Tilesets[27].autotile_names[2]; Tilesets[33].autotile_names[2]; Tilesets[36].autotile_names[4]; Tilesets[40].autotile_names[2]; Tilesets[48].autotile_names[2] |
| Graphics/Autotiles/051-Carpet01.png | saturacion_media_mayor_055, RTP_original | Tilesets[10].autotile_names[1]; Tilesets[26].autotile_names[3]; Tilesets[27].autotile_names[3]; Tilesets[29].autotile_names[1]; Tilesets[31].autotile_names[0]; Tilesets[33].autotile_names[3]; Tilesets[38].autotile_names[1]; Tilesets[42].autotile_names[1] |
| Graphics/Autotiles/054-Wall02.png | RTP_original | Tilesets[10].autotile_names[0]; Tilesets[14].autotile_names[0]; Tilesets[16].autotile_names[0]; Tilesets[22].autotile_names[0]; Tilesets[36].autotile_names[1] |
| Graphics/Autotiles/055-Wall03.png | RTP_original | Tilesets[20].autotile_names[0]; Tilesets[36].autotile_names[2] |
| Graphics/Autotiles/056-CE_Water01.png | RTP_original | Tilesets[43].autotile_names[0] |
| Graphics/Autotiles/057-CE_Shadow01.png | RTP_original | Tilesets[43].autotile_names[1] |
| Graphics/Autotiles/058-CE_Ground01.png | RTP_original | Tilesets[43].autotile_names[2] |
| Graphics/Autotiles/059-CE_Ground02.png | RTP_original | Tilesets[43].autotile_names[3] |
| Graphics/Autotiles/060-CE_Grass01.png | RTP_original | Tilesets[43].autotile_names[4] |
| Graphics/Autotiles/061-CE_Road01.png | RTP_original | Tilesets[43].autotile_names[5] |
| Graphics/Autotiles/062-CF_Lava01.png | RTP_original | Tilesets[44].autotile_names[0] |
| Graphics/Autotiles/063-CF_Shadow01.png | RTP_original | Tilesets[44].autotile_names[1] |
| Graphics/Autotiles/064-CF_Ground01.png | RTP_original | Tilesets[44].autotile_names[2] |
| Graphics/Autotiles/065-CF_Ground02.png | RTP_original | Tilesets[44].autotile_names[3] |
| Graphics/Autotiles/066-CF_Ground03.png | RTP_original | Tilesets[44].autotile_names[4] |
| Graphics/Autotiles/067-CF_Ground04.png | RTP_original | Tilesets[44].autotile_names[5] |
| Graphics/Autotiles/068-CI_Water01.png | RTP_original | Tilesets[45].autotile_names[0] |
| Graphics/Autotiles/069-CI_Shadow01.png | RTP_original | Tilesets[45].autotile_names[1] |
| Graphics/Autotiles/070-CI_Snow01.png | RTP_original | Tilesets[45].autotile_names[2] |
| Graphics/Autotiles/071-CI_Ground01.png | RTP_original | Tilesets[45].autotile_names[3] |
| Graphics/Autotiles/072-CI_Ice01.png | RTP_original | Tilesets[45].autotile_names[4] |
| Graphics/Autotiles/073-CI_Ground02.png | RTP_original | Tilesets[45].autotile_names[5] |
| Graphics/Autotiles/074-CW_Water01.png | RTP_original | Tilesets[46].autotile_names[0] |
| Graphics/Autotiles/075-CW_Shadow01.png | RTP_original | Tilesets[46].autotile_names[1] |
| Graphics/Autotiles/076-CW_Grass01.png | RTP_original | Tilesets[46].autotile_names[2] |
| Graphics/Autotiles/077-CW_Grass02.png | RTP_original | Tilesets[46].autotile_names[3] |
| Graphics/Autotiles/078-CW_Ground01.png | RTP_original | Tilesets[46].autotile_names[4] |
| Graphics/Autotiles/079-CW_Grass03.png | RTP_original | Tilesets[46].autotile_names[5] |
| Graphics/Autotiles/080-B_Ground01.png | RTP_original | Tilesets[49].autotile_names[0] |
| Graphics/Autotiles/081-B_Ground02.png | RTP_original | Tilesets[49].autotile_names[1] |
| Graphics/Battlers/010-Lancer02.png | RTP_original | Actors[2].battler_name |
| Graphics/Battlers/013-Warrior01.png | RTP_original | Actors[3].battler_name |
| Graphics/Battlers/019-Thief04.png | RTP_original | Actors[4].battler_name |
| Graphics/Battlers/022-Hunter03.png | RTP_original | Actors[5].battler_name |
| Graphics/Battlers/023-Gunner01.png | RTP_original | Actors[6].battler_name |
| Graphics/Battlers/029-Cleric05.png | RTP_original | Actors[7].battler_name |
| Graphics/Battlers/038-Mage06.png | RTP_original | Actors[8].battler_name |
| Graphics/Battlers/054-Undead04.png | RTP_original | Enemies[25].battler_name |
| Graphics/Battlers/058-Snake04.png | RTP_original | Enemies[26].battler_name |
| Graphics/Battlers/062-Aquatic04.png | RTP_original | Enemies[27].battler_name |
| Graphics/Battlers/066-Beast04.png | RTP_original | Enemies[28].battler_name |
| Graphics/Battlers/070-Goblin04.png | RTP_original | Enemies[29].battler_name |
| Graphics/Battlers/073-Bird03.png | RTP_original | Enemies[22].battler_name |
| Graphics/Battlers/074-Bird04.png | RTP_original | Enemies[30].battler_name |
| Graphics/Battlers/077-Devil03.png | RTP_original | Enemies[23].battler_name |
| Graphics/Battlers/078-Devil04.png | RTP_original | Enemies[31].battler_name |
| Graphics/Battlers/081-Angel03.png | RTP_original | Enemies[24].battler_name |
| Graphics/Battlers/082-Angel04.png | RTP_original | Enemies[32].battler_name |
| Graphics/Characters/010-Lancer02.png | RTP_original | Actors[2].character_name |
| Graphics/Characters/013-Warrior01.png | saturacion_media_mayor_055, RTP_original | Actors[3].character_name |
| Graphics/Characters/019-Thief04.png | saturacion_media_mayor_055, RTP_original | Actors[4].character_name |
| Graphics/Characters/022-Hunter03.png | RTP_original | Actors[5].character_name |
| Graphics/Characters/023-Gunner01.png | RTP_original | Actors[6].character_name |
| Graphics/Characters/029-Cleric05.png | RTP_original | Actors[7].character_name |
| Graphics/Characters/038-Mage06.png | RTP_original | Actors[8].character_name |
| Graphics/Icons/001-Weapon01.png | RTP_original | Weapons[1].icon_name; Weapons[2].icon_name; Weapons[3].icon_name; Weapons[4].icon_name |
| Graphics/Icons/002-Weapon02.png | RTP_original | Weapons[5].icon_name; Weapons[6].icon_name; Weapons[7].icon_name; Weapons[8].icon_name |
| Graphics/Icons/003-Weapon03.png | RTP_original | Weapons[9].icon_name; Weapons[10].icon_name; Weapons[11].icon_name; Weapons[12].icon_name |
| Graphics/Icons/004-Weapon04.png | RTP_original | Weapons[13].icon_name; Weapons[14].icon_name; Weapons[15].icon_name; Weapons[16].icon_name |
| Graphics/Icons/005-Weapon05.png | RTP_original | Weapons[17].icon_name; Weapons[18].icon_name; Weapons[19].icon_name; Weapons[20].icon_name |
| Graphics/Icons/006-Weapon06.png | RTP_original | Weapons[21].icon_name; Weapons[22].icon_name; Weapons[23].icon_name; Weapons[24].icon_name |
| Graphics/Icons/007-Weapon07.png | RTP_original | Weapons[25].icon_name; Weapons[26].icon_name; Weapons[27].icon_name; Weapons[28].icon_name |
| Graphics/Icons/008-Weapon08.png | RTP_original | Weapons[29].icon_name; Weapons[30].icon_name; Weapons[31].icon_name; Weapons[32].icon_name |
| Graphics/Icons/009-Shield01.png | RTP_original | Armors[1].icon_name; Armors[2].icon_name; Armors[3].icon_name; Armors[4].icon_name |
| Graphics/Icons/010-Head01.png | RTP_original | Armors[5].icon_name; Armors[6].icon_name; Armors[7].icon_name; Armors[8].icon_name |
| Graphics/Icons/011-Head02.png | RTP_original | Armors[9].icon_name; Armors[10].icon_name; Armors[11].icon_name; Armors[12].icon_name |
| Graphics/Icons/013-Body01.png | RTP_original | Armors[13].icon_name; Armors[14].icon_name; Armors[15].icon_name; Armors[16].icon_name |
| Graphics/Icons/014-Body02.png | RTP_original | Armors[17].icon_name; Armors[18].icon_name; Armors[19].icon_name; Armors[20].icon_name |
| Graphics/Icons/015-Body03.png | RTP_original | Armors[21].icon_name; Armors[22].icon_name; Armors[23].icon_name; Armors[24].icon_name |
| Graphics/Icons/016-Accessory01.png | RTP_original | Armors[25].icon_name; Armors[26].icon_name; Armors[27].icon_name; Armors[28].icon_name; Armors[29].icon_name; Armors[30].icon_name; Armors[31].icon_name; Armors[32].icon_name |
| Graphics/Icons/044-Skill01.png | RTP_original | Skills[7].icon_name; Skills[8].icon_name; Skills[9].icon_name; Skills[10].icon_name; Skills[11].icon_name; Skills[12].icon_name; Skills[13].icon_name; Skills[14].icon_name; Skills[15].icon_name; Skills[16].icon_name; Skills[17].icon_name; Skills[18].icon_name; Skills[19].icon_name; Skills[20].icon_name; Skills[21].icon_name; Skills[22].icon_name; Skills[23].icon_name; Skills[24].icon_name; Skills[25].icon_name; Skills[26].icon_name; Skills[27].icon_name; Skills[28].icon_name; Skills[29].icon_name; Skills[30].icon_name; Skills[31].icon_name; Skills[32].icon_name |
| Graphics/Icons/045-Skill02.png | RTP_original | Skills[1].icon_name; Skills[2].icon_name; Skills[3].icon_name; Skills[4].icon_name; Skills[5].icon_name; Skills[6].icon_name |
| Graphics/Icons/046-Skill03.png | RTP_original | Skills[33].icon_name; Skills[34].icon_name; Skills[35].icon_name; Skills[36].icon_name; Skills[37].icon_name; Skills[38].icon_name; Skills[39].icon_name; Skills[40].icon_name; Skills[41].icon_name; Skills[42].icon_name; Skills[43].icon_name; Skills[44].icon_name |
| Graphics/Icons/047-Skill04.png | saturacion_media_mayor_055, RTP_original | Skills[45].icon_name; Skills[46].icon_name; Skills[47].icon_name; Skills[48].icon_name; Skills[49].icon_name; Skills[50].icon_name; Skills[51].icon_name; Skills[52].icon_name |
| Graphics/Icons/048-Skill05.png | saturacion_media_mayor_055, RTP_original | Skills[53].icon_name; Skills[54].icon_name; Skills[55].icon_name; Skills[56].icon_name |
| Graphics/Icons/050-Skill07.png | RTP_original | Skills[57].icon_name; Skills[58].icon_name; Skills[59].icon_name; Skills[60].icon_name; Skills[71].icon_name; Skills[72].icon_name; Skills[73].icon_name; Skills[74].icon_name; Skills[75].icon_name; Skills[76].icon_name; Skills[77].icon_name; Skills[78].icon_name; Skills[79].icon_name; Skills[80].icon_name |
| Graphics/Tilesets/001-Grassland01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[1].tileset_name |
| Graphics/Tilesets/002-Woods01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[2].tileset_name |
| Graphics/Tilesets/003-Forest01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[3].tileset_name |
| Graphics/Tilesets/004-Mountain01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[4].tileset_name |
| Graphics/Tilesets/005-Beach01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[5].tileset_name |
| Graphics/Tilesets/006-Desert01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[6].tileset_name |
| Graphics/Tilesets/007-Swamp01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[7].tileset_name |
| Graphics/Tilesets/008-Snowfield01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[8].tileset_name |
| Graphics/Tilesets/009-CastleTown01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[9].tileset_name |
| Graphics/Tilesets/010-CastleTown02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[10].tileset_name |
| Graphics/Tilesets/011-PortTown01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[11].tileset_name |
| Graphics/Tilesets/012-PortTown02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[12].tileset_name |
| Graphics/Tilesets/013-PostTown01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[13].tileset_name |
| Graphics/Tilesets/014-PostTown02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[14].tileset_name |
| Graphics/Tilesets/015-ForestTown01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[15].tileset_name |
| Graphics/Tilesets/016-ForestTown02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[16].tileset_name |
| Graphics/Tilesets/017-MineTown01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[17].tileset_name |
| Graphics/Tilesets/018-MineTown02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[18].tileset_name |
| Graphics/Tilesets/019-DesertTown01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[19].tileset_name |
| Graphics/Tilesets/020-DesertTown02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[20].tileset_name |
| Graphics/Tilesets/021-SnowTown01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[21].tileset_name |
| Graphics/Tilesets/022-SnowTown02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[22].tileset_name |
| Graphics/Tilesets/023-FarmVillage01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[23].tileset_name |
| Graphics/Tilesets/024-FarmVillage02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[24].tileset_name |
| Graphics/Tilesets/025-Castle01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[25].tileset_name |
| Graphics/Tilesets/026-Castle02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[26].tileset_name |
| Graphics/Tilesets/027-Castle03.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[27].tileset_name |
| Graphics/Tilesets/028-Church01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[28].tileset_name |
| Graphics/Tilesets/029-Church02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[29].tileset_name |
| Graphics/Tilesets/030-Ship01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[30].tileset_name |
| Graphics/Tilesets/031-Ship02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[31].tileset_name |
| Graphics/Tilesets/032-Heaven01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[32].tileset_name |
| Graphics/Tilesets/033-Heaven02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[33].tileset_name |
| Graphics/Tilesets/034-Bridge01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[34].tileset_name |
| Graphics/Tilesets/035-Ruins01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[35].tileset_name |
| Graphics/Tilesets/036-Shop01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[36].tileset_name |
| Graphics/Tilesets/037-Fort01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[37].tileset_name |
| Graphics/Tilesets/038-Fort02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[38].tileset_name |
| Graphics/Tilesets/039-Tower01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[39].tileset_name |
| Graphics/Tilesets/040-Tower02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[40].tileset_name |
| Graphics/Tilesets/041-EvilCastle01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[41].tileset_name |
| Graphics/Tilesets/042-EvilCastle02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[42].tileset_name |
| Graphics/Tilesets/043-Cave01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[43].tileset_name |
| Graphics/Tilesets/044-Cave02.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[44].tileset_name |
| Graphics/Tilesets/045-Cave03.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[45].tileset_name |
| Graphics/Tilesets/046-Cave04.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[46].tileset_name |
| Graphics/Tilesets/047-Mine01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[47].tileset_name |
| Graphics/Tilesets/048-Sewer01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[48].tileset_name |
| Graphics/Tilesets/049-InnerBody01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[49].tileset_name |
| Graphics/Tilesets/050-DarkSpace01.png | alpha_parcial_en_pixel_art, RTP_original | Tilesets[50].tileset_name |
| Graphics/Transitions/003-Blind03.png | RTP_original | Sin referencia literal detectada |

Los panoramas RTP y battlebacks de reservas que solo existen en el RTP externo no son PNG locales y no se incluyen en la medición de Graphics. Sus cadenas están en coherencia_usos.json. No hay panoramas locales que corregir.

185-Light02 ya es una lámpara propia regenerada en la pasada de mapas; su nombre heredado NO la convierte en RTP. No requiere renombrarla. vacas_luz_escalera es un alias preparado y no asignado; no hace falta un cambio de Data por motivos de autoría.
