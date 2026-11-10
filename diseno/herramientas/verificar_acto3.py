"""Referencias dinámicas, puzles y colisiones del Acto III; solo lectura de Data."""
import json,re
from pathlib import Path
from PIL import Image
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
# Reutilizar semántica exacta del auditor XP sin ejecutar su informe histórico.
exec((BASE/'auditar_accesos.py').read_text(encoding='utf-8').split('scenarios=')[0])
errors=[];checks=0
def check(ok,label):
    global checks
    checks+=1
    if not ok:errors.append(label)
seeds={12:(12,17),13:(10,12),14:(3,12),15:(12,17),16:(10,12),2:(6,12),3:(16,4),4:(18,8)}
for stage in ['inicio','encargo','muestras','ensayos','final','persecución']:
    sw={1,2,3,4,5,6,7,8,12,13,14,18,19,20,22,28,34,35,39,43,55,81}
    if stage!='inicio':sw|={82,83}
    if stage in ['muestras','ensayos','final']:sw|={84,85,86,91}
    if stage in ['ensayos','final']:sw|={104,105,106}
    if stage=='final':sw|={88,95,96,98}
    if stage=='persecución':sw|={84,90}
    grids={mid:Grid(mid,sw,{7:3,8:9,19:1,1:40}) for mid in seeds}
    for mid,g in grids.items():
        seen=g.flood(seeds[mid])
        check(any(g.step(*seeds[mid],d) for d in D),f'{stage}: inicio bloqueado {mid}')
        for e,p in g.ev:
            # Solo eventos nuevos o conexiones editadas. Puntos ambientales no son acciones.
            relevant=mid>=12 or (mid,e['id']) in [(3,7),(4,4)] or e['name']=='Hospital cerrado A3'
            if relevant and p['trigger'] in [0,1] and p['list']:
                check(g.interact(e,p,seen),f'{stage}: interacción inaccesible {mid} {e["name"]}')
            if relevant:
                for c in p['list']:
                    if c['code']==201:
                        _,dest,x,y,*_=c['parameters']
                        if dest in grids:check(any(grids[dest].step(x,y,d) for d in D),f'destino bloqueado {dest} {x},{y}')

for mid in range(12,17):
    m=S['Map%03d'%mid]
    for e in m['events'].values():
        for p in e['pages']:
            check(p['list'][-1]['code']==0,f'terminador {mid}/{e["name"]}')
            for c in p['list']:
                audio_folder={241:'BGM',245:'BGS',249:'ME',250:'SE'}.get(c['code'])
                if audio_folder:
                    name=c['parameters'][0]['name']
                    roots=[ROOT/'Audio'/audio_folder,Path('D:/SteamLibrary/steamapps/common/RPGXP/rtp/Audio')/audio_folder]
                    check(any(any(root.glob(name+'.*')) for root in roots),'audio '+audio_folder+'/'+name)
                for value in c['parameters']:
                    if isinstance(value,str):
                        for key in re.findall(r'\\P\[([^\]]+)\]',value):check((ROOT/'Graphics/Pictures'/('retrato_'+key+'.png')).exists(),'retrato '+key)
                        for sid in re.findall(r'susto\((\d+)\)',value):check((ROOT/'Graphics/Pictures'/('screamer_'+sid+'.png')).exists(),'susto '+sid)
for name,size,mode in [('retrato_lucy_quiebre',(240,340),'RGBA'),('retrato_lucy_calma',(240,340),'RGBA'),('retrato_elena_neutral',(240,340),'RGBA'),('screamer_8',(640,480),'RGB'),('screamer_9',(640,480),'RGB')]:
    p=ROOT/'Graphics/Pictures'/(name+'.png')
    check(p.exists(),'asset '+name)
    if p.exists():
        im=Image.open(p);check(im.size==size and im.mode==mode,'formato '+name)
for name in ['tarro','factura','camilla','diagnostico']:
    p=ROOT/'Graphics/Battlers'/('enemigo_'+name+'.png');check(p.exists(),'battler '+name)
    if p.exists():
        im=Image.open(p);check(im.size==(320,300) and im.mode=='RGBA' and im.getchannel('A').getextrema()[0]==0,'formato battler '+name)
for eid in range(10,14):
    check(S['Troops'][eid]['members'][0]['enemy_id']==eid,'tropa '+str(eid))
    check(S['Enemies'][eid]['gold']==0 and S['Enemies'][eid]['exp']==0,'recompensa mental '+str(eid))
for iid in [15,23,24,28,29]:check(S['Items'][iid]['common_event_id']==1,'CE1 '+str(iid))
report={'checks':checks,'errors':errors,'scenarios':6,'scope':'Colisión XP, destinos, eventos, recursos dinámicos, BD. La prueba RGSS ejecuta la progresión.'}
(BASE.parent/'verificacion_acto3.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
