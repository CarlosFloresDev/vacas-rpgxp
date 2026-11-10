"""Lote idempotente sobre snapshot ACTUAL: no regenera ni reemplaza arte aprobado.
Primero node inspeccionar.mjs; mapas3.py crear solo la primera vez.
Después rx.mjs --batch b_acto3.json. Respaldo Data obligatorio antes.
"""
import json,copy
from pathlib import Path
from ev import *
import contenido3 as C
import maps3

BASE=Path(__file__).resolve().parent
s=json.loads((BASE/'snapshot.json').read_text(encoding='utf-8-sig'))
ops=maps3.pintura()
for fn in [C.piso,C.carniceria,C.deposito,C.hospital,C.laboratorio]:
    m=fn();old=s.get('Map%03d'%m.map_id,{}).get('events',{})
    ops+=m.ops({int(i) for i in old})

def patch(mid,eid,commands,**graphic):
    e=copy.deepcopy(s['Map%03d'%mid]['events'][str(eid)])
    e['pages']=[p for p in e['pages'] if not (p['condition']['switch1_valid'] and p['condition']['switch1_id']==81)]
    e['pages'].append(page(commands,sw1=81,**graphic))
    ops.append(['update_map_event',dict(mapId=mid,eventId=eid,updates={'pages':e['pages']})])

# Escalera y calle: conservar páginas originales, añadir solo las del Acto III.
patch(3,7,[IF(c_sw(34),[TRANSFER(12,12,17,8)],[T('Lucy aún no ha vuelto.')])],trigger=1)
patch(3,15,[])
patch(4,4,[TRANSFER(13,10,12,8)])
patch(4,5,[],through=True) # Molina está dentro; evita dos copias simultáneas.
patch(4,19,[T('El camión ya se ha ido. Hoy no hay otro turno.')],char='vacas_reclutador')
for eid in [10,11,12]:patch(4,eid,[],through=True)
# Acceso hospital sobre suelo del extremo este, visible por cartel propio.
events=s['Map004']['events']; existing=next((e for e in events.values() if e['name']=='Hospital cerrado A3'),None)
event=dict(name='Hospital cerrado A3',x=35,y=11,pages=[page([],through=True),page([T('HOSPITAL MUNICIPAL. CERRADO. Una luz sigue encendida en curas.'),TRANSFER(15,12,17,8)],sw1=81,tile=441)])
ops.append(['update_map_event',dict(mapId=4,eventId=existing['id'],updates=event)] if existing else ['create_map_event',dict(mapId=4,**event)])
# Desactivar escenas nocturnas anteriores en la visita libre a casa.
for eid in [1,3,47,48,49,44,46]:patch(2,eid,[],through=True)
for eid in [4,5]:patch(2,eid,[T('No puedes dormir mientras Lucy espera arriba. La tele permite guardar.')])
patch(2,14,[C.say('Madre','La de arriba te ha llenado la cabeza de frascos. Tú siempre buscando quién te dé otra orden.'),
    IF(c_sw(107,False),[CHOICE(['Hoy no te doy explicaciones','Bajar la mirada'],[[C.say('Steven','Voy a subir. No necesito que lo entiendas.'),VEN(-4)],[C.say('Madre','Así me gusta. Aunque no sepas a quién estás obedeciendo.'),C.tension(4)]]),SW(107)])],char='vacas_madre')
patch(2,31,[CHOICE(['Ver la tele','Guardar','Volver'],[[T('La imagen no promete una familia. Solo una pausa.'),VEN(-15)],[SAVE],[]])],char='vacas_muebles',d=2,pat=1,dirfix=True)
patch(2,34,[T('Perro apoya el hocico en tu mano. No mira los tarros.'),VEN(-6)],char='vacas_perro')

items=[(14,'Tarro limpio','Para separar las muestras.'),(15,'Protocolo de Lucy','Dos lotes, dos tarros y un control.'),(16,'Hígado: lote 17','Muestra A en tarro sellado.'),(17,'Riñón sin etiqueta','Muestra B de otra carnicería.'),(18,'Sal sin abrir','Preparación común para A, B y control.'),(19,'Guantes limpios','Material de Elena; no se consume.'),(20,'Pinza de curas','Material de Elena; no se consume.'),(21,'Reactivo R-0','Frasco retirado. Revisar etiqueta.'),(22,'Suero limpio','Control sin tejido animal.'),(23,'Etiquetas de lotes','Procedencia de las muestras.'),(24,'Protocolo de contraste','Procedimiento y lectura del control.'),(25,'Preparación A azul','Hígado tratado, sellado y rotulado.'),(26,'Preparación B azul','Riñón tratado, sellado y rotulado.'),(27,'Control azul','El suero también cambió de color.'),(28,'Cuaderno de resultados','Las tres reacciones y sus límites.'),(29,'Llave del colector','Para el camino bajo la ciudad.')]
for iid,name,desc in items:
    d=copy.deepcopy(s['Items'][13]);d.pop('_class',None)
    d.update(id=iid,name=name,description=desc,icon_name='035-Item04',scope=0,occasion=2 if iid in C.NOTES else 3,consumable=False,common_event_id=1 if iid in C.NOTES else 0,price=0)
    ops.append(['update_database_entry',dict(kind='items',id=iid,updates=d)])

