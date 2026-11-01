# VACAS — plan del juego (RPG Maker XP)

Juego de terror psicológico basado en *Cows* (Matthew Stokoe, 1998).
Se hace en RPG Maker XP (RGSS1). El trabajo se automatiza con el MCP `rpgmaker-xp`.

## 0. Antes de empezar: derechos y límites

- **Derechos de autor.** *Cows* está protegido. Una adaptación fiel (trama, personajes, nombres) puede hacerse para uso personal. Para **publicarla o venderla** (itch, Steam) hace falta permiso del autor o de su editorial.
  - Alternativa segura: un juego **inspirado** en el libro, con nombres, ciudad y giros propios. Se decide antes de publicar; el diseño sirve para ambos caminos.
- **Texto.** No se copia texto del libro. Todos los diálogos y notas del juego son originales y adaptan las escenas.
- **Contenido.** El libro tiene contenido sexual extremo (incluida zoofilia y abuso). El juego lo **omite o lo sugiere fuera de cámara**: elipsis, fundido a negro, consecuencias.
  - El terror sale de la atmósfera, la violencia, el cuerpo y la psicología.
  - Ninguna escena sexual explícita.
  - Aviso de contenido al iniciar.

## 1. Concepto

Steven, de 25 años, vive en un piso sórdido bajo el dominio de su madre (la «Bestia»). Solo tiene a Perro, un chucho paralítico, y la televisión de los 50 como refugio mental.

Entra a trabajar en un **matadero**. Allí el capataz Cripps lo empuja a matar.

Una vaca Guernsey que habla le susurra desde una rejilla de ventilación. Viene de la manada que vive en las **alcantarillas** y que quiere vengarse de Cripps.

Lucy, la vecina de arriba, cree que el sufrimiento se acumula como un **veneno** físico dentro del cuerpo y que puede encontrarse en las vísceras.

Steven pasa de víctima a verdugo y termina como rey-dios de una manada carnívora bajo la ciudad.

**Tema central:** la carne y el control. Quién es ganado y quién es carnicero.

## 2. Estructura (largo: ~8–12 h, 6 actos)

| Acto | Lugar principal | Núcleo jugable | Final del acto |
|---|---|---|---|
| I. El piso | Piso de la madre, escalera, calle | Rutina opresiva: tareas, esconderse de la madre, la tele como «zona segura» | Consigue el trabajo en el matadero |
| II. La cadena | Matadero: corrales, línea de desposte, cámaras frías, oficina de Cripps | Turnos con minijuegos de trabajo, sigilo frente a Cripps, primer contacto con la Guernsey por la rejilla | Primera muerte «obligada» |
| III. Lucy | Piso de arriba, carnicerías, hospital/laboratorio improvisado | Investigación del «veneno»: buscar pruebas en vísceras (puzles de inventario), relación con Lucy | Lucy se rompe; Steven elige |
| IV. Bajo la ciudad | Alcantarillas, la cámara de la manada | Exploración en oscuridad (linterna con batería), la manada como facción, persecuciones | Pacto con la Guernsey contra Cripps |
| V. La matanza | Matadero de noche | Infiltración y venganza; varios caminos (sigilo/violencia) | Muerte de Cripps |
| VI. Rey-dios | Túneles profundos, ciudad tomada | Consecuencias de las decisiones; la madre y Perro | 3 finales según decisiones |

**Finales:**
- Rey de la manada, el final del libro.
- Huida (traiciona a la manada).
- Ganado: Steven termina en la cadena.

## 3. Mecánicas

- **Exploración y puzles** al estilo *Ib*, *Mad Father* o *Yume Nikki*: llaves, notas, inventario y objetos combinables.
- **Cordura/«Veneno»:** una barra que sube con lo que Steven ve y hace.
  - Distorsiona tiles, sonido y diálogos (alucinaciones).
  - La tele del piso la baja.
- **Persecuciones** (madre, Cripps, la manada hambrienta) con escondites (armarios, cámaras frías).
- **Turnos en el matadero:** minijuegos cortos (ritmo y precisión) que pagan dinero y desbloquean zonas.
- **Decisiones con peso:** variables y switches que cambian diálogos, aliados y final.
- **Sin combate clásico.** Si se quiere algo de acción, enfrentamientos puntuales scripteados.
- **Guardado** solo en puntos concretos (la tele, un altar en las alcantarillas).

## 4. Arte y sonido

- Base: tiles de 32 px de RMXP, con paleta desaturada.
  - Piso: amarillento y nicotina.
  - Matadero: blanco clínico con rojo.
  - Alcantarillas: verde negro.
- Retratos (faces) para los diálogos: Steven, la madre, Lucy, Cripps, la Guernsey y Perro.
  - Se pueden crear con PixelLab o ComfyUI local, con un estilo coherente.
- Recursos encontrados (revisar la licencia de cada uno antes de usarlo):
  - **Evil Dungeon asset pack** (sevarihk), hecho para RPG Maker XP: https://sevarihk.itch.io/evil-dungeon-asset-pack
  - **KR Original Horror Kit** (kokororeflections). Permite uso comercial y temas maduros. Es para MV/MZ (48 px) y habría que reescalarlo a 32 px: https://kokororeflections.itch.io/kr-original-horror-kit-for-rpg-maker
  - Lista de recursos de terror para RPG Maker en itch: https://itch.io/game-assets/released/tag-horror/tag-rpgmaker/tag-tileset
  - **Lo que falta y habría que crear:** matadero (ganchos, canales de sangre, cintas), vacas (incluida la Guernsey) y tele de los 50.
- Sonido: ambientes industriales, goteo, mugidos distorsionados y estática de TV. Usar bancos libres (freesound CC0).

## 5. Técnica

- **MCP `rpgmaker-xp`**: crea y edita mapas, eventos, base de datos y scripts directamente en `Data/*.rxdata`.
  - **El editor debe estar cerrado** mientras se modifican los datos.
- Git en el proyecto (commit por avance) y respaldo en `../Vacas_respaldo_original`.
- Scripts RGSS a añadir:
  - Iluminación con linterna.
  - Barra de cordura con efectos de pantalla.
  - Mensajes con retrato.
  - Menú simplificado de terror.
  - Persecución con IA de búsqueda.
  - Guardado restringido.

## 6. Hoja de ruta

1. **Prototipo vertical (Acto I completo):** piso, madre, Perro, tele, cordura y guardado. Sirve para validar el tono.
2. Base de datos y scripts núcleo (cordura, linterna, retratos, persecución).
3. Acto II (matadero) con sus minijuegos.
4. Actos III–IV.
5. Actos V–VI y finales.
6. Arte propio (retratos, matadero, vacas), sonido y pulido.
7. Pruebas y build (Game.exe + RTP incluido).

## Fuentes de investigación

- Wikipedia, Matthew Stokoe: https://en.wikipedia.org/wiki/Matthew_Stokoe
- Kirkus Reviews, *Cows*: https://www.kirkusreviews.com/book-reviews/matthew-stokoe/cows/print/
- SuperSummary (resúmenes y personajes): https://www.supersummary.com/cows/character-list/
