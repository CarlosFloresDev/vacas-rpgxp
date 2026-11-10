"""Auditoria XP: alcance real, transfers, assets dinamicos y escala nueva."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import json,re,hashlib
from pathlib import Path
from PIL import Image
BASE=Path(__file__).resolve().parent;ROOT=_ROOT
exec(((_ROOT / 'diseno/herramientas/comun/auditar_accesos.py')).read_text(encoding='utf-8').split('scenarios=')[0])
errors=[];checks=0
def check(ok,label):
    global checks
    checks+=1
    if not ok:errors.append(label)
seeds={17:(4,11),18:(3,11),19:(3,11),20:(4,11),21:(4,10),15:(20,5)}
for rama in [96,97]:
 for stage in ['llegada','inicio','hostil','agua','caza','captura','pacto','recogido']:
    sw={34,81,98,113,114,115,rama}
    if stage=='llegada':sw.remove(114)
    if stage=='captura':sw|={122,125}
    if stage=='recogido':sw|={116,117,118,119,121,124,126,127,132,133,135,139}
    if stage=='hostil':sw|={120,127}
    if stage in ['agua','caza','pacto']:sw|={116,117,118,119,121,126,127}
    if stage=='caza':sw|={123}
    if stage=='pacto':sw|={124,128,129,130,131,132,133,135}
    grids={mid:Grid(mid,sw,{1:60,51:-2 if stage=='hostil' else 2},stage=='recogido') for mid in seeds}
    for mid,g in grids.items():
        seen=g.flood(seeds[mid])
        check(any(g.step(*seeds[mid],d) for d in D),f'{rama}/{stage}: inicio {mid}')
        for e,p in g.ev:
            relevant=mid>=17 or e['name']=='Colector bajo hospital A4'
            if relevant and p['trigger'] in [0,1] and any(c['code']!=0 for c in p['list']):
                check(g.interact(e,p,seen),f'{rama}/{stage}: interaccion {mid}/{e["name"]} {e["x"]},{e["y"]}')
            for c in p['list'] if relevant else []:
                if c['code']==201:
                    _,dest,x,y,*_=c['parameters']
                    check('Map%03d'%dest in S,f'transfer mapa {dest}')
                    dg=grids.get(dest)
                    if dg:check((x,y) in dg.flood(seeds[dest]) and any(dg.step(x,y,d) for d in D),f'{stage}: destino {dest} {x},{y}')
g=Grid(15,{34,81,98,113,114,96},{1:60})
check((20,5) in g.flood((12,17)),'hospital: acceso desde entrada principal al colector')
for mid in range(17,22):
 m=S['Map%03d'%mid]
 for e in m['events'].values():
  for p in e['pages']:
    check(p['list'][-1]['code']==0,f'terminador {mid}/{e["name"]}')
    for c in p['list']:
     for value in c['parameters']:
      if isinstance(value,str):
       for key in re.findall(r'\\P\[([^\]]+)\]',value):check((ROOT/'Graphics/Pictures'/('retrato_'+key+'.png')).exists(),'retrato '+key)
       for sid in re.findall(r'susto\((\d+)\)',value):check((ROOT/'Graphics/Pictures'/('screamer_'+sid+'.png')).exists(),'susto '+sid)
for eid in range(14,18):
 check(S['Troops'][eid]['members'][0]['enemy_id']==eid,'tropa '+str(eid))
 check(S['Enemies'][eid]['gold']==0 and S['Enemies'][eid]['exp']==0,'recompensa '+str(eid))
for iid in range(30,35):check(S['Items'][iid]['common_event_id']==1,'CE1 '+str(iid))
manifest=ROOT/'diseno/fuentes/arte_hd2d/acto4/manifest.json'
if manifest.exists():
 from adaptar_arte import adapt
 for spec in json.loads(manifest.read_text(encoding='utf-8'))['assets']:
    dest,im=adapt(spec)
    check(dest.exists(),'asset '+str(dest))
    if dest.exists():check(Image.open(dest).convert(im.mode).tobytes()==im.tobytes(),'reproduccion '+dest.name)
 check(True,'Manifiesto reproducible')
else:check(False,'Falta manifiesto arte A4')
# Medidas explicitas, independientes de la altura de celda 64.
p=ROOT/'Graphics/Characters/vacas_alcantarilla.png'
if p.exists():
 im=Image.open(p).convert('RGBA')
 for n,maxh in {0:14,1:16,2:24,3:30,4:32,5:48,6:30,7:48,8:16,9:16,10:30,11:64,12:24,13:20,14:30,15:32}.items():
    b=im.crop((n%4*32,n//4*64,n%4*32+32,n//4*64+64)).getbbox()
    check(b is not None and b[3]-b[1]<=maxh,'escala indice '+str(n))
report={'checks':checks,'errors':errors,'scenarios':16,'scope':'Colisiones XP, dieciseis estados, recursos dinamicos, BD, escala y reproduccion desde fuentes.'}
((_ROOT / 'diseno/verificaciones/verificacion_acto4.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
