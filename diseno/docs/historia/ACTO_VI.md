# Acto VI — Rey-dios y cierre del juego

> **Arte actualizado (10-11-2026):** enemigos 33–37 con PNG exclusivos/hue=0; retrato madre_envejecida_neutral asignado solo al VI; Guernsey con rombo propio; trono generado y utilería image_gen en tileset70. Cinemáticas con cuatro placas originales. Perro conserva sus apariciones estáticas: el seguidor entre mapas continúa pendiente. Las notas provisionales originales se conservan como historia, no como estado actual. Ver [auditoría](../arte/AUDITORIA_ARTE.md).

Construido el 10 de noviembre de 2026. RGSS1, Ruby 1.8, 640×480. Texto original en español; adaptación libre, sin citas del libro. El contenido sexual permanece fuera de pantalla. El desenlace Ganado corta antes del golpe; la violencia se comunica mediante la cadena, las etiquetas y el sonido.

Respaldo anterior a toda escritura: los 42 `Data/*.rxdata` existentes en [respaldos/antes_acto6/Data](../../respaldos/antes_acto6/Data). No se accede a `.git`; no se modifica `Vacas.cfg` ni se cierran procesos Game.exe ajenos.

## Entrada y recorrido

La pantalla de fin del Acto V continúa al VI con la misma partida. Las dos cancelas del patio 27 también ofrecen **Guardar y continuar al Acto VI**; marcan 163 antes de guardar. Esto permite continuar guardados del patio, incluso los anteriores a esta ampliación. Se mantienen las tres decisiones exclusivas 160/161/162; no se vuelven a elegir al llegar al trono.

Ruta: patio 27 → túneles 28 → ciudad 29 → piso 30 → ciudad 29 → galería 31 → altar 32 → jefe de la rama → escena VN → FIN → créditos completos → título.

| ID | Mapa | Escena y accesos |
|---|---|---|
| 28 | Túneles profundos: la raíz | Entrada (3,13). Pilares, nichos de almacenaje, ganchos, tuberías, radio (2,10), Muesca (15,10), carta de Lucy (12,11), visión del Censo (10,4). Salida este (19,12) a 29 (3,13), tras afrontar el Censo. |
| 29 | Ciudad tomada: el nuevo turno | Una manzana con camión, barricada, refugio, tablón de lotes y manada. Obreros vivos o sus botas según 147/171. Radio (16,11). Este (19,12) a 30 (3,13); sur (3,14) a 28 (18,12); portón norte (4,3) a 31 (3,13), tras hablar con la madre. |
| 30 | El piso: la última cena | Regreso al hogar, condensado en salón, cocina y dormitorio. Madre (4,5), Perro (5,6), tele, sofá, medicinas, fogón, cama y recibos. Radio (7,4). Madre exige una última respuesta; visión de la Mesa y elección de límite o silencio. Perro sale vivo con Steven. Ambas salidas vuelven a 29 (18,12); se exige completar la escena. |
| 31 | Galería de compuertas | Tensión de 35 segundos de movimiento libre. Cuadros en (4,4), (10,4), (16,4), orden izquierda-centro-derecha. Este (19,12) a 32 (3,13) tras cerrar. Sur (3,14) permite retirarse a la ciudad y reiniciar sin quedar atrapado. |
| 32 | Rey-dios: el altar | Sofá doméstico convertido en trono, cuernos, bancos, despensa y canales de servicio. Radio (3,10), Perro (5,10), Guernsey (10,6). Confirmar «Afrontar el trono» inicia el jefe y el desenlace. Se puede guardar y volver a la galería antes de confirmar. |

Los cinco mapas son de 20×15, tileset nuevo **70**. Son 51 eventos nuevos. Las radios ofrecen guardar, descansar para recuperar salud/aliento y bajar veneno respetando la huella, o continuar.

## Consecuencias y finales

