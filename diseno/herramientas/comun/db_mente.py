"""BD idempotente: IDs reservados para las alucinaciones."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import json,copy
from pathlib import Path
BASE=Path(__file__).resolve().parent
s=json.loads(((_ROOT / 'diseno/verificaciones/inventario/snapshot.json')).read_text(encoding='utf-8-sig'));ops=[]
def update(kind,entry_id,**kw):ops.append(['update_database_entry',{'kind':kind,'id':entry_id,'updates':kw}])
def table(n):return {'_class':'Table','dim':1,'xsize':n,'ysize':1,'zsize':1,'data':[0]+[3]*(n-1)}
for id,name,changes in [(2,'Pánico',dict(agi_rate=75,hit_rate=85)),(3,'Asco',dict(atk_rate=75)),(4,'Culpa',dict(int_rate=75))]:
 d=copy.deepcopy(s['States'][2]);d.update(id=id,name=name,restriction=0,zero_hp=False,battle_only=True,slip_damage=False,hold_turn=2,auto_release_prob=60,shock_release_prob=0,animation_id=0,plus_state_set=[],minus_state_set=[],maxhp_rate=100,maxsp_rate=100,str_rate=100,dex_rate=100,agi_rate=100,int_rate=100,atk_rate=100,pdef_rate=100,mdef_rate=100,hit_rate=100,cant_evade=False,cant_get_exp=False,nonresistance=False)
 d.update(changes);d.pop('_class',None);update('states',id,**d)
update('states',1,name='Desvanecido')
skills=[(61,'Respirar','Cura 70, recupera 18 de aliento, limpia estados y baja veneno.',7,-70,0,0,[]),(62,'Poner nombre','Nombrar la imagen le quita poder. Impacto mental fiable.',1,62,8,0,[]),(63,'Aferrarse a Perro','El recuerdo de Perro abriga: cura heridas y estados.',7,-140,12,0,[]),(64,'Romper el reflejo','Golpe firme a la alucinación. Puede sembrar Pánico.',1,85,14,100,[2]),(65,'Mugido interior','El mugido parece salir de tu pecho.',1,22,0,0,[2]),(66,'Orden de madre','Tu cuerpo recuerda la orden antes de oírla.',1,24,0,0,[4]),(67,'Hedor del túnel','Un olor que ocupa toda la memoria.',1,20,0,0,[3]),(68,'Tu mano en la suya','El capataz vuelve a mover tus dedos.',1,32,0,100,[4]),(69,'Zumbido','Cada ala repite una palabra distinta.',1,14,0,0,[3]),(70,'Coronación','El cajón tiene tu nombre. Y una corona.',1,38,0,0,[2,4])]
for id,name,desc,scope,power,cost,atk,states in skills:
 d=copy.deepcopy(s['Skills'][1]);d.update(id=id,name=name,description=desc,scope=scope,occasion=1,sp_cost=cost,power=power,atk_f=atk,str_f=0,int_f=40 if atk==0 else 0,dex_f=0,agi_f=0,eva_f=0,pdef_f=60 if power>0 else 0,mdef_f=40 if power>0 else 0,variance=8,hit=100,element_set=[],plus_state_set=states,minus_state_set=[2,3,4] if power<0 else [],animation1_id=0,animation2_id=0,common_event_id=0)
 d.pop('_class',None);update('skills',id,**d)
update('classes',1,name='Superviviente',learnings=[{'_class':'RPG::Class::Learning','level':1,'skill_id':id} for id in [61,62,63,64]],weapon_set=[1],armor_set=[25])
params=copy.deepcopy(s['Actors'][1]['parameters'])
for lvl in range(1,100):
 for j,val in enumerate([360+18*(lvl-1),80+2*(lvl-1),30+lvl-1,32+lvl-1,30+lvl-1,35+lvl-1]):params['data'][6*lvl+j]=val
update('actors',1,initial_level=1,final_level=30,class_id=1,weapon_id=1,armor1_id=0,armor2_id=0,armor3_id=25,armor4_id=0,battler_name='steven_mente',battler_hue=0,parameters=params)
update('weapons',1,name='Tubo oxidado',description='En el sueño, el pasamanos cabe en tu mano.',atk=34,pdef=0,mdef=0,animation1_id=0,animation2_id=0,price=0)
update('armors',25,name='Ropa de trabajo',description='Una capa delgada entre Steven y el mundo.',pdef=26,mdef=24,price=0)
enemies=[('vaca','La Vaca que habla',160,30,65,'Dice lo que Steven todavía no puede pensar.'),('madre','La Madre de yeso',220,34,66,'Cada grieta pronuncia una deuda.'),('tunel','Lo del túnel',240,33,67,'Espera donde la luz deja de recordar.'),('sombra_cripps','Sombra de Cripps',280,38,68,'Obediencia proyectada sobre el azulejo.'),('moscas','Enjambre de moscas',125,25,69,'Pensamientos pequeños que nunca se callan.'),('guernsey','Guernsey de humo',300,36,65,'La promesa adopta una forma que acusa.'),('canal','Canal en el gancho',260,35,67,'Un cuerpo al que Steven teme parecerse.'),('televisor','La Familia de nieve',180,28,66,'La familia feliz recuerda todos sus defectos.'),('rey','El Rey del cajón',650,43,70,'No es Cripps: es el lugar que podrías ocupar.')]
for id,(key,name,hp,atk,skill,lore) in enumerate(enemies,1):
 d=copy.deepcopy(s['Enemies'][1]);act=copy.deepcopy(d['actions'][0]);act.update(kind=1,skill_id=skill,rating=5,condition_turn_a=0,condition_turn_b=1,condition_hp=100,condition_level=1,condition_switch_id=0)
 basic=copy.deepcopy(act);basic.update(kind=0,basic=0,rating=5)
 d.update(id=id,name=name,battler_name='enemigo_'+key,battler_hue=0,maxhp=hp,maxsp=90,str=24,dex=25,agi=24,int=25,atk=atk,pdef=22,mdef=20,eva=0,exp=0,gold=0,item_id=0,weapon_id=0,armor_id=0,treasure_prob=0,animation1_id=0,animation2_id=0,element_ranks=table(17),state_ranks=table(17),actions=[basic,act])
 if id==9:
  extra=copy.deepcopy(act);extra.update(condition_hp=50,rating=6);d['actions'].append(extra)
 d.pop('_class',None);update('enemies',id,**d)
 troop=copy.deepcopy(s['Troops'][1]);troop.update(name='Mente: '+name,members=[{'_class':'RPG::Troop::Member','enemy_id':id,'x':320,'y':300,'hidden':False,'immortal':False}])
 page=troop['pages'][0];page['condition']['turn_valid']=True;page['condition']['turn_a']=0;page['condition']['turn_b']=0
 page['list']=[{'_class':'RPG::EventCommand','code':101,'indent':0,'parameters':['\\P[steven_miedo]\\NOMBRE[Steven]'+lore]},{'_class':'RPG::EventCommand','code':0,'indent':0,'parameters':[]}]
 troop.pop('_class',None);update('troops',id,**troop)
names={45:'familia afrontada',46:'moscas afrontadas',47:'canal afrontada',48:'sombra afrontada',49:'tunel afrontado',50:'vaca afrontada',51:'madre afrontada',52:'guernsey afrontada',53:'secreto del dibujo',54:'tutorial visto',55:'Rey vencido'}
for id,name in names.items():ops.append(['set_switch_name',{'switchId':id,'name':'MENTE: '+name}])
for id in range(1,8):ops.append(['set_switch_name',{'switchId':60+id,'name':'SUSTO: '+str(id)+' visto'}])
ops.append(['set_variable_name',{'variableId':18,'name':'MENTE: resultado (0 victoria / 1 huida / 2 derrota)'}])
((_ROOT / 'diseno/archivo/lotes/b_mente_db.json')).write_text(json.dumps(ops,ensure_ascii=False),encoding='utf-8')
((_ROOT / 'diseno/fuentes/catalogos/ENEMIGOS.json')).write_text(json.dumps([{'id':i,'archivo':'enemigo_'+e[0]+'.png','nombre':e[1],'salud':e[2],'ataque':e[3],'habilidad':e[4],'historia':e[5]} for i,e in enumerate(enemies,1)],ensure_ascii=False,indent=2),encoding='utf-8')
print(len(ops),'operaciones')

