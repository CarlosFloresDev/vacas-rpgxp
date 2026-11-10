"""Actualiza auditoría completa y trazabilidad de la pasada1–16."""
import json, hashlib
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[2];A=R/'diseno/arte_hd2d/arte_mapas';B=R/'diseno/respaldos/antes_arte_mapas'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
current=read(R/'diseno/auditoria_arte.json');initial=read(R/'diseno/auditoria_arte_inicial.json')
old_audit=read(B/'diseno/auditoria_arte.json')
manifest=read(A/'manifest.json');gens=read(A/'generaciones.json')
assert len(gens)==8
for g in gens:
    p=R/g['source'];assert p.exists();g['sha256']=sha(p)
    if g['key']=='props':g['discarded_cells']={'4':'sofá generado para banco; sustituido por banco aprobado de arte_final','6':'camilla horizontal girada; se conserva camilla aprobada fase2 y se sustituye mancha'}
(A/'generaciones.json').write_text(json.dumps(gens,ensure_ascii=False,indent=2),encoding='utf8')
for a in manifest['assets']+manifest['compositions']:
    p=R/a['destination'];a['sha256']=sha(p)
    q=B/p.relative_to(R)
    if not q.exists():q=B/'RTP'/p.relative_to(R/'Graphics')
    assert q.exists(),f'Falta respaldo {p}'
    a['backup']=str(q.relative_to(R)).replace('\\','/');a['backup_sha256']=sha(q)
manifest['review']={'all_comparisons_opened':list(range(1,17)),'light_overview_opened':'diseno/capturas/arte_mapas_luz_resumen.png',
                   'limits':'Renders MCP con páginas de evento iniciales y máscaras reales; no simulan tono narrativo ni niebla animada. No se ejecutó Game.exe.',
                   'retained_unsafe_rtp_tiles':[],'approved_retained':['base industrial vacas_matadero','banco de arte_final','camilla de vacas_laboratorio','personajes/objetos fase2 aprobados','autotiles propios 053-Wall01 y vacas_canal']}
