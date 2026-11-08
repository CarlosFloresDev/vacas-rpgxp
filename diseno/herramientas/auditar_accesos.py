"""Auditor de colisiones XP: prioridades, bits direccionales y páginas activas.
Ejecutar tras node inspeccionar.mjs. Informe reproducible, no modifica datos.
"""
import json
from pathlib import Path
from collections import deque
BASE=Path(__file__).resolve().parent
S=json.loads((BASE/'snapshot.json').read_text(encoding='utf-8-sig'))
D={2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}
SEEDS={1:(9,7),2:(6,12),3:(9,3),4:(7,6),5:(15,19),6:(9,12),7:(28,4),8:(5,21),9:(1,17),10:(9,12),11:(1,7)}
# Destinos temporales de una escena: no se devuelve control aquí. La secuencia
# vuelve a transferir al pasillo al acabar el sueño/escondite.
HIDDEN={(2,1,4):'bajo la cama',(2,7,3):'dentro del armario',(2,10,5):'dentro de la bañera'}
def active(m,sw,var,self_on=False):
 out=[]
 for e in m['events'].values():
  for p in reversed(e['pages']):
   c=p['condition']
   if c['switch1_valid'] and c['switch1_id'] not in sw:continue
   if c['switch2_valid'] and c['switch2_id'] not in sw:continue
   if c['variable_valid'] and var.get(c['variable_id'],0)<c['variable_value']:continue
   if c['self_switch_valid'] and not self_on:continue
   out.append((e,p));break
 return out
class Grid:
 def __init__(self,mid,sw,var,self_on=False):
  self.mid=mid;self.m=S['Map%03d'%mid];self.t=S['Tilesets'][self.m['tileset_id']];self.ev=active(self.m,sw,var,self_on)
 def valid(self,x,y):return 0<=x<self.m['width'] and 0<=y<self.m['height']
 def tilepass(self,x,y,d):
  if not self.valid(x,y):return False
  bit=(1<<(d//2-1))&15 if d else 0
  for e,p in self.ev:
   g=p['graphic'];tid=g['tile_id']
   if (e['x'],e['y'])==(x,y) and not p['through']:
    pas=self.t['passages']['data'][tid]
    if pas&bit or pas&15==15:return False
    if self.t['priorities']['data'][tid]==0:return True
  for z in (2,1,0):
   tid=self.m['data']['data'][x+y*self.m['width']+z*self.m['width']*self.m['height']]
   pas=self.t['passages']['data'][tid]
   if pas&bit or pas&15==15:return False
   if self.t['priorities']['data'][tid]==0:return True
  return True
 def step(self,x,y,d):
  dx,dy=D[d];nx,ny=x+dx,y+dy
  if not(self.tilepass(x,y,d) and self.tilepass(nx,ny,10-d)):return False
  return not any((e['x'],e['y'])==(nx,ny) and not p['through'] and p['graphic']['character_name'] for e,p in self.ev)
 def flood(self,seed):
  seen={seed};q=deque([seed])
  while q:
   x,y=q.popleft()
   for d,(dx,dy) in D.items():
    n=x+dx,y+dy
    if n not in seen and self.step(x,y,d):seen.add(n);q.append(n)
  return seen
 def interact(self,e,p,seen):
  x,y=e['x'],e['y']
  over=(not p['graphic']['character_name'] or p['through']) and self.tilepass(x,y,0)
  if over:return (x,y) in seen
  return any((x+dx,y+dy) in seen for dx,dy in D.values())

scenarios=[('A1 despertar',set(),{}),('A1 tareas',{1,2,18},{2:2}),('A1 cena',set(range(1,9))|{18,19,20},{2:3}),('A1 noche',set(range(1,10))|{18},{2:4}),('A1 busqueda',set(range(1,11))|{18},{2:5}),('A1 manana',set(range(1,9))|{12,13,18},{2:6})]
for turn in range(1,4):
 for phase in range(10):
  sw=set(range(1,9))|{12,13,14,18,19,20,22,23,24,25}
  if turn==2 and phase in [4,5]:sw.add(26)
  if turn==2 and phase in [6,7]:sw.add(29)
  if turn==3:sw.add(43)
  if turn==3 and phase>=5:sw|={34,35,38,41}
  scenarios.append((f'A2 T{turn} F{phase}',sw,{7:turn,8:phase,1:55}))
 scenarios.append((f'A2 noche{turn}',{1,2,3,4,5,6,7,8,12,13,18,22,27,28}|({43} if turn==3 else set()),{7:turn,8:9}))
issues=set();doorchecks=0;targetchecks=0;checked=set();intentional=set()
for name,sw,var in scenarios:
 for selfs in [False,True]:
  grids={i:Grid(i,sw,var,selfs) for i in range(1,12)}
  for mid,g in grids.items():
   reached=g.flood(SEEDS[mid])
   if mid==2:
    for x,y in [(5,8),(12,8),(22,8),(6,17),(22,17),(3,18)]:
     if (x,y) not in reached:issues.add((name,'zona interior inaccesible',mid,x,y))
   for e,p in g.ev:
    transfers=[c for c in p['list'] if c['code']==201]
    if (transfers or any(word in e['name'].lower() for word in ['puerta','salida','portal','manga','bajada'])) and p['trigger'] in [0,1,2]:
     doorchecks+=1;checked.add((mid,e['id'],e['name']))
     if not g.interact(e,p,reached):issues.add((name,'evento de transferencia inaccesible',mid,e['name'],e['x'],e['y']))
    for c in transfers:
     _,dest,x,y,*_=c['parameters'];targetchecks+=1
     if (dest,x,y) in HIDDEN:intentional.add((dest,x,y,HIDDEN[dest,x,y]));continue
     dg=grids[dest]
     if not any(dg.step(x,y,d) for d in D):issues.add((name,'destino sin salida',mid,e['name'],dest,x,y))
report={'escenarios':len(scenarios)*2,'comprobaciones_puerta':doorchecks,'comprobaciones_destino':targetchecks,'puertas':sorted(checked),'destinos_de_escena':sorted(intentional),'problemas':sorted(issues)}
(BASE.parent/'auditoria_accesos.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Escenarios:',report['escenarios'],'puertas:',doorchecks,'destinos:',targetchecks,'problemas:',len(issues))
for i in sorted(issues)[:45]:print(i)
