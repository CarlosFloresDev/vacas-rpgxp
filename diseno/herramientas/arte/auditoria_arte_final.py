"""Auditoría estática RGSS1; no modifica Data/Graphics."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import json,re,hashlib,sys
from pathlib import Path
from collections import Counter
from PIL import Image
R=_ROOT
T=Path('D:/SteamLibrary/steamapps/common/RPGXP/rtp')
INITIAL='--initial' in sys.argv
B=R/'diseno/respaldos/antes_arte_final'
S=json.loads((B/'snapshot_inicial.json' if INITIAL else R/'diseno/verificaciones/inventario/snapshot.json').read_text(encoding='utf8'))
initial_hashes=json.loads((B/'hashes_iniciales.json').read_text(encoding='utf8'))
final_manifest=json.loads((R/'diseno/fuentes/arte_hd2d/arte_final/manifest.json').read_text(encoding='utf8'))
final_paths={a['destination'] for a in final_manifest['assets']+final_manifest.get('compositions',[])}
map_manifest=R/'diseno/fuentes/arte_hd2d/arte_mapas/manifest.json'
if map_manifest.exists():
 map_art=json.loads(map_manifest.read_text(encoding='utf8'))
 final_paths.update(a['destination'] for a in map_art['assets']+map_art.get('compositions',[]))
refs=[]
F=dict(character_name='Characters',battler_name='Battlers',tileset_name='Tilesets',panorama_name='Panoramas',fog_name='Fogs',battleback_name='Battlebacks',windowskin_name='Windowskins',title_name='Titles',gameover_name='Gameovers',icon_name='Icons',animation_name='Animations')
approved={a['path']:a for a in json.loads((R/'diseno/fuentes/arte_hd2d/estado_fase2.json').read_text(encoding='utf8'))['assets']}
provenance={}
for p in (R/'diseno/fuentes/arte_hd2d').rglob('*.json'):
 try:
  d=json.loads(p.read_text(encoding='utf-8-sig')); aa=d.get('assets',[]) if isinstance(d,dict) else d
  if isinstance(aa,list):
   for a in aa:
    if isinstance(a,dict) and a.get('destination') and a.get('source'): provenance[a['destination']]=str(p.relative_to(R)).replace('\\','/')
 except (ValueError,UnicodeError):pass
def act(m):return 'VI' if m>=28 else 'V' if m>=22 else 'IV' if m>=17 else 'III' if m>=12 else 'II' if m>=5 else 'I'
def add(f,n,s,m=None,h=0):
 if isinstance(n,str) and n:refs.append(dict(folder=f,name=n,source=s,map=m,act=act(m) if m else None,hue=h or 0))
def texts(t,s,m):
 for n in re.findall(r'\\P\[([^\]]+)\]',t,re.I):add('Pictures','retrato_'+n,s,m)
 for kind,n in re.findall(r"Cache\.(picture|battler|character|battleback|windowskin|icon|fog|panorama|autotile|tileset|animation|title|gameover)\s*\(\s*['\"]([^'\"]+)['\"]\s*[,)]",t):
  folder={'picture':'Pictures','battler':'Battlers','character':'Characters','battleback':'Battlebacks','windowskin':'Windowskins','icon':'Icons','fog':'Fogs','panorama':'Panoramas','autotile':'Autotiles','tileset':'Tilesets','animation':'Animations','title':'Titles','gameover':'Gameovers'}[kind]
  add(folder,n,s,m)
 for folder,n in re.findall(r'Graphics/(Characters|Battlers|Pictures|Tilesets|Autotiles|Transitions|Animations|Icons|Fogs|Panoramas|Windowskins|Titles|Gameovers|Battlebacks)/([A-Za-z0-9_-]+)(?:\.png|\.jpg|\.bmp)?',t):
  add(folder,n,s,m)
 for n in re.findall(r'(?:susto|screamer)\s*\(?\s*(\d+)',t):add('Pictures','screamer_'+n,s,m)
def walk(x,s,m=None):
 if isinstance(x,list):
  for i,v in enumerate(x):walk(v,f'{s}[{i}]',m)
 elif isinstance(x,dict):
  for k,v in x.items():
   if k in F:add(F[k],v,s+'.'+k,m,x.get(k.replace('_name','_hue'),0))
   if k=='autotile_names':
    for i,n in enumerate(v):add('Autotiles',n,s+f'.autotile_names[{i}]',m)
  c,p=x.get('code'),x.get('parameters',[])
  if x.get('_class')=='RPG::EventCommand':
   if c==231 and len(p)>1:add('Pictures',p[1],s+'.show_picture',m)
   if c==222 and p:add('Transitions',p[0],s+'.transition',m)
   if c in (207,337) and len(p)>1 and isinstance(p[1],int) and 0<p[1]<len(S['Animations']):
    walk(S['Animations'][p[1]],s+'.animation',m)
   if c==322 and len(p)>=5:add('Characters',p[1],s+'.actor_character',m,p[2]);add('Battlers',p[3],s+'.actor_battler',m,p[4])
   if c==131 and p:add('Windowskins',p[0],s+'.windowskin',m)
   if c==204 and len(p)>1:add({0:'Panoramas',1:'Fogs',2:'Battlebacks'}.get(p[0],'Pictures'),p[1],s+'.map_setting',m,p[2] if len(p)>2 else 0)
  if x.get('_class')=='RPG::MoveCommand' and c==41 and p:add('Characters',p[0],s+'.change_graphic',m,p[1] if len(p)>1 else 0)
  for k,v in x.items():
   if k not in ('data','passages','priorities','terrain_tags'):walk(v,s+'.'+k,m)
 elif isinstance(x,str):texts(x,s,m)
def battles(v):
 if isinstance(v,dict):
  if v.get('_class')=='RPG::EventCommand' and v.get('code')==301:
   p=v['parameters']
   if len(p)>1 and p[0]==0:yield p[1]
  for a in v.values():yield from battles(a)
 elif isinstance(v,list):
  for a in v:yield from battles(a)
def troop(tid,s,m=None):
 tr=S['Troops'][tid];walk(tr,s+f'.Troops[{tid}]',m)
 for mem in tr.get('members',[]):
  eid=mem['enemy_id']
  if eid<len(S['Enemies']):walk(S['Enemies'][eid],s+f'.Troops[{tid}].Enemies[{eid}]',m)
for k,d in S.items():
 if k in ('Scripts','MapInfos'):continue
 match=re.fullmatch(r'Map(\d+)',k);m=int(match[1]) if match else None
 walk(d,k,m)
 if m:
  walk(S['Tilesets'][d['tileset_id']],f'{k}.Tilesets[{d["tileset_id"]}]',m)
  for tid in sorted(set(battles(d))|set(d.get('encounter_list',[]))):troop(tid,k+'.battle',m)
def common_calls(v):
 if isinstance(v,dict):
  if v.get('_class')=='RPG::EventCommand' and v.get('code')==117 and v.get('parameters'):yield v['parameters'][0]
  for a in v.values():yield from common_calls(a)
 elif isinstance(v,list):
  for a in v:yield from common_calls(a)
for mid in range(1,33):
 seen=set();todo=list(common_calls(S[f'Map{mid:03}']))
 while todo:
  cid=todo.pop()
  if cid in seen or not (0<cid<len(S['CommonEvents'])):continue
  seen.add(cid);ce=S['CommonEvents'][cid]
  if not ce:continue
  walk(ce,f'Map{mid:03}.CommonEvents[{cid}]',mid)
  for tid in set(battles(ce)):troop(tid,f'Map{mid:03}.CommonEvents[{cid}].battle',mid)
  todo.extend(common_calls(ce))
for tr in S['Troops']:
 if tr:troop(tr['id'],'DB')
index={}
for base in (R,T):
 for p in (base/'Graphics').glob('*/*'):
  if p.suffix.lower() in ('.png','.jpg','.bmp','.jpeg'):index.setdefault(p.stem,set()).add(p.parent.name)
dynamic=[]
for sc in S['Scripts']:
 for ln,line in enumerate(sc['code'].splitlines(),1):
  if line.lstrip().startswith('#'):continue
  where=f'Scripts[{sc["index"]}] {sc["name"]}:{ln}';texts(line,where,None)
  for n in re.findall(r"""['"]([^'"\n]+)['"]""",line):
   for f in index.get(n,[]):add(f,n,where)
   if re.fullmatch(r'(?:steven|madre|lucy|cripps|guernsey|dog|muesca|junco)_(?:neutral|miedo|ira|susurro|calma|quiebre)',n):add('Pictures','retrato_'+n,where)
  if ('Cache.' in line or 'screamer_' in line or 'luz%' in line) and ('+' in line or 'sprintf' in line):dynamic.append(dict(source=where,code=line.strip()))
for m in range(1,33):
 for n in [f'acto6_luz{m:02}',f'acto5_luz{m:02}',f'revision_luz{m:02}',f'revision_luz_{m:02}']:
  if (R/'Graphics/Pictures'/f'{n}.png').exists():add('Pictures',n,'Scripts: máscara del mapa',m)
for n in ('mente_piso','mente_matadero','mente_tunel'):add('Battlebacks',n,'Scripts: Vacas_Mente fondo dinámico')
for f,pat in [('Pictures','ui_*'),('Icons','ui_estado_*'),('Battlebacks','ui_*')]:
 for p in (R/'Graphics'/f).glob(pat+'.png'):add(f,p.stem,'Scripts: Vacas_Interfaz familia dinámica')
zones={}
for sc in S['Scripts']:
 for mid,zone in re.findall(r'(\d+)\s*=>\s*\[:(piso|matadero|camaras|laboratorio|alcantarillas|manada)\b',sc['code']):zones[int(mid)]=zone
 for mid,zone in re.findall(r'MAP_AUDIO\[(\d+)\]\s*=\s*\[:(\w+)',sc['code']):zones[int(mid)]=zone
for mid,zone in zones.items():
 if 1<=mid<=32:add('Battlebacks','ui_'+zone,'Scripts: Scene_Battle fondo por MAP_AUDIO',mid)
def resolve(f,n):
 for base in (R,T):
  for ext in ('.png','.jpg','.bmp','.jpeg',''):
   p=base/'Graphics'/f/(n+ext)
   if p.is_file():
    rel=str(p.relative_to(R)).replace('\\','/') if base==R else None
    if INITIAL and base==R:
     if rel not in initial_hashes:continue
     if (B/rel).exists():return B/rel,False
    return p,base==T
 return None,False
def classify(r,p,rtp):
 n=r['name'];s=r['source'];path=f'Graphics/{r["folder"]}/{n}.png'
 if p is None:return 'FALTA','Sin archivo local ni en RTP instalado.'
 if not INITIAL and path in final_paths:return 'OK','Arte propio final generado con image_gen/adaptar_arte.py, revisado a tama?o final; no implica aprobaci?n humana nueva.'
 if n=='retrato_madre_neutral' and r['map']==30:return 'INCORRECTO','La madre envejecida del VI muestra el retrato anterior; falta variante propia.'
 if rtp or re.match(r'^\d{3}-',n):return 'PLACEHOLDER o RTP','RTP genérico; existencia no acredita autoría propia.'
 if r['hue']:return 'REUTILIZADO o TINTADO',f'Tinte RGSS hue={r["hue"]}.'
 if re.search(r'Enemies\[(18|19|20|21|33|34|35|36|37)\]',s):return 'REUTILIZADO o TINTADO','Enemigo V/VI usa visión anterior; ACTO_V/VI.'
 if n in ('screamer_12','screamer_13'):return 'REUTILIZADO o TINTADO','Reencuadre tintado de sustos 4/7; build_acto5.py.'
 if n in ('screamer_10','screamer_11'):return 'REUTILIZADO o TINTADO','Reencuadre de battler coro/pulmon; arte_acto4.py.'
 if n=='vacas_guernsey4':return 'INCORRECTO','Fuente vaca_canela, identidad distinta de Guernsey según biblia; arte_acto4.py.'
 if n in ('acto5_matanza','acto6_reydios'):return 'PLACEHOLDER o RTP','Hoja mixta con utilería PIL; maps5/maps6. Sofá como trono en 32.'
 if n.startswith('revision_mapa'):return 'PLACEHOLDER o RTP','Hoja mixta RTP/utilería PIL; revision_mapas.py.'
 if n.startswith('cine_'):return 'PLACEHOLDER o RTP','Render de mapa mixto 2/5/32/29; CINEMATICAS.md. Hereda provisional.'
 if path in provenance and n.startswith('ui_'):return 'OK','Dise?o propio image_gen y adaptaci?n t?cnica desde kit generado; arte_interfaz.py y '+provenance[path]
 if n.startswith(('ui_','feka_','acto5_luz','acto6_luz','revision_luz','luz_')):return 'PLACEHOLDER o RTP','Gráfico técnico/interfaz CPU/PIL; no ilustración HD-2D aprobada.'
 if path in approved:return 'OK','Inventario aprobado fase 1/2; tamaño actual revisado por separado.'
 if path in provenance:return 'OK','Fuente image_gen documentada: '+provenance[path]+'; aprobación final no presumida.'
 return 'PLACEHOLDER o RTP','Sin evidencia de aprobación/fuente en manifiestos; requiere revisión.'
catalog={}
for r in refs:
 p,rtp=resolve(r['folder'],r['name']);cat,why=classify(r,p,rtp);r.update(category=cat,reason=why)
 k=(r['folder'],r['name'],r['hue'],cat)
 if k not in catalog:catalog[k]=dict(id=len(catalog)+1,folder=r['folder'],name=r['name'],hue=r['hue'],category=cat,reason=why,resolved=str(p).replace('\\','/') if p else None,rtp=rtp,size=list(Image.open(p).size) if p else None,uses=[],maps=[])
 a=catalog[k];r['asset_id']=a['id'];a['uses'].append(r['source'])
 if r['map'] and r['map'] not in a['maps']:a['maps'].append(r['map'])
rows=list(catalog.values())
for a in rows:a['uses']=list(dict.fromkeys(a['uses']));a['maps'].sort()
sizes=[]
for a in rows:
 wh=a['size'];n=a['name']
 if a['folder']=='Characters' and wh and wh!=[128,192]:sizes.append(dict(asset_id=a['id'],name=n,size=wh,expected='128x192; 32x48',object_exception=any(k in n for k in ('cosas','muebles','matadero','puerta','furgoneta','tablon','vacas_vaca','alcantarilla','vacio','guernsey','laboratorio','perro','muesca','junco','185-Light02'))))
 if a['folder']=='Pictures' and wh and wh!=[640,480]:sizes.append(dict(asset_id=a['id'],name=n,size=wh,expected='640x480 si pantalla completa',component_exception=n.startswith(('retrato_','ui_','feka_','revision_','luz_'))))
counts={k:Counter(a['category'] for a in rows)[k] for k in ['OK','REUTILIZADO o TINTADO','PLACEHOLDER o RTP','INCORRECTO','FALTA']}
report=dict(method='Marshal: 47 rxdata y 106 scripts instalados. Referencias directas, tropas/combates por mapa, retratos VN y familias dinámicas; sin ejecutar Game.exe.',counting='Variantes únicas carpeta/nombre/hue/categoría. Un archivo puede ser OK para I y reutilizado para V. BD incluye reservas no necesariamente alcanzadas.',counts=counts,unique_files=len(set((a['folder'],a['name']) for a in rows)),assets=rows,references=refs,dynamic_script_sites=dynamic,size_findings=sizes,missing=[a['id'] for a in rows if a['category']=='FALTA'],semantic_gaps=[dict(category='FALTA',name='retrato_madre_envejecida',map=30,reason='Se usa madre_neutral; falta variante, no archivo roto.'),dict(category='FALTA',name='seguidor_Perro',act='VI',reason='Falta implementación de arrastre entre mapas; sí hay sprites estáticos.')])
(R/('diseno/verificaciones/auditoria_arte_inicial.json' if INITIAL else 'diseno/verificaciones/auditoria_arte.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
md=['# Auditoría de arte de Vacas','',report['method'],'',report['counting'],'','## Totales del inventario','','| Categoría | Variantes |','|---|---:|']+[f'| {k} | {v} |' for k,v in counts.items()]
md+=['',f'Archivos distintos: {report["unique_files"]}; ocurrencias: {len(refs)}. Las faltas narrativas adicionales se detallan en semantic_gaps y no se suman como archivos rotos.','','OK fase 1/2 se basa en inventario aprobado. Ampliaciones con fuente documentada tienen procedencia image_gen, sin presumir aprobación final. Recursos técnicos se separan por evidencia CPU; no se afirma plagio por parecido.','','## Prioridad de corrección','','1. Nueve enemigos V/VI: 18–21 y 33–37. Diseños propios con hue=0 y nombres exclusivos; preservar visiones anteriores.','2. Sustos 12/13, luego 10/11. Madre envejecida: retrato y asignación exclusiva al VI.','3. Trono 32 y utilería 22–32: sustituir conservando índices, anclas, escala y colisiones; no ejecutar generadores PIL provisionales.','4. Cinemáticas: cine_piso=2, cine_matadero=5, cine_altar=32, cine_ciudad=29; corregir el escenario y su encuadre.','5. Guernsey IV usa vaca_canela de otra identidad. Rubio/Sierra comparten silueta autorizada pero identidades narrativas distintas. Perro requiere seguidor con arrastre.','6. RTP visible y hojas mixtas anteriores, después recursos de BD dormidos. Interfaz/máscaras geométricas son componentes técnicos, no equivalentes a ilustración provisional.','','## Catálogo completo','','| ID | Recurso | Hue | Categoría | Mapas | Tamaño | Evidencia |','|---:|---|---:|---|---|---|---|']
for a in rows:md.append(f'| {a["id"]} | {a["folder"]}/{a["name"]} | {a["hue"]} | {a["category"]} | {", ".join(map(str,a["maps"])) or "BD/scripts"} | {a["size"]} | {a["reason"]} |')
md+=['','## Por mapa y acto','']
for m in range(1,33):
 md += [f'### Mapa {m:02} — Acto {act(m)} — {S["MapInfos"].get(str(m),{}).get("name","")}','']
 for a in rows:
  if m in a['maps']:md.append(f'- #{a["id"]} {a["folder"]}/{a["name"]}, hue {a["hue"]}: **{a["category"]}**.')
md+=['','## Cada referencia en Data/scripts','','Rutas exactas de objeto: evento/página/comando, enemigo y tropa. El JSON permite filtrar todas las ocurrencias.','']
for a in rows:
 md += [f'### #{a["id"]} {a["folder"]}/{a["name"]} — {a["category"]}','']+['- '+chr(96)+u+chr(96) for u in a['uses']]
md+=['','## Tamaños y límites','',f'{len(sizes)} variantes difieren del estándar general: detalle en size_findings del JSON. Objetos, retratos 240×340 y componentes UI tienen excepciones. Madre/Cripps humanos no estándar requieren ajuste a 48 px.','', 'Existir en RTP local no garantiza distribución autónoma. La inspección estática no prueba todas las ramas ni tiempos de animación; puntos de carga dinámica en dynamic_script_sites.','']
(R/('diseno/docs/arte/AUDITORIA_ARTE_INICIAL.md' if INITIAL else 'diseno/docs/arte/AUDITORIA_ARTE.md')).write_text('\n'.join(md),encoding='utf8')
print(json.dumps(dict(counts=counts,unique_files=report['unique_files'],references=len(refs),missing=len(report['missing']),sizes=len(sizes)),ensure_ascii=False))

