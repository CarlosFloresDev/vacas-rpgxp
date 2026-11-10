# Sistemas de Vacas: Actos I, II, III y IV

Actualización del 8 de noviembre de 2026. RGSS1 / Ruby 1.8, resolución 640×480. Diálogos originales en castellano; el contenido sexual permanece fuera de campo. Estos sistemas sustituyen la decisión inicial de prescindir del combate clásico.

## Accesos corregidos

- **Perro, mapa 2:** la tele estaba en **(6,17)**. El hueco del salón ocupa (6,14–16); al terminarlo, el evento de la tele, con gráfico y `through=false`, cerraba el único acceso. Los tiles 388 y la alfombra 116 eran transitables; las prioridades, incluido tile 0 con prioridad 5, eran correctas. Se mueve la tele a **(8,17)**. No se habilitan paredes ni muebles para atravesarlos.
- **Vestíbulo, mapa 5:** Cripps en (24,3) tapaba el único lugar desde el que leer la puerta/cartel de la cadena (24,2), durante fase 2. Se coloca en **(23,3)** y su ruta de presentación termina allí. La entrada real sigue pasando por el vestuario y exige el mono.
- **Partidas anteriores:** `Vacas_Accesos` renueva en memoria el mapa almacenado al cargar una partida anterior a esta versión. Conserva posición del jugador, objetos, variables e interruptores, incluidos los locales. Las posiciones transitorias de los NPC se reconstruyen desde el mapa. Aprende las cuatro técnicas de Steven y elimina las técnicas RTP anteriores. No escribe el archivo de guardado. Esto evita que una partida antigua conserve la tele obstruyendo el salón.

Auditoría: mapas 1–11; pasajes direccionales de ambas casillas, tres capas, prioridades, eventos con gráfico y páginas activas. **78 escenarios**, **2.134 comprobaciones de puertas**, **1.635 destinos**, sin problemas pendientes. Incluye las puertas interiores del piso y de los corrales. Las puertas en tiles de pared funcionan mediante el contacto frontal nativo de XP; no necesitan convertirse en suelo. Los destinos sobre cama, armario y bañera son posiciones temporales de escenas, sin devolver allí el control: se documentan como excepciones justificadas, sin volver transitables esos objetos. Detalle reproducible en `auditoria_accesos.json`.

## Diálogo con retratos

Fuente: `scripts/06_vn.rb`, sección `Vacas_VN` justo antes de Main. Conserva los comandos 101/401 y las opciones nativas de XP, sus ramas y cancelaciones. Busto transparente 240×340, izquierda o derecha; placa de nombre; windowskin oscura semitransparente; texto letra a letra, un glifo cada dos fotogramas. Intro/espacio revela y una segunda pulsación avanza. Mantener Mayús revela el texto. Las opciones se activan al terminar de revelarse: revelar nunca confirma una decisión.

En **Mostrar texto**, escribir:

```
\P[steven_miedo]\L\D[1]\NOMBRE[Steven]No voy a mirar otra vez.
```

- `\P[personaje_expresion]`: carga `Graphics/Pictures/retrato_personaje_expresion.png`.
- `\L` / `\R`: lado del busto.
- `\NOMBRE[Nombre visible]`: placa independiente del cuerpo del texto.
- `\D[1]`: atenuación del fondo; `\D[0]`: sin atenuación.
- `\c[n]`, `\v[n]`, `\n[n]`, opciones y entrada numérica siguen funcionando. La entrada numérica usa la presentación nativa, sin escritura progresiva.
- Cambiar `\P` en la siguiente caja cambia la expresión. Los metadatos duran una caja y se limpian al terminar. El bitmap de caché del retrato no se destruye; los bitmaps propios sí.

`ev.T()` selecciona el hablante, lado y expresión desde `vn_textos.py`; retira del cuerpo los antiguos nombres coloreados. Los pensamientos llevan a Steven; las descripciones de Perro pueden mostrarlo sin atribuirle habla humana. Madre y Cripps alternan neutral/ira; Steven y Perro, neutral/miedo; Lucy y Guernsey tienen susurro. El narrador mantiene la caja y la escritura progresiva sin busto. Se regeneraron ambos actos y las notas: 1.051 cajas en mapas, eventos comunes y tropas; 350 incorporan retrato explícito, contando copias entre páginas.

## Combate mental por turnos

