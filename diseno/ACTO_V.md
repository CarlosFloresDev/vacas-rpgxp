# Acto V — La matanza

Construido el 10 de noviembre de 2026 sobre el final del Acto IV. Respaldo previo de todos los `Data/*.rxdata` en `respaldos/antes_acto5/Data/`. Texto original; el contenido sexual no aparece; el gore se describe y las muertes de la decisión ocurren con la pantalla en negro o fuera de plano.

## Acceso y prueba rápida

- Desde el Acto IV: la pantalla «Fin del Acto IV» ahora continúa en el Acto V (`Vacas.empezar_acto5`). En el altar (mapa 21) el evento **Paso hacia el matadero nocturno** ofrece además «Subir ya al matadero (Acto V)» con transferencia explícita a **22 (3,11)**, útil para partidas guardadas antes del cierre.
- Atajo desde el título: seleccionar **Nueva partida**, mantener **Q** (`Input::L`, también Re Pág) y confirmar con **Z**. Añadir **W** (`Input::R`) prueba el pacto de venganza (134, reputación 0); sin W prueba «nadie es ganado» (133, reputación 3, Junco liberada). Los atajos Mayús/Ctrl/Alt anteriores siguen funcionando. No sobrescribe guardados.
- Controles: flechas, Z/Intro. Sin linterna en este acto: la luz son máscaras fijas por mapa.

## Recorrido y mapas

Todos de 20×15, tileset **69** («Acto V: la matanza» = hoja del matadero + 554 baldosas de utilería troceada), con salas partidas en estancias pequeñas.

| ID | Mapa | Contenido y conexiones |
|---|---|---|
| 22 | Muelle de carga | Llegada por la rejilla (3,11). Vigilante Benito de ronda. Garita 3×2: radio (guardar), tablero con **llave del muelle** y **cizalla**, parte de turno. Dos camiones. Puerta de servicio (4,2) → 23. |
| 23 | Corrales de espera | Cinco corrales con 11 reses, vigilante Sierra en el pasillo central, aliada (Muesca, o Junco si fue liberada; reputación ≥1) que puede alejarlo, cadenas (visión **Res que cuenta** + elección de abrir), caseta con **sirena** y **orden de matanza**. Sur → 22, este → 24. |
| 24 | Sala de matanza | Manga, cajón, noria, cinta, cuarto de control con el **cuadro de la noria** (minijuego), armero con la **pistola de perno** (visión **Turno de noche**), el Rubio y el Chato (avisar / mentir / callar). Puerta del raíl (17,2) → 25 al invertir la noria. |
| 25 | Cámara de sangrado | Tres raíles con 39 canales colgadas formando laberinto. **Persecución** de Cripps, dos canales vaciadas como escondite, visión opcional **Gancho que respira**. Puerta (2,2) → 26 cuando entra la manada. |
| 26 | Oficina alta | Pasarela, antesala (radio para guardar, archivo, etiquetas de lotes) y despacho: escena con Cripps, **jefe** y **decisión**. Escalera de incendios (19,12) → 27. |
| 27 | Patio del alba | La manada libre, Guernsey (diálogo final según decisión y pacto), Muesca, Junco, obreros si fueron avisados. Cancela (9–10,13): guardar y `Scene_FinActo.new(5)`. |

103 eventos. Ruta principal: llaves en la garita → corrales (cortar sirena, decidir cadenas) → hablar o no con los obreros → invertir la noria → sobrevivir en el sangrado → Cripps → decisión → patio.

## Sistemas

`scripts/13_matanza.rb`, instalado como **Vacas_Matanza**, índice 102, antes de Main. `Vacas_Pantallas` (92) recibe el texto del acto 5 y el salto 4 → 5.

- **Infiltración y alarma (variable 57, 0–3).** Los eventos llamados `Vigia A5` ven cinco casillas en línea recta (reutiliza `vacas_ve_al_jugador?`). Ser visto, que el Chato te vea tocar el cuadro, invertir la noria sin cortar la sirena o una captura suben la alarma. Efectos: con alarma ≥2 Cripps corre a velocidad 4 en la persecución; el jefe tiene 860 + 70×alarma de vida; cambia su diálogo. Marcador en pantalla (`Sprite_Alarma`). Ser descubierto devuelve a la entrada del mapa, +4 veneno (tope 96), sin perder objetos.
- **Minijuego nuevo: La noria** (`Vacas_Noria`, variación dura de la cinta). 16 piezas cada vez más rápidas; las azules (40 %) exigen la flecha contraria. Hacen falta 10 aciertos; tras un fallo bastan 8. Resultado en la variable 12.
- **Persecución (interruptor 150).** Se dispara al cruzar la mitad de la cámara. Cripps usa búsqueda en anchura (`matanza_ruta`), no el acercamiento ciego de XP. Hay que aguantar 40 s (30 s si reputación ≥2) hasta que la manada rompe el portón. Captura: +8 veneno, +1 alarma, vuelta a la puerta; el reloj sigue. Escondites: una vez cada uno, 7 s a salvo.
- **Influencia del pacto.** 133: la Guernsey pide avisar a los obreros; la manada «rodea»; si no se avisó, los obreros se encierran y viven. 134: la manada arrasa; si no se avisó, el Rubio y el Chato mueren (171, +dominio). La reputación (variable 51) decide si hay aliada en corrales y la duración de la caza. 96/97 cambian líneas de Cripps y de las etiquetas.
- **Visiones:** 18 El Turno de noche, 19 La Res que cuenta, 20 El Gancho que respira (opcional). **Jefe:** 21 Cripps, el matarife (reintentable hasta vencer).
- **Sustos:** 12 (aparición de Cripps) y 13 (dentro de la canal), una vez cada uno.
- **Audio:** filas 22–27 añadidas a `Vacas_Audio::MAP_AUDIO`; zonas `:matadero` y `:camaras`; la música de persecución se activa con 150; efectos con `Vacas_Audio.play`.
- **Luz:** `Graphics/Pictures/acto5_luzNN.png`, sprite anclado al mapa.

