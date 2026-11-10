# Biblia de personajes — Fase 2

Fecha: 2026-11-09. Autoridad visual: muestra del commit 10d731b aprobada tal cual por el usuario. Incluye acabado ilustrado de retratos y sustos. Esta biblia sustituye las descripciones provisionales que llaman gris a la camisa de Steven. Edades no especificadas en el guion son decisiones visuales, no datos narrativos nuevos.

## Invariantes de producción

- Una referencia frontal y lateral de cuerpo entero por identidad, en `arte_hd2d/referencias/`. Generarla antes de sus assets. Adjuntarla a TODAS las generaciones posteriores de esa identidad, incluidas visiones y sustos.
- Steven se deriva de `arte_hd2d/steven_retrato.png` y `Graphics/Characters/vacas_steven.png`, ambos aprobados. No reinterpretar su cara.
- Retratos: mismo busto, postura, encuadre, ropa, alpha y luz cálida arriba-izquierda con borde frío derecho. Cada expresión se edita desde su neutral, adjuntando además su referencia. Solo cambia el rostro; animales: ojos, orejas y boca, sin anatomía humana.
- Hex = color local, antes de sombras e iluminación; no exigir que todos los píxeles iluminados tengan ese valor. Piel, prendas y materiales conservan sus rampas entre escenas.
- Sprites: detalle legible a 1x, aproximadamente 2,5 cabezas; 4 columnas y filas abajo/izquierda/derecha/arriba. No cambiar dimensiones ni distribución de objetos.
- Retratos y sustos conservan el acabado ilustrado aprobado. No reducirlo a dibujo geométrico ni exigir pixelado adicional.
- Comparar referencia, sprite y todos los retratos con `view_image` antes de marcar terminado. Battler también cuando exista. Ningún personaje sin comparación se considera validado.

## Identidades humanas

