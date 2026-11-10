# Interfaz propia de Vacas

Implementacion del 9 de noviembre de 2026, RGSS1 / Ruby 1.8, cliente 640×480.
Fuente principal: `scripts/11_interfaz.rb`, seccion `Vacas_Interfaz` despues de
`Vacas_BajoCiudad` y antes de Main. `06_vn.rb` consulta la velocidad elegida.
Se conservan los diez scripts narrativos, mapas, BD, tropas y eventos de I–IV.

## Pantallas y controles

- Titulo propio: parallax lento, niebla y fluorescente dependiente de intensidad,
  logotipo tipografico, Nueva partida / Continuar / Ajustes / Salir. Se conserva la
  cadena original de Nueva partida: Mayus → II; Ctrl → III; Alt → IV, con Mayus
  adicional para sus variantes. Z/Intro confirma; Esc vuelve; flechas seleccionan.
- Pausa: Objetos, Estado/Cordura, Notas, Guardar, Ajustes y Salir. Fondo propio,
  transicion, tareas, ubicacion, dinero, cursor animado y skin industrial comunes.
  Inventario en lista vertical con iconos propios; archivos como cuatro recuerdos.
  Salir ofrece titulo, cerrar o cancelar. No se reemplaza la logica de uso de objetos.
- Guardar se habilita junto a la tele de (8,17), mapa 2, y en el altar, mapa 21.
  Se bloquea con menu deshabilitado o persecucion activa. La marca nativa
  `save_disabled` permanece como estaba: el contenido la usa para anular el guardado
  libre de XP y abre sus puntos con el comando SAVE. El menu aplica la restriccion
  espacial equivalente. Los puntos narrativos y sus comandos SAVE se conservan.
- Estado muestra salud, aliento, cordura, veneno y huella; iconos para Panico, Asco
  y Culpa. **Cordura = 100 − veneno**; no se añade una estadistica que pueda divergir.
- Notas lista los documentos presentes en inventario y abre el CE1 existente.
  Mantiene `$vacas_ultimo_objeto`, los textos y las ramas originales. Los objetos
  que no son documentos siguen disponibles en Objetos.
- Game Over propio con fondo animado, cargar / titulo / salir. Las derrotas
  mentales mantienen su recuperacion y reintentos narrativos, con tarjeta propia.

## Ajustes

`Vacas.cfg` es un Marshal independiente de `Save1..4.rxdata`. Defaults seguros si
falta o esta corrupto; tipos y rangos validados. Al volver se escribe mediante
temporal y respaldo `Vacas.cfg.bak`; un fallo de escritura deja la pantalla abierta
con aviso y permite reintentar. No altera las partidas existentes.

| Control | Rango / efecto |
|---|---|
| BGM, BGS, SE, ME | Cuatro canales independientes, 0–100 %, pasos de 5 |
| Texto | Rapida / normal / lenta / muy lenta: 1/2/3/4 frames por glifo |
| Brillo | 50–150 %, capa de negro o luz; conserva los tonos narrativos |
| Sustos y temblores | 0–100 %, escala sacudidas, flashes de Game_Screen, imagen y golpe del susto; 0 retira la imagen |
| Subtitulos de sonido | Si / no, captions editables de los ganchos de audio |
| Pantalla completa | Guia Alt+Enter nativa de RGSS1; no fuerza una resolucion del escritorio |

Izquierda/derecha ajusta; Esc o Guardar y volver persiste. El brillo es una
compensacion visual dentro del juego, **no modifica la gamma del monitor**. La
pantalla completa depende del toggle del motor y no se serializa en `Vacas.cfg`.
Las animaciones RTP pueden contener sus propios flashes: el control escala los
flashes y temblores de Game_Screen y los sustos del juego, no reescribe la BD.

## Combate y exploracion

Se mantienen Scene_Battle, IA, turnos, acciones, seleccion de objetivos, eventos
de tropas, formulas, habilidades y resultados originales. Entrada con tarjeta y
fundido; panel propio compacto de cuatro comandos; panel enemigo con vida y
estados; panel Steven con salud, aliento, cordura y veneno. Barras interpoladas,
cursor/objetivo propios, daño emergente con letra legible y golpes con flash y
sacudida. Las victorias y derrotas usan tarjetas propias. No añade recompensas ni
cambia el balance; la huella, la recuperacion y el reintento de jefes siguen en Mente.

Seis battlebacks nuevos: piso, matadero, camaras, laboratorio, alcantarillas y
manada. Se eligen por zona; tropas 10–13 fuerzan laboratorio y Pastor fuerza
manada. La seleccion no cambia los mapas ni sus fondos almacenados; Mente restaura
el fondo y tono previos al terminar.

HUD discreto abajo a la izquierda: cordura/veneno, interpolacion y pulso al cambiar;
bateria solo en el subsuelo con linterna en inventario. Se oculta con los mensajes
VN, la marca HUD_OCULTO y fuera de Scene_Map. Se desactiva el segundo HUD antiguo
de bateria para evitar duplicados. La linterna y su gasto permanecen intactos.

VN conserva nombre, retrato, lado, atenuacion, opciones, variables, colores,
entrada numerica y callbacks de mensajes. Comparte skin, tipografia y un indicador
de avance propio. Una pulsacion revela y otra confirma; Mayus sigue revelando.

## Arte y audio

Diez fuentes nuevas de `image_gen` en nube; ningun generador/GPU local. Fuentes,
prompts y SHA-256 en `arte_hd2d/interfaz/generaciones.json`. Veinticuatro recursos
instalados por `herramientas/adaptar_arte.py`: tres fondos 640×480, seis battlebacks
640×480, skin XP 192×128, ocho iconos 24×24, tres cursores 16/14/32 px, dos barras
256×8 y niebla 256×256. El kit generado se recorta/compone en CPU para respetar
los slots tecnicos de XP. No se sustituyen los PNG anteriores.

