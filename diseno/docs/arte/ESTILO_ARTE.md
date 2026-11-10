# VACAS — dirección de arte HD-2D / Fase 1

Muestra del 9 de noviembre de 2026, pendiente de aprobación artística. Referencias narrativas: PLAN.md, SISTEMAS.md, ACTO_I.md, ACTO_II.md y ENEMIGOS.json. La nueva dirección de gore amplía la representación visual de las visiones; no cambia los fundidos, eventos ni el argumento. Las antiguas referencias a ComfyUI/Stable Diffusion son históricas: **esta producción usa image_gen, nunca GPU local**. Pillow solo adapta y retoca píxeles en CPU.

## Dirección y lectura en RPG Maker XP

Todo diseño visual es propio de Vacas. HD-2D describe una combinación de píxel legible, volumen e iluminación; no autoriza copiar personajes, vestuario, sprites o escenarios de Octopath Traveler ni Square Enix. El mundo es doméstico e industrial, húmedo y hostil, sin ornamento de fantasía heroica.

- Resolución de juego 640×480; tiles de 32 px. Evaluar siempre a 1×, ampliar a 3× con vecino más próximo para inspección. Una imagen grande reducida no basta: corregir silueta, cara y articulaciones al tamaño final.
- Personajes humanos de mapa: cuerpo completo de aproximadamente 2,5 cabezas; cabeza legible, hombros y manos separados del torso, pies reconocibles. Steven cabe en celda 32×48. Mantener las dimensiones particulares de madre, Cripps, animales y objetos existentes.
- Contorno oscuro selectivo: oscuro en el lado de sombra y bajo brazos, interrumpido en bordes iluminados. El contorno automático de 1 px es opcional y completo; requiere selección manual para el acabado selectivo.
- Tres o cuatro tonos principales por material, agrupaciones deliberadas de píxeles; evitar ruido y dithering. Luz lateral fuerte, normalmente arriba-izquierda; borde frío fino en el lado opuesto. No invertir la iluminación al reflejar una pose.
- Sombras de contacto pequeñas bajo pies y muebles; no incluir un gran halo negro en cada celda. El pie es el ancla de desplazamiento de XP. Animación 4 columnas, filas abajo/izquierda/derecha/arriba; pasos alternos con dos fases de paso. El adaptador conserva el orden: no adivina ni inventa direcciones.
- Profundidad con primer plano oscuro, plano jugable nítido y fondo de menor contraste; oclusión por paredes, canales y tuberías. La perspectiva y los ganchos guían hacia el foco.
- Bloom simulado con Pictures de luz de baja opacidad y bordes suaves, limitado a lámparas y reflejos; neblina mediante Fogs con desplazamiento lento. Viñetado en Picture 640×480 con centro transparente. Reservar imagen 98 para sustos; planificar otros slots antes de integrar. Esta fase no modifica scripts, eventos ni instala efectos nuevos.
- No aplicar desenfoque al plano jugable para fingir profundidad. Evitar que niebla, tono de veneno y viñeta sumados oculten puertas o pistas. Revisar día, noche y veneno alto en Fase 2.

## Paletas por zona

Las listas siguientes son las paletas de cuantización de `../../herramientas/comun/adaptar_arte.py`. Constituyen una opción estricta; retratos, carne y luces pueden conservar rampas adicionales coherentes cuando 16 colores eliminen información. Sin dithering.

| Zona | Sombras → luces / materiales |
|---|---|
| Piso, nicotina | `#141318 #29252A #494039 #71634B #A18A59 #D1BA7B #E8D9AA` |
| Piso, frío / piel / sangre | `#444B50 #77848A #A6B8BE #533E38 #946A55 #C69878 #E4C4A0 #350F19 #701D2C` |
| Matadero, clínico | `#10171D #263239 #465557 #738585 #ADC0BD #DFE7DC #F3F0D9` |
| Matadero, carne / sangre / hueso | `#251018 #4B1020 #78192A #A42A39 #CE5259 #E8908A #694139 #AA7656 #D4B48A` |
| Alcantarillas, verde negro | `#090F12 #142422 #243C34 #3D5744 #62745A #8B9870 #BBC19A` |
| Alcantarillas, agua / carne | `#394C54 #6C8B91 #ACCDCA #30121B #641B2C #9B3442 #C76768 #927461 #D2B996` |