| Identidad / referencia prevista | Edad, cuerpo y cara fijos | Pelo, ojos, piel | Vestuario exacto y distintivos |
|---|---|---|---|
| Steven / `steven.png` | 25; delgado, hombros caídos, rostro alargado, pómulos hundidos, nariz recta, ojeras profundas, barba incipiente; pequeño lunar en mejilla izquierda como retrato aprobado | Negro despeinado `#211C1E`, mechones irregulares sobre frente; ojos castaño oscuro `#382A23`; piel pálida `#C69878`, sombras `#946A55` | Camisa marrón gastada `#594B42`, sombras `#393132`, cuello abierto, botones oscuros, bolsillo en pecho izquierdo; pantalón carbón `#29252A`; zapatos marrón `#494039`. No chaqueta ni accesorios nuevos |
| Madre / `madre.png` | 58; ancha, grandes manos, cuello corto, cara cuadrada y pesada, labios finos, cejas rectas | Castaño gris `#494039`, moño bajo fijo; ojos `#493B28`; piel `#C19A75` | Bata mostaza `#A18A59` hasta tobillos, solapas y cinturón mismo tejido, puños `#71634B`, zapatillas oscuras `#494039`; sin joyas. Corpulenta, no monstruosa fuera de visiones |
| Lucy / `lucy.png` | 28; esbelta, cara estrecha, nariz fina, ojeras suaves, mirada fija inquieta | Rubio ceniza `#B6A17A` recogido en moño bajo, dos mechones finos en sienes; ojos gris verdoso `#6C796E`; piel `#D6BA9B` | Bata pálida `#D4D4BD`, cuello y cinturón `#AAA997`, vestido interior gris `#77848A`, zapatos `#494039`; tarro de vidrio vacío con borde `#A6B8BE`, sin cambiar su tamaño |
| Cripps / `cripps.png` | 48; corpulento, ancho y musculoso, cuello grueso, mandíbula cuadrada, nariz ancha, cejas bajas | Rapado `#393533`; ojos `#493B28`; piel `#AA7656`; sin barba | Camisa industrial gris `#738585`, mangas a antebrazo; delantal marfil sucio `#B7AF91`, manchas secas `#4B1020`, correas `#494039`; pantalón `#263239`, botas negras `#10171D` |
| Benito / `benito.png` | 58; enjuto, espalda algo curva, cara larga arrugada, manos grandes de oficio | Corto canoso `#9B9B8D`, entradas; ojos `#554533`; piel `#AA7656` | Mono blanco gastado `#C7C9B7`, cuello gris `#738585`, dos bolsillos de pecho, remiendo rodilla derecha `#8C9588`, botas `#263239`; sin casco |
| Encarna / `encarna.png` | 44; mediana, brazos firmes, cara oval ancha, labios apretados | Castaño oscuro `#49382E`, recogido bajo redecilla `#B8B9A8`; ojos `#493B28`; piel `#C69878` | Mono blanco `#D0D2C2`, delantal corto `#ADB7AB`, guantes `#738585`, botas `#263239`; sangre seca limitada al bajo `#4B1020` |
| Rubio / `rubio.png` | 32; mediano, atlético delgado, cara angulosa, nariz recta | Rubio corto `#B79C64`; ojos gris `#77848A`; piel `#D4B48A` | Mono blanco `#CFD3C4`, guantes oscuros `#263239`, botas `#10171D`; equipo de seguridad compartido con Sierra, ver limitación inferior |
| Chato / `chato.png` | 40; bajo y robusto, rostro ancho, nariz achatada, mejillas marcadas | Castaño corto `#49382E`; ojos `#493B28`; piel `#B28668` | Mono industrial gris claro `#ADB7AB`, cinturón `#494039`, botas `#263239`, puños sucios `#694139` |
| Sierra / `sierra.png` | 36; mediano, robusto; rostro parcialmente oculto, mandíbula ancha | Rubio oscuro `#A78D60`, ojos gris `#77848A`; piel `#D4B48A` | Mismo mono `#CFD3C4`, guantes `#263239` y botas `#10171D` que Rubio; casco crema `#D4D1B9`, gafas con montura `#263239`, máscara gris `#ADB7AB` |
| Remedios / `remedios.png` | 76; pequeña, encorvada, cara surcada, mejillas hundidas, nariz fina | Blanco gris `#CBC9B9`, moño bajo; ojos `#71634B`; piel `#C6A68A` | Vestido marrón gris `#71634B` hasta tobillos, chal oscuro `#29252A`, zapatos `#494039`; manos entrelazadas |
| Anselmo / `anselmo.png` | 73; delgado, cara larga, nariz curva, bigote ancho | Pelo y bigote gris `#96968A`, entradas; ojos `#554533`; piel `#B99576` | Chaqueta vieja `#71634B`, camisa `#B4AB90`, pantalón `#494039`, zapatos `#29252A`; codos remendados `#594B42` |
| Molina / `molina.png` | 51; robusto, brazos fuertes, cara cuadrada, bigote grueso | Pelo corto y bigote `#393132`; ojos `#493B28`; piel `#B28668` | Camisa crema `#D4C6AA`, mangas recogidas, delantal rojizo `#78192A`, manchas `#4B1020`, pantalón `#494039`, botas `#29252A`. Sprite `vacas_carnicero`, retrato `molina` |
| Borracho / `borracho.png` | 49; delgado desgarbado, cara larga, nariz enrojecida `#A46659`, barba de varios días | Castaño gris revuelto `#594B42`; ojos `#554533`; piel `#B28C73` | Abrigo largo `#494039`, camisa `#8B806C`, pantalón `#393132`, zapatos gastados `#29252A`; botella verde apagado `#3D5744` |
| Reclutador / `reclutador.png` | 46; mediano, vientre leve, cara redonda, sonrisa contenida, afeitado | Castaño `#49382E` bajo gorra; ojos `#554533`; piel `#C69878` | Gorra y chaqueta `#444B50`, camisa `#B4AB90`, pantalón `#29252A`, zapatos `#393132`; carpeta ocre `#A18A59` |
| Transeúnte / `transeunte.png` | 38; mediano y delgado, rostro oval poco contrastado | Castaño `#494039` parcialmente tapado, ojos `#554533`; piel `#B99576` | Impermeable gris `#77848A`, sombrero de lluvia `#444B50`, pantalón `#494039`, zapatos `#29252A`; no paraguas que exceda celda |

