"""Lote repetible del Acto V sobre el snapshot actual (ejecutar inspeccionar.mjs antes)."""
import json,copy
from pathlib import Path
from PIL import Image,ImageOps,ImageEnhance
from ev import *
import contenido5 as C
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[1]
s=json.loads((BASE/'snapshot.json').read_text(encoding='utf-8'))
info=json.loads((BASE/'maps5_info.json').read_text(encoding='utf-8'))
ops=[];errors=[];D4=[(0,1),(-1,0),(1,0),(0,-1)]
maps=[fn() for fn in C.MAPAS]
for m in maps:
    ops+=m.ops({int(i) for i in s.get('Map%03d'%m.map_id,{}).get('events',{})})
# --- comprobacion estatica: alcance de interacciones y destinos
reach={}
for m in maps:
    blocked={tuple(c) for c in info[str(m.map_id)]['blocked']}
    solid={(e['x'],e['y']) for e in m.events if e['pages'][0]['graphic']['character_name'] and not e['pages'][0]['through']}
    seen={C.SEEDS[m.map_id]};todo=[C.SEEDS[m.map_id]]
    while todo:
        x,y=todo.pop()
        for dx,dy in D4:
            n=(x+dx,y+dy)
            if 0<=n[0]<20 and 0<=n[1]<15 and n not in seen and n not in blocked and n not in solid:seen.add(n);todo.append(n)
    reach[m.map_id]=(seen,blocked,solid)
for m in maps:
    seen,blocked,solid=reach[m.map_id]
    for e in m.events:
        p=(e['x'],e['y'])
        for pg in e['pages']:
            active=any(c['code']!=0 for c in pg['list'])
            if active and pg['trigger']==0:
                front=p in blocked or (pg['graphic']['character_name'] and not pg['through'])
                ok=any((p[0]+dx,p[1]+dy) in seen for dx,dy in D4) if front else p in seen
                if not ok:errors.append('inaccesible %d/%s %s'%(m.map_id,e['name'],p))
            if active and pg['trigger']==1 and p not in seen:errors.append('toque inaccesible %d/%s'%(m.map_id,e['name']))
            for c in pg['list']:
                if c['code']==201:
                    _,d,x,y,*_=c['parameters']
                    if d in reach and (x,y) not in reach[d][0]:errors.append('destino %d/%s -> %d %d,%d'%(m.map_id,e['name'],d,x,y))
                if c['code']==202:
                    _,_,x,y,_=c['parameters']
                    if (x,y) not in seen:errors.append('evloc %d %d,%d'%(m.map_id,x,y))
print('errores estaticos:',errors)
if errors:raise SystemExit(1)
# --- base de datos
for iid,n,desc in C.ITEMS:
    d=copy.deepcopy(s['Items'][29]);d.pop('_class',None)
    d.update(id=iid,name=n,description=desc,consumable=False,occasion=2,common_event_id=1,scope=0,price=0)
    ops.append(['update_database_entry',dict(kind='items',id=iid,updates=d)])
for i,n in C.SWITCHES.items():ops.append(['set_switch_name',dict(switchId=i,name='A5: '+n)])
for i,n in C.VARIABLES.items():ops.append(['set_variable_name',dict(variableId=i,name='A5: '+n)])
for eid,key,hue,n,hp,atk,skill,frase in C.ENEMIGOS:
    d=copy.deepcopy(s['Enemies'][13 if eid==21 else 11]);d.pop('_class',None)
    d.update(id=eid,name=n,battler_name='enemigo_'+key,battler_hue=hue,maxhp=hp,atk=atk,gold=0,exp=0)
    for a in d['actions']:
        if a['kind']==1:a['skill_id']=skill
    ops.append(['update_database_entry',dict(kind='enemies',id=eid,updates=d)])
    t=copy.deepcopy(s['Troops'][13]);t.pop('_class',None);t.update(id=eid,name='Mente: '+n)
    t['members'][0]['enemy_id']=eid
    intro=[C.say('Steven',frase,'miedo')] if frase else [C.say('Cripps','Dos dedos por encima de los ojos, chico. ¿O ya se te ha olvidado?','ira'),C.say('Steven','No se me ha olvidado nada. Ese es el problema.','miedo')]
    t['pages'][0]['list']=[{'_class':'RPG::EventCommand',**c} for c in flatten(intro)+[{'code':0,'indent':0,'parameters':[]}]]
    ops.append(['update_database_entry',dict(kind='troops',id=eid,updates=t)])
ce=copy.deepcopy(s['CommonEvents'][1]['list'])
start=next((i for i,c in enumerate(ce) if c['code']==108 and c['parameters']==['ACTO_V_NOTAS']),len(ce)-1)
ce=ce[:start]+[{'code':108,'indent':0,'parameters':['ACTO_V_NOTAS']}]+flatten(C.notas())+[{'code':0,'indent':0,'parameters':[]}]
ops.append(['update_database_entry',dict(kind='common_events',id=1,updates={'list':[{'_class':'RPG::EventCommand',**c} for c in ce]})])
# --- scripts
pan=next(x for x in s['Scripts'] if x['name']=='Vacas_Pantallas');pant=pan['code']
old4='4 => ["Fin del Acto IV", "Bajo la ciudad", "Continuará en el Acto V: La matanza", "Pulsa Intro para volver al título"]'
if old4 in pant:
    pant=pant.replace(old4,'4 => ["Fin del Acto IV", "Bajo la ciudad", "Acto V: La matanza", "Pulsa Intro para seguir"],\n    5 => ["Fin del Acto V", "La matanza", "Continuará en el Acto VI: Rey-dios", "Pulsa Intro para volver al título"]')
    a='elsif @acto == 3\n          Vacas.empezar_acto4\n          $scene = Scene_Map.new\n'
    assert a in pant
    pant=pant.replace(a,a+'        elsif @acto == 4\n          Vacas.empezar_acto5\n          $scene = Scene_Map.new\n')
assert 'Vacas.empezar_acto5' in pant
(ROOT/'diseno/scripts/04_pantallas.rb').write_text(pant,encoding='utf-8')
ops.append(['update_script',dict(index=pan['index'],code=pant)])
code=(ROOT/'diseno/scripts/13_matanza.rb').read_text(encoding='utf-8')
found=next((x for x in s['Scripts'] if x['name']=='Vacas_Matanza'),None)
ops.append(['update_script',dict(index=found['index'],code=code)] if found else ['create_script',dict(name='Vacas_Matanza',code=code)])
# --- sustos provisionales: reencuadres tintados de arte existente (sin generacion)
P=ROOT/'Graphics/Pictures'
for n,src,flip in [(12,4,True),(13,7,False)]:
    im=Image.open(P/('screamer_%d.png'%src)).convert('RGB')
    if flip:im=ImageOps.mirror(im)
    im=im.crop((60,45,580,435)).resize((640,480),Image.LANCZOS)
    g=ImageOps.grayscale(im);im=Image.blend(im,ImageOps.colorize(g,(10,0,0),(255,150,120) if n==12 else (150,215,255)),.6)
    ImageEnhance.Contrast(im).enhance(1.25).save(P/('screamer_%d.png'%n))
(BASE/'b_acto5.json').write_text(json.dumps(ops,ensure_ascii=False),encoding='utf-8')
print(len(ops),'operaciones A5;',sum(len(m.events) for m in maps),'eventos')
