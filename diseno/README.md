# Vacas: índice del proyecto

El juego ejecuta **`Data/Scripts.rxdata`**. `scripts/` contiene las 16 fuentes Ruby propias y `scripts/motor/` las 39 secciones est?ndar adaptadas para HD; [manifest.json](scripts/manifest.json) registra nombre e índice real (base 0). Los scripts estándar del motor y `Main` permanecen en el archivo del motor.

| Carpeta | Contenido |
| --- | --- |
| [docs/](docs/) | Diseño: [historia](docs/historia/), [sistemas](docs/sistemas/), [arte](docs/arte/), [plan](docs/PLAN.md) y [repaso final](docs/REPASO_FINAL.md). |
| [scripts/](scripts/) | Fuentes RGSS1/Ruby 1.8, cabeceras de función, switches y variables. |
| [herramientas/comun/](herramientas/comun/) | Inventario, verificador general, instalador vigente, puente MCP, rutas compartidas y arneses transversales. |
| [herramientas/actos/](herramientas/actos/) | Generadores, mapas, contenido y pruebas propios de cada acto, del 1 al 6. |
| [herramientas/arte/](herramientas/arte/) y [audio/](herramientas/audio/) | Adaptación, composición, instalación y revisiones de recursos. |
| [verificaciones/](verificaciones/) | Todos los informes activos, logs, inventario y extracción temporal de scripts del motor. |
| [capturas/](capturas/) | `actos/`, `arte/` e `interfaz/`; vistas de revisión, ajenas al juego. |
| [fuentes/](fuentes/) | `audio_fuentes/`, `arte_hd2d/`, `arte_provisional/`, `marca/` y `catalogos/`. Los prompts y créditos originales se conservan junto a sus fuentes. |
| [respaldos/](respaldos/) | Instantáneas históricas conservadas con su estructura y contenido originales. |
| [archivo/](archivo/) | Lotes de operaciones, registros auxiliares, `ui_carga.txt`, `Vacas.cfg.bak`, fuentes antiguas y programas de la migración. |

La raíz conserva `Game.exe`, `Game.ini`, `Game.rxproj`, `RGSS104E.dll`, `Data/`, `Graphics/` y `Audio/`, con sus nombres y subcarpetas del motor. También conserva `Vacas.cfg` y `Save1.rxdata`: el guardado debe seguir siendo visible en Cargar. `.mcp-backup/` es la ubicación de trabajo del MCP. Los créditos distribuidos están en [CREDITOS_AUDIO.md](docs/sistemas/CREDITOS_AUDIO.md); el juego ya los incluye en su script de interfaz y no lee ese documento.

## Ejecutar la versi?n HD

Abrir **`Vacas.exe`** desde la ra?z: mkxp-z, lienzo panor?mico 640?360, pantalla completa con escalado entero n?tido (?3 exacto en 1920?1080). **Alt+Enter** alterna entre ventana y pantalla completa. `Game.exe` sigue disponible para el editor y usa 640?480. Los guardados conservan sus nombres.

[Gu?a HD, cambios, licencia y verificaci?n](docs/sistemas/HD.md). Comprobaci?n sin abrir el juego: `python diseno/herramientas/comun/verificar_hd.py`. El respaldo previo est? en `respaldos/antes_hd/`.

## Probar cada acto

Abrir `Game.exe` desde la raíz. En el título, mantener las teclas indicadas **al confirmar Nueva partida** (Enter/Espacio). Los atajos corresponden al mapeo predeterminado de RPG Maker XP.

| Acto | Atajo | Variante y guía |
| --- | --- | --- |
| I | Nueva partida sin modificadores | [Acto I](docs/historia/ACTO_I.md). |
| II | Mayús | [Acto II](docs/historia/ACTO_II.md). |
| III | Ctrl | Ctrl + Mayús prepara resistencia; [Acto III](docs/historia/ACTO_III.md). |
| IV | Alt | Alt + Mayús prepara pruebas; [Acto IV](docs/historia/ACTO_IV.md). |
| V | Q | Q + W prepara venganza; [Acto V](docs/historia/ACTO_V.md). |
| VI | Ctrl + W | Abre selector de rama; añadir Mayús activa la variante cruel; [Acto VI](docs/historia/ACTO_VI.md). |

