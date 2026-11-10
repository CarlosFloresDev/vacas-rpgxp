# Vacas HD: mkxp-z y formato panorámico

## Ejecutar

Abrir **`Vacas.exe`** en la raíz del proyecto. Es la build oficial Windows x64 de mkxp-z que estaba en `D:/DevTools/mkxp-z`, copiada sin modificar; su identificador incluido en el binario es `2.4.2/37a04d1`. Necesita Windows de 64 bits, salida gráfica y un dispositivo de audio disponible.

Arranca a pantalla completa. **Alt+Enter** alterna pantalla completa/ventana; se admiten ambos Alt. La ventana inicial es 1920×1080. F1 abre las asignaciones del motor y F2 muestra los FPS. Al perder el foco puede bajar la frecuencia de actualización; las comprobaciones visuales deben hacerse con el juego enfocado.

`Game.exe`, `Game.ini` y `RGSS104E.dll` siguen intactos: el editor usa el motor original, con lienzo de 640×480. Ambos ejecutables usan `Data/Scripts.rxdata`, `Save1.rxdata`…`Save4.rxdata` y `Vacas.cfg`. Los atajos de actos del índice se conservan. No ejecutar ambos motores para escribir la misma partida simultáneamente.

## Configuración de esta build

La referencia completa suministrada con el ejecutable está conservada en [mkxp-build-reference.jsonc](mkxp-build-reference.jsonc). El archivo activo es [mkxp.json](../../../mkxp.json), JSON estricto, sin comentarios.

| Clave | Valor y propósito |
| --- | --- |
| `rgssVersion`, `gameFolder`, `execName` | `1`, `.`, `Game`: continúa leyendo `Game.ini`. |
| `windowTitle` | `Vacas`. |
| `defScreenW`, `defScreenH`, `fullscreen` | 1920, 1080, true: tamaño de ventana y arranque a pantalla completa. No definen el lienzo lógico. |
| `smoothScaling`, `smoothScalingDown`, `bitmapSmoothScaling` | 0: vecino más cercano. |
| `integerScalingActive`, `integerScalingLastMile` | true, false: solo múltiplos enteros, sin interpolación adicional. |
| `fixedAspectRatio`, `vsync`, `anyAltToggleFS` | true. |

El primer script detecta **`$MKXP`**, la variable que expone esta build, y también admite `System.is_mkxp?` si otro motor compatible la ofrece. Solo entonces llama `Graphics.resize_screen(640,360)`. En un monitor 1920×1080 el escalado es ×3 exacto. En otros tamaños pueden aparecer bandas para conservar píxeles cuadrados y escala entera.

## Interfaz y compatibilidad

`Vacas_HD` centraliza `Graphics.width` y `Graphics.height`, con respaldo 640×480 en RGSS104E. Las medidas de referencia de los diseños anteriores se convierten allí; las duraciones, colores, coordenadas del mundo y tamaños originales de assets no se convierten.

- Título: logotipo a la izquierda, comandos a la derecha y ayuda al borde inferior. Pausa, ajustes, diario, inventario, archivos, aviso, game over y créditos usan el alto disponible. Las listas largas desplazan sus filas y los créditos calculan cuántas líneas caben por página.
- Intro Feka: el conjunto de logotipo/gota/suelo permanece centrado sin alterar sus tiempos. Cinemáticas y tarjetas: fondos con cover uniforme, textos anclados abajo y menú centrado.
- VN: se conservan cuatro líneas, decisiones y entrada numérica; la caja se ancla abajo, los retratos se reducen uniformemente y sus placas siguen la caja. En combate la caja permanece arriba.
- Combate: viewport, fondo, enemigos, flechas y actor se recolocan; comandos y estado se anclan al pie. Fondos `ui_*` y sustos de pantalla completa usan cover centrado, sin deformación. El recorte de un fondo 4:3 en 16:9 es intencional.
- HUD: queda dentro del lienzo y cambia a la esquina superior si el jugador ocupa su zona inferior. Máscaras de luz propias y nieblas siguen ancladas al mundo; no se comprimen las máscaras de mapas. La linterna crea un lienzo del doble del tamaño actual y conserva su centro sobre el jugador.
- Corte, cinta y noria: viewport y posiciones verticales se adaptan; se conservan velocidades, zonas de acierto y resultados. Las ventanas estándar conservan cabeceras legibles y dan a sus listas el espacio restante. El teclado de nombres ajusta también sus filas y cursor.
- Cámara: usa el ancho y alto real en unidades del mapa (cuatro unidades por píxel), incluidos límites no enteros en casillas. Un mapa de 20×15 muestra 20×11,25 casillas y permite recorrer toda su altura. Cargar una partida recentra la cámara para eliminar el desplazamiento del otro formato.

La auditoría de **todas** las secciones originales de `Scripts.rxdata` y de las fuentes propias no encontró llamadas a `Win32API`, `ShowWindow`, `GetAsyncKeyState` ni lecturas propias de `Game.ini`. Los atajos ya usaban Input: ahora se centralizan en `Vacas_HD.key?`. En mkxp se usan las constantes numéricas RGSS1 de Shift/Ctrl/Alt y los estados SDL de Q/W (20/26); en Game.exe se conserva el mapeo A/Ctrl/Alt/L/R. Los símbolos de botones RGSS3 no se usan en modo RGSS1.

