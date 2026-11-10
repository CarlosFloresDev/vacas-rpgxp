"""Referencias, arte y comandos generados. No escribe datos del juego."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import json,re
from pathlib import Path
from PIL import Image
B=Path(__file__).resolve().parent;root=_ROOT
s=json.loads(((_ROOT / 'diseno/verificaciones/inventario/snapshot.json')).read_text(encoding='utf-8-sig'));errors=[];messages=portraits=0
sw=s['System']['switches'];vs=s['System']['variables']
def ref(names,id,where):
 if not 0<id<len(names) or not names[id]:errors.append(f'{where}: referencia sin nombre {id}')
def commands(lst,where):
 global messages,portraits
 if not lst or lst[-1]['code']!=0:errors.append(where+': falta terminador')
 for c in lst:
  p=c['parameters'];code=c['code']
  if code==101:
   messages+=1
   portraits+=bool(re.search(r'\\P\[',p[0]))
  if code in [101,401]:
   for key in re.findall(r'\\P\[([^\]]+)\]',p[0]):
    if not (root/'Graphics/Pictures'/('retrato_'+key+'.png')).exists():errors.append(where+': retrato '+key)
  if code==121:
   for id in range(p[0],p[1]+1):ref(sw,id,where+' interruptor')
  if code==122:
   for id in range(p[0],p[1]+1):ref(vs,id,where+' variable')
  if code==111:
   if p[0]==0:ref(sw,p[1],where+' condicion')
   if p[0]==1:ref(vs,p[1],where+' condicion')
  if code==117 and not s['CommonEvents'][p[0]]:errors.append(where+': evento comun')
  if code==301 and not 1<=p[0]<=9:errors.append(where+': tropa '+str(p))
  if code==355 or code==655:
   for id in re.findall(r'\$game_switches\[(\d+)\]',p[0]):ref(sw,int(id),where+' script')
   for id in re.findall(r'\$game_variables\[(\d+)\]',p[0]):ref(vs,int(id),where+' script')
for mid in range(1,12):
 for e in s['Map%03d'%mid]['events'].values():
  for idx,p in enumerate(e['pages']):
   where=f'mapa {mid}, {e["name"]}, pagina {idx}'
   c=p['condition']
   for k in [1,2]:
    if c[f'switch{k}_valid']:ref(sw,c[f'switch{k}_id'],where)
   if c['variable_valid']:ref(vs,c['variable_id'],where)
   commands(p['list'],where)
for ce in s['CommonEvents'][1:]:
 if ce and ce['list']:commands(ce['list'],'evento comun '+str(ce['id']))
for t in s['Troops'][1:10]:
 for p in t['pages']:commands(p['list'],'tropa '+str(t['id']))
for entry in json.loads((root/'diseno/fuentes/catalogos/arte_provisional.json').read_text(encoding='utf-8')):
 im=Image.open(root/entry['archivo']);im.verify()
for id in range(1,10):
 e=s['Enemies'][id]
 for a in e['actions']:
  if a['kind']==1 and not s['Skills'][a['skill_id']]:errors.append('habilidad enemiga inexistente')
 assert len(e['element_ranks']['data'])==17
for id in range(61,68):ref(sw,id,'susto')
print('Cajas:',messages,'con retrato:',portraits,'PNG:',len(json.loads((root/'diseno/fuentes/catalogos/arte_provisional.json').read_text(encoding='utf-8'))))
print('Errores:',len(errors))
for e in errors:print(e)
if errors:raise SystemExit(1)
