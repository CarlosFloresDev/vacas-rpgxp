# Repaso final — fases 4 y 5

10 de noviembre de 2026. Todo el trabajo se limita al proyecto; no se accede a
`.git`, no se modifica `Vacas.cfg`, no se cierra ningún Game.exe ajeno ni se usa GPU.
Se lanzó **un solo Game.exe propio**. Los detalles visuales están en
[CINEMATICAS.md](CINEMATICAS.md).

## Cambios concretos

- Añadida `Vacas_Cinematicas`: apertura, cinco tarjetas y refuerzo de tres finales.
- Cuatro capturas de mapas en Pictures, derivadas con el renderer existente.
- Suavizado el minijuego de corte en `Vacas_Matadero`; números abajo.
- Añadidos verificador global, recorrido continuo, balance reproducible y pruebas
  de entradas de cinemáticas. Se reutilizan inspección, `rx.mjs`, validadores y arnés del VI.
- Los créditos del título **ya incluían** Carlos — dirección, arte, diseño;
  Alexandre — historia; Ithalo "Ander" — sonido. Se comprobaron y conservaron,
  junto con las atribuciones completas del audio y los créditos finales.

Único Data modificado: **Scripts.rxdata**. Respaldo previo en
[respaldos/antes_fase45/Data](respaldos/antes_fase45/Data/), más la fuente anterior
del minijuego. La auditoría de instalación compara las 105 secciones originales:
solo cambia el código de **Vacas_Matadero**, se añade **Vacas_Cinematicas** y
**Main y las otras 104 secciones originales conservan sus campos exactos**.
El resultado instalado contiene 106 secciones.

## Flujo completo y contratos

`mapa/evento` identifica el punto del editor; S = switch, V = variable, O = objeto.
Las tarjetas llaman a los preparadores existentes y no reemplazan sus guardas.

| Tramo | Productor / estado necesario | Entrada siguiente |
|---|---|---|
| Arranque | Main → Feka → aviso → título. Nueva partida crea solo a Steven. | Apertura de 54 s → mapa 1. |
| Prólogo | **1/1** activa S1, V2=1 y V1=15; se desactiva mediante self-switch A. | Mapa **2**, (2,4), despertar y tareas. |
| Acto I | Madre **2/14** entrega O4/lista y O7/llave. Abrelatas O2 y lata O1 permiten alimentar a Perro; jarabe O3 y carne O5 se entregan; anuncio O6. S2–8, S19/20; escondite o captura producen S12/13. | Reclutador **4/19**, página condicionada por S13, activa S14 y V2=7; `fin_del_acto`. |
| I → II | `empezar_acto2`: S22/23, V7=1, V8=0; misma partida y llave. | Tarjeta II → mapa **5**, (15,19). |
| Acto II | V7 turnos 1–3, V8 fases 0–9. Fichar → mono → cinta/manguera → corte/clasificar/registro → cajón. **8/59** activa S34 y una sola rama S35/S36; O10 registro; **3/15** da O13/nota de Lucy. Última noche en **2/4** o cama duplicada enlaza `fin_del_acto2`. | Guarda de III: **S34**. El recorrido prueba las tres jornadas sin usar el atajo. |
| II → III | `empezar_acto3`: S81 y personaje sin mono; conserva elección, huella y nota. | Tarjeta III → mapa **12**, (12,17). |
| Acto III | O14 tarros; O16 hígado, O17 riñón, O18 sal; Elena entrega material/control. S104–106 preparaciones; S88 resultados. **16/8** resuelve jefe y decisión: S95/98, S96 o S97, V23=1 o 2; O28/cuaderno y O29/llave. | Guarda de IV: **S98**. |
| III → IV | `empezar_acto4`: S113/115; O30/linterna y dos O31/pilas; V52=100; V51 según Lucy. Inicialización idempotente. | Tarjeta IV → mapa **17**, (4,11); acceso físico también desde **15/8**. |
| Acto IV | Rueda O32; retorno antes de descarga produce S118, V54=2. **20/4** resuelve Cencerro/Pastor y pacto: S130/131/132/135, S133 o S134; O33/chapa. **21/6** cierra el acto. | Guarda de V: **S132**. |
| IV → V | `empezar_acto5`: S140; V57 alarma=0, V58/59 dominio/piedad según pacto, V60 capturas=0, V61=1. | Tarjeta V → mapa **22**, (3,11). |
| Acto V | O35/llave y O36/cizalla en **22/6**. Noria S148; persecución de 25 termina en S151. Umbral **26/8** activa S167. **26/9** exige vencer a Cripps (S156) y elige una rama S160/Rey, S161/Ganado o S162/Huida; S159. **27/3** activa S168. | Cancelas **27/15–16** activan **S163** y llaman a VI. |
| V → VI | `empezar_acto6` exige **S163 y una rama 160–162**; activa S176 y limpia persecuciones/temporizador/bloqueos. | Tarjeta VI, también por puerta física → mapa **28**, (3,13). |
| Acto VI | **28/4**: Censo/S178 → ciudad 29; madre **30/5**: S181/182 y elección S192. Galería **31/3–5**: V65=3 y S184; altar 32. | **32/7** prepara tropa 35, 36 o 37; derrota permite reintento, victoria activa S187. |
| Cierre | Epílogo VN → `reydios_terminar`: S188, S189/190/191, V68=1/2/3 y registro de final visto. | Dos planos de la rama → FIN → créditos completos → título, sin volver a Feka. |