No se cambió el formato de guardado ni su ruta. Marshal conserva las clases RGSS y los datos existentes. Se incorporaron 265 archivos del RTP referenciados por datos/scripts que faltaban localmente; [lista exacta](../../verificaciones/hd_rtp_incluido.json). Los assets RTP mantienen su licencia de RPG Maker XP, independiente de la licencia de mkxp-z.

## Fuentes, instalación y respaldo

El respaldo previo completo de Scripts y fuentes está en [antes_hd](../../respaldos/antes_hd/), con sus rutas originales. También se conservó el índice anterior. No se reemplazaron los gráficos existentes.

Hay 16 secciones propias y 39 secciones estándar adaptadas en `diseno/scripts/motor/`. El [manifiesto](../../scripts/manifest.json) identifica las 55 por nombre e índice; el instalador existente las reemplaza sin agregar/reordenar secciones. `Main` conserva su arranque original.

```powershell
node diseno/herramientas/comun/instalar_scripts.mjs
node diseno/herramientas/comun/instalar_scripts.mjs --aplicar
python diseno/herramientas/comun/verificar_hd.py
```

Para volver completamente al estado previo, restaurar `Data/Scripts.rxdata`, `diseno/scripts/` y el índice desde `antes_hd/`. Los archivos nuevos del motor HD pueden permanecer sin afectar a Game.exe.

## Verificación realizada y límites

[Informe reproducible](../../verificaciones/hd_verificacion.json): sintaxis de las 55 fuentes con Ruby 3.3.6, correspondencia de tokens con las secciones instaladas, carga Marshal de 324 `.rxdata` (incluidos respaldos y guardado existente), y simulación de carga de las 105 secciones anteriores a Main. El código de producción conserva sintaxis Ruby 1.8; no se abrió Game.exe para comprobar su runtime.

[Simulación 640×360](../../verificaciones/hd_simulado_360.txt) y [640×480](../../verificaciones/hd_simulado_480.txt): escenas propias y estándar, VN, combate, minijuegos, todos los mapas en ambos extremos y todas las clases de ventana instanciables. [comprobar_limites_hd.rb](../../herramientas/comun/comprobar_limites_hd.rb) recorre las clases de escena/ventana y detecta ventanas visibles que salgan del lienzo. Estas pruebas cargan los datos Marshal reales y usan dobles de las primitivas gráficas: no prueban render, métricas de fuente, audio ni foco.

[Assets sin RTP externo](../../verificaciones/hd_assets_sin_rtp_final.json): 1051 referencias comprobadas, ninguna ausente. [Integridad](../../verificaciones/hd_integridad.json): Game.exe, RGSS104E.dll, Game.ini, Vacas.cfg y Save1.rxdata idénticos antes y después del arnés. No se tocó `.git` ni se cerró ningún Game.exe.

Se lanzó **una sola vez** Vacas.exe mediante [probar_hd.mjs](../../herramientas/comun/probar_hd.mjs). El motor se detuvo antes de ejecutar Ruby: **“Could not detect an available audio device.”** Véase [log nativo](../../verificaciones/hd_motor.log). La sesión tampoco permitió capturar la pantalla de su diálogo de error (`screen grab failed`). Solo se terminó el proceso Vacas.exe creado por el arnés y se restauró mkxp.json. No existen capturas nativas HD de título, diálogo, combate o mapa; no se sustituyeron por imágenes simuladas.

Pendiente: ejecutar el arnés nativo en una sesión Windows con audio y escritorio accesibles, revisar las capturas `diseno/capturas/interfaz/hd_*.png`, comprobar visualmente cortes de texto/retratos/fondos y recorrer los actos. El arnés evita escribir Vacas.cfg y partidas. Para terminar su espera final puede crearse `diseno/verificaciones/hd_terminar`.

## Licencia y atribución del motor

**La licencia que acompaña a esta build dice GNU GPL versión 3**, aunque la descripción inicial la identificaba como GPLv2+. Se conserva íntegra como [LICENSE-mkxp-z.txt](../../../LICENSE-mkxp-z.txt); no se ha relicenciado el ejecutable ni se ha cambiado su contenido.

mkxp-z, Copyright © 2013–2023 sus colaboradores, incluidos **Amaryllis Kulla, Struma, Splendide Imaginarius y otros**. Proyecto y fuentes: [mkxp-z](https://github.com/mkxp-z/mkxp-z), [revisión incluida en el binario](https://github.com/mkxp-z/mkxp-z/tree/37a04d1). La atribución también aparece en los créditos del juego. Los wrappers distribuidos conservan sus avisos CC0; `stdlib/` conserva los archivos de la build oficial.

Antes de preparar una publicación pública, acompañar el paquete con el código fuente correspondiente a esta build, sus componentes y avisos de distribución: esta copia local conserva la licencia y la referencia a fuentes, pero no incluye un archivo completo de fuentes del motor. La licencia del motor no convierte los assets de RPG Maker XP ni los recursos de terceros en recursos GPL.
