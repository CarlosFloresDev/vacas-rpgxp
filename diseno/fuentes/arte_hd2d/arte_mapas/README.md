# Pasada de arte de mapas1–16

Fuentes: ocho generaciones reales con la herramienta integrada `image_gen`, conservadas como `*_fuente.png`. Prompts exactos y rutas de generación en `generaciones.json`; hashes, adaptaciones, fuentes aprobadas conservadas y respaldos en `manifest.json`. Pillow solo adapta, cuantiza y compone imágenes. No se usa GPU local ni se genera ilustración con formas PIL.

`arte_mapas.py prepare` reconstruyó la distribución histórica en memoria, contrastó las16 hojas píxel a píxel y sus índices, y guardó `layout.json`, `floor_NN.png`, `props_old_NN.png` y `overlay_old_NN.png`. Utiliza el snapshot anterior a la revisión y las dimensiones originales de objetos únicamente para reproducir anclas. No vuelve a ejecutar los constructores históricos sobre Graphics/Data.

El respaldo `diseno/respaldos/antes_arte_mapas` conserva Data completo,16 hojas locales, siete hojas RTP y el objeto de luz RTP (bajo `RTP/`), auditoría anterior y hashes de archivos protegidos. Se mantiene el primer respaldo por ruta. Los nuevos PNG locales de autotiles/luz sobreponen el RTP sin modificar su instalación.

## Reproducción desde la raíz

El respaldo y las fuentes seleccionadas deben existir. No regenerar los renders «antes» sobre los gráficos ya sustituidos; los originales están guardados en capturas y respaldos.

```powershell
python -X utf8 diseno/herramientas/arte/arte_mapas.py install
python -X utf8 diseno/herramientas/arte/arte_mapas.py extras
python -X utf8 diseno/herramientas/arte/arte_mapas.py floors
python -X utf8 diseno/herramientas/arte/arte_mapas.py corrections
node diseno/herramientas/arte/verificar_arte_mapas.mjs --apply
Push-Location diseno/herramientas
node inspeccionar.mjs
Pop-Location
node diseno/herramientas/comun/rx.mjs --batch diseno/archivo/lotes/b_arte_mapas_despues.json
python -X utf8 diseno/herramientas/arte/laminas_arte_mapas.py
node diseno/herramientas/comun/rx.mjs validate_assets
python -X utf8 diseno/herramientas/arte/auditoria_arte_final.py
python -X utf8 diseno/herramientas/arte/finalizar_arte_mapas.py
```

`install` recompone el desorden con las mismas huellas y recorta únicamente a los índices que ya estaban asignados. `extras` preserva las máscaras y dimensiones de los siete autotiles, iguala las clases de aristas16px que eran idénticas en el original y verifica sus equivalencias; el agua conserva cuatro fases, de material generado. `floors` corrige nueve índices de suelo con rampas de32 colores sin dithering y bordes opuestos idénticos. `corrections` conserva la camilla aprobada, reemplaza su mancha PIL por sangre generada y coloca las pantallas de lámpara en la huella original. El banco también procede del atlas aprobado de22–32; el sofá y la camilla girada de la fuente nueva se descartaron.

No se amplían hojas, no se añaden índices y no se escribe ningún mapa. La única escritura de Data son tres cadenas `battleback_name` de Tilesets53–55, con Marshal binario y comparación semántica estricta. Todas las tablas de pasabilidad, prioridades y terreno, y todos los demás datos conservan sus bytes.

## Revisión

Se abrieron las16 comparaciones nativas `diseno/capturas/arte/arte_mapas_comparacion_NN.png`, se corrigieron repetición/ruido de suelos, rampas de gris, banco, camilla y pantallas de luz, y se abrió el resumen con máscaras reales `../../../capturas/arte/arte_mapas_luz_resumen.png`. El informe registra125.280 pasos direccionales idénticos,47 archivos Marshal válidos y1.051 referencias de gráficos/audio existentes. No quedan excepciones RTP por unión en esta pasada. Los materiales industriales, personajes y objetos ya aprobados se conservan.

Los renders muestran la primera página gráfica de eventos y marcadores MCP azules, que no aparecen en el juego. Las vistas con luz usan las máscaras existentes; no simulan tono narrativo ni niebla animada. No se inició ni cerró Game.exe. Vacas.cfg y Scripts.rxdata conservan sus hashes; no se accedió a .git.
