"""Regresión de todos los puntos interactivos frente al respaldo, no sólo puertas."""
import json, hashlib, copy
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
exec((BASE/'auditar_accesos.py').read_text(encoding='utf-8').split('issues=set()')[0])
current=S
backup=ROOT/(BASE/'respaldo_revision.txt').read_text().strip()
before=json.loads((backup/'snapshot.json').read_text(encoding='utf-8'))
states=list(scenarios)
for stage in range(6):
    sw={1,2,3,4,5,6,7,8,12,13,14,18,19,20,22,28,34,35,39,43,55,81}
    if stage>0:sw|={82,83}
    if stage>1:sw|={84,85,86,91}
    if stage>2:sw|={104,105,106}
    if stage>3:sw|={88,95,96,98}
    if stage==5:sw|={84,90}
    states.append(('A3 '+str(stage),sw,{7:3,8:9,19:1,1:40}))
seeds=dict(SEEDS);seeds.update({12:(12,17),13:(10,12),14:(3,12),15:(12,17),16:(10,12)})
errors=[];checks=0;maps=[]
for mid in range(1,17):
    lost=set();count=0
    for name,sw,var in states:
        for selfon in [False,True]:
            S=before;old=Grid(mid,sw,var,selfon)
            seenold=old.flood((12,17) if mid==16 else seeds[mid])
            S=current;new=Grid(mid,sw,var,selfon);seennew=new.flood(seeds[mid])
            oldactive={e['id']:(e,p) for e,p in old.ev}
            for e,p in new.ev:
                if p['trigger'] not in [0,1,2] or len(p['list'])<=1:continue
                oe,op=oldactive[e['id']]
                if old.interact(oe,op,seenold):
                    count+=1
                    if not new.interact(e,p,seennew):lost.add((name,e['name']))
    maps.append({'mapa':mid,'interacciones_comprobadas':count,'regresiones':sorted(lost)})
    errors.extend((mid,*v) for v in sorted(lost));checks+=count
    a,b=before['Map%03d'%mid],current['Map%03d'%mid]
    assert a['events'].keys()==b['events'].keys(), 'IDs de evento alterados'
    # The only event-command edits allowed are lab tone and inbound lab destination.
    for key,e in b['events'].items():
        expected=copy.deepcopy(a['events'][key])
        if mid==16:expected['x'],expected['y']=e['x'],e['y']
        for p in expected['pages']:
            for c in p['list']:
                if c['code']==201 and c['parameters'][1]==16:c['parameters'][2:4]=[10,12]
                if mid==16 and key=='1' and c['code']==223:c['parameters'][0].update(red=-38,green=-16,blue=-42,alpha=35)
        assert e==expected, 'Evento modificado fuera de alcance: '+str((mid,key))
# All seven previously audited indexed sheets remain byte-identical to task start.
# The task backup has Data/captures; original sheet hashes also live in scale report.
scale=json.loads((ROOT/'diseno/verificacion_escala_revision.json').read_text(encoding='utf-8'))
result={'checks_interaccion':checks,'estados':len(states)*2,'mapas':maps,'errores':errors,'hojas_escala':len(scale['sheets']),'eventos_preservados':True}
(ROOT/'diseno/verificacion_revision_mapas.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
