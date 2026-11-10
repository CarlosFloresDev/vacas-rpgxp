# Audio de Vacas

Actualización Acto VI: `15_reydios.rb` amplía `MAP_AUDIO` con mapas 28–32:
28/31, `:alcantarillas` con `:alcantarillas_bgm`; 29, `:matadero` con calle
nocturna y lluvia; 30, `:piso` con tema seguro y reloj; 32, `:manada` con
drone y eco. El switch 185 activa persecución y las tropas 35–37 usan música
de jefe. Las compuertas usan `Vacas_Audio.play(:cadena_gancho)`. Los créditos
del cierre incluyen íntegro el audio CC y el equipo de Feka Studios; también
se conserva el listado del título. Detalles en [ACTO_VI.md](../historia/ACTO_VI.md).

Integración del 10 de noviembre de 2026, RGSS1 / Ruby 1.8.
Se instalaron las **120 entradas** del manifiesto en `Audio/BGM`, `BGS`, `ME` y
`SE`. Las 96 entradas sin destino explícito usan `Audio/TIPO/nombre_original`.
Se conservan `diseno/fuentes/audio_fuentes`, su manifiesto y sus créditos originales.
Para los diez destinos WAV se copian los WAV PCM reales incluidos en el pack;
también se conserva su versión OGG en Audio/SE. No se renombra un OGG a WAV.

## Catálogo y mezcla

`Vacas_Audio::TABLE`, en `scripts/12_interfaz.rb`, contiene 120 claves únicas:
`clave => [tipo, nombre_sin_extension, volumen_base, tono, subtitulo]`.
Las claves extra derivan de `use`; las variantes numeradas conservan muestras
distintas. `../../fuentes/catalogos/audio_catalogo.json` documenta clave, fuente, destino, uso, bucle,
licencia y volumen de cada entrada. Los nombres respetan mayúsculas y minúsculas.

Volúmenes base: BGS 26, exploración BGM 42, título 56, combate 60, jefe y
persecución 64, SE 52, interfaz 42, pasos 24, sustos 62, ME 56. Se multiplican
una sola vez por el ajuste de su canal. Los sustos también respetan intensidad.
El valor de tono en la traducción RTP es 100 para reproducir las muestras a su
velocidad original. Los valores dejan margen para sumar música, ambiente y SE;
la escucha y el balance subjetivo durante un recorrido siguen siendo humanos.
BGM/BGS usan el bucle nativo de XP; ME/SE se disparan una vez.

## Mapas I–IV

`MAP_AUDIO` es la tabla explícita de `zone`: zona visual, clave BGM, clave BGS y
superficie por defecto. `zone` conserva las seis zonas de battlebacks existentes.
`Game_Map#autoplay` y `Scene_Map#update` aplican la pareja del mapa sin reiniciar
pistas iguales. Los BGS RTP de los eventos Ambiente se traducen a la selección
del mapa; se conservan sus tonos, niebla y narrativa. No se editó ningún mapa.

