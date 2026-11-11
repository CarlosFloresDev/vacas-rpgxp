# Coherencia de arte — cierre incremental

11 de noviembre de 2026. Continuación del trabajo parcial de `arreglos-concurso` (b2fb7a4), sin restaurar respaldos ni rehacer el proyecto. Esta intervención escribe solo Graphics y herramientas, fuentes, informes y láminas de diseno. No modifica Data ni diseno/scripts y no hace commits. Los cambios simultáneos de esas rutas pertenecen a otra tarea.

## Criterios aplicados

- Mapa: perspectiva elevada 3/4, superficies superiores visibles, luz arriba-izquierda, sombras frías y contorno oscuro selectivo. Personajes en celda habitual32×48; silueta visible34–48px. La Biblia aprobada prevalece sobre los textos provisionales: Steven lleva camisa marrón y los retratos/sustos conservan su acabado ilustrado.
- Characters direccionales:4×4, abajo/izquierda/derecha/arriba. Los objetos indexados no son ciclos de marcha: cada índice conserva su función. Una TV, una rejilla o una lámpara frontal no debe convertirse en cuatro direcciones de un personaje.
- Ancla: conservar el borde inferior opaco original de CADA celda, no llevar todas las figuras hasta el borde del PNG. Medición con alpha>=128. No compensar además en RGSS. Vacas:76 en celda80; furgoneta:61 en celda64; muebles:63/64 según índice.
- Bovinos adultos: longitud lateral54–68px, altura lateral objetivo38px y frontal hasta48px; centrados en su celda. Una celda48 no permite alojar una longitud de58px: esa limitación requiere asignar otra hoja en Data, no recortar el animal.
- Props pequeños10–16px; cama58px, armario52–56px, banco28px alto. No todos los objetos deben tener la misma altura. Recortes explícitos por pieza para evitar contaminación de celdas en una fuente generada.
- NEAREST para adaptar sprites; cuantización sin dithering, alpha binario en plano jugable. Saturación media máxima0,55 y alpha parcial máximo1% en Characters/Tilesets/Autotiles/Icons; humo, luz y retratos no usan ese límite. Se informa brillo medio sin inventar un mínimo global que invalide la oscuridad narrativa.
- Tilesets: ancho256, índices/celdas32px intactos. Autotiles conservan geometría y fases. Pantallas640×480 conservadas, foco dentro de la franja central640×360 (y60–420); las láminas marcan el recorte para revisión.

## Trabajo conservado y terminado

Se conservaron las seis fuentes image_gen y las adaptaciones de la pasada parcial: furgoneta, muebles, dos vacas, suelo y título. El manifiesto completo registra60 recursos; es la autoridad de nombres, tamaños y hashes, no una afirmación de que todos sean dibujos nuevos.

| Grupo | Resultado |
|---|---|
| Furgoneta384×256 | Cuatro vistas distintas, techo visible y acabado industrial sucio. Corrección adicional de las16 anclas:64→61. No cambian ruedas, escala ni rejilla durante el cierre. |
| Vaca y vaca_canela320×320 | Fuentes regeneradas conservadas, paleta apagada, anatomía más pesada; laterales55–58px de longitud y38px de alto.32 anclas corregidas80→76. |
| Muebles128×256 | Regeneración anterior conservada: TV y variantes por índice, armarios, nevera, bañera, aseo, lavabo, silla y mesa. Seis anclas corregidas64→63. |
| Laboratorio128×256 | Nueva regeneración con image_gen integrado: cama, biombo, microscopio, frascos, muestras, suero, banco, lámpara, archivo, armario y lavabo; adaptación CPU por16 recortes explícitos, escala por función,64 colores y apoyo original. Fuente y prompt guardados en el proyecto. |
| Cosas / matadero / alcantarilla | Conservada la adaptación anterior de paleta y alpha por índice. No se altera la distribución de tarros, papeles, carne, balanza, ganchos, rejillas, válvulas ni puertas. |
| Guernsey / Junco / Muesca | Paleta de la pasada parcial conservada. Las variantes `_80` preparadas ahora tienen laterales58×38px; sus referencias de mapa siguen pendientes. Las hojas48×48 originales se mantienen por contrato. |
| Tilesets / autotiles / iconos | Limpieza selectiva anterior de alpha y saturación conservada. Suelo de alcantarilla: índices384/385 y399, menor contraste y bordes enlazados; los otros13 tiles permanecen idénticos al respaldo. No se cambian índices/pasabilidad. |
| Título | Regeneración previa640×480 conservada; título y televisor dentro del recorte panorámico. |
| Sustitutos de reserva | Siete hojas civiles y siete battlers preparados desde arte propio; dos hojas de animación con ancho960 preparadas. Las animaciones siguen siendo RTP y se identifican como tales. |

Manifiesto y fuentes: [coherencia_arte](../../fuentes/coherencia_arte/manifest.json). Prompt nuevo exacto: [laboratorio](../../fuentes/coherencia_arte/prompt_laboratorio.txt). Los prompts de las seis generaciones anteriores no estaban guardados en este lote; se conservan sus fuentes y hashes sin inventar su texto.

## Revisión visual por categoría

