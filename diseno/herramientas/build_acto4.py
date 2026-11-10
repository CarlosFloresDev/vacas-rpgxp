"""Lote repetible A4 sobre snapshot actual; reutiliza el respaldo existente sin crearlo."""
import json,copy
from pathlib import Path
from ev import *
import contenido4 as C
import maps4
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
s=json.loads((BASE/'snapshot.json').read_text(encoding='utf-8'))
ops=maps4.pintura()
for fn in [C.entrada,C.tuneles,C.inundada,C.camara,C.altar]:
    m=fn();ops+=m.ops({int(i) for i in s.get('Map%03d'%m.map_id,{}).get('events',{})})

# Conexiones desde partida final previa y acceso fisico por hospital.
e=next(e for e in s['Map016']['events'].values() if e['name']=='Lucy: diagnóstico')
ps=copy.deepcopy(e['pages'])
ps=[p for p in ps if not (p['condition']['switch1_valid'] and p['condition']['switch1_id']==98)]
ps.append(page([C.say('Lucy','Elena está aquí. No tienes que llevarnos en el bolsillo.'),CHOICE(['Bajar al colector','Guardar','Quedarme'],[C.bajar(),[SAVE],[]])],sw1=98,char='vacas_lucy'))
ops.append(['update_map_event',dict(mapId=16,eventId=e['id'],updates={'pages':ps})])
name='Colector bajo hospital A4'
e=next((e for e in s['Map015']['events'].values() if e['name']==name),None)
new=dict(name=name,x=22,y=5,pages=[page([],through=True),page([IF(c_item(29),C.bajar(),[T('La cerradura pide la llave del colector.')])],sw1=98,char='vacas_alcantarilla',d=6,pat=3,dirfix=True,walk=False)])
ops.append(['update_map_event',dict(mapId=15,eventId=e['id'],updates=new)] if e else ['create_map_event',dict(mapId=15,**new)])
for iid,n,desc in C.ITEMS:
    d=copy.deepcopy(s['Items'][29]);d.pop('_class',None)
    d.update(id=iid,name=n,description=desc,consumable=False,occasion=2,common_event_id=1,scope=0,price=0)
    ops.append(['update_database_entry',dict(kind='items',id=iid,updates=d)])
for i,n in C.SWITCHES.items():ops.append(['set_switch_name',dict(switchId=i,name='A4: '+n)])
for i,n in C.VARIABLES.items():ops.append(['set_variable_name',dict(variableId=i,name='A4: '+n)])
for eid,key,n,hp,atk,skill in [(14,'coro','El Coro del tubo',270,31,65),(15,'pulmon','El Pulmon de cieno',310,33,67),(16,'cencerro','El Cencerro sin lengua',290,32,66),(17,'pastor','El Pastor hueco',760,39,70)]:
    d=copy.deepcopy(s['Enemies'][13 if eid==17 else 11]);d.pop('_class',None)
    d.update(id=eid,name=n,battler_name='enemigo_'+key,maxhp=hp,atk=atk,gold=0,exp=0)
    for a in d['actions']:
        if a['kind']==1:a['skill_id']=skill
    ops.append(['update_database_entry',dict(kind='enemies',id=eid,updates=d)])
    t=copy.deepcopy(s['Troops'][13]);t.pop('_class',None);t.update(id=eid,name='Mente: '+n)
    t['members'][0]['enemy_id']=eid
    t['pages'][0]['list']=[{'_class':'RPG::EventCommand',**c} for c in flatten([C.say('Steven','Una imagen no puede darme órdenes. Puedo respirar.','miedo')])+[{'code':0,'indent':0,'parameters':[]}]]
    ops.append(['update_database_entry',dict(kind='troops',id=eid,updates=t)])
ce=copy.deepcopy(s['CommonEvents'][1]['list'])
start=next((i for i,c in enumerate(ce) if c['code']==108 and c['parameters']==['ACTO_IV_NOTAS']),len(ce)-1)
ce=ce[:start]+[{'code':108,'indent':0,'parameters':['ACTO_IV_NOTAS']}]+flatten(C.notas())+[{'code':0,'indent':0,'parameters':[]}]
ops.append(['update_database_entry',dict(kind='common_events',id=1,updates={'list':[{'_class':'RPG::EventCommand',**c} for c in ce]})])
pant=(ROOT/'diseno/scripts/04_pantallas.rb').read_text(encoding='utf-8')
pant=pant.replace('3 => ["Fin del Acto III", "Lucy", "Continuará en el Acto IV: Bajo la ciudad", "Pulsa Intro para volver al título"]','3 => ["Fin del Acto III", "Lucy", "Acto IV: Bajo la ciudad", "Pulsa Intro para seguir"],\n    4 => ["Fin del Acto IV", "Bajo la ciudad", "Continuará en el Acto V: La matanza", "Pulsa Intro para volver al título"]')
if 'elsif @acto == 3' not in pant:
    pant=pant.replace('Vacas.empezar_acto3\n          $scene = Scene_Map.new\n        else','Vacas.empezar_acto3\n          $scene = Scene_Map.new\n        elsif @acto == 3\n          Vacas.empezar_acto4\n          $scene = Scene_Map.new\n        else')
(ROOT/'diseno/scripts/04_pantallas.rb').write_text(pant,encoding='utf-8')
ops.append(['update_script',dict(index=next(x['index'] for x in s['Scripts'] if x['name']=='Vacas_Pantallas'),code=pant)])
mente=(ROOT/'diseno/scripts/07_mente.rb').read_text(encoding='utf-8').replace('[3, 6].include?(troop)','[3, 6, 14, 15, 16, 17].include?(troop)')
(ROOT/'diseno/scripts/07_mente.rb').write_text(mente,encoding='utf-8')
ops.append(['update_script',dict(index=next(x['index'] for x in s['Scripts'] if x['name']=='Vacas_Mente'),code=mente)])
code=(ROOT/'diseno/scripts/10_bajo_ciudad.rb').read_text(encoding='utf-8')
found=next((x for x in s['Scripts'] if x['name']=='Vacas_BajoCiudad'),None)
ops.append(['update_script',dict(index=found['index'],code=code)] if found else ['create_script',dict(name='Vacas_BajoCiudad',code=code)])
(BASE/'b_acto4.json').write_text(json.dumps(ops,ensure_ascii=False),encoding='utf-8')
(BASE/'b_render4.json').write_text(json.dumps([['render_map',dict(mapId=i,drawEvents=True,outPath=str(ROOT/'diseno/capturas'/('acto4_%d.png'%i)))] for i,*_ in maps4.MAPAS]),encoding='utf-8')
print(len(ops),'operaciones A4')