| Mapa | Nombre | BGM (archivo) | BGS (archivo) | Pasos por defecto |
|---|---|---|---|---|
| 1 | MAP001 | `../../fuentes/audio_fuentes/bgm/bgm_piso_exploracion.ogg` | `../../fuentes/audio_fuentes/bgs/vacas_piso.ogg` | baldosa |
| 2 | El piso | `../../fuentes/audio_fuentes/bgm/bgm_piso_exploracion.ogg` | `../../fuentes/audio_fuentes/bgs/vacas_piso.ogg` | baldosa |
| 3 | La escalera | `../../fuentes/audio_fuentes/bgm/bgm_piso_exploracion.ogg` | `../../fuentes/audio_fuentes/bgs/bgs_edificio_abandonado.ogg` | baldosa |
| 4 | La calle | `../../fuentes/audio_fuentes/bgm/bgm_extra_calle_noche.ogg` | `../../fuentes/audio_fuentes/bgs/bgs_lluvia_calle.ogg` | concreto |
| 5 | Matadero: entrada | `../../fuentes/audio_fuentes/bgm/bgm_matadero_exploracion.ogg` | `../../fuentes/audio_fuentes/bgs/bgs_lluvia_calle.ogg` | concreto |
| 6 | Matadero: vestuario | `../../fuentes/audio_fuentes/bgm/bgm_matadero_exploracion.ogg` | `../../fuentes/audio_fuentes/bgs/bgs_nevera_zumbido.ogg` | baldosa |
| 7 | Matadero: corrales | `../../fuentes/audio_fuentes/bgm/bgm_matadero_exploracion.ogg` | `../../fuentes/audio_fuentes/bgs/bgs_corral_ganado.ogg` | concreto |
| 8 | Matadero: la cadena | `../../fuentes/audio_fuentes/bgm/bgm_matadero_exploracion.ogg` | `../../fuentes/audio_fuentes/bgs/vacas_matadero.ogg` | metal |
| 9 | Matadero: cámaras frías | `../../fuentes/audio_fuentes/bgm/bgm_camaras_frias.ogg` | `../../fuentes/audio_fuentes/bgs/vacas_camaras.ogg` | metal |
| 10 | Matadero: oficina de Cripps | `../../fuentes/audio_fuentes/bgm/bgm_matadero_exploracion.ogg` | `../../fuentes/audio_fuentes/bgs/bgs_reloj_tictac.ogg` | madera |
| 11 | Matadero: pasillo de mantenimiento | `../../fuentes/audio_fuentes/bgm/bgm_matadero_exploracion.ogg` | `../../fuentes/audio_fuentes/bgs/bgs_matadero_cadenas.ogg` | metal |
| 12 | Lucy: el piso de arriba | `../../fuentes/audio_fuentes/bgm/bgm_tv_segura.ogg` | `../../fuentes/audio_fuentes/bgs/bgs_reloj_tictac.ogg` | madera |
| 13 | Carnicería Molina | `../../fuentes/audio_fuentes/bgm/bgm_lucy_laboratorio.ogg` | `../../fuentes/audio_fuentes/bgs/bgs_nevera_zumbido.ogg` | baldosa |
| 14 | Carnicería cerrada: depósito | `../../fuentes/audio_fuentes/bgm/bgm_extra_sotano.ogg` | `../../fuentes/audio_fuentes/bgs/bgs_edificio_abandonado.ogg` | concreto |
| 15 | Hospital cerrado: curas | `../../fuentes/audio_fuentes/bgm/bgm_lucy_laboratorio.ogg` | `../../fuentes/audio_fuentes/bgs/bgs_fluorescente_zumbido.ogg` | baldosa |
| 16 | Lucy: laboratorio improvisado | `../../fuentes/audio_fuentes/bgm/bgm_extra_tension_lab.ogg` | `../../fuentes/audio_fuentes/bgs/vacas_laboratorio.ogg` | baldosa |
| 17 | Colector: la ultima escalera | `../../fuentes/audio_fuentes/bgm/bgm_alcantarillas.ogg` | `../../fuentes/audio_fuentes/bgs/vacas_alcantarillas.ogg` | concreto |
| 18 | Tuneles: nombres sin collar | `../../fuentes/audio_fuentes/bgm/bgm_extra_dark_drone.ogg` | `../../fuentes/audio_fuentes/bgs/bgs_alcantarilla_goteo.ogg` | concreto |
| 19 | Canal de retorno | `../../fuentes/audio_fuentes/bgm/bgm_alcantarillas.ogg` | `../../fuentes/audio_fuentes/bgs/bgs_agua_corriente.ogg` | agua |
| 20 | La camara de la manada | `../../fuentes/audio_fuentes/bgm/bgm_camara_manada.ogg` | `../../fuentes/audio_fuentes/bgs/vacas_manada.ogg` | concreto |
| 21 | Altar de las cosas salvadas | `../../fuentes/audio_fuentes/bgm/bgm_tv_segura.ogg` | `../../fuentes/audio_fuentes/bgs/bgs_mazmorra_eco.ogg` | concreto |

Las marcas 10/90/120/122 cambian la BGM a `vacas_persecucion`. Al terminar,
se restaura la música y ambiente de la ubicación actual, también tras cambiar de
mapa o volver de pausa. Las tropas 9 (Rey), 13 (Diagnóstico) y 17 (Pastor) usan
`vacas_jefe`; las otras visiones usan `vacas_combate`. Victoria y derrota usan
sus ME. El título y Game Over mantienen sus temas propios.

## Pasos y eventos

Los pasos suenan cada tres movimientos, con al menos 12 frames entre sonidos,
a volumen 24, sin pasos durante mensajes o rutas forzadas. Se alternan tres
muestras de baldosa, rejilla metálica, agua, madera o concreto. Se consulta
`terrain_tag(x,y)` primero: tags 1=agua, 2=metal, 3=madera, 4=concreto,
5=baldosa; tag 0 u otros usan la superficie del mapa. No se modifican tilesets.

