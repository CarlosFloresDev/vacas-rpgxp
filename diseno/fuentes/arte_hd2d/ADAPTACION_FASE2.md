# Reproducción del arte instalado

Generación: `image_gen` integrado en la nube. Fuentes originales PNG y prompts exactos conservados en esta carpeta; referencias en `referencias/`. No se usaron GPU local, SD ni ComfyUI. Los descartes llevan nombre explícito y no se instalan.

`PROMPTS_FASE2.json` conserva los lotes previos. `PROMPTS_CONTINUACION.json` reúne las 70 llamadas de esta continuación: 63 salidas aceptadas, tres descartes visuales y cuatro rechazos sin imagen. Los archivos `prompt_*.json` guardan también cada llamada individual. Las referencias de entrada antiguas que ya fueron sustituidas apuntan al respaldo inmutable del mismo PNG.

Los manifiestos `lote_*.json` contienen los 67 destinos de fase 2 y sus parámetros. Para readaptar un lote:

```powershell
python diseno/herramientas/comun/adaptar_arte.py --batch diseno/fuentes/arte_hd2d/lote_guernsey.json
```

No regenerar mapas, BD, eventos ni scripts. El adaptador solo escribe PNG en carpetas gráficas RGSS1 autorizadas y conserva el primer respaldo.

- `character`: 4×4 poses; `source_rows`/`source_columns` opcionales separan filas/columnas desiguales de una fuente generada. No reordenan direcciones.
- `indexed`, mediante JSON: `layout_source` es el respaldo; `size` y `cell` fijan tamaño e índices. El modo `fit` coloca cada objeto dentro de la caja ocupada original, dejando vacíos los índices vacíos. No interpreta una hoja de objetos como caminata.
- `indexed_mode: resize`: escala cada celda sin recortarla; permite conservar paneles de dos celdas contiguas. `preserve_alpha` mantiene la máscara técnica; `layout_mix` mezcla una fracción documentada del layout para conservar geometría de detalle. Tileset: 20%; windowskin: 15%. El resto usa fuente generada directa.
- `repeat_source`: repite una única fuente en cada celda ocupada. La furgoneta conserva los dieciséis fotogramas idénticos del original.
- Humo de Guernsey y alas de moscas conservan semitransparencia. Las expresiones reutilizan su neutral fuera de la máscara facial.

Auditoría reproducible, sin escribir Data ni scripts:

```powershell
python diseno/herramientas/comun/adaptar_arte.py --review-inventory diseno/fuentes/arte_hd2d/inventario_fase2.json
```

Comprueba los 72 PNG frente al inventario y respaldo: tamaños, modos, celdas, ocupación vacía/llena de hojas indexadas, anclas, máscaras técnicas, igualdad de celdas repetidas y hashes protegidos. Escribe `../../verificaciones/fuentes/verificacion_fase2.json` y las tres láminas 1×/2× de `diseno/capturas/`. No certifica animación ni mezcla de tonos dentro de Game.exe.
