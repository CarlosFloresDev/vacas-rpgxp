# Jugabilidad: cierre incremental de la revisión

Revisión del 11-11-2026 sobre el trabajo de `b2fb7a4`. Se conservaron Data, Graphics y respaldos existentes; no se restauraron mapas ni se crearon commits. Las fuentes instaladas y los datos actuales se verifican juntos.

## Jarabe de madre: diagnóstico comprobado

El evento 11 del mapa 2 está en (13,3), usa `vacas_muebles`, dirección 8, patrón 1, acción y `through=false`. La casilla (13,4) es alcanzable desde (6,12) tanto en el respaldo anterior como en Data actual. El bloqueo de la bañera, evento 49 en (10,4), no corta ese camino. No se encontró una colisión ni una página incorrecta que impidiera recoger el jarabe después de recibir las órdenes.

La primera página comprueba **switch 2: madre dio las órdenes** dentro de su lista de comandos. Antes de activarlo solo describía el espejo, sin indicar que allí estaba el encargo ni cómo habilitarlo. El guardado examinado tampoco tenía activado ese switch ni poseía el objeto. La corrección conservada informa «El jarabe de madre esta detras del espejo. Primero debo hablar con ella». No se elimina el requisito narrativo. Tras hablar con madre, mirar hacia arriba desde (13,4) entrega el objeto 3 y activa el autoswitch A; volver a madre consume el objeto y activa switch 4.

La prueba ejecuta esa secuencia con las clases e intérprete instalados: visita anterior a las órdenes sin consumir el evento, acceso físico, recogida, segunda visita sin duplicación y entrega. Pasa en 640×360 y 640×480. [Diagnóstico comparado](../../verificaciones/diagnostico_lavabo.json), [guardado examinado](../../verificaciones/diagnostico_guardado_jarabe.json).

XP serializa el mapa dentro de la partida. La migración `@jugabilidad_mapas_v1` ya estaba escrita pero **no instalada** al reanudar esta tarea. Ahora se instala: al cargar recarga el mapa actual en memoria y recentra la cámara, conservando posición, switches e inventario. No escribe ni reemplaza `Save1.rxdata`.

## Correcciones por mapa

La misma auditoría sobre `antes_jugabilidad/Data` encuentra **38 errores**, y sobre Data actual encuentra **0**. El informe anterior se reconstruyó leyendo el respaldo, sin restaurarlo. Son hallazgos de geometría y páginas, no 38 casillas distintas. El registro de reparación contiene **72 cambios de campos**; varios campos reparan un mismo problema.

| Mapa | Errores antes | Corregidos | Errores actuales | Intervención conservada |
|---|---:|---:|---:|---|
| 1 | 0 | 0 | 0 | Sin cambios de geometría |
| 2 | 8 | 8 | 0 | Ventana accesible sobre cajonera con counter; 7 huellas de muebles; pista del jarabe |
| 3 | 0 | 0 | 0 | Sin cambios de geometría |
| 4 | 0 | 0 | 0 | Sin cambios de geometría |
| 5 | 0 | 0 | 0 | Sin cambios de geometría |
| 6 | 0 | 0 | 0 | Sin cambios de geometría |
| 7 | 13 | 13 | 0 | Vacas junto a valla, counter sin abrir corrales, cubo accesible, ruta ajustada; página vacía tras salida; 4 huellas |
| 8 | 9 | 9 | 0 | 9 huellas de muebles grandes |
| 9 | 3 | 3 | 0 | 3 huellas de muebles grandes |
| 10 | 0 | 0 | 0 | Sin cambios de geometría |
| 11 | 0 | 0 | 0 | Sin cambios de geometría |
| 12 | 0 | 0 | 0 | Sin cambios de geometría |
| 13 | 0 | 0 | 0 | Sin cambios de geometría |
| 14 | 5 | 5 | 0 | 5 huellas de muebles grandes |
| 15 | 0 | 0 | 0 | Sin cambios de geometría |
| 16 | 0 | 0 | 0 | Sin cambios de geometría |
| 17 | 0 | 0 | 0 | Sin cambios de geometría |
| 18 | 0 | 0 | 0 | Sin cambios de geometría |
| 19 | 0 | 0 | 0 | Sin cambios de geometría |
| 20 | 0 | 0 | 0 | Sin cambios de geometría |
| 21 | 0 | 0 | 0 | Sin cambios de geometría |
| 22 | 0 | 0 | 0 | Sin cambios de geometría |
| 23 | 0 | 0 | 0 | Sin cambios de geometría |
| 24 | 0 | 0 | 0 | Sin cambios de geometría |
| 25 | 0 | 0 | 0 | Sin cambios de geometría |
| 26 | 0 | 0 | 0 | Sin cambios de geometría |
| 27 | 0 | 0 | 0 | Sin cambios de geometría |
| 28 | 0 | 0 | 0 | Sin cambios de geometría |
| 29 | 0 | 0 | 0 | Sin cambios de geometría |
| 30 | 0 | 0 | 0 | Sin cambios de geometría |
| 31 | 0 | 0 | 0 | Sin cambios de geometría |
| 32 | 0 | 0 | 0 | Sin cambios de geometría |

[Registro de campos, antes/después y motivos](../../verificaciones/correcciones_jugabilidad.json). Los tilesets efectivos incluyen atlas particulares por mapa: no se corrigió indiscriminadamente el 51 o el 70. Las huellas verificadas se conservan en `jugabilidad_reglas.json`. Las prioridades altas por sí solas no significan pared: bloquearlas todas rompería lámparas, raíles y decoración elevada.

