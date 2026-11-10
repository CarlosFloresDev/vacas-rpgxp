# Organización del proyecto

La raíz mezclaba el juego, `CREDITOS_AUDIO.md`, una partida y un respaldo de configuración. `diseno/` mezclaba documentos de los seis actos, sistemas y arte con catálogos JSON, `ui_carga.txt`, docenas de informes `verificacion_*`, auditorías y validaciones. `herramientas/` reunía scripts Python/Ruby/Node de todos los actos, lotes `b_*.json`, logs, snapshot y fuentes temporales extraídas. Había además cuatro carpetas de fuentes, capturas sin categorías y respaldos de varias fases.

Se aplicó la separación descrita en el [índice](../README.md), conservando cada archivo. El [inventario original](../verificaciones/inventario_antes.json) enumera las entradas y el [registro de traslados](../verificaciones/traslados.json) permite localizar cualquier ruta anterior. Los informes de arte que estaban dentro de las fuentes se agruparon en `verificaciones/fuentes/`, respetando sus subcarpetas para evitar colisiones de nombres.

## Fuentes y herramientas

Las fuentes propias corresponden a las posiciones 89–104 de `Scripts.rxdata`. Faltaba la copia numerada de `Vacas_Revision_Luces` (posición 98): ahora es `10_revision_luces.rb`. BajoCiudad, Interfaz, IntroFeka, Matanza, Reydios y Cinematicas pasan a los números 11–16. El [manifiesto](../scripts/manifest.json) es la correspondencia oficial; las referencias de los instaladores se actualizaron.

Tres fuentes antiguas no coincidían con lo instalado: Veneno, Matadero y VN. Sus versiones anteriores quedan en [archivo/scripts_anteriores/](../archivo/scripts_anteriores/). Las fuentes vigentes se extrajeron de las secciones instaladas y solo recibieron cabeceras de comentario. La comparación de tokens de Ruby comprueba que no se cambió su lógica. No se reinstalaron fuentes ni se escribió en `Data/Scripts.rxdata`.

Se centralizaron la resolución de raíz y las importaciones Python en `rutas.py`, y la raíz de Node en `proyecto.mjs`. Se añadió un instalador único para las fuentes actuales, que funciona como vista previa por defecto. Los instaladores y verificadores de cada fase siguen disponibles porque sus precondiciones, alcance y respaldos son diferentes. El verificador general vigente se llama `verificar_proyecto.py`.

Se actualizaron rutas de documentos, manifiestos, catálogos, créditos, progreso, herramientas, lotes y capturas. Los respaldos mantienen sus rutas internas históricas: reescribirlas alteraría las instantáneas. El comprobador de enlaces valida los documentos activos, con anclas, y excluye esos respaldos y los antecedentes de `archivo/`.

## Conservado y límites

`Save1.rxdata` permanece en la raíz para Cargar. `Vacas.cfg` conserva exactamente los bytes encontrados, incluidos los cambios que ya tenía el usuario. Su `.bak` está en `archivo/`. `.git` no recibió escrituras. Los respaldos de `diseno/respaldos/` no se movieron ni editaron. El respaldo oculto `.mcp-backup/` y las carpetas ocultas del MCP en Data conservan su ubicación operativa.

`Data/.mcp-backup/` no estaba versionado (`git ls-files Data/.mcp-backup` vacío); se mantuvo su exclusión. `.gitignore` cubre cachés Python, `*.pyc`, `*.tmp`, logs y las salidas temporales del inventario. Los informes, fuentes y antecedentes organizados pueden versionarse normalmente.

Algunos manifiestos de generaciones mencionan destinos intermedios de composición, como `arte_final_intermedio.png`, que no son recursos instalados. Se conservan como recetas históricas; el validador de assets del juego comprueba las referencias efectivas de los datos. Las herramientas de nube y reconstrucción no se ejecutaron: esta tarea valida lectura, inventario, sintaxis y render, sin regenerar contenido ni alterar la lógica del juego.