`LEGACY` resuelve 133 nombres antiguos de la BD, mapas y scripts a recursos
locales, incluidas animaciones de combate. Puertas de madera/metal, manijas,
interruptores, papel, llaves, mugidos, impactos y curación reutilizan llamadas
existentes. Los sonidos de acción genéricos usan muestras locales apropiadas,
sin depender de archivos RTP externos. Los BGS mantienen la prioridad del mapa.

Los sustos `Game_Screen#vacas_susto` seleccionan `se_screamer_1..3` por ID y
sustituyen su impacto original: no se suman dos gritos. El control de intensidad
escala el SE además de imagen, flash y temblor. `gain_item` dispara llaves,
papeles, frascos u objeto genérico solo cuando aumenta realmente el inventario
en exploración, con un límite de un SE por entrega de varios objetos. Los
aciertos del minijuego de corte usan cuchillada; la cinta usa gancho metálico;
los fallos conservan el gancho de error. La linterna hace clic al alternar,
quedarse sin batería o recargar, evitando duplicar el clic de recarga.

## Créditos accesibles

El título ofrece **Creditos**, con las 120 atribuciones de `../../fuentes/audio_fuentes/CREDITOS.md`:
obras, autores secundarios, licencias, enlaces y modificaciones de las mezclas.
El texto está incorporado en el script y preparado en líneas de hasta 54
caracteres para Courier New de 16 px. Son 107 páginas de 12 líneas; flechas
izquierda/arriba retroceden, derecha/abajo o Z/Intro avanzan; Esc vuelve al título.
Se incluye `diseno/docs/sistemas/CREDITOS_AUDIO.md` en la raíz para distribuir el listado completo.
Las fuentes originales de atribución no se han alterado.

## Instalación y verificación

Respaldo previo en la ruta registrada en `../../archivo/herramientas/respaldo_audio.txt`.
Solo se reemplaza la sección `Vacas_Interfaz` en Data/Scripts.rxdata mediante
`../../herramientas/audio/instalar_audio.rb`, que carga y escribe con Ruby Marshal y valida
el archivo temporal antes de instalarlo. Main, IDs y las otras 101 secciones se
conservan byte a byte en sus campos; no se reescriben eventos ni otros Data.
No se accede a `.git`.

Repetir desde la raíz, sin el editor ni otro arnés abiertos:

1. `D:/DevTools/ruby/rubyinstaller-3.3.6-1-x64/bin/ruby.exe --disable-gems diseno/herramientas/audio/instalar_audio.rb`
2. `node diseno/herramientas/comun/probar_interfaz.mjs prueba_audio.rb`
3. Desde `diseno/herramientas`: `node inspeccionar.mjs`.
4. Desde la raíz: `python diseno/herramientas/audio/verificar_audio.py`.

El arnés abre título y créditos reales, comprueba navegación y vuelta, reproduce
las 120 entradas mediante Audio nativo, comprueba BGM/BGS de los 21 mapas,
prioridad frente a BGS RTP, persecuciones y restauración, pausa, variantes y
frecuencia de pasos, recogida, screamer/intensidad, linterna y volumen global.
También comprueba los SE de corte/cinta y la selección de música en la entrada
real de las tropas 2/9/13/17, omitiendo el bucle de turnos en esa prueba de audio.
Simula entradas; no sustituye una escucha humana ni un recorrido manual completo.
El arnés acelera los fotogramas y omite el renderer que espera al foco de ventana;
las llamadas Audio finales sí se ejecutan en el motor, sin sustituirlas por mocks.
`../../verificaciones/verificacion_audio_motor.txt` registra el resultado. El runner restaura los bytes
originales de Scripts.rxdata al terminar incluso si falla el motor.
`../../verificaciones/verificacion_audio.json` registra sintaxis de las 102 secciones instaladas y
fuentes Ruby, carga Marshal, referencias resueltas, SHA-256 de copias, mapas,
créditos y comprobación de que solo cambió la sección autorizada.

Resultado final: **212 comprobaciones del motor**, 120 claves únicas con archivos
reales, diez copias OGG adicionales junto a sus WAV, 115 verificaciones de sintaxis
(102 secciones instaladas, once fuentes y dos herramientas Ruby), carga Marshal
correcta y cero referencias sin resolver. Se verificó además que las 631 líneas
de atribuciones se muestran completas en las 1284 líneas preparadas para pantalla.
