# Vacas: Acto III, «Lucy»

Implementado el 9 de noviembre de 2026 en RPG Maker XP / RGSS1. Texto original en castellano. El contenido sexual permanece fuera de campo. El veneno es un sistema narrativo; los experimentos del juego no constituyen un diagnóstico.

## 1. Continuidad y arranque

Al confirmar «Fin del Acto II», continúa la misma partida en el piso de Lucy. Se exige **34: primera muerte hecha** y se conservan **35: obedeció**, **36: se resistió**, **38: pacto con Guernsey**, el inventario y la huella. La confesión inicial cambia según 35/36; la voz final cambia según 38. No se reinician decisiones anteriores.

Se desactivan turno, mono, patrullas, escenas nocturnas y búsqueda anteriores. En casa se puede hablar con madre y Perro, ver la tele y guardar. Las camas ya no reinician el Acto II. El menú muestra los objetivos de la investigación. Las partidas antiguas recargan su mapa en memoria para incorporar las páginas nuevas, sin escribir el guardado.

**Atajos en «Nueva partida»:**

- **Ctrl**: Acto III, rama obediente, veneno 40, huella 35.
- **Ctrl + Mayús**: Acto III, rama resistente, veneno 40, huella 25.
- **Mayús** conserva el acceso al Acto II. Sin teclas empieza el Acto I.

Soltar las teclas después de confirmar. Los atajos preparan los estados narrativos previos; no dan las soluciones de los puzles del Acto III.

## 2. Mapas

Todos usan el **tileset 51**, sin modificar sus pasajes, prioridades ni autotiles. Tres capas con suelo, mobiliario y lámparas/raíles en sus funciones respectivas. Los objetos nuevos son una hoja indexada RGSS1; no se interpretan como animaciones de caminata.

| ID | Nombre | Tamaño | Contenido y conexiones |
|---|---|---|---|
| 12 | Lucy: el piso de arriba | 25×20 | Estar con tele, mesa de Lucy, tazas, dormitorio, cocina y acceso al laboratorio. Sale a escalera 3. Entrada de escalera en (17,3), destino (12,17). |
| 13 | Carnicería Molina | 20×15 | Mostrador, Molina, etiquetas, visión de la factura y paso al local cerrado. Entrada desde el mostrador de la calle 4, (18,7). |
| 14 | Carnicería cerrada: depósito | 20×15 | Riñón del lote borrado, dos islas que permiten rodear al perseguidor, cortina azul, llamador y visión del tarro. Vuelve a Molina. |
| 15 | Hospital cerrado: curas | 25×20 | Sala de espera, Elena, archivo, camilla, gotero y lavabo de descanso/guardado. Cartel de acceso en calle 4, (35,11). |
| 16 | Lucy: laboratorio improvisado | 25×20 | Tres puestos separados por biombos, microscopio/comparador y conversación final. Acceso desde (21,4) del piso tras recoger el material de Elena. |

Renders con eventos: `capturas/acto3_12.png` hasta `acto3_16.png`. Son vistas planas con la primera página de cada evento; los marcadores azules indican eventos invisibles y no aparecen en el juego. No representan niebla, tono, oclusión ni estado final de las páginas.

## 3. Recorrido y puzles