El recorrido de prueba ejecuta páginas **activas** del intérprete original en I–V,
no inyecta los switches de historia y conserva inventario/variables entre actos.
Solo acelera el reloj de la caza de V, responde a mensajes, sustituye la destreza
manual por resultados de minijuego y resuelve los combates del recorrido como victoria.
Después se prueban las acciones y minijuegos por separado. El VI cubre seis casos:
tres ramas por dos antecedentes, incluyendo derrota/reintento, madre, Perro,
captura recuperable, compuertas, persistencia, FIN, créditos y título.

## Equilibrio

Steven parte de **360 Salud y 80 Aliento**. Respirar cuesta 0, tiene potencia de
curación 70, devuelve 18 de aliento y limpia Pánico/Asco/Culpa; Poner nombre cuesta
8 y tiene potencia 62. Los encuentros preparan recursos y recuperan al terminar.
El inventario **no contiene pociones de Salud/Aliento**: los objetos son herramientas,
muestras y recuerdos; tele, Perro, altar y radios cubren el descanso y el veneno.
No se añaden consumibles que puedan gastarse y bloquear un jefe obligatorio.

Se revisaron las tropas usadas **1–21 y 33–37**: un enemigo por tropa.
Las 22–32 son entradas RTP sin encuentros de la campaña; no se alteran.

| Etapa | Enemigos normales / jefes, Salud | Medianas de rondas observadas |
|---|---|---|
| I–II | Normales 125–300; Rey del cajón 650 | Normales 2–5; Rey 15 |
| III | 230–300; Diagnóstico 720 | 3–5; jefe 18 |
| IV | 270–310; Pastor 760 | 5; jefe 18 |
| V | 330–360; Cripps 860–1070 según alarma 0–3 | 5–6; jefe 21–29 |
| VI | Censo 340, Mesa 390; final limitado a 650–990 | 5–6; jefe 13–25 según rama y Salud |

[balance_fase45.tsv](balance_fase45.tsv) registra **680 simulaciones**: 34 casos
por 20 semillas, con los métodos reales `attack_effect`, `skill_effect`, selección
`make_action` y eliminación automática de estados. Incluye extremos de Cripps y
las tres variantes finales. Todas terminan con victoria usando Respirar ante estados,
Salud <200 o Aliento <8; jefes entre **10 y 39 rondas** en los extremos probados.
Se conserva la Salud/ataque de los enemigos: no hay evidencia para subirlos o bajarlos.
La simulación usa actor primero, no reproduce toda la iniciativa, selección de menú,
animaciones ni presión humana. No demuestra la dificultad percibida de un combate nativo.

**Cambio del corte:** antes, ancho `70 − 8×r` (mínimo 26), velocidad `4 + 0,9×r`.
Ahora, ancho `70 − 6×r` (mínimo 38), velocidad `min(4 + 0,6×r, 7)`.
En sus seis rondas reales, la ventana baja de 70 a **40 píxeles**, velocidad 4 a **7**:
la última pasa de aproximadamente **88 ms a 143 ms** a 40 fps. Se mantienen seis
rondas, espera máxima de nueve segundos por ronda y condiciones de continuación;
fallar sigue permitiendo progresar. El mínimo de 38 protege posibles llamadas con más rondas.

La cinta conserva 12 piezas, velocidad inicial 3 y +0,25 por pieza; la noria 16,
con 40% de flechas invertidas. Se ejecutaron sus bucles originales, así como el
corte, con entradas perfectas y con cero entradas: resultado máximo o cero,
terminación y liberación de recursos en los seis casos.

Persecuciones conservadas: madre **30 s**; persiana III **35 s**; Muesca IV **32 s**;
descarga IV **28 s**; Cripps V **30/40 s** según reputación; compuertas VI **35 s**.
Los refugios/capturas dejan continuar. En VI los mensajes pausan el reloj, el orden
incorrecto resta 3 s y el agua reinicia cierres sin quitar objetos ni causar game over.
No se cambia tiempo sin evidencia de una imposibilidad geométrica o de control.