Fuente: `scripts/07_mente.rb`, sección `Vacas_Mente`. Se conserva `Scene_Battle` frontal de XP: acciones, selección de objetivo, turnos, huida y resultados. Vocabulario y mensajes de combate en español; fondos propios oscuros y música RTP `036-Dungeon02` grave. La etiqueta inglesa interna de críticos no se presenta; el multiplicador de daño se conserva. Las derrotas de estas visiones no causan el game over de la historia.

Steven empieza con **360 de salud**, **80 de aliento**, un **Tubo oxidado** y **Ropa de trabajo**. Las visiones no conceden dinero ni experiencia: no alteran el sueldo ni permiten subir niveles repitiendo encuentros. El menú de exploración sigue siendo el de terror; los recursos se eligen dentro del combate.

| Técnica | Coste | Uso |
|---|---:|---|
| Respirar (61) | 0 | Cura con potencia base 70, devuelve 18 de aliento, elimina los tres estados y baja 6 de veneno. Escala con voluntad. |
| Poner nombre (62) | 8 | Daño mental fiable; permite responder al Asco sin depender del ataque físico. |
| Aferrarse a Perro (63) | 12 | Curación base 140 y limpieza de estados. |
| Romper el reflejo (64) | 14 | Ataque fuerte que puede causar Pánico al enemigo. |

Antes de cada visión se asegura al menos el 75% de salud y aliento; las escenas preparadas restauran por completo. Al salir se recupera al grupo y se eliminan los estados. La derrota añade 8 de veneno; ganar baja 5. Los encuentros normales se dan por afrontados incluso al perder; **el Rey exige ganar y ofrece reintento automático con recursos completos**.

| Estado | Efecto |
|---|---|
| Pánico (2) | Reflejos al 75%, acierto físico al 85%. |
| Asco (3) | Ataque al 75%. |
| Culpa (4) | Voluntad al 75%; añade un punto extra al incremento de veneno por ronda. |

Duran al menos dos turnos y después pueden desaparecer con probabilidad del 60%; Respirar los limpia. No paralizan ni obligan a atacar aliados. Cada ronda adicional sube 1 de veneno (2 con Culpa); las técnicas enemigas suben otros 3–7. Se respeta la huella y se limita el incremento de combate a 96: los riesgos narrativos de llegar a 100 siguen existiendo fuera de las visiones.

### Enemigos y tropas

IDs 1–9 para enemigos y tropas; técnicas enemigas 65–70. `ENEMIGOS.json` conserva las fichas de datos. Son alucinaciones de Steven, no combates literales con los personajes.

| ID | Enemigo | Salud | Técnica / estado | Sentido y aparición |
|---:|---|---:|---|---|
| 1 | La Vaca que habla | 160 | Mugido interior / Pánico | La voz que no sabe reconocer. Opcional al examinar vacas con veneno ≥35. |
| 2 | La Madre de yeso | 220 | Orden de madre / Culpa | Deudas y obediencia. Sueño del Acto I, antes de comenzar el temporizador de búsqueda. |
| 3 | Lo del túnel | 240 | Hedor del túnel / Asco | Lo enterrado que espera. Segundo sueño del Acto II y encuentros del pasillo. |
| 4 | Sombra de Cripps | 280 | Tu mano en la suya / Culpa | El control que permanece sin el capataz. Foto de la oficina y encuentros de cámaras. |
| 5 | Enjambre de moscas | 125 | Zumbido / Asco | Pensamientos diminutos insistentes. Desagüe del vestuario y encuentros de cadena. |
| 6 | Guernsey de humo | 300 | Mugido interior / Pánico | Una promesa que acusa. Trampilla tras pactar, y encuentros del pasillo. |
| 7 | Canal en el gancho | 260 | Hedor del túnel / Asco | Miedo a ocupar el gancho. Primer sueño del Acto II, canales y encuentros industriales. |
| 8 | La Familia de nieve | 180 | Orden de madre / Culpa | La tele deja de proteger. Opcional al verla de noche, una vez. |
| 9 | El Rey del cajón | 650 | Coronación / Pánico y Culpa | Steven reflejado como verdugo; prioriza Coronación por debajo del 50% de salud. Jefe al acostarse tras Lucy y el tercer sueldo, antes del fin del Acto II. |