1. **Dos golpes.** Lucy abre. Steven cuenta lo ocurrido en el cajón según su rama. Ella permite que no la obedezca. Hablar con ella en (10,6) entrega **dos tarros limpios** y el protocolo.
2. **La taza.** Encuentro opcional en (7,8): sentarse sin interrogar aumenta confianza y baja seis de veneno. La confianza añade una frase íntima al final; no bloquea ninguna elección.
3. **Molina.** Entrega hígado del lote 17, sal cerrada y etiquetas; utiliza uno de los tarros. El depósito vecino abre después. La factura cosida es una visión opcional.
4. **La otra carnicería.** La persiana inicia una persecución de **35 segundos** y el susto 8. El riñón en (16,4) utiliza el segundo tarro. La salida está en (3,13); la cortina azul, en (9,9). Recoger la muestra y salir o esconderse resuelve la sección. La cortina también permite cortar la persecución antes de recogerla y continuar explorando. El llamador permite reactivarla si aún no se ha superado.
5. **Captura.** Contacto con la sombra o temporizador agotado: +8 de veneno, contador de capturas, temporizador detenido, menú restaurado y devolución a Molina. **Conserva todo el inventario**. Se puede volver a entrar; la ruta nunca exige perder un objeto único.
6. **Elena.** La enfermera retirada entrega guantes, pinza, reactivo R-0, suero limpio y protocolo de contraste cuando se llevan las dos muestras. Su conversación apunta al control y a la etiqueta del reactivo. Se puede descansar o guardar en el lavabo.
7. **Inventario y contraste.** El laboratorio verifica la posesión de muestra, guantes, pinza, sal y reactivo. En cada puesto se elige la preparación: **sal y reactivo** produce una preparación azul y consume solamente hígado, riñón o suero; las herramientas y reactivos permanecen. «Solo reactivo» explica el error sin gastar la muestra. Cada puesto funciona una vez; no duplica preparados.
8. **Comparar.** El microscopio no deja avanzar sin A, B y CONTROL. Los tres cambian de color. Afirmar que todo es veneno sube siete; reconocer los límites del ensayo aumenta confianza. La etiqueta R-0, legible en hospital y laboratorio, revela la reacción a la sal. Cualquier respuesta permite seguir y conserva los resultados.
9. **El quiebre.** Lucy deja de buscar una «parte mala» que extirpar. Retrato de quiebre, susto 9 y cuaderno de resultados. Puede guardarse antes del jefe.
10. **El Diagnóstico.** Hablar con Lucy al fondo. Es una visión de la orden de arreglarla, no una transformación literal de Lucy. El jefe exige ganar y repite la batalla con salud/aliento completos tras perder. Después se puede elegir o volver a explorar/guardar.

Los objetos legibles **15, 23, 24, 28 y 29** usan el **evento común 1** y `$vacas_ultimo_objeto`, igual que las notas anteriores. Las muestras se combinan en los puestos del laboratorio mediante comprobaciones reales de inventario.

## 4. Veneno, combate y sustos

La barra, distorsiones y huella son las existentes. Los aumentos de este acto se limitan a **96** mediante `lucy_tension`, para permitir reintentar sin bloquear la investigación. Descansar y Respirar respetan siempre la huella. No hay encuentros aleatorios nuevos durante la persecución ni en el piso.

| Enemigo/tropa | Salud | Técnica existente | Disparador |
|---|---:|---|---|
| 10: El Tarro testigo | 230 | Mugido interior / Pánico | Tarros del depósito, fuera de persecución. Opcional. |
| 11: La Factura cosida | 260 | Orden de madre / Culpa | Factura del mostrador. Opcional. |
| 12: La Camilla vacía | 300 | Hedor del túnel / Asco | Camilla del hospital. Opcional. |
| 13: El Diagnóstico | 720 | Coronación / Pánico y Culpa | Lucy tras comparar las tres preparaciones. Jefe obligatorio. |

Usan `preparar_mente`, comando **301 de XP `[tropa,false,true]`**, variable 18, las cuatro técnicas de Steven, recuperación posterior y cero dinero/experiencia. No se crean habilidades ni estados nuevos. Las tres visiones opcionales se consideran afrontadas incluso al perder; el jefe exige victoria.

**Sustos 8 y 9:** misma imagen reservada 98, sonido, flash, temblor y limpieza a los 24 fotogramas que el sistema previo. Sus marcas son **99 y 100**, sin reutilizar 68/69 ni colisionar con datos anteriores. Cada uno aparece una sola vez por partida.

## 5. Final y continuidad

| Elección | Interruptor | Variable 23 | Consecuencia |
|---|---|---:|---|
| Quedarse con Lucy | 96 verdadero, 97 falso | 1 | Steven llama a Elena y se queda; Lucy recupera una expresión de calma. Veneno −12. |
| Llevar las pruebas abajo | 97 verdadero, 96 falso | 2 | Elena se queda con Lucy; Steven lleva los lotes al colector. Veneno +8, limitado a 96. |

Ambas ramas entregan la **Llave del colector (29)**, activan **98: Acto III terminado**, fijan etapa 8 y ofrecen la pantalla de guardado antes del cierre. **Hay que confirmar el guardado** para conservar la elección al regresar al título. Cancelar esa pantalla no guarda automáticamente.