## Animales

| Identidad / referencia | Edad, anatomía y rostro | Colores y distintivos invariantes |
|---|---|---|
| Perro / `perro.png` | Mestizo adulto, 8 años visuales, pequeño-mediano, delgado, hocico alargado, orejas caídas; patas traseras paralizadas, tumbado o arrastrándose con delanteras | Pelo marrón `#8B674A`, lomo oscuro `#494039`, pecho y punta de hocico crema `#C9B58F`, ojos cálidos `#694139`, nariz `#211C1E`; sin collar nuevo, sin gore. Alias retratos `dog` |
| Guernsey / `guernsey.png` | Vaca adulta, 6 años visuales, pesada, frente ancha, cuernos curvos simétricos; mirada castaña inteligente | Canela `#AA7656`, frente crema en rombo `#D4B48A`, hocico oscuro húmedo `#694139`, ojo `#694139`, cuernos marfil `#D4C6AA`, pezuñas `#494039`. Mantener ojo y manchas en rejilla y visión |
| Vaca de corral / `vaca_corral.png` | Adulta, 5 años visuales, anatomía bovina pesada, cuello grueso; sin cara humana | Crema `#D4C6AA` con parches marrón `#694139`, cuernos `#D4B48A`, hocico `#927461`, ojos `#694139`, pezuñas `#494039`; misma distribución de manchas por lado |
| Vaca del fondo / `vaca_canela.png` | Adulta, 5 años visuales, cuerpo pesado, cabeza algo baja; distinta de la Guernsey narrativa | Canela `#AA7656`, frente canela sin rombo, vientre crema `#D4B48A`, ojo `#694139`, cuernos `#D4C6AA`, pezuñas `#494039`; `vacas_vaca_canela` |

## Cambios de acto y límites del juego existente

- Acto I: Steven conserva camisa aprobada, polvo discreto en bajos, sin sangre permanente. Las bofetadas son ramas opcionales: los PNG compartidos no deben imponer heridas a todas las partidas.
- Acto II: `vacas_steven_mono` cambia solo la ropa: mono blanco gris `#C7C9B7`, abierto lo suficiente para reconocer cuello de camisa marrón, botas `#263239`, suciedad `#694139` y manchas secas limitadas `#4B1020`. Misma cara, pelo, cuerpo. Al volver a casa recupera la camisa. No inventar uniforme por turno sin soporte de eventos.
- Los dos retratos de Steven se comparten entre casa y matadero: conservar camisa marrón aprobada. No cambiar el neutral a mono ni crear alternancia sin scripts. El battler mental también conserva camisa para funcionar en ambos actos.
- Madre, Lucy, vecinos y Perro conservan ropa/apariencia en I–II. Obreros y Cripps usan manchas constantes de trabajo; no son heridas personales. La vaca cotidiana no lleva heridas de su visión.
- Acto III implementado: Lucy añade calma y quiebre facial sin cambiar cuerpo, ropa, tarro ni identidad; ambos estados se usan en eventos. Actos IV–VI continúan en planificación: no fabricar variantes de heridas o muertes que no existen en los assets/eventos actuales.
- Confirmado en `herramientas/contenido2.py`: obrero1=Benito; obrero3=Encarna; obrero4=Chato; **obrero2=Rubio Y obrero de la sierra** (líneas 414 y 603). No es posible hacer dos sprites distintos sin modificar eventos. Diseño compartido con equipo protector compatible en ambas referencias, dejando al Rubio reconocible por pelo visible; no afirmar que son el mismo personaje. Registrar limitación y revisar juntos sus retratos. No cambiar Data para resolverla.
- Guernsey aparece mediante celdas de rejilla de `vacas_matadero`, no asignar su identidad a la vaca del fondo por semejanza de color.

## Visiones y sustos: transformación permitida

Siempre adjuntar referencia de identidad y base aprobada de estilo. Gore explícito ficticio: sangre burdeos `#78192A`, coágulos `#4B1020`, músculo `#A42A39`, grasa `#D4B48A`, hueso `#D4C6AA`, vísceras con peso. Sin contenido sexual.