| Origen | Consecuencia visible |
|---|---|
| Lucy 96/97 | Carta distinta, diálogo con madre sobre quedarse o llevar pruebas, tablón público de etiquetas y recuerdos del epílogo. No se promete curación ni relación obligatoria. |
| Pacto 132–135 | Reconocimiento de la chapa y del camino pactado; 133 muestra agua compartida y «nadie es ganado», 134 muestra represalias. La ley del Rey y la despedida de Huida cambian. |
| Reputación 51 | Con ≥2, Muesca entrega una ruta, el refugio ofrece agua y en Huida deja el paso; con menos, recelo y salida por un hueco. |
| Dominio/Piedad 58/59 | Diálogo de la manada, salud del jefe y variantes del epílogo. Piedad > Dominio permite un Rey con límites, una última protección deliberada de Perro en Ganado o aprender a aflojar la correa en Huida. |
| Corrales 145 | Reses liberadas descansan en nichos; si no se abrieron quedan candados y ausencias. |
| Obreros 147/171 | El Rubio está vivo y ayuda con agua, instrucciones y desenlace, o quedan botas y una chapa. Sin aviso ni muerte se reconoce que sobrevivieron encerrados. |
| Elección del piso 192 | Poner límite sin castigo suma Piedad y permite que la madre baje; callar suma Dominio y deja a la madre viva en el piso. Ambos caminos rescatan a Perro y permiten terminar. |

**160 — Rey de la manada:** jefe **El Rey sin rostro**. La Guernsey ofrece el asiento. Con más Piedad, Steven deja marcharse a quienes no quieran seguir; con más Dominio, aprende a contar nucas. El pacto se convierte en límite público o en ley de venganza. Perro queda al alcance de su mano. Texto final: la ciudad y Steven duermen con un ojo abierto.

**161 — Ganado:** jefe **Tu Número en la cadena**. El altar descubre su cinta transportadora; la lógica de sustituir al verdugo acaba sustituyendo a la víctima. Muesca saca a Perro vivo y este vuelve con la madre. La advertencia a los obreros compra un minuto de resistencia; sus muertes dejan un número reciclado. La puerta se cierra antes de la violencia. El registro añade una cabeza, sin tumba.

**162 — Huida:** jefe **La Puerta que muerde**. Steven rechaza el asiento y reconoce la traición a la manada. Reputación alta abre el paso; baja obliga a seguir a Perro por un hueco. La carta de Lucy y el pacto acompañan la salida; los obreros vivos pueden alcanzar las vías. La madre acompaña si aceptó bajar. La Piedad cambia cómo Steven lleva la correa. Queda un camino sin promesa de salvación.

Cada rama tiene diálogo VN con retratos existentes, epílogo propio y pantalla FIN con nombre y dos líneas exclusivas. FIN pasa automáticamente a créditos tras 12 segundos o con Z/Intro. Los créditos muestran Feka Studios: **Carlos – dirección, arte, diseño; Alexandre – historia; Ithalo "Ander" – sonido**, seguidos de **todas** las líneas de atribución CC ya existentes. Desplazamiento automático, mantener Z acelera, Esc vuelve al título; al terminar el desplazamiento vuelve automáticamente. La pantalla Créditos del título conserva todo el audio y añade el equipo al principio.

## Sistemas e IDs

Script [15_reydios.rb](../../scripts/15_reydios.rb), sección **Vacas_Reydios**, antes de Main. Se actualizan Vacas_Pantallas para la continuidad V→VI y Vacas_Interfaz para créditos y música de jefes. 105 secciones instaladas.

