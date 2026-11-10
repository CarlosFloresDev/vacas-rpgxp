# Cinemáticas — fases 4 y 5

> **Arte actualizado (10-11-2026):** cine_piso, cine_matadero, cine_ciudad y cine_altar son ahora cuatro placas originales image_gen, adaptadas a640×480. Los renders de mapas de la implementación original se conservaron en el respaldo. No ejecutar b_cine_render.json para reemplazarlas: destruiría el acabado nuevo. Escenas, música, saltos y tiempos no cambian. Fuentes/prompts/manifiesto: arte_hd2d/arte_final/.

Implementación del 10 de noviembre de 2026. RGSS1 / Ruby 1.8, 640×480.
Texto nuevo en español. No se incorporan citas de la novela ni escenas sexuales.

## Instalación y recursos

Nueva sección **Vacas_Cinematicas**, fuente [15_cinematicas.rb](scripts/15_cinematicas.rb),
inmediatamente antes de Main. Reutiliza `RPG::Cache.picture`, los retratos VN,
`Vacas_Audio`, los fondos y las escenas FIN/créditos del VI. No necesita GPU.
Las capturas `Graphics/Pictures/cine_piso.png`, `cine_matadero.png`,
`cine_altar.png` y `cine_ciudad.png` se renderizan desde los mapas **2, 5, 32 y 29**
con `rx.mjs` / `render_map`, sin eventos, cuadrícula ni marcadores del editor.
`b_cine_render.json` permite regenerarlas si cambia el arte de esos mapas.

Solo cambia `Data/Scripts.rxdata`. Respaldo inicial:
[respaldos/antes_fase45/Data/Scripts.rxdata](respaldos/antes_fase45/Data/Scripts.rxdata).
El instalador [instalar_fase45.mjs](herramientas/instalar_fase45.mjs) reutiliza
el formato Marshal y el criterio de inserción del instalador de interfaz.
Conserva IDs, Main y todas las secciones anteriores salvo el ajuste de corte
documentado en [REPASO_FINAL.md](REPASO_FINAL.md).

## Apertura

`Scene_Title#command_new_game` llama primero a toda la cadena existente.
En una nueva partida normal, su destino `Scene_Map` se conserva y se envuelve
con `Scene_VacasCine`. Después vuelve al mapa **1**, cuyo prólogo original sigue
activando la partida y transfiriendo al piso **2**. Saltar nunca omite esa preparación.

| Plano | Duración | Tratamiento |
|---|---:|---|
| Steven | 13 s | Piso, retrato neutral y presentación sobria. |
| El piso | 14 s | Casa sin figuras, paneo lento sobre habitaciones. |
| Madre | 12 s | Mismo espacio, retrato neutral; amenaza mediante texto y reloj. |
| Matadero al otro lado de la calle | 15 s | Fachada del mapa 5, paneo, lluvia y tema de exploración del matadero. |

**54 segundos** de secuencia a la frecuencia configurada del motor, más la
transición inicial. Cada plano tiene entrada/salida de un segundo, tono frío,
encuadre ampliado y desplazamiento suave. Música segura y reloj en el hogar;
música del matadero y lluvia en el último plano. No se añade un screamer.

Mantener **Z/Intro un segundo**, después de soltar la confirmación de entrada,
salta toda la secuencia. **Esc** abre un menú: continuar o saltar; Esc vuelve a
la película. El menú pausa la duración. Saltar aplica un fundido de 12 frames.
La confirmación usada para abrir Nueva partida no provoca un salto accidental.

## Entre actos

`Scene_FinActo` muestra una tarjeta de seis segundos y llama al mismo
`Vacas.empezar_actoN` que usaba antes. Son automáticas y comparten el salto y menú.

| Entrada | Título | Frase original | Ambiente |
|---|---|---|---|
| I → II | Acto II — La cadena | El reloj de la casa se convierte en sirena. | Cadenas |
| II → III | Acto III — Lucy | Alguien pregunta por lo que no se ve. | Reloj |
| III → IV | Acto IV — Bajo la ciudad | El agua conserva los nombres borrados. | Eco |
| IV → V | Acto V — La matanza | Esta noche, nadie quiere ocupar su puesto. | Cadenas |
| V → VI | Acto VI — Rey-dios | Todo camino de vuelta exige una respuesta. | Eco |

Las entradas físicas que llaman directamente a `empezar_actoN` también funcionan:
al activar por primera vez el switch del acto, dejan una tarjeta pendiente en
`Game_Temp`. `Scene_Map#update` espera a terminar mensaje, intérprete y transferencia
antes de mostrarla. La tarjeta no se guarda en disco. `Scene_FinActo` consume su
propia petición para evitar duplicados. Reentrar en un acto activo no la repite.

**Shift, Ctrl, Alt, Q, Q+W y Ctrl+W** conservan sus entradas originales; la cadena
del título limpia las peticiones de tarjetas creadas por los preparadores de prueba.
Ctrl+W conserva el selector de finales y su variante con Shift.

## Tres finales

Se conserva el epílogo VN de cada rama. Antes del `Scene_FinalVacas#main` original
se reproducen **dos planos de 7 y 6 segundos**, con los mismos controles de salto:

| Rama | Planos y sonido |
|---|---|
| 160 / Rey | Altar con la Guernsey, pausa ante el asiento; ciudad, drone y lluvia. |
| 161 / Ganado | Matadero y golpe de cadena; segundo plano completamente negro: puerta cerrada, solo motor. No se representa el golpe ni la muerte. |
| 162 / Huida | Ciudad con retrato de Perro; ciudad vacía, pasos sugeridos por el texto, tema seguro y lluvia. |

Después: **FIN de la rama → créditos completos → título**. Se conservan los
12 segundos de FIN, su avance con Z/Intro, los créditos automáticos, Z para
acelerarlos y Esc para volver al título. Los fundidos nativos entre esas escenas
siguen activos. La persistencia de finales 188–191 / variable 68 no cambia.

## Estado compartido y comprobaciones

Los planos usan sprites propios con bitmaps de Pictures; no ocupan las Pictures
de `Game_Screen`, incluida **98**, reservada para sustos. El tono se aplica al
sprite de la captura, sin modificar el tono del mapa. Durante la película no se
actualizan intérpretes, veneno, perseguidores ni temporizadores del mapa.
No se altera inventario, posiciones o decisiones. Al volver directamente al mapa,
se detienen los canales fundidos y se reaplica su BGM/BGS; así la caché de audio
no conserva como activa una pista que estaba desapareciendo.

No se incorpora «anteriormente» al cargar: era opcional y se conserva la carga
existente sin añadir una espera a los guardados.

La apertura completa, menú, salto y atajos se ejecutaron en **RGSS nativo**.
El arnés se detuvo después en una ruta forzada del Acto I; los finales nuevos y
la continuidad completa se verificaron después mediante simulación de lógica.
Detalles, límites y comandos en [REPASO_FINAL.md](REPASO_FINAL.md).

Pendiente humano: encuadres y ritmo, lectura de frases y menú, mezcla de las
transiciones, tono del cierre de Ganado y una pasada de las tres ramas en el motor.