La calle conecta el gris frío y la nicotina; las cámaras frías usan el tramo frío del matadero. La sangre ocupa un área focal, no un filtro rojo uniforme.

## Gore: materiales y puesta en escena

Mostrar sangre oscura saturada, coágulos, músculo abierto, grasa, huesos rotos y vísceras identificables; cuerpos deformes en las alucinaciones, canales y restos de matadero. Sangre fresca: volumen burdeos y reflejos pequeños; seca: costras casi negras y bordes marrones. Carne húmeda: fibras agrupadas y brillo especular estrecho, nunca blanco repartido como ruido. Hueso: marfil sucio, sombra ocre y fracturas angulares. Vísceras: masas tubulares con peso y pliegues, sin confundirlas con tentáculos decorativos.

La deformación expresa control y culpa: manos que sujetan, costillas-barrotes, cuernos-tuberías, corona-ganchos. Mantener foco y silueta: el detalle visceral no debe destruir la lectura. Los NPC cotidianos siguen siendo personas; sus versiones mentales concentran las alteraciones. Perro debe conservar ternura y discapacidad, sin convertirlo por defecto en monstruo. **Sin contenido sexual, genitales, violencia sexual ni erotización.**

## Biblia visual de personajes

Los rasgos de indumentaria nuevos son propuestas artísticas; deben fijarse al aprobar la muestra. Conservar identidad entre sprite, busto, expresiones y battler.

| Personaje | Descripción para insertar en prompts |
|---|---|
| Steven | 25 años, delgado y exhausto, pelo negro desordenado, piel pálida, ojos hundidos, camisa gris gastada, pantalón carbón y zapatos marrones; postura encorvada. Neutral: vigilancia contenida; miedo: mandíbula tensa y ojos abiertos. Mono: misma cabeza y cuerpo, uniforme de trabajo sucio. |
| Madre / Bestia | Figura ancha y dominante, pelo recogido, bata mostaza, grandes manos; luz nicotina. Neutral: autoridad inmóvil; ira: mandíbula y manos tensas. No confundir corpulencia con deformación monstruosa fuera de la visión. |
| Lucy | Pelo claro recogido, bata pálida, tarro vacío, mirada inquieta y atención obsesiva. Susurro: inclinación leve y labios entreabiertos. |
| Cripps | Capataz corpulento, rapado, cuello grueso, rostro duro y delantal manchado; postura que ocupa el paso. Ira sobria, sin caricatura cómica. |
| Perro / dog | Mestizo tumbado, orejas caídas, ojos castaños cálidos, patas traseras paralizadas; movimiento de arrastre, nunca ciclo humano de caminar. |
| Guernsey | Vaca canela, cuernos curvos, ojo castaño inteligente entre barrotes; hocico húmedo, presencia que observa. Susurro de boca y ojo, sin labios humanos añadidos. |
| Benito | Obrero veterano, canas, arrugas y mono gastado; manos de oficio. |
| Encarna | Obrera de pelo recogido, uniforme blanco desgastado, cansancio contenido. |
| Rubio | Obrero rubio, guantes oscuros, mono blanco, mirada lateral. |
| Chato | Obrero bajo, rostro ancho, nariz achatada, ropa industrial sucia. |
| Sierra | Obrero con máscara protectora, gafas y casco; equipo legible antes que rostro. |
| Remedios | Vecina anciana, pelo blanco, chal oscuro y rostro surcado. |
| Anselmo | Vecino anciano, bigote gris y chaqueta vieja. |
| Molina | Carnicero de bigote, brazos fuertes, delantal rojizo y utensilios de oficio. |
| Borracho | Hombre desaliñado, abrigo largo, barba incipiente y nariz enrojecida. |
| Reclutador | Conductor con gorra, chaqueta y carpeta de contratación; sonrisa burocrática. |
| Transeúnte | Silueta urbana anónima bajo ropa de lluvia gris; poco contraste, sin competir con Steven. |
| Vacas de corral | Anatomía bovina pesada, pezuñas claras en silueta; variante canela del fondo diferenciada sin añadir monstruosidad a la escena cotidiana. |

Los cuatro `vacas_obrero*` son hojas compartidas: confirmar asignaciones de eventos antes de especializarlas. No asumir cinco hojas porque existen cinco retratos de trabajadores.

## Biblia de las nueve visiones

