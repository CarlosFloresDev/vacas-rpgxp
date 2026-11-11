"""Regenera la lista precisa de cambios que requieren Data, en solo lectura."""
import collections,json,re
from pathlib import Path
from auditar_coherencia import ROOT,OUT

def main():
    audit=json.loads((OUT/'auditoria_coherencia_arte.json').read_text(encoding='utf8'))
    data=json.loads((OUT/'coherencia_datos_lectura.json').read_text(encoding='utf8'))
    refs=json.loads((OUT/'coherencia_usos.json').read_text(encoding='utf8'))
    lines=['# Cambios de Data pendientes — coherencia de arte', '',
        'Lectura del estado actual; esta herramienta no modifica Data ni diseno/scripts. Índices de páginas/comandos entre corchetes desde cero; eventos y registros conservan su ID real.', '',
        '## Integración de anclas: comprobar primero', '',
        'Los PNG corregidos conservan su apoyo original: vacas 76/80, furgoneta 61/64 y muebles según índice. **No deben sumar una compensación adicional en Sprite_Character.**', '']
    source=(ROOT/'diseno/scripts/16_cinematicas.rb').read_text(encoding='utf8')
    if 'module Vacas_Anclas' in source:
        lines+=['PENDIENTE ACTIVO: la tarea paralela añadió `Vacas_Anclas::DESPLAZAMIENTOS` y la resta en `Sprite_Character#update` (16_cinematicas.rb). Retirar ese bloque y reinstalar únicamente esa sección en Scripts.rxdata. No quitar otras modificaciones de esa tarea. El verificador debe exigir igualdad de ancla PNG sin restar compensaciones antiguas. Todas las referencias afectadas figuran en coherencia_usos.json.', '']
    else:lines+=['No se detecta el bloque de compensaciones antiguo en la fuente actual. El verificador final comprueba los PNG directamente.', '']
    lines+=['## Actores RTP de reserva', '',
        'No aparecen como gráficos de eventos de mapa. Se prepararon hojas civiles propias y battlers con otros nombres. No se ha cambiado la identidad de un NPC del guion. System.party_members todavía contiene 1,2,7,8; el evento 1 del mapa 1 retira 2,7,8 con comandos129. Al limpiar las reservas, revisar también esta inicialización.', '',
        '| Registro (mapa/evento: ninguno) | Original | Sustituto preparado para character_name y battler_name | Contexto visual |',
        '|---|---|---|---|']
    roles=['obrero veterano','obrero bajo','obrera','transeúnte','reclutador','Lucy (reserva)','Remedios (reserva)']
    for i,role in zip(range(2,9),roles):
        a=data['Actors'][i]
        lines.append(f"| Actors[{i}] | {a['character_name']} / {a['battler_name']} | vacas_reserva_actor{i:02} (ambas carpetas) | {role} |")
    lines+=['','Cambiar ambos campos al nombre indicado; character_hue/battler_hue deben ser0. Estos recursos están preparados; las referencias originales siguen visibles en la auditoría hasta que otra tarea integre Data.', '',
        '## Bovinos: escala adulta que exige cambiar la hoja asignada', '',
        'Guernsey, Junco y Muesca usan celdas48×48: una longitud adulta de62px no cabe sin cambiar la geometría. Las hojas originales conservan tamaño; variantes320×320/celdas80×80 preparadas con sufijo `_80`. Al asignarlas, conservar dirección, patrón y resto de propiedades; revisar pasos estrechos/solapes en el motor. No cambia automáticamente la colisión de un evento XP.', '',
        '| Mapa | Evento | Página (editor, desde1) | Campo exacto | Sustituto |', '|---|---|---|---|---|']
    cows={'vacas_'+n:f'vacas_{n}_80' for n in ('guernsey4','junco','muesca')}
    for key,m in data.items():
        if not re.fullmatch(r'Map\d+',key):continue
        for eid,event in m['events'].items():
            for pi,page in enumerate(event['pages']):
                name=page['graphic']['character_name']
                if name in cows:lines.append(f"| {int(key[3:])} | {eid} | {pi+1} | graphic.character_name ({name}) | {cows[name]} |")
    lines+=['', 'Guernsey tras barrotes de vacas_matadero conserva su celda indexada; no sustituir toda esa hoja por un ciclo de marcha.', '',
        '## Animaciones con geometría heredada', '',
        '| Archivo original | Registros que lo referencian | Hoja preparada | Acción |','|---|---|---|---|']
    for name in ('016-Ice01','024-Support01'):
        uses=refs.get(f'Graphics/Animations/{name}.png',[])
        lines.append(f"| {name} | {'; '.join(u['ruta'] for u in uses)} | vacas_rejilla_{name} | Cambiar animation_name; mantiene celdas192 y añade ancho transparente hasta960. Sigue siendo arte RTP: no considerarlo regeneración. |")
    lines+=['', '## Restricción compartida Rubio / Sierra', '',
        'Map007 evento15, Map008 evento55 y Map023 evento4 comparten vacas_obrero2. Se conserva el equipo protector compatible con ambos retratos de la Biblia. Si se exige distinguirlos, preparar otra hoja de32×48 y cambiar solo graphic.character_name en las páginas del obrero de la sierra tras confirmar el rol narrativo. No se ha inventado una asignación.', '',
        '## Catálogo RTP: incidencias conservadas, no aprobadas', '',
        'La tabla enumera todos los PNG RTP locales con avisos y sus referencias exactas. Un registro de Tilesets/Animations/Armors no demuestra que sea alcanzable durante la partida. Los mapas actuales usan tilesets52–70, propios; no se sustituyen cincuenta atlas ajenos sin uso de mapa para silenciar el informe. Los avisos de alpha/saturación y las dos geometrías heredadas siguen pendientes en este catálogo. Antes de usar una reserva, sustituirla por arte del juego o retirar su referencia; no borrar archivos de forma indiscriminada.', '',
        '| PNG | Avisos | Referencias de solo lectura |', '|---|---|---|']
    for f in audit['archivos']:
        if f['rtp']['hash_identico']:
            lines.append(f"| {f['archivo']} | {', '.join(f['avisos'])} | {'; '.join(u['ruta'] for u in f['usos']) or 'Sin referencia literal detectada'} |")
    lines+=['', 'Los panoramas RTP y battlebacks de reservas que solo existen en el RTP externo no son PNG locales y no se incluyen en la medición de Graphics. Sus cadenas están en coherencia_usos.json. No hay panoramas locales que corregir.', '',
        '185-Light02 ya es una lámpara propia regenerada en la pasada de mapas; su nombre heredado NO la convierte en RTP. No requiere renombrarla. vacas_luz_escalera es un alias preparado y no asignado; no hace falta un cambio de Data por motivos de autoría.', '']
    (ROOT/'diseno/docs/arte/CAMBIOS_DATA_PENDIENTES.md').write_text('\n'.join(lines),encoding='utf8')
    summary={}
    for cat in sorted({Path(f['archivo']).parent.name for f in audit['archivos']}):
        fs=[f for f in audit['archivos'] if Path(f['archivo']).parent.name==cat]
        summary[cat]={'total':len(fs),'con_avisos':sum(bool(f['avisos']) for f in fs)}
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':main()
