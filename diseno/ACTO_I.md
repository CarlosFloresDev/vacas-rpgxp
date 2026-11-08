# Vacas: Acto I, «El piso» (prototipo jugable)

Prototipo del Acto I hecho en RPG Maker XP (RGSS1). Dura unos 20–30 minutos si se exploran los objetos.
Todo el texto es original y en castellano. No hay contenido sexual.

## 1. Arranque

1. **Aviso de contenido** (`Scene_Aviso`, en el script `Vacas_Pantallas`). Se muestra una sola vez, al abrir el juego, antes del título.
2. **Título** «VACAS / Acto I: El piso». Usa gráfico propio y comandos en castellano: Nueva partida / Continuar / Salir.
3. **Prólogo** en el mapa 1 (MAP001, pantalla negra): un narrador presenta el piso, a Steven, a la madre, a Perro y la tele. Después lleva al jugador al cuarto de Steven.

## 2. Mapas

| ID | Nombre | Tamaño | Tileset | Contenido |
|---|---|---|---|---|
| 1 | MAP001 (prólogo) | 20×15 | — (negro) | Solo el evento «Prologo» (autorun). |
| 2 | El piso | 30×22 | 18 Mine Town In | Cuarto de Steven, baño, cuarto de la madre, pasillo, salón con la tele y Perro, cocina. Salida abajo, en (14–15, 21). |
| 3 | La escalera | 20×15 | 18 Mine Town In | Rellano de la 3ª planta: puertas 3ºA/3ºB/3ºC, doña Remedios, el señor Anselmo, la escalera que sube (bloqueada, referencia a Lucy) y la que baja a la calle. |
| 4 | La calle | 40×20 | 9 Castle Town | Calle cortada con lluvia: portal del bloque, tablón con el anuncio del matadero, carnicería de Molina con toldo, borracho, transeúnte, alcantarilla, charcos y, por la mañana, la furgoneta del matadero y su reclutador. |

**Ambiente.** Cada mapa tiene un evento paralelo, «Ambiente», que fija el tono de pantalla, la niebla (`002-Clouds01`) y el sonido de fondo según la hora, y luego se borra:

- El piso: amarillo nicotina de día, azul oscuro de noche, rojizo oscuro durante la búsqueda y gris de madrugada.
- La escalera: goteo.
- La calle: lluvia, que es más suave por la mañana.

**Gráficos propios** (en `Graphics/`):

- Personajes: `vacas_steven`, `vacas_madre` (más grande que un personaje normal), `vacas_perro` y los vecinos. Son sprites del RTP desaturados.
- Muebles dibujados a mano en `vacas_muebles`: tele de los 50 (apagada, con nieve animada, carta de ajuste, silueta de vaca y pantalla roja), armario, nevera, bañera, váter, lavabo con espejo, sillón y piano tapado.
- Objetos pequeños en `vacas_cosas`: cuencos, carne, manchas, botellas, cenicero y cesta.
- Otros: `vacas_furgoneta`, `vacas_vacio` (bloqueador invisible), título, game over y windowskin oscura.

**Cambios en la base de datos.** En el tileset 18 se marcaron como impasables los muebles que se pisaban: camas, mesa, fogón, aparador, cajoneras, banco, cajas y leña.

## 3. Flujo de la historia

**Etapa 1. Despertar.** La madre grita desde su cuarto (veneno +5). Un texto de ayuda explica el indicador y el menú.

**Etapa 2. Las órdenes.** Hablar con la madre, que está en su sillón (cuarto de arriba a la derecha). Da 3 monedas, la *Lista de madre*, la *Llave del piso* y tres encargos, además de leer el tablón. Desde ese momento la puerta del piso se abre.

| Tarea | Cómo se resuelve |
|---|---|
| Jarabe | Baño → lavabo/espejo → *Jarabe de madre*. Se lo das a la madre. |
| Perro | Cocina → alacena → *Lata para perro*. El cajón de cubiertos tiene una nota: «EL ABRELATAS LO TENGO YO». En el cuarto de la madre, la cómoda tiene el *Abrelatas*, que hay que **pedírselo de rodillas** (veneno +6) o **cogerlo sin más** (golpe, veneno +10). Luego se usa con Perro (veneno −10). |
| Carne | Calle → carnicería de Molina (2 monedas) → *Carne picada*. Se la das a la madre, junto con la moneda del cambio. |
| Anuncio | Calle → tablón junto al portal → *Anuncio del matadero*. |