(A/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
rank={v:i for i,v in enumerate(['OK','PLACEHOLDER o RTP','REUTILIZADO o TINTADO','INCORRECTO','FALTA'])}
def counts(rows):
    files={}
    for a in rows:
        k=(a['folder'],a['name']);files[k]=max(files.get(k,'OK'),a['category'],key=lambda c:rank[c])
    c=Counter(files.values());return {k:c[k] for k in ['OK','REUTILIZADO o TINTADO','PLACEHOLDER o RTP','INCORRECTO','FALTA']}
final=counts(current['assets']);initial_counts=counts(initial['assets'])
pending=[]
for a in current['assets']:
    if a['category']=='OK':continue
    tech=a['name'].startswith(('revision_luz','acto5_luz','acto6_luz','feka_'))
    exposure='componente_tecnico' if tech else 'mapas' if a['maps'] else 'solo_base_datos'
    pending.append(dict(asset_id=a['id'],name=a['folder']+'/'+a['name'],maps=a['maps'],technical=tech,exposure=exposure))
assert not any(p['exposure']=='mapas' for p in pending)
current.update(initial_file_counts=initial_counts,final_file_counts=final,initial_variant_counts=initial['counts'],
               final_variant_counts=current['counts'],pending=pending,
               completion_status='Pasada de mapas1–16 terminada; quedan recursos solo en BD, componentes técnicos y lógica del seguidor de Perro.',
               verification_reports=['diseno/verificacion_arte_mapas.json','diseno/verificacion_arte_mapas_marshal.json','diseno/validacion_assets_arte_mapas.json'],
               map_art_pass={'graphics':24,'replaced_local':16,'local_rtp_overrides':8,'source_generations':8,
                             'overlay_tiles':1955,'prop_instances':122,'battleback_fields':3,
                             'manifest':'diseno/arte_hd2d/arte_mapas/manifest.json'},
               previous_art_pass=old_audit.get('corrections',{}))
current['semantic_gaps']=[g for g in current['semantic_gaps'] if g['name']=='seguidor_Perro']
(R/'diseno/auditoria_arte.json').write_text(json.dumps(current,ensure_ascii=False,indent=2),encoding='utf8')
generated_md=(R/'diseno/AUDITORIA_ARTE.md').read_text(encoding='utf8')
catalog=generated_md[generated_md.index('## Catálogo completo'):]
header=(B/'AUDITORIA_ARTE.md').read_text(encoding='utf8').split('## Inventario actual completo')[0]
header=header.replace('| OK | 108 | 187 |',f'| OK | 108 | {final["OK"]} |').replace('| PLACEHOLDER o RTP | 326 | 308 |',f'| PLACEHOLDER o RTP | 326 | {final["PLACEHOLDER o RTP"]} |')
header=header.replace('## Correcciones integradas','## Correcciones integradas de la pasada22–32').replace('## Verificación y láminas','## Verificación y láminas de la pasada22–32')
new='''## Pasada de arte de mapas1–16 — 10 de noviembre de2026

Terminada con ocho fuentes nuevas de **image_gen integrado**, adaptación con `adaptar_arte.py` y composición CPU del mismo modo que22–32. No se ha dibujado utilería nueva en PIL. [Prompts y fuentes](arte_hd2d/arte_mapas/generaciones.json), [manifiesto con hashes y respaldos](arte_hd2d/arte_mapas/manifest.json), [método/reproducción](arte_hd2d/arte_mapas/README.md).

- 24 PNG integrados: las16 hojas `revision_mapaNN` reemplazadas y ocho recursos RTP sustituidos mediante archivos locales (siete autotiles y `185-Light02`). Se conserva la base industrial aprobada y los personajes/objetos ya aprobados; se recomponen1.955 tiles de decoración y122 instancias de mobiliario con sus anclas originales. Las bases doméstica/urbana RTP tienen materiales nuevos.
- Se mantienen exactamente dimensiones de hoja, cuadrícula de32px, índices de cada tile, capas, coordenadas, eventos, pasabilidad, prioridades y terreno. Las hojas se reconstruyeron antes de intervenir y coincidieron píxel a píxel con las16 originales. Los siete autotiles conservan alfa, disposición, número de fotogramas y1.330 equivalencias de aristas de cuartos16px; el agua tiene cuatro fases propias.
- `185-Light02` conserva128×256, celdas32×64 y las cuatro filas/patrones. Su evento no cambió. Se conservan las máscaras de luz técnicas existentes. Tres pantallas de lámpara del laboratorio se adaptaron a sus huellas.
- Las referencias `battleback_name` de los tilesets53/54/55 (mapas2–4) apuntan a `ui_piso`, el mismo fondo propio que usa su zona en `Scene_Battle`. Los registros RTP originales18/9 siguen como recursos de BD sin mapa; no se modificaron fuera de alcance.
- Revisión visual de las16 láminas a escala nativa y del resumen con luz. Se corrigió ruido en suelos, anclas de bandas del atlas urbano y rampas de grises. El sofá generado para banco y la camilla girada se descartaron: se usan los diseños aprobados de banco y camilla, con la mancha PIL de esta última sustituida por sangre generada. Objetos de mesa pequeños y camilla de64px conservados.
- No quedaron tiles RTP pendientes por riesgo de unión en esta pasada. Los materiales ya aprobados conservados no constituyen excepciones RTP. Las seis hojas de autotile declaradas para la calle se han sustituido aunque el mapa4 no contiene celdas de autotile.

Respaldo inmutable de los reemplazos locales, originales RTP, Data completo y auditoría: [antes_arte_mapas](respaldos/antes_arte_mapas/). No se accedió a `.git`, no se modificó `Vacas.cfg` y no se inició ni cerró `Game.exe`.

Validación: [47 archivos Marshal](verificacion_arte_mapas_marshal.json),46 idénticos byte a byte; los32 mapas permanecen idénticos. Solo cambian tres cadenas de fondo en `Tilesets.rxdata`; **todas** las tablas de pasabilidad, prioridades y terreno son idénticas. [125.280 pasos direccionales](verificacion_arte_mapas.json) en cuatro estados por mapa, cero diferencias. [Gráficos/audio](validacion_assets_arte_mapas.json):1.051 referencias, cero ausencias; auditoría ampliada de gráficos/scripts:2.055 ocurrencias, cero ausencias. Carga y round-trip con el lector Marshal de RGSS/MCP; no se ejecutó el motor.

Láminas antes/después a1×:

'''
new+='\n'.join(f'- [Mapa {i:02}](capturas/arte_mapas_comparacion_{i:02}.png)' for i in range(1,17))
new+='\n\n[Resumen con máscaras de luz reales](capturas/arte_mapas_luz_resumen.png). También se guardan renders individuales antes/después y sus vistas con luz. Los cuadrados azules son marcadores del render MCP; no aparecen en el juego. Los renders no simulan tono narrativo, niebla animada ni transiciones del motor.\n\n'
header=header.replace('## Correcciones integradas de la pasada22–32',new+'## Correcciones integradas de la pasada22–32')
start=header.index('## Pendientes reales, por prioridad');end=header.index('## Reproducción',start)
replacement='''## Pendientes reales, por prioridad

1. Recursos sin mapa asociado:259 variantes solo en BD (incluidos los dos battlebacks RTP que ya no se usan en mapas2–4). Resolver uso efectivo antes de regenerar o limpiar registros; no se presume que estén muertos.
2. Treinta y dos componentes técnicos propios:27 máscaras de luz y cinco de marca Feka. Conservan su clasificación estricta PLACEHOLDER por procedencia CPU; su geometría y alfa se mantienen. No equivalen a utilería plana pendiente.
3. Seguidor de Perro: pendiente de lógica de arrastre entre mapas; sus assets existen.

Las291 variantes no OK equivalen a284 archivos distintos. Hay211 archivos OK de495; no quedan recursos ilustrativos RTP/PIL asociados a mapas en el inventario actual. No se afirma que todo el inventario de BD tenga arte propio. La valoración humana de la partida en motor sigue pendiente.

'''
header=header[:start]+replacement+header[end:]
header=header.replace('## Reproducción','## Reproducción histórica de la pasada22–32')
header+='\nLa pasada1–16 se reproduce con `arte_mapas.py install`, `extras`, `floors`, `corrections`, y `verificar_arte_mapas.mjs --apply`; ver su [README](arte_hd2d/arte_mapas/README.md). No ejecutar `finalizar_arte_final.py` para cerrar esta pasada: usar `finalizar_arte_mapas.py` después de la auditoría, para conservar los recuentos actuales.\n\n## Inventario actual completo\n\n'
(R/'diseno/AUDITORIA_ARTE.md').write_text(header+catalog,encoding='utf8')
(A/'resultado.json').write_text(json.dumps({'file_counts':final,'variant_counts':current['counts'],'graphics':24,'sources':8,'pending':dict(Counter(p['exposure'] for p in pending)),'global_complete':False},ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'files':final,'variants':current['counts'],'missing':len(current['missing'])},ensure_ascii=False))
