"""Auditoría de los cinco mapas con colisiones direccionales nativas XP."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import json,re,subprocess,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parent;ROOT=_ROOT
exec(((_ROOT / 'diseno/herramientas/comun/auditar_accesos.py')).read_text(encoding='utf8').split('scenarios=')[0])
errors=[];checks=0
def check(ok,label):
    global checks
    checks+=1
    if not ok:errors.append(label)
seeds={28:(3,13),29:(3,13),30:(3,13),31:(3,13),32:(3,13)}
for rama in (160,161,162):
 for cruel in (False,True):
  for stage in ('inicio','casa','cierre','final'):
   sw={132,135,140,159,163,176,rama,97 if cruel else 96,134 if cruel else 133,171 if cruel else 147}
   if not cruel:sw.add(145)
   if stage!='inicio':sw|={177,178,179,180}
   if stage in ('cierre','final'):sw|={181,182}
   if stage=='cierre':sw.add(185)
   if stage=='final':sw|={184,186,187,188}
   for selfs in (False,True):
    grids={i:Grid(i,sw,{51:0 if cruel else 3,58:5 if cruel else 1,59:0 if cruel else 4},selfs) for i in seeds}
    for mid,g in grids.items():
     seen=g.flood(seeds[mid]);check(len(seen)>15,f'{mid}: entrada libre')
     for e,p in g.ev:
      if p['trigger'] in (0,1,2) and any(c['code']!=0 for c in p['list']):
       check(g.interact(e,p,seen),f'{rama}/{stage}/{selfs}: interacción {mid}/{e["name"]} ({e["x"]},{e["y"]})')
      for c in p['list']:
       if c['code']==201:
        _,dest,x,y,*_=c['parameters']
        check('Map%03d'%dest in S,f'mapa destino {dest}')
        if dest in grids:
         check((x,y) in grids[dest].flood(seeds[dest]) and any(grids[dest].step(x,y,d) for d in D),f'destino inaccesible {mid} -> {dest} ({x},{y})')
for mid in seeds:
 m=S['Map%03d'%mid]
 check(m['width']==20 and m['height']==15,f'escala mapa {mid}')
 for e in m['events'].values():
  for p in e['pages']:
   check(p['list'][-1]['code']==0,f'terminador {mid}/{e["name"]}')
   for c in p['list']:
    for v in c['parameters']:
     if isinstance(v,str):
      for key in re.findall(r'\\P\[([^\]]+)\]',v):check((ROOT/'Graphics/Pictures'/('retrato_'+key+'.png')).exists(),'retrato '+key)
for eid in range(33,38):
 check(S['Troops'][eid]['members'][0]['enemy_id']==eid,'tropa '+str(eid))
 check(S['Enemies'][eid]['gold']==0 and S['Enemies'][eid]['exp']==0,'sin recompensa '+str(eid))
 check((ROOT/'Graphics/Battlers'/(S['Enemies'][eid]['battler_name']+'.png')).exists(),'battler '+str(eid))
report={'checks':checks,'scenarios':48,'errors':sorted(set(errors))}
(ROOT/'diseno/verificaciones/verificacion_acto6.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(checks,'comprobaciones;',len(report['errors']),'errores')
for e in report['errors'][:40]:print(e)
if errors:raise SystemExit(1)