Los programas `probar_*.mjs` y `prueba_*.rb` son arneses de integración: algunos instalan temporalmente un `Main` de prueba y abren su propio juego. Para revisar esta organización se usaron las comprobaciones de lectura que siguen; no se abrió ni cerró ningún `Game.exe`.

## Instalar fuentes Ruby

Ejecutar desde la raíz:

```powershell
node diseno/herramientas/comun/instalar_scripts.mjs
# Vista previa: comprueba nombre, índice y Marshal, sin escribir Data.
node diseno/herramientas/comun/instalar_scripts.mjs --aplicar
# Instalación explícita: respalda y reemplaza solo las 55 secciones del manifiesto.
```

El instalador vigente es `instalar_scripts.mjs`. No agrega ni reordena secciones. El manifiesto HD incluye las 16 secciones propias y 39 est?ndar adaptadas. Los instaladores anteriores (`instalar_interfaz.mjs`, `instalar_fase45.mjs`, `instalar_intro_feka.rb`, `audio/instalar_audio.rb`) se conservan como pasos de sus fases: afectan subconjuntos distintos, por eso no se fusionaron. Los `build_*`, `preparar_*`, `maps*`, `aplicar_*` y `integrar_*` reconstruyen contenido y pueden modificar datos o fuentes; no forman parte de la instalación habitual de scripts.

## Verificar e inventariar

La revisión de concurso está documentada en [Jugabilidad](docs/sistemas/JUGABILIDAD.md): diagnóstico del jarabe, correcciones por mapa, auditoría reproducible y límites de las pruebas HD.

Requiere Python con Pillow, Node.js, Ruby y el MCP local de RPG Maker XP utilizado por el proyecto. Ruby se detecta por `VACAS_RUBY`, `PATH` o su ubicación original en `D:/DevTools/ruby/`. El puente MCP conserva su dependencia externa en `D:/DevTools/mcp/rpgmaker-xp/`. El RTP se puede indicar con `RPGMAKER_RTP_PATH`; por defecto se usa la instalación original de Steam.

```powershell
python diseno/herramientas/comun/verificar_proyecto.py
node diseno/herramientas/comun/inspeccionar.mjs --solo-lectura
python diseno/herramientas/comun/verificar_sistemas.py
python diseno/herramientas/comun/verificar_enlaces.py
node diseno/herramientas/comun/render_captura.mjs 1
```

El verificador general comprueba hashes del motor, configuración y partida frente al inventario anterior, Marshal con Ruby, sintaxis, igualdad de tokens entre fuentes y secciones instaladas, enlaces y assets de datos con RTP. También comprueba que ningún script instalado lea `diseno/`. `--informe` guarda el resultado en [verificacion_organizacion.json](verificaciones/verificacion_organizacion.json). No ejecuta el juego.

`inspeccionar.mjs` sin `--solo-lectura` actualiza únicamente `verificaciones/inventario/snapshot.json` y `verificaciones/scripts_motor/`; hacerlo antes de usar verificadores históricos que dependen del snapshot. `sincronizar_scripts.py` extrae las fuentes desde ese snapshot y conserva copias anteriores si difieren: usarlo después de cambiar scripts desde el editor, no para instalar cambios de las fuentes.

El render lee los datos y gráficos y escribe solamente un PNG en `capturas/actos/`. Acepta un segundo argumento con otra ruta PNG dentro de `capturas/`. No reproduce niebla animada, tono narrativo ni prioridades del motor. [Captura comprobada](capturas/actos/comprobacion_mapa1.png).

Los verificadores de fases conservan sus escenarios y comparaciones con respaldos de aquella fase. Para comprobar el estado actual completo se usa `verificar_proyecto.py`; una comparación histórica fallida no equivale a un fallo de carga del proyecto actual.

## Inventario y trazabilidad

[Inventario anterior](verificaciones/inventario_antes.json): entradas originales de raíz, `diseno/` y herramientas, más hashes de los 475 archivos protegidos. [Traslados](verificaciones/traslados.json): correspondencia de las 1.885 rutas movidas. [Organización y decisiones](docs/ORGANIZACION.md).
