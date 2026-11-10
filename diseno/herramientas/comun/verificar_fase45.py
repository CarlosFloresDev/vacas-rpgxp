"""Repaso global reproducible sobre snapshot de inspeccionar.mjs. Solo lectura Data."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import json,re,subprocess,hashlib
from pathlib import Path
ROOT=_ROOT; BASE=Path(__file__).resolve().parent
S=json.loads(((_ROOT / 'diseno/verificaciones/inventario/snapshot.json')).read_text(encoding='utf8'))
code='\n'.join(s['code'] for s in S['Scripts'])
errors=[]; reads={}; writes={}; timers=[]; items=[]; fights=[]
def add(d,n,where):d.setdefault(int(n),set()).add(where)
constants=dict((k,int(v)) for k,v in re.findall(r'^\s*(SW_\w+)\s*=\s*(\d+)',code,re.M))
for script in S['Scripts']:
 text=script['code']; where='script '+script['name']
 for expr,rhs in re.findall(r'\$game_switches\[([^\]]+)\]\s*=(?!=)\s*([^\n]+)',text):
  if re.match(r'false\b',rhs):continue
  if expr.isdigit():add(writes,expr,where)
  elif expr in constants:add(writes,constants[expr],where)
 # Bucles con conjuntos literales: IDs reservados en los sistemas existentes.
 for var,body in re.findall(r'for\s+(\w+)\s+in\s+(\[[^\]]+\]|\d+\.\.\d+)',text):
  if re.search(r'\$game_switches\['+var+r'\]\s*=(?!=)\s*(?!false\b)\S',text):
   if body.startswith('['):ids=[constants.get(v.strip(),int(v.strip()) if v.strip().isdigit() else None) for v in body[1:-1].split(',')]
   else:
    a,b=map(int,body.split('..'));ids=range(a,b+1)
   for n in ids:
    if n is not None:add(writes,n,where+' bucle '+var)
# registrar_final: 188+rama, ramas 1..3. No supone que todas se activen juntas.
for n in [189,190,191]:add(writes,n,'Vacas.registrar_final: 188+rama (1..3)')

def commands(lst,where):
 for c in lst:
  p=c['parameters'];n=c['code']
  if n==121 and p[2]==0:
   for sid in range(p[0],p[1]+1):add(writes,sid,where)
  if n==111 and p[0]==0 and p[2]==0:add(reads,p[1],where)
  if n==124 and p[0]==0:timers.append([where,p[1]])
  if n==126:items.append([where,p])
  if n==301:fights.append([where,p[0]])
  if n in [101,401,102,402]:
   if any(bad in str(p) for bad in ['Ã¡','Ã©','Ã³','Â¿','�']):errors.append('Codificacion: '+where)
  if n in [355,655]:
   for sid in re.findall(r'\$game_switches\[(\d+)\]\s*=(?!=)\s*(?!false\b)\S',p[0]):add(writes,sid,where+' script de evento')
  if n==126 and not (0<p[0]<len(S['Items']) and S['Items'][p[0]]):errors.append('Item ausente '+where)
  if n==301 and not (0<p[0]<len(S['Troops']) and S['Troops'][p[0]]):errors.append('Tropa ausente '+where)
for mid in range(1,33):
 for e in S['Map%03d'%mid]['events'].values():
  for pi,p in enumerate(e['pages']):
   where='%d/%d %s p%d'%(mid,e['id'],e['name'],pi)
   for k in [1,2]:
    if p['condition']['switch%d_valid'%k]:add(reads,p['condition']['switch%d_id'%k],where)
   commands(p['list'],where)
for e in S['CommonEvents'][1:]:
 if e:commands(e['list'],'CE '+str(e['id']))
for t in S['Troops'][1:]:
 if t:
  for p in t['pages']:commands(p['list'],'tropa '+str(t['id']))
orphans=sorted(set(reads)-set(writes))
errors+=['Switch leido sin escritor: '+str(n) for n in orphans]
used=sorted(set(t for _,t in fights)|{1,4,5,7})
enemy_ids=sorted(set(m['enemy_id'] for t in used for m in S['Troops'][t]['members']))
enemies=[{k:e[k] for k in ['id','name','maxhp','maxsp','atk','pdef','mdef','agi']} for e in S['Enemies'][1:] if e['id'] in enemy_ids]
syntax=[]
for file in sorted((_tools.parent/'verificaciones/scripts_motor').glob('*.rb'))+sorted((ROOT/'diseno/scripts').glob('*.rb'))+[BASE/n for n in [str(_ROOT / 'diseno/herramientas/comun/prueba_fase45.rb'),str(_ROOT / 'diseno/herramientas/comun/recorrido_fase45.rb'),str(_ROOT / 'diseno/herramientas/comun/balance_fase45.rb'),str(_ROOT / 'diseno/herramientas/comun/simular_fase45.rb')]]:
 if not file.exists():continue
 p=subprocess.run(['D:/DevTools/ruby/rubyinstaller-3.3.6-1-x64/bin/ruby.exe','-c',str(file)],capture_output=True,text=True)
 syntax.append([str(file.relative_to(ROOT)),p.returncode==0])
 if p.returncode:errors.append(p.stderr)
backup=ROOT/'diseno/respaldos/antes_fase45/Data'
changed=[]
for p in backup.glob('*.rxdata'):
 if p.read_bytes()!=(ROOT/'Data'/p.name).read_bytes():changed.append(p.name)
exec(((_ROOT / 'diseno/herramientas/comun/auditar_accesos.py')).read_text(encoding='utf8').split('scenarios=')[0])
checks5=0;seeds5={22:(3,11),23:(12,13),24:(1,7),25:(2,3),26:(3,13),27:(3,3)}
for cruel in [False,True]:
 for stage in range(6):
  switches={98,113,118,132,135,140,134 if cruel else 133,97 if cruel else 96}
  if stage>0:switches|={143,144,145}
  if stage>1:switches|={146,147,148,152}
  if stage==3:switches|={150}
  if stage>3:switches|={151,167}
  if stage>4:switches|={156,159,160,168,163}
  for selfon in [False,True]:
   for mid,seed in seeds5.items():
    g=Grid(mid,switches,{51:0 if cruel else 3,57:3 if cruel else 0,58:5 if cruel else 1,59:0 if cruel else 4},selfon)
    seen=g.flood(seed)
    for event,page in g.ev:
     if page['trigger'] in [0,1,2] and any(c['code'] for c in page['list']):
      checks5+=1
      if not g.interact(event,page,seen):errors.append('Acceso V: %d/%s etapa%d'%(mid,event['name'],stage))
assets_cine=[]
from PIL import Image
for name in ['piso','matadero','altar','ciudad']:
 path=ROOT/'Graphics/Pictures'/('cine_'+name+'.png')
 with Image.open(path) as im:
  assets_cine.append([path.name,list(im.size)]);im.verify()
# Las cinco guardas y los destinos se verifican ademas ejecutando el interprete.
contracts=[{'desde':1,'hasta':2,'guardas':[13,14],'activa':22,'mapa':5,'xy':[15,19]},
 {'desde':2,'hasta':3,'guardas':[34],'activa':81,'mapa':12,'xy':[12,17]},
 {'desde':3,'hasta':4,'guardas':[98],'activa':113,'mapa':17,'xy':[4,11],'objetos':[29,30,31]},
 {'desde':4,'hasta':5,'guardas':[132],'activa':140,'mapa':22,'xy':[3,11],'objetos':[33]},
 {'desde':5,'hasta':6,'guardas':[163,'160|161|162'],'activa':176,'mapa':28,'xy':[3,13]}]
report={'errores':errors,'contratos':contracts,'switches_leidos':len(reads),'switches_sin_escritor':orphans,
 'lectores':{n:sorted(v) for n,v in reads.items()},'escritores':{n:sorted(v) for n,v in writes.items()},
 'temporizadores_segundos':timers,'entregas_consumos_items':items,'combates':fights,'enemigos_usados':enemies,
 'sintaxis':syntax,'rxdata_cargados':len(S),'Data_modificados':changed,
 'colisiones_acto5':checks5,'capturas_cinematicas':assets_cine,
 'alcance':'Escritores potenciales ON: asignaciones distintas de false y bucles literales. Lectores requieren ON. Existencia no demuestra alcanzabilidad. Contratos y rutas se ejecutan con interprete original; ver informe sobre limite del arnes RGSS nativo.'}
(ROOT/'diseno/verificaciones/verificacion_fase45.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('Repaso:',len(S),'rxdata;',len(syntax),'Ruby;',len(reads),'switches con lectores;',len(errors),'errores')
for e in errors:print(e)
raise SystemExit(bool(errors))