**Encuentros aleatorios:** mapas 8, 9 y 11, solo con mono y veneno ≥35; como máximo dos por turno, con separación de 45–173 pasos. Se pausan durante patrullas, escondites y eventos. No hay encuentros aleatorios en casa, la calle ni durante la persecución de madre. Se usa la lista de encuentros del motor mediante un filtro en `Game_Map`; no se alteran los tiles ni se añaden mapas.

**Añadir una visión desde el generador:** `battle(tropa, interruptor)` / `optional(tropa, interruptor)` de `contenido_sistemas.py`. En un evento manual: Llamar script `preparar_mente`, después Procesar batalla con la tropa correspondiente y «continuar incluso si pierde». El comando 301 de XP lleva `[tropa, permitir_huida, permitir_derrota]`, sin el parámetro de designación de motores posteriores. El resultado queda en variable 18: 0 victoria, 1 huida, 2 derrota.

## Sustos

En un evento del mapa, **Llamar script: `susto(1)`**. IDs válidos 1–7. Cada uno se dispara una sola vez por partida mediante interruptores 61–67. Muestra la imagen 98, reproduce `092-Attack04` del RTP a volumen 100 y tono 65, añade flash y temblor, espera 24 fotogramas y borra la imagen. El contador pertenece a `Game_Screen`, continúa con el intérprete esperando y se serializa con el resto de la pantalla. Reservar **imagen 98** para este sistema; se invoca fuera del combate.

| ID | Momento |
|---:|---|
| 1 | Al abrir el espejo para recoger el jarabe. |
| 2 | Primera visión de los cuernos en la tele nocturna. |
| 3 | Golpe dentro del camión de ganado. |
| 4 | Desagüe del vestuario, después de ponerse el mono. |
| 5 | Primer acercamiento y charla de la rejilla. |
| 6 | Escrito en la escarcha o foto de la oficina: comparten marca, solo ocurre uno. |
| 7 | Reflejo coronado, justo antes del jefe final del Acto II. |

Los puntos opcionales pueden omitirse; explorar ambos actos permite encontrar los siete. No aparecen por temporizador aleatorio. El susto del espejo no inicia la persecución, y el del jefe termina antes de abrir la batalla.

## Atmósfera y secreto

Se conservan tonos, niebla y sonidos de los actos originales. El combate guarda y restaura el tono del mapa: una escena de sueño con pantalla negra no vuelve invisible la batalla. Se añade un dibujo escondido en el libro infantil de Steven: una puerta abierta y Perro. Encontrarlo una vez baja 5 de veneno (interruptor 53).

## Datos reservados y mantenimiento

### Ampliación del Acto III (9-11-2026)

Implementación y recorrido: [ACTO_III.md](ACTO_III.md). Los rangos anteriores permanecen intactos. Nuevos datos después del máximo reservado anterior (80 interruptores, variable 18, objeto 13):

| Interruptor | Uso |
|---|---|
| 81–86 | Acto activo; introducción; encargo; hígado; riñón; material de Elena |
| 87, 89 | Reservados para A3; sin uso actual |
| 88 | Resultados comparados y quiebre de Lucy |
| 90–91 | Persecución de la persiana activa; depósito superado |
| 92–95 | Tarro, Factura y Camilla afrontados; Diagnóstico vencido |
| 96–97 | Elección futura: quedarse con Lucy / llevar pruebas abajo. Mutuamente excluyentes |
| 98 | Acto III terminado |
| 99–100 | Sustos 8 y 9 vistos; se conserva imagen 98 y duración de 24 fotogramas |
| 101–103 | Captura pendiente (paralelo → autorun); tazas compartidas; etiqueta R-0 leída |
| 104–106 | Preparaciones A, B y CONTROL hechas |
| 107 | Conversación de límites con madre hecha |

System tiene ahora **112 interruptores**; 108–112 siguen libres. Variables nuevas: **19** etapa (1–8), **20** confianza con Lucy, **21** capturas, **22** número de preparaciones (0–3), **23** elección (1 Lucy / 2 pruebas). Variable 18 mantiene el resultado mental. No se modifican habilidades ni estados existentes.

