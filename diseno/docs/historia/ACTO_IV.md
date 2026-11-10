# Acto IV — Bajo la ciudad

Continuación completada el 9 de noviembre de 2026 sobre la instalación interrumpida. Se inspeccionaron `git status`, el diff, los mapas 17–21, el snapshot y las herramientas `*acto4*`. Se conservó el respaldo existente `respaldos/antes_acto4_20261109_194935/Data/`; no se volvió a respaldar Data ni se escribió en `.git`. Las modificaciones previas se conservaron.

## Acceso y prueba rápida

En el final del Acto III, Intro continúa al colector. También se puede bajar hablando con Lucy después del cierre del acto, o por el colector del hospital, mapa 15, evento **Colector bajo hospital A4**, en **(22,5)**, con la llave 29 y el interruptor 98 activo. La llegada es a **17 (4,11)**. Las ramas **96 (quedarse con Lucy)** y **97 (llevar las pruebas)** conservan sus decisiones, reciben diálogos distintos y reputación inicial 0/1.

Atajo desde el título: seleccionar **Nueva partida**, mantener **Alt** y confirmar con **Z**. Añadir **Mayús** prueba la rama 97; sin Mayús prueba la 96. Se recomienda Z para evitar que Alt+Intro active el cambio de pantalla de Windows/RGSS. Los accesos anteriores de Mayús y Ctrl continúan funcionando. El atajo crea una partida en memoria; no sobrescribe guardados.

Controles: flechas para caminar; Z/Intro/espacio para interactuar; **A** alterna la linterna; **S** consume una pila si falta batería. El altar permite descansar, recargar y guardar. La salida final ofrece guardar antes de mostrar el cierre del acto.

## Recorrido y mapas

| ID | Mapa | Tamaño | Contenido y conexiones |
|---|---|---|---|
| 17 | Colector: la última escalera | 20×15 | Llegada por ambas ramas, pila, croquis y pista de resonancias; regreso al hospital y paso a 18. |
| 18 | Túneles: nombres sin collar | 22×15 | Muesca, reputación, rueda, Coro, nicho de sacos; conexiones con 17, 19 y ramal seco a 21. |
| 19 | Canal de retorno | 20×15 | Junco, válvulas, Pulmón, persecución y armario de bombas; compuerta a 20. |
| 20 | La cámara de la manada | 20×15 | Consejo, Cencerro, Pastor hueco y elección del pacto; regreso a 19 y acceso a 21. |
| 21 | Altar de las cosas salvadas | 20×15 | Descanso, guardado, repuestos, dinamo y cierre; regreso a 18 o a 20 cuando se drena el umbral. |

47 eventos en los cinco mapas. Baldosas de 32 px, pasarelas estrechas, bucles y masas de roca/pared que delimitan los interiores. Tres capas con suelo, papeles/limo/paja y tuberías superiores; agua y muros bloqueados. Tileset **68**, tono **(-16,-6,-20,28)**, goteo RTP y niebla `002-Clouds01` con opacidad 24, zoom 200 y movimiento (1,-1). El cono de la linterna aporta la luz móvil; cámara y altar son zonas seguras.

Ruta principal: recoger rueda en 18 → ayudar o abandonar a Junco → cerrar **RETORNO** → abrir **DESCARGA** → refugiarse/salir durante la caza → hablar con Guernsey → afrontar Cencerro/Pastor → elegir pacto → altar y cierre. El altar es accesible por el ramal seco desde el principio: quedarse sin batería nunca bloquea la progresión.

## Sistemas y contenido

`scripts/11_bajo_ciudad.rb` se instala como **Vacas_BajoCiudad**, índice 99, antes de Main (100). Integra la linterna con Scene_Map/Spriteset_Map, inventario y el sistema existente de veneno/huella y combate mental. No añade una segunda estadística independiente de cordura.