## Pantalla y perspectiva

Las 55 fuentes instaladas usan `Vacas_HD` para consultar el lienzo (con respaldo RGSS1 de 640×480). Cámara y scroll admiten límites fraccionarios y centrado negativo en mapas pequeños; los márgenes se cubren de negro. Se conservan las adaptaciones de mensajes, elecciones, VN, HUD, menús, archivos, tienda, nombres, batalla, minijuegos, cine y créditos. Los centros horizontales restantes de nombre/cargar/salir se derivan ahora del ancho. Las pictures de pantalla completa usan cover; las máscaras de iluminación conservan coordenadas del mundo.

`numeros_pantalla.txt` recoge la búsqueda de 480/320/240/416/304/160. Los valores restantes incluyen colores, opacidad, duraciones, anchos de columnas, tamaños de assets y medidas de referencia pasadas a las funciones de adaptación; no deben sustituirse automáticamente como si todos fueran posiciones verticales. Los comandos 231/232 se enumeran con sus parámetros en el informe de jugabilidad.

En los mapas actuales no hay comandos 231/232: las imágenes se controlan desde scripts. La auditoría registra una lista vacía, no coordenadas omitidas.

Durante esta continuación otra tarea modificó Graphics y su manifiesto de coherencia. Se conservaron esas modificaciones. Sus ajustes de ancla corrigen 54 celdas de cuatro hojas; se retiró la compensación temporal en Sprite_Character para evitar una doble corrección. El verificador de arte comprueba dimensiones, ocupación y anclas contra el respaldo. El verificador general admite cambios de arte únicamente cuando coinciden con el hash del manifiesto, y sigue detectando cualquier escritura durante la prueba.

## Cómo repetir las pruebas

Desde la raíz del proyecto, sin red ni editor:

```powershell
node diseno/herramientas/comun/auditar_jugabilidad.mjs
node diseno/herramientas/comun/diagnosticar_lavabo.mjs
# Comparación histórica opcional: termina con código 1 porque encuentra 38 errores antiguos.
node diseno/herramientas/comun/auditar_jugabilidad.mjs --datos diseno/respaldos/antes_jugabilidad/Data --nombre auditoria_jugabilidad_antes
python diseno/herramientas/comun/verificar_hd.py
& 'D:/DevTools/ruby/rubyinstaller-3.3.6-1-x64/bin/ruby.exe' diseno/herramientas/comun/simular_fase45.rb
python diseno/herramientas/arte/verificar_coherencia.py
python diseno/herramientas/comun/verificar_proyecto.py --informe
node diseno/herramientas/comun/render_captura.mjs 2
```

Tras modificar fuentes: `node diseno/herramientas/comun/instalar_scripts.mjs --aplicar` (crea su propio respaldo), seguido de `node diseno/herramientas/comun/inspeccionar.mjs` para renovar los inventarios auxiliares. El simulador de progresión carga ahora Data y Scripts actuales mediante Marshal, no el contenido histórico del snapshot; normaliza las cadenas UTF-8 solo para Ruby moderno del arnés.

## Alcance y pendientes reales

Resultado final de esta continuación: verificador general **0 errores**, HD **55 fuentes / 0 errores**, jugabilidad **143 comprobaciones de proveedores / 0 errores bloqueantes**, coherencia de arte **933 comprobaciones / 0 fallos** y recorrido simulado con `OK FIN`. Los archivos protegidos permanecieron idénticos durante la última verificación. Informes: [proyecto](../../verificaciones/verificacion_organizacion.json), [HD](../../verificaciones/hd_verificacion.json), [recorrido](../../verificaciones/verificacion_simulada_fase45.txt), [arte](../../verificaciones/verificacion_coherencia_arte.json).

La auditoría determinista recorre 32 mapas y 443 páginas con BFS desde System y destinos de transferencia explícitos. Reproduce las tres capas, bits direccionales, prioridades, eventos con gráfico y through, tile de evento, bush y counter. Los destinos de escondites se distinguen de las entradas de exploración. Comprueba proveedores de objetos 1–40, switches requeridos y huellas conocidas. Los productores Ruby son evidencia estática; no se confunden con una ejecución de todas las ramas. La progresión I–VI y finales se complementa con el arnés de recorridos, que automatiza elecciones y combate y no acredita destreza manual.

Quedan **2.349 advertencias heurísticas** de superposición/páginas que no son errores bloqueantes demostrados. La auditoría no certifica semánticamente todas las imágenes ni todas las combinaciones posibles de estados. No se hicieron transitables paredes para eliminar avisos.

Las pruebas HD incluyen carga del guardado existente, ventanas visibles, mapas en ambos extremos y mapas pequeños sintéticos. Usan dobles gráficos; no prueban fuentes, audio ni render nativo. El intento nativo de esta continuación falló antes de Ruby con **“Could not detect an available audio device”**. Se restauró `mkxp.json` y se comprobó la integridad de ejecutables, configuración y guardado. No hay capturas nativas nuevas de 640×360. La captura de mapa generada es un render estático completo, no una captura de juego.

Pendiente para certificar el concurso: recorrido visual/sonoro en una sesión Windows con audio, incluyendo persecuciones y finales. No se declara esa validación manual como realizada.