Reproducir: `python diseno/herramientas/arte_interfaz.py`, luego
`python diseno/herramientas/adaptar_arte.py --batch diseno/arte_hd2d/interfaz/manifest.json`.
El adaptador añade `preserve_alpha` para Pictures/skin/iconos y conserva el
comportamiento opaco anterior cuando no se solicita. No regenerar las fuentes.

`Vacas_Audio` centraliza nombres y ganchos. El envoltorio de `Audio` aplica los
cuatro volumenes incluso a llamadas directas desde eventos y animaciones. Ambiente
por zona, menu, pasos por superficie, persecucion, combate/jefes, resultados y
puertas estan preparados. Ausencias silenciosas. Lista exacta de **24 archivos**,
tipo, uso y bucle sugerido en [AUDIO.md](AUDIO.md). Ningun audio descargado.

## Respaldo, pruebas y capturas

Respaldo anterior a la primera escritura de Data y scripts: ruta absoluta en
`herramientas/respaldo_interfaz.txt`, bajo `respaldos/antes_interfaz_*`.
Solamente Scripts.rxdata cambia en Data. No se ha escrito en `.git`.

`herramientas/probar_interfaz.mjs` instala temporalmente el arnes Ruby, ejecuta
Game.exe y restaura **los bytes originales de Scripts.rxdata** en finally, incluso
con error o timeout. No ejecutar dos arneses a la vez ni abrir el editor mientras
se escriben scripts. Cada pantalla ejecuta sus clases reales; entradas simuladas,
GDI del cliente de la ventana RGSS y fotogramas nativos para las capturas. Entre
capturas se acelera Graphics y se conserva una actualizacion nativa periodica.
El log distingue capturas y comprobaciones; no se presenta como recorrido manual.

El arnes abre titulo, pausa, objetos, estado, notas, archivos, ajustes, VN y Game
Over. Comprueba los cuatro accesos, persistencia, cambios mediante flecha, los
cuatro canales globales y silencio ante ausencias, guardado permitido/bloqueado y
que revelar texto no confirme una decision. Ejecuta ocho combates completos:

| Acceso | Vision de prueba | Encuentro destacado / jefe |
|---|---|---|
| Acto I | Familia de nieve, tropa 8, prueba aislada | Madre de yeso, tropa 2 |
| Mayus, Acto II | Enjambre de moscas, tropa 5 | Rey del cajon, tropa 9 |
| Ctrl, Acto III | Tarro, tropa 10 | Diagnostico, tropa 13 |
| Alt, Acto IV | Coro del tubo, tropa 14 | Pastor hueco, tropa 17 |

El Acto I **no contiene un jefe final independiente ni un encuentro normal
repetible**. Se prueban esas dos tropas con su estado inicial sin añadir combates
al argumento ni fingir la existencia de un jefe nuevo. Se conservan las estadisticas
en los ocho combates; el arnes elige Respirar o Poner nombre automaticamente.

Resultados: `verificacion_interfaz.txt` (motor) y `verificacion_interfaz.json`
(sintaxis de los scripts extraidos con D:/DevTools/ruby, fuentes, reproduccion de
assets, dimensiones, alpha, Data protegida y capturas).

Resultado final: 79 comprobaciones de interfaz en Game.exe, ocho combates completos,
102 scripts con sintaxis valida y 24 recursos reproducibles. Las regresiones
anteriores I–II, III y IV tambien pasan; incluyen recorridos de eventos y 120
simulaciones por ampliacion. Sus logs conservan las marcas FIN de los actos III/IV.
Se actualizaron los arneses I–II/III/IV para avanzar `Graphics.frame_count` y ejecutar
un fotograma nativo cada cien actualizaciones: con el contador congelado podian
activar el watchdog `Hangup` de RGSS durante las pruebas aceleradas.

La captura VN se repitio con el ciclo nativo de apertura/revelado en
`herramientas/prueba_ui_vn.rb`; log `verificacion_vn_interfaz.txt`. El primer arnes
de captura hacia dos refresh manuales y perdia el metadato del retrato en su propia
captura, aunque los mensajes nativos y las decisiones funcionaban. El arnes completo
ya usa el ciclo corregido. Hay 20 capturas del cliente y dos laminas PNG.

Repetir, en este orden:

1. `node diseno/herramientas/instalar_interfaz.mjs` si se editaron las fuentes.
2. `node diseno/herramientas/probar_interfaz.mjs`.
3. Desde `diseno/herramientas`: `node inspeccionar.mjs`.
4. `python diseno/herramientas/verificar_interfaz.py`.

Capturas reales `capturas/ui_*.png`; [lamina de interfaz](capturas/ui_resumen.png)
y [fondos nuevos](capturas/ui_fondos.png). Las imagenes no son maquetas: corresponden
al cliente 640×480 de Game.exe. La lamina de fondos muestra los PNG instalados.

## Incidencias y pendiente

Durante desarrollo se corrigio una llamada al instalador de metodos de Audio que
fallaba en Ruby 1.8 antes de Main. Los primeros intentos de captura conservaron
fotogramas anteriores: se corrigieron forzando frame_reset y varios fotogramas
nativos antes de GDI. El limite de 55 s era insuficiente para ocho combates con
capturas; el runner permite 180 s y restaura Scripts al terminar.

Pendiente externo: colocar los 24 archivos de audio y escuchar la mezcla. Pendiente
de valoracion humana: recorrido continuo I–IV, ritmo del texto, legibilidad en su
monitor, sustos y modo de pantalla completa. Alt+Enter se documenta como guia; el
arnes no cambia el modo de video. Actos V–VI conservan su estado anterior.