Son alucinaciones de Steven, no combates físicos con los NPC. Nombres y correspondencias proceden de ENEMIGOS.json.

| Archivo / enemigo | Descripción del prompt y sentido |
|---|---|
| enemigo_vaca / La Vaca que habla | Cabeza bovina suspendida, ojo acusador, mejilla desgarrada, músculo cervical, vértebras y lengua larga como cinta de televisión. Dice lo que Steven aún no puede pensar. |
| enemigo_madre / La Madre de yeso | Bata vacía mostaza, rostro de yeso agrietado y manos enormes; carne húmeda en grietas puntuales. Cada grieta es una deuda. |
| enemigo_tunel / Lo del túnel | Forma larga sin rostro, piel húmeda y huesos insinuados en un conducto; ojos al fondo. Lo enterrado espera fuera de la luz. |
| enemigo_sombra_cripps / Sombra de Cripps | Capataz proyectado como sombra deforme, manos y ganchos fundidos, bordes de carne oscura. Control que persiste sin su dueño. |
| enemigo_moscas / Enjambre de moscas | Moscas agrupadas en una cara incompleta, vacío entre grupos y reflejos mínimos. Pensamientos insistentes; conservar transparencia entre insectos. |
| enemigo_guernsey / Guernsey de humo | Vaca canela espectral, cuernos de tubería, humo verde negro y costillas visibles entre jirones. Promesa que acusa; conservar el ojo castaño del NPC. |
| enemigo_canal / Canal en el gancho | Canal suspendida con músculo, grasa y costillas como barrotes; acero frío y goteo oscuro. Miedo a ocupar ese lugar. |
| enemigo_televisor / La Familia de nieve | Tele de los cincuenta, familia de rostros de estática y bocas vacías, cables como tendones. La protección doméstica se vuelve acusación. |
| enemigo_rey / El Rey del cajón | Steven adulto reconocible, corona de ganchos, ropa ensangrentada y postura de verdugo; reflejo fragmentado. Jefe: lo que podría llegar a ser. |

## Plantillas de generación

Añadir a todas: «Diseño visual original de Vacas; pixel art detallado de terror industrial; agrupaciones de píxeles intencionales, contorno oscuro selectivo, 3–4 tonos principales por material, luz lateral fuerte y borde frío discreto; paleta {zona}; sin texto, firma ni marca; sin contenido sexual; no reutilizar assets ni personajes de otras obras». Para variantes usar la imagen aprobada como referencia de identidad y enumerar lo que no cambia.

### Character sheet

«Hoja de caminar de {personaje: descripción de la biblia}, vista ortográfica elevada de RPG. Cuerpo completo de unas 2,5 cabezas. Cuadrícula EXACTA 4×4 sin líneas: filas abajo, izquierda, derecha, arriba; columnas paso izquierdo, paso intermedio, paso derecho, paso intermedio. Misma cabeza, ropa, escala y luz; pies en línea común por fila. Fondo realmente transparente, margen entre celdas, nada cortado. Destino {celda}, por defecto 32×48; hoja 128×192. No invertir la luz al cambiar dirección». Si falla la coherencia, fijar cabeza/torso desde una pose y reconstruir piernas y brazos con edición de píxeles. Los objetos no usan este ciclo: preservar su distribución por evento.

### Battler

«{Enemigo: descripción y sentido de la tabla}. Una sola silueta frontal en tres cuartos, figura completa y margen para cuernos, ganchos y vísceras; fondo realmente transparente. Anatomía grotesca legible, sangre burdeos, brillos pequeños de humedad y hueso marfil. Destino 320×300 para visiones; Steven mental 240×340. Sin suelo ni rectángulo de escena. Evitar detalle minúsculo que se vuelva ruido a 1×».

### Face / retrato

«Busto de {personaje}, expresión {neutral/miedo/ira/susurro}; conservar rasgos, edad, peinado y ropa de la referencia aprobada. Cabeza y hombros dentro de cuadro, cintura al borde inferior, transparencia real. 240×340, cara en mitad superior; el cuadro de diálogo tapa parte inferior. Proporciones adultas de retrato, sin chibi. Cambiar solamente expresión para variantes».

### Susto a pantalla completa