| Asset | Identidad que se conserva / deformación narrativa |
|---|---|
| enemigo_vaca; screamer_3 | Muestra aprobada: cabeza bovina crema/marrón, ojo castaño, mejilla abierta, vértebras y lengua-cinta; crear referencia propia `vaca_vision.png` desde fuente aprobada antes de nuevas variantes |
| enemigo_madre; screamer_1 | Madre: misma bata mostaza, moño, cejas, manos; yeso roto con carne húmeda, ojo reconocible en espejo |
| enemigo_sombra_cripps; screamer_6 | Cripps: rapado, cuello y delantal; manos fundidas con ganchos, carne oscura desgarrada |
| enemigo_guernsey; screamer_5 | Guernsey: rombo frontal, ojo castaño; cuernos-tuberías, humo verde negro, costillas y carne; susto ojo tras rejilla |
| enemigo_rey; screamer_7 | Steven: cara, lunar, pelo y camisa marrón intactos como identidad; corona de ganchos, sangre y tejido abierto, verdugo reflejado |
| enemigo_tunel | Entidad sin cara, cuerpo largo húmedo, huesos y ojos en conducto; referencia propia `tunel.png` |
| enemigo_moscas | Enjambre de moscas formando cara incompleta, materia orgánica y huecos transparentes; referencia `moscas.png` |
| enemigo_canal | Canal bovina sin piel, músculo, grasa, vísceras, costillas-barrotes y gancho; referencia `canal.png` |
| enemigo_televisor; screamer_2 | Televisor de los cincuenta de `vacas_muebles`; familia anónima de tres adultos con rostros de estática y bocas vacías, cables-tendones. Referencia `familia_nieve.png`; no atribuir identidades del reparto |
| screamer_4 | Rostro anónimo adulto sustituido por sumidero con carne desgarrada, no cambiar identidad de Steven; referencia `sumidero.png` |

Las referencias de entidades sin cuerpo humano usarán frontal y lateral de su forma completa, sin inventar piernas para completar una hoja.

## Ampliación Acto III — 9-11-2026

- **Elena / `referencias/elena.png`:** 56 años, enfermera retirada, baja y robusta, cara ancha cansada, piel oliva, ojos castaño oscuro, pelo corto rizado gris; cárdigan carbón sobre blusa de enfermería azul gastado, pantalón oscuro y zapatos planos marrones. Llaves de latón pequeñas. Referencia frontal/lateral, retrato neutral y sprite propio comparados. No es médica ni emite un diagnóstico; presta material y acompaña a Lucy.
- **Lucy:** `retrato_lucy_quiebre` (lágrimas, mirada perdida, boca temblorosa) y `retrato_lucy_calma` (leve sonrisa cansada, cejas relajadas). Generación desde neutral y referencia; adaptación con máscara facial y lienzo preservado. Resto de los píxeles del neutral se conserva fuera del área facial y su fundido. La crisis no añade heridas ni transforma a Lucy en enemigo.
- **Tarro testigo / `tarro.png`:** recipiente de vidrio con tapa envejecida, boca de tejido burdeos, etiqueta sin letras. Susto 8 lo acerca al hueco de una persiana.
- **Factura cosida / `factura.png`:** tiras de papel marfil sin escritura, hilo quirúrgico negro, sellos burdeos y balanza de latón. Visión de convertir el sufrimiento en un precio.
- **Camilla vacía / `camilla.png`:** camilla oxidada sin paciente, sábana hundida en un vacío, brazos de tejido oscuro y ruedas torcidas. No representa un cuerpo humano real.
- **Diagnóstico / `diagnostico.png`:** silla hospitalaria vacía dentro de un gran tarro, tiras de papel como costillas, corona de pinzas de latón y raíces fibrosas burdeos. Personifica una orden de encontrar una pieza defectuosa; no es Lucy. Susto 9 muestra el mismo motivo desde dentro del vidrio.
- Fuentes, prompts y manifiesto del lote en `arte_hd2d/acto3/`. Referencias, battlers, retratos, sprite y objetos revisados con `view_image`; no se reemplazó arte aprobado de I/II.