- Batería 0–100; consume un punto cada 120 fotogramas de exploración libre. Pausa durante mensajes, intérprete, menús y combate, y en 20/21. Las pilas restauran 60 puntos hasta 100; no se gastan si está llena. Sin luz queda un radio mínimo y el veneno aumenta un punto cada 240 fotogramas, con tope 96. La huella conserva su función previa. El altar recarga gratuitamente y reduce veneno sin saltarse la huella.
- Manada como facción: Muesca y Junco responden a las acciones; reputación **-3..5**. Bajar la luz/escuchar, ayudar a Junco, resolver la dinamo y el límite elegido en el pacto alteran la reputación. Exigir paso puede iniciar la primera caza. Diálogos VN con retratos nuevos y las identidades existentes de Steven/Guernsey.
- Dos persecuciones: túneles, **32 segundos**, si Muesca queda hostil; agua, **28 segundos**, al abrir descarga. Nicho de sacos y armario de bombas son escondites; las salidas seguras también detienen la caza. Contacto o tiempo agotado lleva al altar, suma captura y ocho puntos de veneno con tope 96. Conserva objetos y decisiones; limpia temporizador, invisibilidad y bloqueo del menú.
- Puzle hidráulico: rueda única → retorno → descarga. Abrir descarga antes de cerrar retorno sube tensión; permite reintentar y conserva la rueda. La compuerta y el atajo del altar respetan el interruptor 118.
- Puzle opcional de resonancias: pista en 17 **(14,5)**; dinamo en 21 **(12,8)**. Orden correcto **tubo, aire, campana**. Error: +2 de tensión y reintento. Acierto: una pila, +1 reputación y -8 veneno; recompensa única, interruptor 139.
- Tres visiones: **Coro del tubo (14)**, **Pulmón de cieno (15)** y **Cencerro sin lengua (16)**. **Pastor hueco (17)** es el jefe obligatorio, reintentable hasta victoria. Se usan las técnicas mentales y los estados existentes; cero oro/experiencia.
- Dos sustos únicos: **10**, ligado a la hostilidad de Muesca; **11**, al drenar el canal. Comparten la imagen 98 del sistema existente, se limpian tras 24 fotogramas y usan marcas 136/137. Una ruta amistosa evita el primero.

## IDs y continuidad V–VI

| Rango | Uso |
|---|---|
| Mapas 17–21; tileset 68 | Alcantarillas, manada y altar. |
| Interruptores 113–119 | Acto activo, llegada, luz, retorno, descarga, umbral y rueda. |
| 120–125 | Caza/resolución/captura pendiente de túneles y agua. |
| 126–131 | Junco liberada, Muesca escuchada y cuatro visiones afrontadas/vencidas. |
| 132 | Pacto contra Cripps sellado. |
| 133 / 134 | Opciones exclusivas: nadie es ganado / venganza. |
| 135 | Ruta del Acto V desbloqueada. |
| 136–139 | Sustos 10/11 vistos, bajar luz ante Muesca, dinamo afinada. |
| Variables 51–56 | Reputación, batería, capturas, válvulas 0–2, etapa 1–6 y reloj de exploración. |
| Objetos 30–34 | Linterna, pila seca, rueda, chapa del pacto y croquis. |
| Enemigos/tropas 14–17 | Coro, Pulmón, Cencerro y Pastor. |

Se conservan los interruptores 35/36/38 y 96/97. El cierre entrega una sola chapa 33. Volver a entrar no duplica pilas ni reinicia batería/reputación. Los actos V y VI deben leer **132, 133/134, 135, 126, variable 51** y las decisiones heredadas; todavía no se construye contenido de esos actos. `Scene_FinActo.new(4)` vuelve al título después del cierre.

## Arte y escala

**13 PNG instalados**: tileset, hoja de objetos, tres hojas de vacas, dos retratos, cuatro battlers y dos sustos. Cinco fuentes nuevas aceptadas de seis llamadas a **image_gen integrado en nube**; el intento de separar los dos retratos se descartó visualmente y se conservó como tal. Se recuperaron las fuentes anteriores; no se inventan sus prompts perdidos. Guernsey reutiliza su fuente canela aprobada. Cencerro/Pastor usan vistas frontales de la referencia recuperada; sustos usan reencuadres del Coro/Pulmón, sin generación local.

Fuentes, prompts nuevos, hashes y [manifest.json](../../fuentes/arte_hd2d/acto4/manifest.json) en `arte_hd2d/acto4/`. Instalación reproducible con `adaptar_arte.py --batch diseno/fuentes/arte_hd2d/acto4/manifest.json`; `../../herramientas/actos/acto4/arte_acto4.py` reconstruye el manifiesto y la lámina. El adaptador admite recortes de fuente, cuadrículas de origen distintas y opacidad explícita de terrenos. Las filas de caminata se recortan con límites medidos para evitar restos de otras poses.

Personajes: **celdas 48×48**, siluetas dentro de 44 px; Steven conserva celda humana 32×48 y silueta previa de 40 px. Objetos pequeños: pila 14, etiqueta 12, botas/mapa como máximo 16 px. El altar cabe en 32 px de ancho y sus utensilios quedan pequeños respecto al personaje. Cada objeto conserva su proporción y apoyo inferior. Las cotas exactas de los 16 índices están en el manifiesto y se auditan separadamente de la altura 64 de la celda.

