# Vacas: Acto II, «La cadena» (el matadero)

Continúa el Acto I en la misma partida: al pulsar Intro en «Fin del Acto I», Steven aparece en el patio del matadero.
Dura unos 30–40 minutos: tres turnos de trabajo y tres noches en casa.
Todo el texto es original y en castellano. No hay contenido sexual. La violencia contra los animales se sugiere con fundidos, sonido y consecuencias.

## 1. Mapas

| ID | Nombre | Tamaño | Contenido |
|---|---|---|---|
| 5 | Matadero: entrada | 30×22 | Patio con lluvia, furgoneta, camión de ganado y verja. Arriba está el vestíbulo, con la **fichadora**, el tablón de normas, Cripps (fase 2) y las puertas al vestuario y a la cadena (esta última solo tiene un cartel). |
| 6 | Matadero: vestuario | 20×15 | Taquillas (la **13** es la de Steven), bancos, fregaderos, sumidero, Encarna y el Chato. Salida a la cadena (solo con el mono). |
| 7 | Matadero: corrales | 30×20 | Manga de entrada (filas 3–4), pasillo (fila 6) y tres corrales con paja. Hay vacas que deambulan, la **vaca del fondo** (color canela, corral 3), el Rubio y la picana. |
| 8 | Matadero: la cadena | 40×24 | La sala de matanza: dos railes con ganchos y canales colgadas, dos **canales de desagüe** (autotile rojo), la **cinta** animada, el puesto de corte, el **cajón de aturdimiento** con la pistola de perno, Cripps, Benito, el obrero de la sierra y Encarna. |
| 9 | Matadero: cámaras frías | 30×20 | Tres cámaras (cuartos / vísceras / cabezas) con filas de canales heladas, un pasillo y **Cripps patrullando**. Hay escondites entre las canales y detrás de las cajas, y un mensaje en la escarcha. |
| 10 | Matadero: oficina de Cripps | 20×15 | Escritorio (el **Registro de reses**), archivadores (el **Plano del desagüe**), persiana sobre la cadena y foto. **Cripps sube y baja**. Hay escondites bajo la mesa y en el rincón. |
| 11 | Matadero: pasillo de mantenimiento | 30×15 | Tuberías, manguera, la **rejilla de ventilación** (la Guernsey) y la trampilla del colector 4 (pista para el Acto IV). |
| 2, 3 | El piso / La escalera | — | Son los mapas del Acto I, con páginas nuevas para las noches del Acto II (interruptor 27). |

**Tileset propio**: el 51, «Vacas Matadero» (`Graphics/Tilesets/vacas_matadero.png`, 64 tiles dibujados con PIL). Incluye azulejo blanco y sucio, sangre, hormigón, paja, paredes de azulejo, hormigón, frío, madera y ladrillo, vallas, taquillas, cinta, railes y ganchos, mesas de acero, archivadores, rejillas, cuchillos y lámparas.

- Autotiles: `053-Wall01`, el muro del Acto I, y `vacas_canal`, que es el canal de agua del RTP recoloreado en sangre (el desagüe; se puede pisar y tiene efecto «matorral»).
- Pasabilidad y prioridades en `gfx_acto2.tables()`. La prioridad del tile 0 es 5, como en RMXP, para que los eventos sin tile no abran paso.

**Gráficos nuevos** (`Graphics/Characters/`):

- `vacas_cripps`: Grappler del RTP, más grande, oscuro y manchado.
- `vacas_obrero1-4`: monos blanqueados con sangre.
- `vacas_steven_mono`.
- `vacas_vaca` y `vacas_vaca_canela`.
- `vacas_lucy`.
- `vacas_matadero`, una hoja de objetos:
  - fila 1: la cinta en 4 fotogramas;
  - fila 2: canales colgadas y gancho vacío;
  - fila 3: fichadora, pistola de perno, cubo y caja;
  - fila 4: la rejilla normal, con **ojo**, con **hocico** y doblada.

**Ambiente**: cada mapa tiene un evento paralelo «Ambiente» que pone el tono, el BGS y la niebla y luego se borra, como en el Acto I.