«Primerísimo plano de {motivo}, terror visceral con lectura inmediata de {ojo/boca/corona}, perspectiva asfixiante; encuadre 4:3 lleno, opaco, destino 640×480. Borde oscuro, contraste localizado y luz lateral clínica. Carne húmeda, sangre oscura y fracturas según motivo; no es un retrato aislado sobre fondo liso». Motivos: 1 ojo de madre en espejo; 2 familia con bocas de estática; 3 hocico contra cristal del camión; 4 rostro-sumidero; 5 ojo tras rejilla; 6 capataz entre ganchos; 7 Steven con corona de ganchos. No cambiar IDs ni momentos.

### Fondo de combate

«Espacio mental de {piso/matadero/túnel}, perspectiva opresiva, suelo y fondo separados por luz, centro con espacio para battlers, periferia oscura con {muebles/ganchos/tuberías}. 4:3, 640×480 opaco. Menor detalle detrás de enemigos, no incluir enemigos ni texto. Mantener puntos de fuga y escala humana; clínica blanca con rojo para matadero, nicotina para piso, verde negro para túnel».

## Herramienta y reproducción

Requisito: Python 3 con Pillow. Todas las rutas relativas se resuelven respecto a la raíz del proyecto, independientemente del directorio actual. Los destinos se limitan a PNG dentro de Graphics. No se modifica Data ni scripts.

```powershell
python diseno/herramientas/comun/adaptar_arte.py --source diseno/fuentes/arte_hd2d/steven_coherente.png --destination Graphics/Characters/vacas_steven.png --type character --cell 32x48 --padding 4 --alpha-threshold 128 --zone piso
python diseno/herramientas/comun/adaptar_arte.py --batch diseno/fuentes/arte_hd2d/muestra.json
```

JSON: lista de objetos, o `{"assets": [...]}`. Campos: `source`, `destination`, `type`; opcionales `cell`, `size`, `max_height`, `padding`, `zone`, `alpha_threshold`, `key`, `key_tolerance`, `outline`, `resample`, `background`. Los nombres JSON usan guiones bajos; CLI usa guiones. Ejemplo de color clave: `--key '#FF00FF' --key-tolerance 12`; contorno: `--outline '#141318'`. `face` y `retrato` son equivalentes. `--size 320x300` mantiene el lienzo de battler existente; sin `size`, battler recorta y limita altura conservando proporción. Picture/battleback cubre el lienzo sin deformar y recorta el exceso al centro.

Alpha se conserva salvo limpieza explícita; `alpha_threshold=128` lo hace binario. Para humo y niebla conservar semitransparencia. La clave elimina todos los píxeles del color indicado: no elegir un color presente en el sujeto. La herramienta no segmenta fondos complejos ni detecta un falso damero de transparencia. `nearest` preserva bordes; `box` sirve para reducir una fuente sobredimensionada antes del retoque; `lanczos` está disponible para fondos suaves. La cuantización usa paletas fijas sin dithering.

Cada archivo reemplazado se respalda primero en `diseno/fuentes/arte_provisional/sd_v1/Graphics/...`. El primer respaldo se conserva al iterar; no se sobreescribe. La escritura de cada PNG es atómica; el lote valida todas las imágenes antes de empezar, pero no constituye una transacción global frente a errores de disco. Para restaurar, copiar los cuatro PNG del respaldo a sus rutas equivalentes de Graphics.

## Muestra entregada y revisión

Cuatro generaciones reales con la herramienta integrada `image_gen` (sin CLI/API alternativo ni SD); fuentes sin adaptar en `diseno/fuentes/arte_hd2d/`. El manifiesto `../../fuentes/arte_hd2d/muestra.json` conserva parámetros de conversión. Hoja inicial, retrato y vaca tienen alpha real; susto es opaco. `../../herramientas/arte/refinar_muestra_hd2d.py` fija cabeza/torso por dirección y ajusta la proporción a 16 px de cabeza + 24 px de cuerpo antes de la adaptación final; las piernas conservan las fases generadas. No añade dibujo ajeno ni descarga assets.