**Etapa 3. La cena.** Con las cuatro tareas hechas, se habla con la madre. La cena se cuenta a oscuras: ella come la carne cruda. Hay que elegir:

- **Comer**: veneno +12.
- **Negarte**: bofetada, veneno +18.

Después se burla del anuncio y ordena ir al camión a las seis.

**Etapa 4. La noche.** La puerta no se abre. La tele muestra otra cosa: nieve y una forma con cuernos. El piano suena solo una vez. Para seguir hay que acostarse en la cama de Steven.

**Etapa 5. La búsqueda (secuencia tensa).** Steven tiene una pesadilla (veneno +8). La madre se despierta acusándole de robarle dinero. Empieza un **temporizador de 30 s** visible en pantalla y «Madre cazadora» sale al pasillo y persigue al jugador (movimiento «acercarse», contacto = pillado).

Escondites posibles:

- **Armario** (cuarto de Steven) o **bañera** (baño). Son escondites seguros. La madre entra con una ruta de movimiento fija y se para delante. Entonces hay que elegir:
  - **Contener la respiración**: te salvas (veneno +8).
  - **Mirar/Asomarse**: te pilla.
- **Debajo de la cama**: es una trampa y siempre te pilla.
- **Si se acaba el tiempo** o **te toca**: te pilla.

Si te pilla: destello rojo, temblor y escena a oscuras, con **veneno +35**. Si el veneno llega a 100, hay **game over** (pantalla propia, «La Bestia te ha encontrado»). Si no, pasa a la mañana con el interruptor «pillado».

**Etapa 6. La mañana.** La madre desayuna en la cocina. Perro se despide (veneno −6). Los vecinos tienen frases nuevas. En la calle están la furgoneta del matadero y su reclutador.

**Etapa 7. La entrevista.** Tres preguntas con opciones (cambian el diálogo y se menciona por primera vez a Cripps). Steven queda contratado y sube a la furgoneta. Sigue un epílogo en texto y la pantalla **«Fin del Acto I / El piso / Continuará en el Acto II: La cadena»** (`Scene_FinActo`). Al pulsar Intro vuelve al título.

## 4. Mecánicas y scripts (`Data/Scripts.rxdata`, copia en `diseno/scripts/`)

- **`Vacas_Nucleo`**:
  - Constantes del juego.
  - Ajustes de `$data_system` en tiempo de ejecución: grupo inicial solo con Steven, título, game over, windowskin, vocabulario («monedas», «Objetos») y música del título.
  - Comandos para eventos: `subir_veneno(n)`, `bajar_veneno(n)`, `veneno_al_maximo?` y `fin_del_acto`. Todos devuelven `true` para que el intérprete no repita el comando.
- **`Vacas_Veneno`**:
  - Indicador discreto abajo a la izquierda (la palabra «veneno» y una barra fina). Late más rápido a partir de 50 y parpadea cuando sube.
  - Efectos según el valor:
    - El tono amarillea y pierde color, de forma proporcional.
    - Desde 35: temblores aleatorios.
    - Desde 55: destellos rojos.
    - Desde 75: golpes y fundidos breves a negro.
  - Los efectos se pausan mientras hay un mensaje en pantalla y con el interruptor 16.
- **`Vacas_Menu`**:
  - Menú reducido: **Objetos / Guardar / Salir**, sin batallas, estado ni equipo.
  - «Guardar» está siempre en gris y avisa: «Solo puedes guardar delante de la tele».
  - Muestra la lista de **tareas pendientes**, el lugar y las monedas.
  - Pantalla de salir y textos de guardar y cargar en castellano.
  - Las notas (lista, anuncio y foto) se leen usando el objeto, a través del evento común 1.