- La cadena: zumbido de máquinas (`015-Quake01` grave).
- Las cámaras: goteo y frío azulado. Hay BGM (`036-Dungeon02` grave) solo mientras Cripps patrulla.
- Los corrales: mugidos distorsionados (`070-Animal05` con el tono bajado).

## 2. Flujo

La variable 7 es el **turno** (1–3) y la 8 es la **fase**: 0 llegada · 1 fichar · 2 mono · 3+ tareas · 9 fichar la salida.

### Turno 1: la cinta

1. Llegada (autorun en el mapa 5).
2. Fichar: se recibe la **Tarjeta de fichar** (STEPHEN) y Cripps se presenta. Hay que elegir entre bajar la mirada o sostenérsela.
3. Taquilla 13: el mono de R. Mata. El gráfico de Steven cambia.
4. La cadena: el **puesto de la cinta** (19,15) lanza el **minijuego de la cinta**.
5. Cripps manda a por la manguera. En el pasillo, al cogerla, algo susurra desde la rejilla. **Charla 1** con la Guernsey: aparece un ojo.
6. Se devuelve la manguera a Cripps («¿Te ha contado algo la rejilla?»).
7. Fichar la salida. La furgoneta deja a Steven en la escalera.

### Noche (turnos 1, 2 y 3)

- Madre pide el **sueldo**. Se puede elegir:
  - **Dárselo todo**.
  - **Guardarte una moneda** (interruptor 37). Hay un tercio de probabilidad de que madre lo pille (bofetada, veneno +10, interruptor 42). La noche siguiente lo recuerda.
- Perro baja el veneno −6 una vez por noche.
- La tele funciona igual: ver la tele (programación nocturna) o **guardar**.
- La puerta del piso no se abre.
- Acostarse en la cama. Hay un sueño distinto cada noche y luego empieza el turno siguiente (`nuevo_turno`).

### Turno 2: el corte, las cámaras y la oficina

1. El **puesto de corte** (canal en (21,12)) lanza el **minijuego del corte**. Si se hacen menos de 3 cortes limpios, Cripps te guía la mano.
2. **Clasificar**: se coge una pieza al **final de la cinta** (30,15) y se lleva a su cámara: cuartos a la 1, vísceras a la 2, cabezas a la 3. Hacen falta 3 entregas. **Cripps patrulla** (interruptor 26).
3. Descanso. **Charla 2** en la rejilla (hocico): la Guernsey pide el libro de Cripps. Se abre la oficina y Cripps sube y baja (interruptor 29).
4. Oficina:
   - El escritorio da el **Registro de reses** (obligatorio).
   - El archivador da el **Plano del desagüe** (opcional).
5. **Charla 3**: Steven lee en voz alta «Lote 7. Guernsey… fuga por el colector 4. No consta». Ella le habla de **la manada de abajo** («Abajo somos muchas»), le avisa del cajón y le pide una promesa:
   - «Volveré» activa el **pacto** (interruptor 38).
6. Cripps: «Mañana te toca el cajón». Fichar la salida.

### Turno 3: la primera muerte obligada

1. Cripps: hay que traer «la del fondo».
2. Corrales, puerta del corral 3. Se elige entre **llamarla en voz baja** o **usar la picana**. La vaca entra en la manga (interruptor 41).
3. Al volver a la cadena empieza un autorun, «El cajón». Cripps, la pistola de perno y una alucinación si el veneno es ≥ 60. Hay que elegir:
   - **Apretar**: fundido a negro, perno y caída. Activa **Obedeció** (35), veneno +32 (con tope de 96) y **huella 20**.
   - **Bajar la pistola**: Cripps te fuerza el dedo y te pega. Activa **Se resistió** (36), veneno +24 y **huella 12**.
   - En los dos casos se activa el interruptor 34, **Primera muerte hecha**.
4. Steven despierta en el pasillo, junto a la rejilla. **Charla 4**: cambia según haya obedecido o resistido y según el pacto. Ella le habla de «alguien en tu escalera». Se cobra la «propina» (6).
5. Fichar la salida. En la escalera de noche, **Lucy** baja del cuarto piso:
   - presentación;
   - su teoría del dolor que se queda dentro, «como la cal en una tetera»;
   - da la **Nota de Lucy** («llama dos veces»).
