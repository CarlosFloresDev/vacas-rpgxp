"""Reutiliza el constructor y utilería a escala del Acto V; CPU/PIL solamente."""
import inspect,json
import maps5 as m
from maps5 import P,D,O,F
from PIL import Image
# Reencuadres de muebles existentes: cama 32x64, fogón 48x48,
# televisión 28x44, mesillas y objetos menores que el personaje de 48 px.
house=Image.open(m.ROOT/'Graphics/Tilesets/revision_mapa02.png').convert('RGBA')
furniture=Image.open(m.ROOT/'Graphics/Characters/vacas_muebles.png').convert('RGBA')
def native_grid(ids):
    im=Image.new('RGBA',(len(ids[0])*32,len(ids)*32))
    for y,row in enumerate(ids):
        for x,tid in enumerate(row):
            if tid:
                k=tid-384;im.alpha_composite(house.crop((k%8*32,k//8*32,k%8*32+32,k//8*32+32)),(x*32,y*32))
    return im
native={'bed':native_grid([[447],[455]]),'cabinet':native_grid([[458,459],[466,467]]).resize((48,48),Image.Resampling.NEAREST),
        'stove':native_grid([[0,436,0],[443,444,445],[451,452,453]]).resize((48,48),Image.Resampling.NEAREST),
        'tv':furniture.crop((0,64,32,128))}
original_draw=m.draw
def draw(kind,r):return native[kind].copy() if kind in native else original_draw(kind,r)
m.draw=draw
m.M.clear()
def room(mid,floor,wall,partitions,props,lights,tint,dark=92):
    rows=['#'*20,wall*20,wall.lower()*20]+['#'+floor*18+'#' for _ in range(11)]+['#'*20]
    rows=[list(r) for r in rows]
    for x,y in partitions:rows[y][x]='#'
    # Ruta de acceso común y salida este.
    rows[14][3]=floor;rows[12][19]=floor
    m.mapa(mid,[''.join(r) for r in rows],[],props,lights,tint,dark)
# Nichos de mantenimiento separados por pilares; corredor central estrecho.
room(28,',','H',[(x,y) for x in (6,13) for y in range(3,12) if y not in (6,10)],
 [P('shelf',1,4),P('barrel',5,4),P('sacks',7,3),P('rack',14,4),P('crate',18,4),P('radiotable',2,10),P('bucket',8,8),P('crates2',12,9),P('shelf',17,9),P('bench',14,12),P('fusebox',10,3),D('note',3,4),D('bottles',7,4),D('dung',11,6),D('bloodtrail',16,6),O('hook',5,3)],
 [(3,9,1.1),(10,5,1.3),(17,11,1.1)],(30,55,58))
# Una sola manzana: fachada, acera, camión atravesado, refugio y puesto de manada.
room(29,'a','L',[(x,8) for x in range(2,18) if x not in (4,5,10,11,15)],
 [P('truck',6,6),P('dumpster',15,6),P('farol',3,4),P('farol',18,11),P('barrel',2,8),P('crates2',12,8),P('bench',1,11),P('radiotable',16,11),P('sacks',6,11),P('cone',11,6),D('note',4,5),D('note',14,11),D('drag',8,12),D('blood',17,7),D('dung',12,4),P('board',12,3)],
 [(4,4,1.4),(16,10,1.5),(8,12,.8)],(65,44,30),78)
# Piso reconocible por sofá, tele/radio, medicinas y cocina. Tres cuartos pequeños.
room(30,'o','M',[(10,y) for y in range(3,13) if y not in (6,11)]+[(x,8) for x in range(1,10) if x not in (4,5)],
 [P('sofa',2,5),P('radiotable',7,4),P('rug',3,6,block=False),P('shelf',1,7),P('heater',8,7),P('coatrack',1,10),P('plant',8,11),P('deskset',12,4),P('bench',12,5),P('shelf',17,4),P('bucket',18,7),P('stool',15,6),P('sofa',12,10),P('calendar',18,3),D('bottles',14,4),D('note',6,5),D('note',13,10),P('sacks',18,12)],
 [(5,5,1.2),(14,5,1.1),(5,11,1.0),(14,11,.9)],(80,55,32),65)
# Galería de tres bombas; las válvulas se leen izquierda-centro-derecha.
room(31,',','H',[(x,y) for x in (7,13) for y in range(7,12) if y!=9],
 [P('fusebox',4,4),P('fusebox',10,4),P('fusebox',16,4),P('barrel',1,6),P('rack',8,7),P('shelf',14,7),P('sacks',18,8),P('crate',6,11),P('bucket',12,12),P('bench',1,11),O('hook',6,3),O('hook',12,3),O('hook',18,3),D('drag',8,10),D('bloodtrail',17,10),D('note',2,6)],
 [(4,5,.9),(10,5,.9),(16,5,.9),(3,12,1.1)],(35,55,65),95)
# Altar en un comedor subterráneo: el trono está hecho del mismo sofá doméstico.
room(32,':','F',[(x,y) for x in (6,13) for y in (3,4,9,10)],
 [P('sofa',9,5),P('rug',9,7,block=False),P('skull',8,4),P('skull',12,4),P('radiotable',3,10),P('shelf',1,4),P('shelf',17,4),P('sacks',2,7),P('crate',17,7),P('bench',7,11),P('bench',13,11),P('barrel',18,12),D('note',4,5),D('bottles',14,6),D('blood',9,6),O('hook',4,3),O('hook',15,3)],
 [(10,5,1.6),(3,10,1.0),(16,10,1.0)],(65,28,23),96)
# Más almacenaje, estaciones de trabajo y restos a lo largo de los recorridos.
extras={
28:[P('barrel',2,6),P('barrel',3,6),P('crate',5,8),P('bench',7,8),P('sacks',11,3),P('rack',14,8),P('bucket',17,5),P('crates2',15,11),D('note',9,7),D('bottles',3,7),D('drag',9,11),P('shelf',7,12)],
29:[P('crates2',5,3),P('shelf',1,6),P('sacks',8,3),P('pallet',9,9),P('crate',10,9),P('bucket',18,4),P('barrel',13,12),P('bench',15,3),D('note',10,11),D('drag',3,9),D('bottles',15,9),P('cone',4,7)],
30:[P('tv',7,3),P('cabinet',1,4),P('stove',16,4),P('bed',12,12),P('cabinet',16,12),P('bench',2,12),P('stool',5,7),D('bottles',7,5),D('note',2,11),P('crate',8,9),P('plant',11,7),D('rug',13,11),P('stool',17,10),D('note',8,12)],
31:[P('barrel',2,4),P('barrel',6,4),P('barrel',12,4),P('barrel',18,4),P('sacks',2,8),P('crate',5,8),P('bucket',9,10),P('rack',16,10),P('pallet',9,12),D('note',11,7),D('drag',3,10),D('bottles',14,12)],
32:[P('shelf',2,4),P('shelf',16,4),P('sacks',4,7),P('sacks',15,7),P('barrel',1,10),P('barrel',18,10),P('crate',7,4),P('bucket',12,8),P('bench',1,12),P('bench',15,12),P('rack',7,9),P('rack',14,9),D('note',11,11),D('drag',9,10),D('bottles',8,6)]}
for mid,props in extras.items():
    m.M[mid]['props']+=props
    m.M[mid]['dark']+=35
    m.M[mid]['lights']=[(x,y,size*.8) for x,y,size in m.M[mid]['lights']]
# El cuerpo del generador conserva pasajes/prioridades/huellas y máscaras.
source=inspect.getsource(m.build).replace('id=69','id=70').replace('acto5','acto6').replace('maps5_info','maps6_info').replace('b_tiles5','b_tiles6').replace('acto6_matanza','acto6_reydios')
exec(source,m.__dict__)
if __name__=='__main__':m.build()