- Steven mapa: `Graphics/Characters/vacas_steven.png`, 128×192, celdas 32×48, paleta piso. Se revisó a 1× y 3× y se corrigió la estrechez y variación de cabeza inicial.
- Steven neutral: `Graphics/Pictures/retrato_steven_neutral.png`, 240×340, luz lateral cálida y borde frío.
- La Vaca que habla: `Graphics/Battlers/enemigo_vaca.png`, 320×300, cabeza suspendida con carne, columna cervical y lengua-cinta.
- Susto del camión: `Graphics/Pictures/screamer_3.png`, 640×480, hocico desgarrado contra cristal.
- Comparativa: `diseno/capturas/arte/muestra_hd2d.png`; contiene antes/después completos a 1× y 3×, sin suavizado. Es una lámina grande para inspeccionar al 100%, no una captura del motor.

Revisión visual realizada sobre los cuatro PNG adaptados. Limitaciones para aprobación: el susto conserva un acabado más ilustrativo y granular que el sprite; la luz naranja del retrato puede requerir moderación para casar con la nicotina del mapa. No se ha validado caminata dentro de Game.exe ni mezcla con tonos/Fogs. La variante miedo y el mono siguen con arte anterior hasta Fase 2: el cambio de identidad entre variantes es temporal y conocido. No se regeneró el resto, no se tocó Data y no se hizo commit.

## Fase 2: inventario completo

Las tablas siguientes conservan el **estado inicial** de producción. Estado actual de fase 2: [PROGRESO.md](../../fuentes/arte_hd2d/PROGRESO.md), [estado_fase2.json](../../fuentes/arte_hd2d/estado_fase2.json) y [verificación](../../verificaciones/fuentes/verificacion_fase2.json). La muestra fue aprobada y el inventario completo está cubierto.

Lista obtenida de Graphics y contrastada con los 42 PNG de SISTEMAS.md. Conservar nombre, tamaño y distribución interna: especialmente muebles y objetos indexados por dirección/patrón. `../../fuentes/arte_provisional/sd_v1/Graphics/Characters/vacas_vacio.png` debe permanecer transparente (recurso técnico, no personaje para redibujar).

### Graphics/Characters

| Archivo | Tamaño | Estado |
|---|---|---|
| `Graphics/Characters/vacas_anselmo.png` | 128×192 | Pendiente |
| `Graphics/Characters/vacas_borracho.png` | 128×192 | Pendiente |
| `Graphics/Characters/vacas_carnicero.png` | 128×192 | Pendiente |
| `Graphics/Characters/vacas_cosas.png` | 128×128 | Pendiente |
| `Graphics/Characters/vacas_cripps.png` | 168×240 | Pendiente |
| `Graphics/Characters/vacas_furgoneta.png` | 384×256 | Pendiente |
| `Graphics/Characters/vacas_lucy.png` | 128×192 | Pendiente |
| `Graphics/Characters/vacas_madre.png` | 192×268 | Pendiente |
| `Graphics/Characters/vacas_matadero.png` | 128×256 | Pendiente |
| `Graphics/Characters/vacas_muebles.png` | 128×256 | Pendiente |
| `Graphics/Characters/vacas_obrero1.png` | 128×192 | Pendiente |
| `Graphics/Characters/vacas_obrero2.png` | 128×192 | Pendiente |
| `Graphics/Characters/vacas_obrero3.png` | 128×192 | Pendiente |
| `Graphics/Characters/vacas_obrero4.png` | 128×192 | Pendiente |
| `Graphics/Characters/vacas_perro.png` | 160×160 | Pendiente |
| `Graphics/Characters/vacas_puerta.png` | 128×256 | Pendiente |
| `Graphics/Characters/vacas_reclutador.png` | 128×192 | Pendiente |
| `Graphics/Characters/vacas_remedios.png` | 128×192 | Pendiente |
| `Graphics/Characters/vacas_steven.png` | 128×192 | Muestra: aprobar o revisar |
| `Graphics/Characters/vacas_steven_mono.png` | 128×192 | Pendiente |
| `Graphics/Characters/vacas_tablon.png` | 128×192 | Pendiente |
| `Graphics/Characters/vacas_transeunte.png` | 128×192 | Pendiente |
| `Graphics/Characters/vacas_vaca.png` | 320×320 | Pendiente |
| `Graphics/Characters/vacas_vaca_canela.png` | 320×320 | Pendiente |
| `Graphics/Characters/vacas_vacio.png` | 128×192 | Conservar transparente |

### Graphics/Battlers