6. En casa: el sueldo y madre, que nota algo («Hueles a hombre, por fin»). Se puede guardar en la tele.
7. Al acostarse: escena final y **«Fin del Acto II / La cadena / Continuará en el Acto III: Lucy»**. Luego se vuelve al título.

**Huella** (variable 15): el veneno ya no baja de ese valor. Lo hecho en el cajón se queda.

## 3. Mecánicas (script `Vacas_Matadero`, copia en `diseno/scripts/05_matadero.rb`)

- **El corte**: `minijuego_corte(rondas)`. Una cuchilla va y viene por una barra y hay que pulsar Intro sobre la franja roja.
  - La franja se estrecha y la cuchilla acelera en cada ronda.
  - Con veneno ≥ 40 la canal «respira». Con veneno ≥ 50 la cuchilla tiembla.
  - Resultado en la variable 12. Paga 4 + aciertos.
- **La cinta**: `minijuego_cinta(piezas)`. Llegan piezas por la derecha y hay que pulsar la flecha marcada cuando entran en el recuadro. La cinta acelera.
  - Resultado en la variable 12. Paga 3 + aciertos/2.
- **Clasificar**: se hace con eventos (final de la cinta y los rótulos de las cámaras, variables 13 y 14, interruptor 40). Paga 1 por entrega.
- **Vigilancia de Cripps**: los eventos llamados `Cripps vigila` ven 5 casillas en línea recta hacia donde miran y además notan al jugador pegado a ellos.
  - Las paredes y las canales colgadas tapan la vista.
  - Si te ven, se activa el interruptor 31 y un autorun «Pillado» en ese mapa. Veneno +15, frases que empeoran (variable 16), pierdes la pieza y te echa a la cadena. Con veneno 100 hay game over.
  - Solo funciona con el interruptor 26 (cámaras) o el 29 (oficina).
- **Escondites**: se pulsa Intro sobre una canal suelta o sobre unas cajas y se elige «Esconderte aquí». Steven se mete en el hueco, queda semitransparente y se activa el interruptor 30. Mientras está escondido Cripps no le ve. Cualquier dirección le saca.
- **Núcleo** (`Vacas_Nucleo`):
  - `subir_veneno_tope`, `huella`, `poner_mono`, `cobrar`, `entregar_sueldo`, `nuevo_turno`, `fase`, `perro_esta_noche?`/`perro_hecho` y `fin_del_acto2`.
  - `Vacas.empezar_acto2` encadena el fin del Acto I con el Acto II.
- **Menú**: la lista de «Pendiente» sigue el turno y la fase del Acto II.
- **Guardado**: solo en la tele del piso, igual que en el Acto I.

## 4. Interruptores y variables nuevos

| Interruptor | Nombre |
|---|---|
| 22 | A2: Acto II empezado |
| 23 | A2: En el matadero (turno) |
| 24 | A2: Fichado |
| 25 | A2: Mono puesto |
| 26 | A2: Cripps patrulla cámaras |
| 27 | A2: Noche en casa |
| 28 | A2: Sueldo entregado |
| 29 | A2: Cripps patrulla oficina |
| 30 | A2: Steven escondido |
| 31 | A2: Pillado por Cripps |
| 32 | A2: Registro cogido |
| 33 | A2: Plano cogido |
| 34 | **A2: PRIMERA MUERTE hecha** |
| 35 | **A2: Obedeció en el cajón** (rama de finales) |
| 36 | **A2: Se resistió en el cajón** (rama de finales) |
| 37 | A2: Se guardó dinero |
| 38 | **A2: Pacto con la Guernsey** (Acto IV) |
| 39 | **A2: Lucy conocida** (Acto III) |
| 40 | A2: Lleva una pieza |
| 41 | A2: Vaca del fondo en la manga |
| 42 | A2: Madre le pilló la moneda |
| 43 | A2: Tercer turno |
| 44 | A2: Manguera cogida |