- **`Vacas_Pantallas`**: aviso de contenido, título, fin del acto y game over.
- **Guardado:** se desactiva al empezar (comando 134). La tele ofrece «Guardar partida», que llama a la pantalla de guardar con el comando 352.
- **La tele:** «Ver la tele» va rotando cinco programas originales y anima la pantalla (veneno −15; de noche −8). La tercera vez, la madre grita que apagues (veneno +4).

## 5. Interruptores y variables

| Interruptor | Nombre |
|---|---|
| 1 | Intro vista |
| 2 | Madre dio las ordenes |
| 3 | Perro alimentado |
| 4 | Jarabe entregado |
| 5 | Carne comprada |
| 6 | Carne entregada |
| 7 | Anuncio leido |
| 8 | Cena hecha |
| 9 | Es de noche |
| 10 | BUSQUEDA: la Bestia busca |
| 11 | BUSQUEDA: Steven escondido |
| 12 | BUSQUEDA: terminada |
| 13 | Manana del dia 2 |
| 14 | Contratado en el matadero |
| 15 | HUD veneno oculto |
| 16 | Sin efectos de veneno |
| 17 | BUSQUEDA: Steven pillado |
| 18 | Puerta del piso abierta |
| 19 | Abrelatas conseguido |
| 20 | Lata encontrada |
| 21 | BUSQUEDA: tiempo agotado |

| Variable | Nombre |
|---|---|
| 1 | Veneno (0-100). Empieza en 15 |
| 2 | Etapa de la historia (1 despertar … 7 contratado) |
| 3 | Canal de la tele (1-5) |
| 4 | Veces viendo la tele |
| 5 | Auxiliar |
| 6 | Insulto de madre (aleatorio 1-4) |

**Objetos:**

1. Lata para perro
2. Abrelatas
3. Jarabe de madre
4. Lista de madre (se lee)
5. Carne picada
6. Anuncio del matadero (se lee)
7. Llave del piso
8. Foto rascada (se lee; está en la cajonera de Steven)

**Evento común 1:** «Leer notas (objetos)».

## 6. Cómo probarlo

1. Cierra el editor si está abierto. Abre `Game.exe` (necesita el RTP Standard de RPG Maker XP instalado).
2. Recorrido rápido:
   1. Madre (órdenes).
   2. Baño (jarabe) → madre.
   3. Cocina: alacena (lata) y cajón (nota).
   4. Cómoda de la madre (abrelatas) → Perro.
   5. Salir: escalera → calle. Tablón y carnicería.
   6. Volver → madre (carne) → madre (cena).
   7. Tele: guardar.
   8. Cama → esconderse en el armario y contener la respiración.
   9. Mañana: calle → hombre del matadero → fin.
3. Para probar el game over: pide el abrelatas «sin más», niégate en la cena, no veas la tele y escóndete debajo de la cama. O sube la variable 1 con F9 (depuración, solo en prueba desde el editor).
4. En el editor:
   - Revisa la oclusión de los muebles (el render plano no la muestra).
   - Comprueba que la ruta de la madre entra bien al cuarto y al baño.
   - Ajusta el volumen de los BGS a tu gusto.

## 7. Herramientas

`diseno/herramientas/` contiene los generadores usados:

- `maps.py`: tiles.
- `ev.py` y `contenido.py`: eventos y textos.
- `build_events.py`: aplica los cambios en lote.
- `gfx_*.py`: gráficos.
- `rx.mjs`: cliente del MCP con la ruta corregida.

Para cambiar textos se edita `contenido.py`, se ejecuta `python build_events.py` y luego `node rx.mjs --batch b_events.json`. Hay que ejecutarlo desde una carpeta que contenga `rx.mjs`, `ev.py` y `contenido.py`. Los eventos se actualizan por id, en el mismo orden.


## Actualización: sistemas de noviembre de 2026

Diálogos con bustos, nombre y texto progresivo; alucinaciones por turnos, sustos y un pequeño secreto. El salón de Perro vuelve a ser accesible; Cripps deja libre la aproximación al cartel de la cadena. El Acto II añade un jefe mental al acostarse tras el tercer sueldo. La guía [SISTEMAS.md](SISTEMAS.md) documenta controles, encuentros, migración de partidas, validaciones y los 42 PNG provisionales que deben sustituirse.