| Objeto | Nombre |
|---|---|
| 14–15 | Tarro limpio; Protocolo de Lucy |
| 16–18 | Hígado: lote 17; Riñón sin etiqueta; Sal sin abrir |
| 19–22 | Guantes limpios; Pinza de curas; Reactivo R-0; Suero limpio |
| 23–24 | Etiquetas de lotes; Protocolo de contraste |
| 25–27 | Preparación A azul; Preparación B azul; Control azul |
| 28–29 | Cuaderno de resultados; Llave del colector |

Notas **15, 23, 24, 28 y 29** se leen con **CE1**, conservando el apéndice de I/II. Dos tarros iniciales, una muestra por tarro; los tres ensayos consumen solo su muestra. Los puzles comprueban objetos reales, no solamente interruptores.

**Enemigos/tropas 10–13:** Tarro testigo (230 HP, técnica 65), Factura cosida (260, 66), Camilla vacía (300, 67), Diagnóstico (720, 70). Usan las técnicas 61–70 y estados 2–4 existentes; cero dinero/experiencia. El jefe exige victoria y permite reintento completo. No hay nuevos encuentros aleatorios.

**Mapas 12–16**, tileset **51** sin alterar pasajes. **Vacas_Lucy / scripts/09_lucy.rb** añade continuidad, tareas, migración de mapas y Ctrl + Nueva partida; Ctrl+Mayús selecciona resistencia. El fin del II continúa en III; el fin del III ofrece guardado y vuelve al título. Guardar requiere confirmación del jugador. La carga de un guardado final conserva 96/97 para Acto IV, todavía pendiente.

`lucy_tension` limita los incrementos del acto a 96 y respeta la huella. Captura o tiempo agotado conservan objetos, detienen temporizador y restauran menú/visibilidad. El descanso no borra la huella. Nueva hoja **vacas_laboratorio**: 128×256, 4×4 objetos estáticos de 32×64; fijar dirección y patrón. `vacas_elena`: 128×192, 4×4 caminata de 32×48.

**Reaplicar A3 después de regenerar eventos o scripts previos:** `node inspeccionar.mjs`, `python build_acto3.py`, `node rx.mjs --batch b_acto3.json`. Este lote instala sus páginas sin duplicar ni sustituir las páginas históricas. `ampliar_sistema3.mjs` usa el mismo codec del MCP; hacer respaldo completo de Data antes de cualquier escritura. No ejecutar `maps3.py crear` si los mapas 12–16 ya existen.

**Corrección de combate compartida:** `Vacas_Mente` restaura el tono usando `unless $vacas_tone_antes.nil?`; comparar un Tone de RGSS1 con nil mediante `!=` daba TypeError al volver de una batalla real.

**Verificación A3:** 31 rxdata; 99 scripts; 16 mapas y 67 transferencias válidas; 871 referencias sin ausencias; auditoría de seis estados en `verificacion_acto3.json`; `Game.exe` ejecuta los cuatro accesos de Nueva partida, ambas ramas y decisiones, puzles, refugio, 120 simulaciones y jefe nativo. Detalles y límites en ACTO_III.md. El informe histórico de fase 2 de arte corresponde a antes de esta ampliación autorizada de Data/scripts; la auditoría nueva de arte se guarda por separado en `arte_hd2d/acto3/verificacion.json`.

- Interruptores 45–52: visiones afrontadas; 53: secreto; 54: tutorial visto; 55: jefe vencido; 61–67: sustos vistos. System se amplió a 80 interruptores; los no usados permanecen libres.
- Variable 18: resultado de combate. No se reutilizan variables narrativas de los actos originales.
- `Vacas_Accesos`: versión 1 de migración de partidas anteriores; se almacena en `Game_System` al cargar.
- `gfx_sistemas.py` produce las imágenes y `arte_provisional.json` sin descargas ni instalaciones. Todos los archivos generados se escriben dentro de este proyecto en D:.
- `db_mente.py`, `contenido_sistemas.py` y `build_scripts.py` son repetibles sin duplicar enemigos, scripts ni eventos. No reejecutar generadores antiguos de BD después sin volver a aplicar estos sistemas.
- `rx.mjs` ahora detiene el lote también ante respuestas textuales `Error:` del MCP.

Desde `diseno/herramientas`, con el editor cerrado:

```powershell
node inspeccionar.mjs
node ampliar_sistema.mjs
python gfx_sistemas.py
python db_mente.py
node rx.mjs --batch b_mente_db.json
python build_scripts.py
node rx.mjs --batch b_sistemas_scripts.json
python build_events.py
node rx.mjs --batch b_events.json
node inspeccionar.mjs
python auditar_accesos.py
python verificar_sistemas.py
node probar_rgss.mjs
```