| Variable | Nombre |
|---|---|
| 7 | A2: Turno (1-3) |
| 8 | A2: Fase del turno (0-9) |
| 9 | A2: Sueldo de hoy |
| 10 | A2: Sueldo total |
| 11 | A2: Charlas con la Guernsey (confianza: 5–7 al final) |
| 12 | A2: Resultado del minijuego |
| 13 | A2: Piezas clasificadas |
| 14 | A2: Pieza que lleva (1 cuartos, 2 vísceras, 3 cabezas) |
| 15 | Huella (veneno mínimo) |
| 16 | A2: Veces pillado por Cripps |
| 17 | A2: Última noche con Perro |

**Objetos nuevos**:

- 9: Tarjeta de fichar
- 10: Registro de reses
- 11: Plano del desagüe
- 12: Manguera
- 13: Nota de Lucy

Las notas (9, 10, 11 y 13) se leen desde el menú con el evento común 1, que se ha ampliado.

## 5. Cómo probarlo

1. Cierra el editor. Abre `Game.exe`.
2. **Atajo de prueba**: mantén **Mayús** al elegir «Nueva partida» y empezarás directamente en el Acto II, con los interruptores del Acto I hechos y veneno 30. Sin Mayús, la partida empieza en el Acto I y al terminarlo sigue sola.
3. Recorrido rápido:
   1. **T1**: fichadora → vestuario (taquilla 13) → cadena (cinta, en el centro) → pasillo (manguera → rejilla) → Cripps → vestuario → fichadora.
   2. **Noche**: 3ºB → madre → (tele) → cama.
   3. **T2**: fichadora → mono → corte (canal con tiza en (21,12)) → final de la cinta ↔ cámaras ×3 → pasillo (rejilla) → puerta metálica del fondo de la cadena → oficina (escritorio y archivador) → rejilla → fichadora.
   4. **Noche**.
   5. **T3**: fichadora → mono → Cripps → corrales (puerta del corral 3) → cadena (escena) → pasillo → fichadora → Lucy → madre → cama → fin.
4. Con F9 (prueba desde el editor) puedes tocar la variable 8 (fase) para saltar partes.
5. **Comprobado automáticamente** con un arnés temporal dentro de Game.exe, ya borrado:
   - todos los mapas 5–11 en 14 combinaciones de turno y fase, y las noches;
   - los dos minijuegos;
   - la vigilancia (te ve de frente y no te ve escondido);
   - la huella, el sueldo, el nuevo turno, el mono y Perro.
   - Además: `validate_connectivity` sin errores (55 transferencias) y `validate_assets` sin referencias rotas.
6. **Revisar a mano** en el juego y en el editor:
   - la dificultad de los minijuegos;
   - el ritmo de las patrullas (que se pueda pasar sin frustrar);
   - que la vaca del fondo recorra bien la manga;
   - la ruta de Lucy por la escalera;
   - la oclusión de las canales colgadas sobre Steven;
   - los volúmenes de los BGS y SE.

## 6. Herramientas

- `../../herramientas/actos/acto2/gfx_acto2.py`: tileset, autotile, personajes y objetos.
- `../../herramientas/actos/acto2/maps2.py`: crea los mapas (`crear`) y pinta los tiles (`tiles`).
- `../../herramientas/actos/acto2/contenido2.py`: los eventos del Acto II y las páginas nuevas del piso y la escalera.
- `../../herramientas/actos/acto2/db2.py`: objetos y nombres de interruptores y variables.
- `../../herramientas/actos/acto1/build_events.py`: regenera los eventos de **todos** los mapas, del 1 al 11.
- Flujo: `python build_events.py` y luego `node rx.mjs --batch b_events.json`.


## Actualización: sistemas de noviembre de 2026

Desde el 9-11-2026, confirmar el fin del Acto II continúa en la misma partida con [Acto III: Lucy](ACTO_III.md); ya no vuelve al título. Las ramas 34–36 y el pacto 38 se conservan. Ctrl + Nueva partida permite probar III; Mayús conserva el atajo de II.

Diálogos con bustos, nombre y texto progresivo; alucinaciones por turnos, sustos y un pequeño secreto. El salón de Perro vuelve a ser accesible; Cripps deja libre la aproximación al cartel de la cadena. El Acto II añade un jefe mental al acostarse tras el tercer sueldo. La guía [SISTEMAS.md](../sistemas/SISTEMAS.md) documenta controles, encuentros, migración de partidas, validaciones y los 42 PNG provisionales que deben sustituirse.