| Archivo | Tamaño | Estado |
|---|---|---|
| `Graphics/Battlers/enemigo_canal.png` | 320×300 | Pendiente |
| `Graphics/Battlers/enemigo_guernsey.png` | 320×300 | Pendiente |
| `Graphics/Battlers/enemigo_madre.png` | 320×300 | Pendiente |
| `Graphics/Battlers/enemigo_moscas.png` | 320×300 | Pendiente |
| `Graphics/Battlers/enemigo_rey.png` | 320×300 | Pendiente |
| `Graphics/Battlers/enemigo_sombra_cripps.png` | 320×300 | Pendiente |
| `Graphics/Battlers/enemigo_televisor.png` | 320×300 | Pendiente |
| `Graphics/Battlers/enemigo_tunel.png` | 320×300 | Pendiente |
| `Graphics/Battlers/enemigo_vaca.png` | 320×300 | Muestra: aprobar o revisar |
| `Graphics/Battlers/steven_mente.png` | 240×340 | Pendiente |

### Graphics/Pictures

| Archivo | Tamaño | Estado |
|---|---|---|
| `Graphics/Pictures/retrato_anselmo_neutral.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_benito_neutral.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_borracho_neutral.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_chato_neutral.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_cripps_ira.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_cripps_neutral.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_dog_miedo.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_dog_neutral.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_encarna_neutral.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_guernsey_neutral.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_guernsey_susurro.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_lucy_neutral.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_lucy_susurro.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_madre_ira.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_madre_neutral.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_molina_neutral.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_reclutador_neutral.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_remedios_neutral.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_rubio_neutral.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_sierra_neutral.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_steven_miedo.png` | 240×340 | Pendiente |
| `Graphics/Pictures/retrato_steven_neutral.png` | 240×340 | Muestra: aprobar o revisar |
| `Graphics/Pictures/screamer_1.png` | 640×480 | Pendiente |
| `Graphics/Pictures/screamer_2.png` | 640×480 | Pendiente |
| `Graphics/Pictures/screamer_3.png` | 640×480 | Muestra: aprobar o revisar |
| `Graphics/Pictures/screamer_4.png` | 640×480 | Pendiente |
| `Graphics/Pictures/screamer_5.png` | 640×480 | Pendiente |
| `Graphics/Pictures/screamer_6.png` | 640×480 | Pendiente |
| `Graphics/Pictures/screamer_7.png` | 640×480 | Pendiente |

### Graphics/Battlebacks

| Archivo | Tamaño | Estado |
|---|---|---|
| `Graphics/Battlebacks/mente_matadero.png` | 640×480 | Pendiente |
| `Graphics/Battlebacks/mente_piso.png` | 640×480 | Pendiente |
| `Graphics/Battlebacks/mente_tunel.png` | 640×480 | Pendiente |

### Graphics/Tilesets

| Archivo | Tamaño | Estado |
|---|---|---|
| `Graphics/Tilesets/vacas_matadero.png` | 256×256 | Pendiente |

### Graphics/Autotiles

| Archivo | Tamaño | Estado |
|---|---|---|
| `Graphics/Autotiles/vacas_canal.png` | 384×128 | Pendiente |

### Graphics/Titles

| Archivo | Tamaño | Estado |
|---|---|---|
| `Graphics/Titles/vacas_titulo.png` | 640×480 | Pendiente |

### Graphics/Gameovers

| Archivo | Tamaño | Estado |
|---|---|---|
| `Graphics/Gameovers/vacas_gameover.png` | 640×480 | Pendiente |

### Graphics/Windowskins

| Archivo | Tamaño | Estado |
|---|---|---|
| `Graphics/Windowskins/vacas_ventana.png` | 192×128 | Pendiente |

Además: diseñar Fogs y Pictures de luz/viñeta propios en Fase 2, y sustituir los tiles de piso/calle procedentes del RTP solo cuando se autorice esa ampliación. No se inventan archivos existentes para esos recursos. Prioridad: aprobar identidad y nivel de gore; después expresiones de Steven y mono, demás protagonistas, nueve visiones, NPC, sustos, fondos y entorno. Revisar oclusiones y legibilidad en el motor antes de producir todo el catálogo.


Prompts exactos de las cuatro generaciones: [arte_hd2d/PROMPTS.md](../../fuentes/arte_hd2d/PROMPTS.md). Parámetros y comprobaciones: [muestra.json](../../fuentes/arte_hd2d/muestra.json), [verificacion.json](../../verificaciones/fuentes/verificacion.json).