Se revisaron las láminas de Characters (todas las hojas, frontal/lateral a escala real y cuatro filas en catálogo), Tilesets y Autotiles, Battlers, Battlebacks, Pictures, Icons, Titles y Windowskins; Panoramas no contiene PNG locales. También se conservan láminas de Animations, Fogs, Gameovers y Transitions.

Las18 láminas de identidad comparan sprite, retratos, battlers cuando existen y referencia de producción cuando está disponible. Se revisaron Steven, Madre, Lucy, Cripps, Perro, Guernsey, Junco, Muesca, Elena, Benito, Rubio/Sierra, Encarna, Chato, Molina, Anselmo, Remedios, Borracho y Reclutador. Se conservan la camisa marrón, bata mostaza, tarro de Lucy, delantal de Cripps, vestuario industrial y marcas bovinas. Rubio/Sierra sigue siendo una hoja compartida, limitación registrada en la Biblia.

Los fondos de batalla y los sustos comparten materiales industriales y luz focal; conservan el acabado ilustrado aprobado. Los encuadres centrales mantienen ojos, bocas, figuras y zonas de acción; no se ha aplicado una pixelación global que destruya los retratos aprobados. Windowskins conservan geometría XP y lectura del cursor. La lámpara185-Light02 ya es arte propio de la pasada de mapas, aunque conserve un nombre RTP.

Las láminas de catálogo son miniaturas, no una prueba de cada píxel ni una animación en motor. Los renders de mapa02/17 proceden de la pasada parcial y se conservan como evidencia histórica; no se presentan como capturas nuevas del motor. No se ejecutó Game.exe ni se instalaron scripts en esta continuación.

## Validación final y pendientes reales

- [Verificación de contratos](../../verificaciones/verificacion_coherencia_arte.json):933 comprobaciones,0 fallos. Comprueba hashes de manifiesto y respaldos, tamaño de todos los446 PNG iniciales, ocupación/ancla de cada celda reemplazada, otros13 tiles de alcantarilla intactos y continuidad horizontal/vertical del nuevo suelo.
- [Auditoría completa](../../verificaciones/auditoria_coherencia_arte.json):466 PNG locales medidos.261 sin avisos;205 conservan incidencias explícitas:200 originales RTP,2 variantes de animación todavía derivadas de RTP y3 bovinos pequeños cuya ampliación exige cambiar la hoja asignada en Data. Las56 incidencias de alpha,7 de saturación y2 geometrías de animación heredadas están dentro del catálogo RTP, no se han borrado del informe para obtener un falso cero.
- Todos los reemplazos propios integrados que pueden cumplir la escala dentro de su geometría están dentro de las reglas medidas. Las variantes adultas `_80` están preparadas dentro de rango. **El catálogo completo todavía no está todo dentro de rango**: el cierre de reservas y las tres asignaciones bovinas requieren la integración indicada abajo.
- [CAMBIOS_DATA_PENDIENTES](CAMBIOS_DATA_PENDIENTES.md) contiene IDs exactos de actores, mapas/eventos/páginas bovinas, animaciones, limitación Rubio/Sierra y catálogo RTP con referencias de lectura. Los mapas actuales usan los tilesets propios52–70; los50 atlas RTP siguen en registros de reserva. No se confunde presencia en BD con aparición confirmada en una escena.

Durante el trabajo, la tarea paralela añadió temporalmente compensaciones de ancla en16_cinematicas.rb y en el verificador. Tras avisar del conflicto, esa compensación dejó de aparecer en la fuente y el verificador volvió a comparar anclas PNG directamente. La [lectura de las106 secciones instaladas](../../verificaciones/coherencia_anclas_instaladas.json) confirma que tampoco permanece el módulo de compensación en Scripts.rxdata. Esta tarea no editó esos scripts. La lista de pendientes vuelve a comprobar el estado actual al regenerarse.

## Reproducción sin tocar Data

Desde la raíz:

```powershell
python -X utf8 diseno/herramientas/arte/continuar_coherencia.py
python -X utf8 diseno/herramientas/arte/auditar_coherencia.py
python -X utf8 diseno/herramientas/arte/verificar_coherencia.py
python -X utf8 diseno/herramientas/arte/documentar_coherencia.py
python -X utf8 diseno/herramientas/arte/laminas_coherencia.py
```

La continuación es incremental e idempotente: conserva el arte actual, corrige anclas y adapta únicamente la nueva fuente de laboratorio y las variantes adultas. `aplicar_coherencia.py` conserva la producción histórica completa y no es necesario volver a ejecutarlo para cerrar esta continuación. La auditoría inicial no se sobrescribe; no usar `--inicial` sobre el estado final.

Respaldos originales preservados en [antes_coherencia_arte](../../respaldos/antes_coherencia_arte/Graphics/). Las variantes `_80`, nuevas en la primera pasada, tienen además respaldo de su estado previo a este ajuste. Las herramientas leen Marshal y fuentes de scripts; no importan instaladores ni arrancan el juego.

Láminas actualizadas: `diseno/capturas/arte/coherencia_<categoría>.png` y partes numeradas; [personajes1:1](../../capturas/arte/coherencia_personajes_1x.png), [personajes×3](../../capturas/arte/coherencia_personajes_3x.png), [laboratorio ampliado](../../capturas/arte/coherencia_laboratorio_detalle.png). La escala es real en las láminas de personajes; los catálogos antes/después ajustan miniaturas al recuadro.