## Coherencia y verificaciones

- `inspeccionar.mjs`: **47 rxdata** cargados y round-trip Marshal semántico en memoria.
- Sintaxis con `D:/DevTools/ruby/rubyinstaller-3.3.6-1-x64/bin/ruby.exe -c`:
  **125 archivos** (106 secciones, 15 fuentes y cuatro auxiliares), cero errores.
  Los scripts instalados nuevos/modificados mantienen sintaxis RGSS1/Ruby 1.8.
- Verificador global: **99 switches requeridos ON** por páginas/ramas, todos con
  productor potencial; no cuenta simples asignaciones `false` como activación.
  El informe lista lectores, escritores, entregas/consumos, temporizadores y contratos.
  El análisis estático de bucles es conservador; se complementa con el recorrido ejecutado.
- Conectividad MCP: **32 mapas, 110 transferencias**, cero destinos rotos,
  mapas huérfanos o inalcanzables.
- Colisión direccional XP: I–II, 78 escenarios, 2.134 puertas y 1.635 destinos;
  III, 493 comprobaciones; IV, 1.226; V, **1.616 interacciones**; VI, 3.153.
  Cero problemas en los escenarios comprobados.
- Assets MCP: **1.051 referencias**, cero ausentes; cuatro capturas nuevas verificadas
  como PNG válidos. Los 32 mapas tienen BGM y BGS válidos en `MAP_AUDIO`/`zone`.
  Se conservan las claves locales y traducciones de audio RTP existentes.
- Nombres y textos: referencias de objetos/tropas y retratos coherentes, sin errores
  evidentes de codificación en mensajes. **STEPHEN** en la tarjeta de fichar es un
  error intencional de Cripps descrito por el juego; Steven conserva su nombre.
  No se promete una corrección literaria exhaustiva de todos los diálogos.
- Instalación: [auditoria_instalacion_fase45.json](auditoria_instalacion_fase45.json),
  secciones e IDs conservados; no cambian mapas ni otras bases de datos.

**Resultado del motor nativo: parcial, no aprobado como recorrido completo.**
[verificacion_rgss_fase45.txt](verificacion_rgss_fase45.txt) conserva el intento
real, incluida su falla. Antes de detenerse comprobó apertura completa de 54 s,
salto, continuar/cancelar/saltar desde menú, atajos, BGM/BGS de 32 zonas, equipo Feka,
Marshal y tareas del I. Se detuvo en el armario porque el arnés local no actualizaba
personajes durante la ruta forzada; el juego normal sí los actualiza en Scene_Map.
Se corrigió `prueba_fase45.rb` para actualizar jugador y eventos en cada paso.
**No se volvió a ejecutar Game.exe**, respetando el máximo de una ejecución.
El pequeño ajuste de corte se instaló después de ese intento y se comprobó en simulación.

La continuación usa [simular_fase45.rb](herramientas/simular_fase45.rb), Ruby 3 y
dobles de primitivas de RGSS, cargando la lógica instalada desde el snapshot.
[verificacion_simulada_fase45.txt](verificacion_simulada_fase45.txt) termina en OK:
**601 registros**, recorrido continuo de los seis actos, seis ramas/antecedentes,
680 balances y seis ejecuciones de minijuegos. Las fórmulas, intérprete y escenas
son originales; **el renderer y el sonido son dobles**, y los datos se reconstruyen
del snapshot JSON. Esta prueba no equivale a una aprobación de RGSS nativo.

## Reproducir y pendiente humano

Desde la raíz, con el editor cerrado:

```powershell
node diseno/herramientas/instalar_fase45.mjs
Push-Location diseno/herramientas
node inspeccionar.mjs
Pop-Location
node diseno/herramientas/auditar_instalacion45.mjs
python -X utf8 diseno/herramientas/verificar_fase45.py
& 'D:/DevTools/ruby/rubyinstaller-3.3.6-1-x64/bin/ruby.exe' --disable-gems diseno/herramientas/simular_fase45.rb
```

Para un futuro turno sin el límite ya consumido: `node diseno/herramientas/probar_fase45.mjs`
ejecuta el arnés corregido en un Game.exe propio; restaura Scripts y finales de prueba,
y comprueba que Vacas.cfg sigue idéntico. No manipula procesos ajenos.

Pendiente: repetir ese arnés nativo corregido; partida humana desde Nueva partida
y desde guardados antiguos; tres finales; dificultad con iniciativa y errores de
jugador reales; reacción al corte y flechas azules; escucha de mezcla; encuadres,
legibilidad y ritmo de los planos; retorno de BGM tras saltos y puertas físicas.
Se mantienen los battlers y utilería provisionales ya documentados en los actos.