Al cargar un guardado final se vuelve al laboratorio con el acto terminado; hablar con Lucy permite guardar otra vez o ver el cierre. El Acto IV todavía no está implementado. Los interruptores 35/36, 38 y 96/97 quedan disponibles para sus consecuencias futuras.

## 6. IDs reservados

- **Mapas:** 12–16.
- **Interruptores:** 81–107. Detalle en SISTEMAS.md. 87 y 89 quedan reservados sin uso. System se amplía a 112.
- **Variables:** 19 etapa; 20 confianza; 21 capturas; 22 preparaciones; 23 elección. Variable 18 continúa siendo resultado de combate; no se reutiliza.
- **Objetos:** 14–29, enumerados en SISTEMAS.md.
- **Enemigos y tropas:** 10–13. **Sustos:** 8–9. **Imagen:** 98, compartida por el sistema de sustos.
- **Script:** `Vacas_Lucy`, antes de Main; fuente `scripts/09_lucy.rb`.

## 7. Herramientas y reproducción

Respaldo previo a la primera escritura: `respaldos/antes_acto3_20261109_185019/Data/`. Editor cerrado. No se escribe `.git` ni se crean commits.

Desde `diseno/herramientas`:

```powershell
# Solo la primera instalación, cuando 12–16 todavía no existen:
python maps3.py crear
node rx.mjs --batch b_mapas3.json
node ampliar_sistema3.mjs

# Actualización repetible, también tras regenerar actos anteriores:
node inspeccionar.mjs
python build_acto3.py
node rx.mjs --batch b_acto3.json
node inspeccionar.mjs
python verificar_acto3.py
node probar_acto3.mjs
node rx.mjs --batch b_render3.json
```

`build_acto3.py` añade páginas a los mapas 2–4, conserva sus páginas originales y actualiza sus propias páginas sin duplicarlas. Añade el apéndice de notas a CE1. Utiliza `rx.mjs`, `ev.py`, el codec Marshal del MCP y los generadores existentes. **Después de usar `build_events.py` hay que volver a ejecutar `build_acto3.py`** para reinstalar las conexiones y el apéndice del Acto III; después de actualizar scripts generales, reaplicar también este lote.

Arte: `python diseno/herramientas/adaptar_arte.py --batch diseno/arte_hd2d/acto3/manifest.json`, desde la raíz. Fuentes y 16 prompts de generación en nube guardados en `arte_hd2d/acto3/`, referencias en `arte_hd2d/referencias/`. No requiere GPU local.

## 8. Verificación y límites

- 31 archivos `.rxdata`: round-trip estructural del codec y carga/serialización con Marshal de RGSS1 real.
- 99 scripts comprobados con Ruby portable de `D:/DevTools/ruby`; arnés ejecutado dentro de `Game.exe` y Main restaurado al terminar.
- 16 mapas, 67 transferencias: ninguna rota, huérfana ni inaccesible en el grafo. Auditoría adicional de colisión XP en seis estados narrativos, recursos dinámicos y BD: informe `verificacion_acto3.json`.
- 871 referencias del validador de assets: ninguna ausente. El auditor adicional revisa retratos, sustos y audio de eventos.
- Prueba real: Nueva partida sin teclas, Mayús, Ctrl y Ctrl+Mayús; progresión de las dos ramas del cajón y elecciones finales; captura conserva muestras; refugio restaura control; error de preparación no consume; comparación exige control; no hay duplicación de preparados; spritesets de los 16 mapas; retratos VN; dos sustos y limpieza; 120 simulaciones con daño/estados del motor y batalla completa del jefe en `Scene_Battle`.
- Se corrigió un fallo anterior de `Vacas_Mente`: RGSS1 no admite comparar un `Tone` con `nil` mediante `!=`; la restauración usa ahora `.nil?`.
- Informe real: `verificacion_rgss_acto3.txt`. La progresión se automatiza directamente con el intérprete de eventos; las decisiones y mensajes se resuelven desde el arnés. La batalla completa del jefe sí recorre `Scene_Battle` nativo. No equivale a una partida humana completa ni certifica el ritmo de la persecución, volumen, encuadre al desplazarse o sensación del texto.
- Pendiente: revisión humana de ritmo y balance visual/sonoro, y desarrollo del Acto IV. No queda contenido funcional del Acto III marcado como provisional.