## IDs y continuidad para el Acto VI

| Rango | Uso |
|---|---|
| Mapas 22–27; tileset 69 | Matadero de noche. |
| Interruptores 140–141 | Acto V activo, llegada vista. |
| 142–149 | Descubierto pendiente, vigía distraído, sirena cortada, **corrales abiertos (145)**, obreros convencidos (146), **obreros avisados (147)**, noria invertida, pistola recogida. |
| 150–152 | Caza activa, manada dentro, sangrado visto. |
| 153–158 | Visiones 19/18/20 y jefe (156) vencidos; sustos 12/13 vistos. |
| **159** | Decisión tomada. |
| **160 / 161 / 162** | Exclusivos: **Cripps entregado a la manada** / **Steven aprieta el perno** / **Cripps soltado (muere en el patio)**. |
| **163** | Acto V completo (ruta del Acto VI). |
| 164–169, 171 | Orden leída, escondites usados, escena de oficina, Guernsey del patio, noria fallada, **obreros muertos (171)**. 170 y 172–175 libres. |
| Variables 57–61 | Alarma 0–3, **Dominio 0–6 (58)**, **Piedad 0–6 (59)**, capturas, etapa 1–6. 62–64 libres. |
| Objetos 35–38 | Llave del muelle, cizalla, pistola de perno, orden de matanza. |
| Enemigos/tropas 18–21 | Tres visiones y el jefe. |

**Lectura propuesta para los tres finales del Acto VI:** 160 inclina a *Rey de la manada*; 161 a *Ganado* (Steven ocupa el sitio de Cripps y acaba en la cadena); 162 a *Huida* (pacto cumplido con patas ajenas). Matizar con Dominio (58) frente a Piedad (59), 145, 147/171, el pacto 133/134, la reputación (51), 126 y 96/97. Cripps muere en las tres ramas.

## Arte

Sin generación por IA ni GPU. La utilería (camiones, bidones, palés, noria, armero, sirena, sofá, trofeos, sangre, cables…) se dibuja con PIL en `herramientas/maps5.py` y se combina con los sprites existentes de canales, cubos y cajas. Escala: personaje 48 px; objetos de mesa 5–16 px; bidón 30, caja 32, estante 56, camión 128×64.

**Arte provisional pendiente de sustituir:**

- Battlers 18 y 21: `enemigo_sombra_cripps` (tono 190 y 0); 19: `enemigo_vaca` tono 330; 20: `enemigo_canal` tono 20.
- `screamer_12.png` y `screamer_13.png`: reencuadres tintados de `screamer_4` y `screamer_7`.
- Sin retrato de Cripps herido ni sprite de Cripps caído; los obreros reutilizan `vacas_obrero1–4`.
- La utilería procedural es más plana que el arte HD-2D de los actos previos.

Capturas (izquierda sin luz, derecha con máscara; los cuadrados azules son eventos invisibles): [lámina 1](capturas/acto5_lamina_1.png), [lámina 2](capturas/acto5_lamina_2.png), [lámina 3](capturas/acto5_lamina_3.png) y `capturas/acto5_22.png` … `acto5_27.png`.

## Verificación

- Sintaxis: 104 scripts de Scripts.rxdata con `ruby -c` (D:/DevTools/ruby), cero errores. El script evita sintaxis posterior a Ruby 1.8.
- `inspeccionar.mjs`: carga y round-trip Marshal de los 42 `.rxdata`.
- `build_acto5.py`: alcance por inundación desde las 6 entradas; todas las interacciones, toques, destinos de transferencia y recolocaciones son accesibles (cero errores).
- `herramientas/validar_conectividad5.json`: 27 mapas, 99 transferencias, cero rotas, huérfanas o inalcanzables.
- `herramientas/validar_assets5.json`: 1.024 referencias, cero ausentes.
- `verificacion_rgss_acto5.txt`: una sola ejecución de Game.exe con arnés (`probar_acto5.mjs`): atajo Q y Q+W, spritesets y audio de los seis mapas, ruta y movimiento de Cripps, topes, jefe escalado, minijuego construido, sustos, battlers y tropas. Main restaurado.

Para recompilar: `node inspeccionar.mjs` → `python maps5.py` → `node rx.mjs --batch b_tiles5.json` → `python build_acto5.py` → `node rx.mjs --batch b_acto5.json` → `python capturas5.py eventos`. No repetir `preparar_acto5.mjs` ni `b_mapas5.json` (crean los mapas).

## Pendiente y límites

- **No se ha jugado a mano.** El arnés no recorre diálogos, combates ni el minijuego en tiempo real: falta ajustar la dificultad de la noria, de la persecución y del jefe, y el ritmo de los vigilantes.
- **Duración estimada 35–50 min**, por debajo del objetivo de 60–90: haría falta un tramo más (por ejemplo cámaras frías o vestuario nocturno) o más puzles.
- El tono de pantalla y la máscara nocturna no se han valorado juntos en el motor; puede quedar demasiado oscuro o claro.
- Los escondites dependen de que el intérprete bloquee el toque de Cripps; comprobado por lógica, no jugando.
- Durante el trabajo había un `Game.exe` ajeno abierto; no se tocó. `Vacas.cfg` ya aparecía modificado y no se incluye en el commit.
- Acto VI pendiente.