`ampliar_sistema.mjs` utiliza el codec Marshal y el respaldo del MCP para ampliar System, que no tiene endpoint de actualización completa. Las demás mutaciones pasan por `rx.mjs`. No hay edición manual de bytes `.rxdata`.

## Verificación y límites

- **26 archivos Data/*.rxdata**: load → dump → load en memoria con igualdad estructural, usando el codec del MCP; además Marshal de RGSS1 los carga y serializa dentro de Game.exe.
- **98 scripts** extraídos y comprobados con `D:/DevTools/ruby/rubyinstaller-3.3.6-1-x64/bin/ruby.exe -c`; definiciones cargadas también por RGSS104E real.
- `validate_connectivity`: 11 mapas, 55 transferencias, ninguna rota, huérfana o inaccesible en el grafo. La auditoría de colisiones adicional consta arriba.
- `validate_assets`: 841 referencias, ninguna rota, incluyendo comprobación del RTP en D:. `verificar_sistemas.py` comprueba además los PNG dinámicos de retratos, manifiesto de arte, habilidades, tropas, terminadores y nombres de interruptores/variables: cero errores.
- **Game.exe real**: partida nueva, 11 spritesets de mapa, 21 muestras de diálogo cubriendo los retratos usados y narrador, escritura progresiva, confirmación en dos pasos, cancelación de opciones, limpieza del susto, Respirar y estados.
- Balance: nueve enemigos × 30 semillas = 270 simulaciones, con curación, estados y daño del motor original. Todas ganadas con una estrategia sencilla. El jefe termina además una ejecución completa de `Scene_Battle` nativo y vuelve al mapa.
- Carga de `Save1.rxdata` de solo lectura: migración en memoria, tele en (8,17), técnicas actualizadas. El archivo no se modifica ni se incluye en commits; `Save*.rxdata` queda ignorado.
- `prueba_rgss.rb` se instala temporalmente como Main; `probar_rgss.mjs` restaura siempre el Main original. El arnés evita la espera de foco de `Graphics.update` y automatiza entradas/transiciones: prueba lógica, bitmaps y escenas nativas, **no certifica el aspecto final ni sustituye una partida manual completa**. No quedan ganchos de prueba activos en el juego.
- Pendiente de revisión humana: sensación de velocidad del texto, mezcla de volumen, ritmo de los sustos, composición del arte definitivo y recorrido interactivo completo.

## Arte provisional para sustituir

42 PNG de Pillow, rotulados como provisionales. Sustituir conservando nombre y dimensiones. Los bustos y battlers tienen transparencia; fondos y sustos son imágenes completas. El aspecto de la tabla es la dirección para el arte definitivo, no una promesa de detalle del boceto geométrico.

| Archivo | Aspecto previsto |
|---|---|
| `Graphics/Pictures/retrato_steven_neutral.png` | Joven exhausto, pelo oscuro, ropa gris, ojos hundidos. Expresión: neutral. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_steven_miedo.png` | Joven exhausto, pelo oscuro, ropa gris, ojos hundidos. Expresión: miedo. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_madre_neutral.png` | Figura ancha, bata mostaza, rostro dominante bajo luz de nicotina. Expresión: neutral. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_madre_ira.png` | Figura ancha, bata mostaza, rostro dominante bajo luz de nicotina. Expresión: ira. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_lucy_neutral.png` | Pelo claro recogido, bata pálida, tarro vacío y mirada inquieta. Expresión: neutral. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_lucy_susurro.png` | Pelo claro recogido, bata pálida, tarro vacío y mirada inquieta. Expresión: susurro. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_cripps_neutral.png` | Capataz corpulento, cabeza rapada, delantal de trabajo. Expresión: neutral. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_cripps_ira.png` | Capataz corpulento, cabeza rapada, delantal de trabajo. Expresión: ira. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_dog_neutral.png` | Perro mestizo tumbado, orejas caídas, mirada cálida. Expresión: neutral. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_dog_miedo.png` | Perro mestizo tumbado, orejas caídas, mirada cálida. Expresión: miedo. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_guernsey_neutral.png` | Vaca canela, cuernos curvos y un ojo castaño a través de una rejilla. Expresión: neutral. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_guernsey_susurro.png` | Vaca canela, cuernos curvos y un ojo castaño a través de una rejilla. Expresión: susurro. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_benito_neutral.png` | Obrero veterano con canas y mono gastado. Expresión: neutral. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_encarna_neutral.png` | Obrera de pelo recogido y mono blanco. Expresión: neutral. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_rubio_neutral.png` | Obrero de cabello rubio y guantes oscuros. Expresión: neutral. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_chato_neutral.png` | Obrero bajo, rostro ancho y nariz achatada. Expresión: neutral. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_sierra_neutral.png` | Obrero con máscara protectora y casco. Expresión: neutral. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_remedios_neutral.png` | Vecina anciana con pelo blanco y chal oscuro. Expresión: neutral. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_anselmo_neutral.png` | Vecino anciano con bigote gris y chaqueta. Expresión: neutral. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_molina_neutral.png` | Carnicero con bigote y delantal rojizo. Expresión: neutral. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_borracho_neutral.png` | Hombre desaliñado con abrigo y nariz roja. Expresión: neutral. Busto transparente 240×340. |
| `Graphics/Pictures/retrato_reclutador_neutral.png` | Conductor con gorra, chaqueta y carpeta de contratación. Expresión: neutral. Busto transparente 240×340. |
| `Graphics/Battlers/enemigo_vaca.png` | Cabeza bovina suspendida, lengua como cinta de tele. Silueta transparente 320×300. |
| `Graphics/Battlers/enemigo_madre.png` | Bata vacía, rostro agrietado y manos enormes. Silueta transparente 320×300. |
| `Graphics/Battlers/enemigo_tunel.png` | Forma alargada sin rostro, ojos al fondo de un conducto. Silueta transparente 320×300. |
| `Graphics/Battlers/enemigo_sombra_cripps.png` | Silueta de capataz deformada por ganchos. Silueta transparente 320×300. |
| `Graphics/Battlers/enemigo_moscas.png` | Nube de moscas formando una cara. Silueta transparente 320×300. |
| `Graphics/Battlers/enemigo_guernsey.png` | Vaca canela espectral, cuernos de tubería. Silueta transparente 320×300. |
| `Graphics/Battlers/enemigo_canal.png` | Carcasa abstracta colgada, costillas como barrotes. Silueta transparente 320×300. |
| `Graphics/Battlers/enemigo_televisor.png` | Televisor de los cincuenta con rostros de estática. Silueta transparente 320×300. |
| `Graphics/Battlers/enemigo_rey.png` | Jefe: Steven coronado con ganchos, reflejo del verdugo. Silueta transparente 320×300. |
| `Graphics/Battlers/steven_mente.png` | Steven pequeño frente a sus alucinaciones. Sustituir por figura completa 240×340. |
| `Graphics/Battlebacks/mente_piso.png` | Espacio mental de piso: perspectiva opresiva, sombras verdes/negras, luz central mínima. 640×480. |
| `Graphics/Battlebacks/mente_matadero.png` | Espacio mental de matadero: perspectiva opresiva, sombras verdes/negras, luz central mínima. 640×480. |
| `Graphics/Battlebacks/mente_tunel.png` | Espacio mental de tunel: perspectiva opresiva, sombras verdes/negras, luz central mínima. 640×480. |
| `Graphics/Pictures/screamer_1.png` | Ojo de madre al otro lado del espejo. Imagen repentina a pantalla completa 640×480. |
| `Graphics/Pictures/screamer_2.png` | Familia de televisión con bocas de estática. Imagen repentina a pantalla completa 640×480. |
| `Graphics/Pictures/screamer_3.png` | Hocico bovino pegado al cristal del camión. Imagen repentina a pantalla completa 640×480. |
| `Graphics/Pictures/screamer_4.png` | Rostro sustituido por un sumidero. Imagen repentina a pantalla completa 640×480. |
| `Graphics/Pictures/screamer_5.png` | Ojo castaño tras la rejilla. Imagen repentina a pantalla completa 640×480. |
| `Graphics/Pictures/screamer_6.png` | Sombra del capataz entre ganchos. Imagen repentina a pantalla completa 640×480. |
| `Graphics/Pictures/screamer_7.png` | Corona de ganchos sobre el reflejo de Steven. Imagen repentina a pantalla completa 640×480. |


## Acto IV: Bajo la ciudad — 9 de noviembre de 2026

Guía de recorrido, IDs y verificaciones en [ACTO_IV.md](ACTO_IV.md). Continuación sobre la instalación interrumpida; se conserva el respaldo `respaldos/antes_acto4_20261109_194935/Data/` y no se escribe en `.git`.

- **Acceso:** final del III, Lucy tras el cierre o colector del hospital 15 (22,5), con llave 29/switch 98; llegada 17 (4,11). Los eventos 15/16 usan transferencias 201 explícitas. Atajo: **Alt + Nueva partida**, confirmar con Z; añadir Mayús elige 97/pruebas, sin Mayús 96/Lucy. Se conservan decisiones previas y atajos anteriores.
- **Mapas:** 17 colector, 18 túneles, 19 canal, 20 cámara y 21 altar; 47 eventos, tileset 68, tres capas, pasarelas, agua bloqueada, tono oscuro y niebla móvil. Altar accesible desde 18 sin resolver el agua; cámara/altar son zonas seguras.
- **Linterna:** `scripts/10_bajo_ciudad.rb`, sección 99 `Vacas_BajoCiudad`, antes de Main 100. A alterna luz; S usa pila 31 (+60). Batería 0–100, -1/120 fotogramas libres; sin luz, radio mínimo y +1 veneno/240, tope 96. Pausa en mensajes, intérprete, menús, combate y mapas 20/21. Respeta veneno/huella existentes; no introduce una segunda estadística de cordura. Cinco máscaras por spriteset, liberadas al transferir. Altar recarga y reduce veneno respetando huella.
- **Manada:** reputación -3..5, inicial 0/1 según 96/97; diálogos VN de Muesca/Junco/consejo. La modifican respeto, ayuda, dinamo y pacto. Dos cazas: 18, 32 s con nicho; 19, 28 s con armario. Contacto/tiempo llevan al altar, +1 captura y +8 veneno tope 96, conservando objetos. Refugios/salidas limpian temporizador, transparencia y control.
- **Puzles:** rueda → retorno → descarga; error recuperable. Dinamo opcional: tubo → aire → campana; pista en 17 (14,5), panel 21 (12,8), recompensa única con marca 139. Tres visiones y Pastor obligatorio reintentable, usando combate mental existente. Dos sustos únicos, el primero condicionado por hostilidad.
- **IDs:** switches 113–139; variables 51 reputación, 52 batería, 53 capturas, 54 válvulas, 55 etapa y 56 reloj; objetos 30–34; enemigos/tropas 14–17; sustos 10/11, marcas 136/137 e imagen 98. Pacto 132; alternativas exclusivas 133/134; ruta V 135. Conservar también 126, variable 51, 35/36/38 y 96/97 para V–VI. FinActo 4 vuelve al título; V–VI pendientes de desarrollo.
- **Arte:** 13 PNG con fuentes/manifiesto/prompts nuevos/hashes en `arte_hd2d/acto4/`; adaptación por `adaptar_arte.py`. Cinco fuentes nuevas aceptadas de seis llamadas image_gen en nube, fuentes recuperadas y Guernsey canela aprobada. Personajes en celda 48 px; objetos pequeños 10–16 px. Siete hojas previas pasan `verificar_escala.py --permitir-data-modificada`; el auditor IV verifica cotas nuevas y reproducción exacta de los 13 assets.
- **Correcciones y pruebas:** accesos 15/16 verificables por el grafo; consulta del intérprete y recorrido de máscaras compatibles con RGSS1; recortes de filas sin fragmentos de otras poses. Auditoría: 1.210 comprobaciones/16 escenarios sin errores; 983 referencias sin ausencias; 21 mapas/84 transferencias sin errores ni avisos; 101 scripts con Ruby portable. Game.exe prueba 96/97 × ambos pactos, entradas, puzles, capturas/refugios, batería, 21 spritesets, 120 simulaciones y jefe nativo. Main restaurado.

Capturas estáticas 17–21 y `acto4_arte.png` revisadas. No incluyen tono/niebla animada. Un intento adicional de captura normal del motor agotó 55 s; quedan pendientes la revisión interactiva visual, el ritmo y la mezcla sonora. El arnés de lógica evita esperas de foco de Graphics. Ver límites y logs en ACTO_IV.md.
