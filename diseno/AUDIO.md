# Audio de Vacas

Tabla editable: `Vacas_Audio::TABLE` en `scripts/11_interfaz.rb`. Cada entrada es
`clave => [tipo, nombre_sin_extension, volumen_base, tono, subtitulo]`.
Los nombres distinguen mayusculas en otros sistemas. Instalar los archivos en la
carpeta del tipo correspondiente. No se han descargado ni generado sonidos.

Se recomienda OGG para bucles y WAV para efectos cortos. Los nombres exactos de
la siguiente tabla usan esas extensiones; el cargador tambien reconoce MP3, MID y
WMA. Basta un archivo por nombre. La ausencia de cualquier archivo es silenciosa.

| Archivo esperado | Tipo | Uso / clave | Duracion y bucle sugeridos |
|---|---|---|---|
| `Audio/BGM/vacas_titulo.ogg` | BGM | titulo | 60–90 s, bucle sin corte |
| `Audio/BGS/vacas_menu.ogg` | BGS | pausa / menu | 20–40 s, bucle tenue |
| `Audio/BGS/vacas_piso.ogg` | BGS | piso y calle / piso | 45–90 s, bucle |
| `Audio/BGS/vacas_matadero.ogg` | BGS | zona industrial / matadero | 45–90 s, bucle |
| `Audio/BGS/vacas_camaras.ogg` | BGS | camaras frias / camaras | 45–90 s, bucle |
| `Audio/BGS/vacas_laboratorio.ogg` | BGS | Lucy, hospital, laboratorio / laboratorio | 45–90 s, bucle |
| `Audio/BGS/vacas_alcantarillas.ogg` | BGS | colector, tuneles, canal / alcantarillas | 45–90 s, bucle |
| `Audio/BGS/vacas_manada.ogg` | BGS | camara y altar / manada | 45–90 s, bucle |
| `Audio/BGM/vacas_combate.ogg` | BGM | visiones normales / combate | 60–120 s, bucle |
| `Audio/BGM/vacas_jefe.ogg` | BGM | Rey, Diagnostico y Pastor / jefe | 90–150 s, bucle |
| `Audio/BGM/vacas_persecucion.ogg` | BGM | cazas de I, III y IV / persecucion | 30–60 s, bucle |
| `Audio/ME/vacas_victoria.ogg` | ME | victoria | 3–6 s, una vez |
| `Audio/ME/vacas_derrota.ogg` | ME | derrota o retirada mental | 3–6 s, una vez |
| `Audio/BGM/vacas_gameover.ogg` | BGM | fin de partida / gameover | 30–60 s, bucle |
| `Audio/SE/ui_cursor.wav` | SE | mover seleccion / cursor | 40–100 ms, una vez |
| `Audio/SE/ui_confirmar.wav` | SE | aceptar / confirmar | 100–250 ms, una vez |
| `Audio/SE/ui_cancelar.wav` | SE | volver / cancelar | 100–250 ms, una vez |
| `Audio/SE/ui_error.wav` | SE | opcion bloqueada / error | 150–300 ms, una vez |
| `Audio/SE/mente_golpe.wav` | SE | impacto mental / golpe | 150–600 ms, una vez |
| `Audio/SE/mente_susto.wav` | SE | sustos existentes / susto | 300–1200 ms, una vez |
| `Audio/SE/paso_baldosa.wav` | SE | piso, hospital / paso_baldosa | 100–300 ms, una vez |
| `Audio/SE/paso_metal.wav` | SE | matadero, camaras / paso_metal | 100–300 ms, una vez |
| `Audio/SE/paso_agua.wav` | SE | subsuelo / paso_agua | 150–400 ms, una vez |
| `Audio/SE/puerta_oxido.wav` | SE | puertas / puerta | 500–1500 ms, una vez |

Los cuatro controles BGM/BGS/SE/ME se aplican a las llamadas de `Audio`, incluidas
las de eventos, animaciones, `Game_System` y scripts. El volumen final es
`volumen_llamada * ajuste_canal / 100`; el tono se conserva. BGM/BGS activos se
actualizan al mover el control. Los subtitulos son editables en la ultima columna
de TABLE y solo aparecen si existe el archivo correspondiente. Son descripciones
de sonido; no sustituyen el texto narrativo ni describen pasos repetidos.

`Vacas_Audio.play(:clave)` es el gancho publico. `zone` elige el ambiente por mapa.
La entrada de combate distingue jefes 9/13/17; las marcas de persecucion existentes
se consultan sin cambiar sus eventos. Los pasos se alternan cada dos pasos del
jugador, con superficie por zona; se puede ampliar por terreno en `increase_steps`.
`LEGACY` traduce seis nombres RTP usados por los scripts existentes. Otros sonidos
de eventos que no tengan archivo local permanecen silenciosos; para sustituirlos,
añadir su nombre sin extension a LEGACY o llamar a `play` desde el evento.

No normalizar todos los archivos al mismo pico: dejar margen para ambiente,
voz implicita y efectos. Pendiente de otro proceso: proporcionar estos 24 archivos
y valorar mezcla, puntos de bucle y duracion dentro de una partida.
