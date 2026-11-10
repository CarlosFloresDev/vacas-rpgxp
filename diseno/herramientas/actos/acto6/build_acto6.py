"""Instala eventos/BD/scripts sin regenerar contenido de actos anteriores."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import json,copy
from pathlib import Path
from ev import *
import contenido6 as C
BASE=Path(__file__).resolve().parent;ROOT=_ROOT
s=json.loads(((_ROOT / 'diseno/verificaciones/inventario/snapshot.json')).read_text(encoding='utf8'))
ops=[]
for m in [fn() for fn in C.MAPAS]:ops+=m.ops({int(i) for i in s['Map%03d'%m.map_id]['events']})
for iid,name,desc in C.ITEMS:
    d=copy.deepcopy(s['Items'][29]);d.pop('_class',None)
    d.update(id=iid,icon_name="vacas_item_%02d"%iid,name=name,description=desc,consumable=False,occasion=2,common_event_id=1,scope=0,price=0)
    ops.append(['update_database_entry',dict(kind='items',id=iid,updates=d)])
for i,n in C.SWITCHES.items():ops.append(['set_switch_name',dict(switchId=i,name='A6: '+n)])
for i,n in C.VARIABLES.items():ops.append(['set_variable_name',dict(variableId=i,name='A6: '+n)])
for eid,key,hue,name,hp,atk,skill in C.ENEMIGOS:
    d=copy.deepcopy(s['Enemies'][13]);d.pop('_class',None)
    d.update(id=eid,name=name,battler_name='enemigo_'+key,battler_hue=hue,maxhp=hp,atk=atk,gold=0,exp=0)
    for a in d['actions']:
        if a['kind']==1:a['skill_id']=skill
    ops.append(['update_database_entry',dict(kind='enemies',id=eid,updates=d)])
    t=copy.deepcopy(s['Troops'][13]);t.pop('_class',None);t.update(id=eid,name='Mente: '+name)
    t['members'][0]['enemy_id']=eid
    t['pages'][0]['list']=[{'_class':'RPG::EventCommand',**c} for c in flatten([C.say('Steven','Puedo respirar. Puedo ponerle nombre.','miedo')])+[{'code':0,'indent':0,'parameters':[]}]]
    ops.append(['update_database_entry',dict(kind='troops',id=eid,updates=t)])
# Lectura de recuerdos con el mismo CE1 que los objetos anteriores.
ce=copy.deepcopy(s['CommonEvents'][1]['list'])
mark=next((i for i,c in enumerate(ce) if c['code']==108 and c['parameters']==['ACTO_VI_NOTAS']),len(ce)-1)
ce=ce[:mark]+[{'code':108,'indent':0,'parameters':['ACTO_VI_NOTAS']}]
for iid,name,desc in C.ITEMS:
    ce+=flatten([IF(c_script('$vacas_ultimo_objeto == %d'%iid),[T(name+': '+desc)])])
ce+=[{'code':0,'indent':0,'parameters':[]}]
ops.append(['update_database_entry',dict(kind='common_events',id=1,updates={'list':[{'_class':'RPG::EventCommand',**c} for c in ce]})])
# Actualiza el cierre V, conservando el resto de la sección.
pan=next(x for x in s['Scripts'] if x['name']=='Vacas_Pantallas');code=pan['code']
code=code.replace('Continuará en el Acto VI: Rey-dios','Acto VI: Rey-dios').replace('5 => ["Fin del Acto V", "La matanza", "Acto VI: Rey-dios", "Pulsa Intro para volver al título"]','5 => ["Fin del Acto V", "La matanza", "Acto VI: Rey-dios", "Pulsa Intro para seguir"]')
anchor='          Vacas.empezar_acto5\n          $scene = Scene_Map.new\n'
if 'Vacas.empezar_acto6' not in code:
    assert anchor in code
    code=code.replace(anchor,anchor+'        elsif @acto == 5\n          Vacas.empezar_acto6\n          $scene = Scene_Map.new\n')
(ROOT/'diseno/scripts/04_pantallas.rb').write_text(code,encoding='utf8')
ops.append(['update_script',dict(index=pan['index'],code=code)])
# Mantiene acceso a todos los créditos CC y añade el equipo al principio.
ui=next(x for x in s['Scripts'] if x['name']=='Vacas_Interfaz');code=ui['code'].replace('\r\n','\n').replace('\r','\n')
if 'Carlos - dirección, arte, diseño' not in code:
    code=code.replace('  CREDITS_LINES = [','  CREDITS_LINES = [\n    "FEKA STUDIOS - VACAS",\n    "Carlos - dirección, arte, diseño",\n    "Alexandre - historia",\n    \'Ithalo "Ander" - sonido\',\n    "",')
code=code.replace('[9,13,17].include?($game_temp.battle_troop_id) ? :jefe','[9,13,17,21,35,36,37].include?($game_temp.battle_troop_id) ? :jefe')
(ROOT/'diseno/scripts/12_interfaz.rb').write_text(code,encoding='utf8')
ops.append(['update_script',dict(index=ui['index'],code=code)])
code=(ROOT/'diseno/scripts/15_reydios.rb').read_text(encoding='utf8')
found=next((x for x in s['Scripts'] if x['name']=='Vacas_Reydios'),None)
ops.append(['update_script',dict(index=found['index'],code=code)] if found else ['create_script',dict(name='Vacas_Reydios',code=code)])
# Salida física adicional y continuación de guardados de V previos al cierre.
gate=next(e for e in s['Map027']['events'].values() if e['name']=='Cancela abierta')
lst=[IF(c_sw(168),[CHOICE(['Guardar y continuar al Acto VI','Seguir en el patio'],[[SW(163),SAVEACCESS(True),SAVE,SCRIPT('Vacas.empezar_acto6'),TRANSFER(28,3,13,8)],[MOVE(-1,[UP]),WAITMOVE]])],[T('Habla primero con la Guernsey en el patio.'),MOVE(-1,[UP]),WAITMOVE])]
for eid,e in s['Map027']['events'].items():
    if e['name']=='Cancela abierta':ops.append(['update_map_event',dict(mapId=27,eventId=int(eid),updates={'pages':[page(lst,trigger=1)]})])
((_ROOT / 'diseno/archivo/lotes/b_acto6.json')).write_text(json.dumps(ops,ensure_ascii=False),encoding='utf8')
print(len(ops),'operaciones A6;',sum(len(fn().events) for fn in C.MAPAS),'eventos nuevos')