switches={81:'Acto III activo',82:'Dos golpes vistos',83:'Encargo de Lucy',84:'Hígado recogido',85:'Riñón recogido',86:'Material de Elena',87:'RESERVADO A3',88:'Resultados comparados',89:'RESERVADO A3',90:'Persiana persigue',91:'Depósito superado',92:'Tarro afrontado',93:'Factura afrontada',94:'Camilla afrontada',95:'Diagnóstico vencido',96:'ELECCIÓN: quedarse con Lucy',97:'ELECCIÓN: llevar pruebas abajo',98:'Acto III terminado',99:'Susto 8 visto',100:'Susto 9 visto',101:'Persiana: captura pendiente',102:'Tazas compartidas',103:'Etiqueta R-0 leída',104:'Preparación A hecha',105:'Preparación B hecha',106:'Control hecho',107:'Límite con madre'}
for i,n in switches.items():ops.append(['set_switch_name',dict(switchId=i,name='A3: '+n)])
for i,n in {19:'Etapa (1-8)',20:'Confianza de Lucy',21:'Capturas persiana',22:'Preparaciones (0-3)',23:'Elección (1 Lucy / 2 pruebas)'}.items():ops.append(['set_variable_name',dict(variableId=i,name='A3: '+n)])

# Tres enemigos y jefe, estadísticas de la BD mental existente, cero XP/dinero.
for eid,key,name,hp,atk,skill in [(10,'tarro','El Tarro testigo',230,30,65),(11,'factura','La Factura cosida',260,32,66),(12,'camilla','La Camilla vacía',300,34,67),(13,'diagnostico','El Diagnóstico',720,41,70)]:
    d=copy.deepcopy(s['Enemies'][9 if eid==13 else 3]);d.pop('_class',None)
    d.update(id=eid,name=name,battler_name='enemigo_'+key,maxhp=hp,atk=atk,exp=0,gold=0)
    for a in d['actions']:
        if a['kind']==1:a['skill_id']=skill
    ops.append(['update_database_entry',dict(kind='enemies',id=eid,updates=d)])
    t=copy.deepcopy(s['Troops'][9]);t.pop('_class',None)
    t.update(id=eid,name='Mente: '+name)
    t['members'][0]['enemy_id']=eid
    t['pages'][0]['list']=[{'_class':'RPG::EventCommand',**c} for c in flatten([C.say('Steven','Esto es una imagen. Puedo respirar antes de responder.','miedo')])+[{'code':0,'indent':0,'parameters':[]}]]
    ops.append(['update_database_entry',dict(kind='troops',id=eid,updates=t)])

# CE1: reemplazar solo apéndice de A3; dejar intactas las notas de I/II.
ce=copy.deepcopy(s['CommonEvents'][1]['list'])
marker='ACTO_III_NOTAS'
start=next((i for i,c in enumerate(ce) if c['code']==108 and c['parameters']==[marker]),len(ce)-1)
ce=ce[:start]+[{'code':108,'indent':0,'parameters':[marker]}]+flatten(C.notas())+[{'code':0,'indent':0,'parameters':[]}]
ops.append(['update_database_entry',dict(kind='common_events',id=1,updates={'list':[{'_class':'RPG::EventCommand',**c} for c in ce]})])

# Fin II -> III sin perder partida; fin III devuelve título y permite continuar.
pant=(BASE.parent/'scripts/04_pantallas.rb').read_text(encoding='utf-8')
pant=pant.replace('Continuará en el Acto III: Lucy','Acto III: Lucy')
pant=pant.replace('2 => ["Fin del Acto II", "La cadena", "Acto III: Lucy", "Pulsa Intro"]','2 => ["Fin del Acto II", "La cadena", "Acto III: Lucy", "Pulsa Intro para seguir"],\n    3 => ["Fin del Acto III", "Lucy", "Continuará en el Acto IV: Bajo la ciudad", "Pulsa Intro para volver al título"]')
pant=pant.replace('Partida guardada: Continuar para volver','Pulsa Intro para volver al título')
pant=pant.replace('Vacas.empezar_acto2\n          $scene = Scene_Map.new\n        else','Vacas.empezar_acto2\n          $scene = Scene_Map.new\n        elsif @acto == 2\n          Vacas.empezar_acto3\n          $scene = Scene_Map.new\n        else')
(BASE.parent/'scripts/04_pantallas.rb').write_text(pant,encoding='utf-8')
ops.append(['update_script',dict(index=next(x['index'] for x in s['Scripts'] if x['name']=='Vacas_Pantallas'),code=pant)])
code=(BASE.parent/'scripts/09_lucy.rb').read_text(encoding='utf-8')
mente=(BASE.parent/'scripts/07_mente.rb').read_text(encoding='utf-8')
ops.append(['update_script',dict(index=next(x['index'] for x in s['Scripts'] if x['name']=='Vacas_Mente'),code=mente)])
found=next((x for x in s['Scripts'] if x['name']=='Vacas_Lucy'),None)
ops.append(['update_script',dict(index=found['index'],code=code)] if found else ['create_script',dict(name='Vacas_Lucy',code=code)])
(BASE/'b_acto3.json').write_text(json.dumps(ops,ensure_ascii=False),encoding='utf-8')
print(len(ops),'operaciones Acto III')