| Rango | Uso |
|---|---|
| Mapas 28–32; tileset 70 | Cinco mapas nuevos y hoja derivada sin sobrescribir arte anterior. |
| Switches 176–180 | Acto activo, llegada a túneles, Censo afrontado, ciudad vista, llegada al piso. |
| 181–186 | Escena de madre terminada, Perro acompaña, carta de Lucy, compuertas cerradas, tensión activa, altar visto. |
| 187–192 | Jefe vencido, juego completado, finales Rey/Ganado/Huida vistos, límite sin castigo. |
| 195–196 | Mesa afrontada, presentación de la galería vista. |
| 193–194, 197–199 | Libres, ampliación reservada de System. |
| Variables 65–69 | Cierres 0–3, frames de tensión, golpes de agua, último final 1–3, reserva. |
| Objetos 39–40 | Ruta de tiza y Carta de Lucy. Recuerdos sin consumo, lectura mediante CE1. |
| Enemigos/tropas 33–34 | El Censo de las bocas (340 HP) y La Mesa que exige (390 HP). |
| Enemigos/tropas 35–37 | Tres variantes del jefe. HP = 780 + 35×Dominio − 25×Piedad, limitado a 650–990. Reintento hasta victoria, recursos completos; sin experiencia ni dinero. |

Se comprobaron los rangos reales antes de reservarlos: Items terminaba en 38, Tilesets en 69, System en 175/64. Los enemigos y tropas 22–32 seguían siendo entradas RTP; **no se sustituyen**, los nuevos empiezan en 33. Se reutilizan técnicas y estados existentes 61–70 y 2–4.

La tensión usa 1.400 frames a 40 fps y se pausa durante mensajes/intérprete. Orden incorrecto: −120 frames, sin reiniciar cierres correctos. Golpe de agua: +4 veneno con tope 96, contador +1 y vuelta al nicho (3,12), cierres a cero y tiempo completo. No pierde objetos ni historia. No hay game over ni temporizador global residual; salir restaura menú/guardado, reentrar reinicia, completar detiene la música de persecución. Marcador bajo el HUD con tiempo, cierres y orden.

**Completado persistente:** `Vacas_finales.dat`, texto con números 1–3 sin Marshal. Se escribe solo tras el epílogo, conserva los finales anteriores y muestra contador y nombres vistos en el título. 188 y 189/190/191 permiten consultar el resultado dentro de la partida. Un error de escritura no interrumpe el final. El arnés restaura o elimina sus propios archivos de finales al acabar.

## Prueba rápida

En el título, seleccionar **Nueva partida**, mantener **Ctrl+W** (Input::CTRL + Input::R; W también puede ser Av Pág) y confirmar con **Z**. Aparece un selector de las tres ramas. **Ctrl+W+Mayús** usa antecedentes duros: Lucy 97, pacto de venganza 134, reputación 0, Dominio 5, Piedad 0, obreros muertos y corrales cerrados. Sin Mayús: Lucy 96, pacto 133, reputación 3, Dominio 1, Piedad 4, obreros avisados y corrales abiertos. El selector crea una partida en memoria y no sobrescribe guardados. Los atajos anteriores se conservan; Q y Q+W siguen llevando al V con sus respectivos pactos.

## Audio y arte

`Vacas_Audio::MAP_AUDIO` añade filas 28–32 usando las zonas existentes `:alcantarillas`, `:matadero`, `:piso`, `:manada`. 28/31: alcantarillas; 29: calle nocturna y lluvia; 30: tema seguro y reloj; 32: drone y eco. 185 activa persecución. Tropas 35–37 usan música de jefe; efectos de compuertas mediante `Vacas_Audio.play(:cadena_gancho)`.

Escala: personajes de ~48 px, cama 32×64, fogón 48×48, cajonera 48×48, TV 32×64 con dibujo de ~40 px, utilería de mesa 10–16 px. Salas divididas, estantes de 56 px, cajas/bidones/sacos agrupados, platos/recibos/medicinas, luces locales, máscara y tono suave. El camión es el recurso 128×64 del V. No se usa generación de imágenes ni GPU local: PIL reutiliza y recorta hojas existentes. La hoja derivada contiene 154 baldosas de utilería adicionales.