Capturas revisadas: [17](../../capturas/actos/acto4_17.png), [18](../../capturas/actos/acto4_18.png), [19](../../capturas/actos/acto4_19.png), [20](../../capturas/actos/acto4_20.png), [21](../../capturas/actos/acto4_21.png) y [lámina de arte](../../capturas/actos/acto4_arte.png). Son renders estáticos del mapa con eventos de primera página; los cuadrados azules son marcadores técnicos invisibles en el juego. No simulan tono narrativo, cono dinámico ni niebla animada.

## Correcciones y verificación

La auditoría heredada mostraba como inaccesible la llegada en (1,1). Tras renovar el snapshot se comprobó que es un autorun, no una interacción física, y su página final vacía no necesita acceso. Se mantuvo el control real de colisiones y se amplió a 16 escenarios, incluidas capturas y objetos recogidos. Hospital y colector están comunicados desde la entrada principal; agua/muros no se hicieron transitables para silenciar errores.

Los dos accesos de eventos desde 15/16 ahora usan **comando 201 explícito** después de inicializar el estado; el salto desde la pantalla final conserva la cola RGSS. Esto elimina los cinco avisos de inaccesibilidad del grafo estático, que no podía seguir asignaciones de destino hechas en Ruby. Se corrigieron además la consulta al intérprete (`$game_system.map_interpreter`) y el uso de `Range#step` sin bloque, incompatible con Ruby 1.8; ambos fallaban al actualizar la linterna. Se corrigieron recortes de filas de Muesca/Junco y se instalaron los recursos ausentes.

- `../../verificaciones/verificacion_acto4.json`: **1.210 comprobaciones**, 16 escenarios, cero errores; acciones, destinos, recursos dinámicos, BD, escala y reproducción exacta de los 13 PNG desde fuentes.
- `../../verificaciones/herramientas/validar_assets4.json`: **983 referencias**, cero recursos ausentes.
- `../../verificaciones/herramientas/validar_conectividad4.json`: **21 mapas, 84 transferencias**, cero destinos rotos, mapas aislados, inaccesibles o avisos.
- Ruby portable de **D:/DevTools/ruby**: **101 scripts** de Scripts.rxdata con sintaxis válida. La compatibilidad RGSS1 se comprobó también en el motor, no solo con Ruby moderno.
- `verificar_escala.py --permitir-data-modificada`: siete hojas históricas válidas, escala y reproducción conservadas. La opción está prevista para cambios autorizados de mapas: Data difiere legítimamente del respaldo de escala anterior al Acto IV. El informe actualizado está en `../../verificaciones/verificacion_escala_revision.json`.
- `../../verificaciones/verificacion_rgss_acto4.txt`: Game.exe/RGSS104E real, cuatro partidas (96/97 × dos pactos), seis accesos de título, entrada física del hospital, idempotencia, válvulas, dinamo, capturas por contacto y tiempo, refugios, batería/veneno/controles, los 21 spritesets, retratos y sustos; 120 simulaciones de combate y batalla nativa del Pastor. Main restaurado al finalizar.
- Regresión posterior: `../../herramientas/actos/acto3/probar_acto3.mjs` y `../../herramientas/comun/probar_rgss.mjs` pasan en Game.exe y restauran Main; auditoría del III con 493 comprobaciones sin errores y accesos I–II en 78 escenarios, 2.134 puertas y 1.635 destinos sin problemas. Sintaxis registrada en `../../verificaciones/verificacion_sintaxis_acto4.json`.

Repetir verificaciones desde `diseno/herramientas`: `node inspeccionar.mjs`, `python verificar_acto4.py`, `node probar_acto4.mjs`. Ejecutar los arneses de Game.exe de uno en uno porque reemplazan Main temporalmente. Para recompilar contenido: snapshot actual → `python build_acto4.py` → `node rx.mjs --batch b_acto4.json`. **No ejecutar creación de mapas ni respaldo nuevamente sobre esta instalación.**

## Pendiente y límites

No quedan errores conocidos de referencias, progresión o colisión en los escenarios auditados. Pendiente: revisión humana del ritmo de diálogos/sustos, duración de persecuciones, mezcla sonora y legibilidad de luz/niebla durante una partida completa. El arnés acelera Graphics y entradas para evitar la espera de foco; verifica lógica, bitmaps y escenas nativas, pero no acredita una sesión manual. Un intento adicional de capturar la ventana del motor con actualización gráfica normal agotó 55 segundos sin producir imágenes; Main se restauró y se retiraron esos auxiliares experimentales. Las capturas estáticas entregadas sí se generaron y revisaron. Los prompts de las seis fuentes recuperadas de la tarea interrumpida no estaban guardados; las fuentes originales permanecen disponibles. Actos V–VI pendientes de desarrollo.
