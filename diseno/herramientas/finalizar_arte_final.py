"""Añade resultados, trazabilidad y pendientes al inventario completo."""
import json,hashlib
from collections import Counter
from pathlib import Path
from instalar_arte_final import R,A,B
CATS=['OK','REUTILIZADO o TINTADO','PLACEHOLDER o RTP','INCORRECTO','FALTA']
rank={v:i for i,v in enumerate(['OK','PLACEHOLDER o RTP','REUTILIZADO o TINTADO','INCORRECTO','FALTA'])}
def file_counts(rows):
 groups={}
 for a in rows:
  k=(a['folder'],a['name'])
  groups[k]=max([groups.get(k,'OK'),a['category']],key=lambda c:rank[c])
 counts=Counter(groups.values())
 return {c:counts[c] for c in CATS}
def run():
 before=json.loads((R/'diseno/auditoria_arte_inicial.json').read_text(encoding='utf8'))
 current=json.loads((R/'diseno/auditoria_arte.json').read_text(encoding='utf8'))
 hashes=json.loads((B/'hashes_iniciales.json').read_text(encoding='utf8'))
 changed=[]
 for p in (R/'Graphics').glob('*/*.png'):
  rel=str(p.relative_to(R)).replace('\\','/');sha=hashlib.sha256(p.read_bytes()).hexdigest()
  if hashes.get(rel)!=sha:changed.append(dict(path=rel,sha256=sha,new=rel not in hashes,backup=('diseno/respaldos/antes_arte_final/'+rel) if rel in hashes else None))
 pending=[]
 for a in current['assets']:
  if a['category']=='OK':continue
  technical=a['name'].startswith(('revision_luz','acto5_luz','acto6_luz','feka_'))
  exposure='mapas' if a['maps'] else 'scripts' if any(u.startswith('Scripts') for u in a['uses']) else 'solo_base_datos'
  a['exposure']=exposure;a['technical_component']=technical
  action='Revisar clasificación de componente técnico propio: máscara de luz/logo derivado de SVG. No equivale a utilería plana.' if technical else ('Sustituir arte mixto/RTP conservando índices y semántica de zona.' if a['maps'] else 'Resolver uso efectivo y sustituir/limpiar referencias RTP de BD; no presumir que sea visible ni que sea una reserva.')
  priority=4 if technical else 1 if a['maps'] else 3
  pending.append(dict(asset_id=a['id'],name=a['folder']+'/'+a['name'],maps=a['maps'],exposure=exposure,technical=technical,priority=priority,action=action))
 pending.sort(key=lambda a:(a['priority'],a['name']))
 initial_counts=file_counts(before['assets']);final_counts=file_counts(current['assets'])
 current.update(initial_file_counts=initial_counts,final_file_counts=final_counts,initial_variant_counts=before['counts'],final_variant_counts=current['counts'],corrections=dict(changed_graphics=changed,changed_graphics_count=len(changed),new_graphics=sum(a['new'] for a in changed),replaced_graphics=sum(not a['new'] for a in changed),sources='diseno/arte_hd2d/arte_final/generaciones.json',manifest='diseno/arte_hd2d/arte_final/manifest.json',method='image_gen integrado; adaptar_arte.py y composición CPU, sin nueva ilustración PIL ni GPU local.'),pending=pending,completion_status='Auditoría e integración prioritaria finalizadas. Sustitución global de todo el arte todavía incompleta: quedan escenarios iniciales/RTP y revisión de recursos de BD/técnicos.',verification_reports=['diseno/verificacion_arte_final.json','diseno/verificacion_arte_final_marshal.json'])
 current['counting']+=' file_counts usa un recurso por carpeta/nombre, tomando la categoría más grave de sus usos; counts sigue contando variantes por hue/contexto.'
 (R/'diseno/auditoria_arte.json').write_text(json.dumps(current,ensure_ascii=False,indent=2),encoding='utf8')
 gens=json.loads((A/'generaciones.json').read_text(encoding='utf-8-sig'))
 for g in gens:
  g['sha256']=hashlib.sha256((R/g['source']).read_bytes()).hexdigest()
  g['selected']=g['key']!='madre_envejecida'
  if not g['selected']:g['discard_reason']='Primer busto descartado por encuadre diferente del neutral; reemplazado por edición facial anclada al original.'
 (A/'generaciones.json').write_text(json.dumps(gens,ensure_ascii=False,indent=2),encoding='utf8')
 counts=dict(Counter(a['exposure'] for a in pending))
 summary=['# Auditoría de arte de Vacas','',
 '**Estado:** auditoría terminada e integración prioritaria hecha; todavía no puede afirmarse que todo el juego tenga arte propio.','',
 'Inventario inicial: 445 archivos gráficos distintos. Inventario actual: 495. La tabla cuenta archivos; el catálogo posterior distingue variantes de tono/uso. Un recurso correcto en un acto y mal reutilizado en otro recibe aquí la categoría más grave.','',
 '| Categoría por archivo | Inicial | Actual |','|---|---:|---:|']
 summary += [f'| {c} | {initial_counts[c]} | {final_counts[c]} |' for c in CATS]
 summary += ['', 'No hay referencias gráficas inexistentes entre las 2.055 ocurrencias rastreadas. Falta funcional aparte: seguidor de Perro entre mapas; su arte/sprites estáticos existen.','',
 '## Correcciones integradas','',
 f'- {len(changed)} PNG integrados: {sum(a["new"] for a in changed)} nuevos y {sum(not a["new"] for a in changed)} reemplazos. Originales en [respaldo](respaldos/antes_arte_final/).',
 '- Nueve battlers exclusivos para enemigos 18–21 y 33–37, sin tintes RGSS. Se conservan las visiones anteriores de los mismos personajes.',
 '- Sustos 10–13 con composiciones nuevas; ya no son reencuadres de battlers/sustos anteriores. Cuatro placas cine_piso/matadero/ciudad/altar originales 640×480.',
 '- Madre envejecida: edición de cabeza anclada al busto original, ropa/encuadre conservados y seis claves de retrato cambiadas solo en VI.',
 '- Trono/altar de 64 px y 56 tipos de utilería (52 del atlas más cuatro muebles domésticos) adaptados a huellas existentes en mapas 22–32; los objetos aprobados se conservan. Los objetos de mesa siguen a10–16px.',
 '- Guernsey de mapa con rombo crema, independiente de vaca_canela; madre y Cripps en hojas 128×192/celdas 32×48. Muesca/Junco son bovinos y conservan sus 192×192.',
 '- Cuarenta iconos de objeto y diez de habilidades mentales propios 24×24. Aferrarse a Perro se deriva de su referencia aprobada.',
 '- Autotile de muro y niebla propios. Se actualizaron defaults gráficos de System y fuentes de eventos para impedir que reaparezcan tintes/iconos viejos; los constructores PIL históricos se protegen contra ejecución directa.','',
 f'Fuentes: {len(gens)} generaciones en nube, {sum(g["selected"] for g in gens)} seleccionadas y una descartada por encuadre. [Prompts y fuentes](arte_hd2d/arte_final/generaciones.json), [manifiesto](arte_hd2d/arte_final/manifest.json). Los sustos/retratos conservan acabado ilustrado como fase 2; las paletas de zona se dirigen en prompts y los battlers/objetos se cuantizan sin dithering, conservando rampas de material.','',
 '## Verificación y láminas','',
 '4.005 comprobaciones de referencias de producción, tamaño, reproducción, estadísticas, eventos y respaldo; 158.400 pasos direccionales comparados en 12 escenarios de 11 mapas, sin diferencias. Comparación Marshal de 16 archivos: únicamente campos gráficos/iconos/tablas y seis claves de retrato; resto de textos y objetos conservados. Vacas.cfg y Scripts.rxdata mantienen sus hashes iniciales. No se ejecutó ni cerró Game.exe; no se accedió a .git.',
 '',
 'Mapas renderizados y las seis láminas revisadas visualmente a1×:']
 summary += [f'- [Mapas {n}–{min(n+1,32)}](capturas/arte_final_comparacion_{n:02}.png)' for n in range(22,33,2)]
 summary += ['', '[Enemigos](capturas/arte_final_enemigos.png), [personajes](capturas/arte_final_personajes.png), [madre](capturas/arte_final_madre.png), [iconos1×/3×](capturas/arte_final_iconos.png), [sustos 10/11](capturas/arte_final_sustos_10.png), [sustos 12/13](capturas/arte_final_sustos_12.png), [cinemáticas1](capturas/arte_final_cinematicas_1.png), [cinemáticas2](capturas/arte_final_cinematicas_2.png). También se revisaron vistas con las máscaras reales de luz.',
 '',
 'Los marcadores azules pertenecen al render de eventos MCP: no son gráficos del juego. Los renders no simulan niebla animada, tono narrativo ni movimiento/transición dentro de Game.exe. Queda la pasada humana en motor.','',
 '## Pendientes reales, por prioridad','',
 '1. Arte visible de los mapas1–16: las 16 hojas revision_mapaNN siguen mezclando RTP/utilería PIL. Revisar también sus siete autotiles RTP y el objeto 185-Light02 del mapa 3. Este trabajo no se ha reemplazado con generación apresurada de hojas que pueda romper sus uniones.',
 '2. Dos battlebacks RTP siguen declarados en tilesets de los mapas2–4. Scene_Battle los reemplaza por fondos ui_* propios, pero la referencia de BD todavía debe corregirse.',
 '3. Recursos sin mapa asociado: el inventario conserva las referencias de actores/enemigos/tilesets/animaciones/iconos predeterminados. Son 257 variantes solo en BD; no se afirma que todas estén muertas. Resolver su alcance antes de regenerar o limpiar registros.',
 '4. Treinta y dos componentes técnicos propios (27 máscaras de luz y cinco de marca Feka) se mantienen en PLACEHOLDER bajo la clasificación estricta de recursos PIL; su función técnica no es el problema de utilería plana. Validar esta excepción, conservando geometría/alpha si se retocan.',
 '5. Seguidor de Perro: pendiente de lógica de arrastre entre mapas, no de un PNG inexistente.','',
 'Las 315 variantes no OK equivalen a 308 archivos distintos. Los fallos de reutilización e identidad encontrados en los actos V/VI quedaron corregidos; la conversión de todo el juego sigue pendiente.','',
 '## Reproducción','',
 'Desde la raíz: generar snapshot con inspeccionar.mjs desde su carpeta; instalar_arte_final.py → componer_arte_final.py → instalar_iconos_arte_final.py → aplicar_arte_final.mjs → aplicar_iconos_arte_final.mjs. Volver a inspeccionar, ejecutar verificar_arte_final.py y verificar_arte_final_marshal.mjs, renderizar b_arte_final_despues.json y componer laminas_arte_final.py. Auditar con auditoria_arte_final.py --initial y sin argumento; finalizar_arte_final.py añade este resumen. Todos los comandos de Python bajo diseno/herramientas se ejecutan con -X utf8.',
 '',
 'Los manifiestos históricos de fase2/acto4 conservan la evidencia anterior; los PNG sustituidos se reproducen con el manifiesto final. No ejecutar arte_acto4.py/maps5.py/maps6.py ni b_cine_render.json para volver a dibujar recursos con sus constructores provisionales.','',
 '## Inventario actual completo','']
 original=(R/'diseno/AUDITORIA_ARTE.md').read_text(encoding='utf8')
 start=original.find('## Catálogo completo')
 if start>=0:original=original[start:]
 else:
  start=original.find('## Inventario actual completo')
  original=original[start:].split('## Inventario actual completo',1)[1].lstrip() if start>=0 else original
 (R/'diseno/AUDITORIA_ARTE.md').write_text('\n'.join(summary)+'\n'+original,encoding='utf8')
 (A/'resultado.json').write_text(json.dumps(dict(initial_file_counts=initial_counts,final_file_counts=final_counts,changed_graphics=len(changed),sources=len(gens),selected_sources=sum(g['selected'] for g in gens),pending_exposure=counts,global_complete=False),ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps(dict(initial_file_counts=initial_counts,final_file_counts=final_counts,graphics=len(changed),sources=len(gens),pending_exposure=counts),ensure_ascii=False))
if __name__=='__main__':run()