**Provisional:** battlers reutilizados y tintados (`enemigo_vaca`, `enemigo_madre`, `enemigo_rey`, `enemigo_canal`, `enemigo_sombra_cripps`); figuras de manada y obreros existentes; trono representado por el sofá; no hay retrato nuevo de madre envejecida ni seguidor animado de Perro entre mapas. El piso es una condensación escénica del hogar, no una copia geométrica del mapa 2. La utilería del V tiene acabado más plano que el arte HD-2D original.

Capturas revisadas: [lámina de los cinco mapas](../../capturas/actos/acto6_lamina.png), [túneles](../../capturas/actos/acto6_28.png), [ciudad](../../capturas/actos/acto6_29.png), [piso](../../capturas/actos/acto6_30.png), [galería](../../capturas/actos/acto6_31.png), [altar](../../capturas/actos/acto6_32.png). Los cuadrados azules son marcadores de eventos del render; no aparecen jugando. El render incorpora la máscara real, pero no simula niebla animada ni el tono final del motor.

## Verificación y reproducción

- `../../verificaciones/verificacion_sintaxis_acto6.json`: Ruby `-c` de las 105 secciones instaladas, 14 fuentes y arnés; 120 comprobaciones, cero errores. El script nuevo usa sintaxis Ruby 1.8, sin hashes modernos, keywords ni navegación segura.
- `../../herramientas/comun/inspeccionar.mjs`: carga y round-trip Marshal de los 47 archivos rxdata finales.
- `../../verificaciones/verificacion_acto6.json`: 3.153 comprobaciones de colisiones direccionales, páginas activas, interacción y destinos en 48 escenarios; cero errores.
- `../../verificaciones/herramientas/validar_conectividad6.json`: 32 mapas, 110 transferencias; cero rotas, huérfanas o inalcanzables.
- `../../verificaciones/herramientas/validar_assets6.json`: 1.051 referencias, cero ausentes; el arnés comprueba además retratos VN, zonas/battlebacks y claves dinámicas de audio.
- `../../verificaciones/verificacion_rgss_acto6.txt`: seis recorridos del intérprete (tres ramas × dos antecedentes), derrota/reintento del jefe, madre, Perro, tensión y captura recuperable, transferencia, FIN, créditos y persistencia de los tres finales. Cien simulaciones de balance con fórmulas/estados reales y arranque/salida de las tres variantes en Scene_Battle nativo. **La victoria se fuerza tras 24 frames en esa última prueba**, para no bloquear el renderer sin foco; no verifica una batalla completa jugada en tiempo real. El desplazamiento de créditos se muestrea al inicio y al final, sin esperar todos sus minutos. `../../herramientas/actos/acto6/probar_acto6.mjs` termina con exit 0 y «OK FIN», restaura los bytes exactos de Scripts.rxdata y los finales de prueba, y comprueba que Vacas.cfg no cambió.

Para modificar eventos o scripts: `node inspeccionar.mjs` → `python -X utf8 build_acto6.py` → `node rx.mjs --batch b_acto6.json`. Para arte/mapas: `python -X utf8 maps6.py` → `node rx.mjs --batch b_tiles6.json`. Después: `node inspeccionar.mjs` → `python -X utf8 verificar_acto6.py` → `python -X utf8 capturas6.py`. Trabajar desde `diseno/herramientas`; no volver a ejecutar `../../archivo/lotes/b_mapas6.json`, que crea mapas. `../../herramientas/actos/acto6/preparar_acto6.mjs` es idempotente para las reservas, pero no sustituye el respaldo previo.

## Pendientes

- Recorrido humano completo para ritmo, emoción, legibilidad conjunta de luz/tono y dificultad percibida; duración estimada del VI de 20–35 minutos.
- Escucha humana de mezcla, transición al tema de créditos y volumen de compuertas.
- Sustituir el arte provisional y, si se desea, implementar un seguidor visual de Perro. Su presencia narrativa y sus sprites de piso/altar ya están incorporados.
- Revisar distribución final con RTP y las licencias de todos los recursos. El cierre narrativo y las tres rutas están implementados; estas tareas son de pulido y empaquetado.
