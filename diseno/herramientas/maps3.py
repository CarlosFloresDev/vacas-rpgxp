"""Mapas compactos del Acto III. Conserva tileset 51 y sus pasajes."""
import json,random
from gfx_acto2 import ID

MAPAS=[(12,'Lucy: el piso de arriba',25,20),(13,'Carnicería Molina',20,15),(14,'Carnicería cerrada: depósito',20,15),(15,'Hospital cerrado: curas',25,20),(16,'Lucy: laboratorio improvisado',25,20)]

def crear():
    return [['create_map',dict(name=n,width=w,height=h,tilesetId=51,purpose='interior',parentId=3 if i==12 else 4)] for i,n,w,h in MAPAS]

def tiles(mid,w,h):
    r=random.Random(mid)
    floor='linoleo' if mid==12 else 'suelo_frio' if mid==14 else 'azulejo'
    z=[[[0]*w for _ in range(h)] for _ in range(3)]
    def put(x,y,t,layer=1):z[layer][y][x]=ID[t]
    for y in range(h):
        for x in range(w):
            if y in [0,h-1] or x in [0,w-1]:t='pared_madera_alta' if mid==12 else 'pared_hormigon_alta'
            elif y==1:t='pared_madera_alta' if mid==12 else 'pared_fria_alta'
            elif y==2:t='pared_madera_baja' if mid==12 else 'pared_fria_baja'
            else:t='azulejo_sucio' if floor=='azulejo' and r.random()<.24 else floor
            z[0][y][x]=ID[t]
    # Salidas físicas: siempre suelo transitable; puertas internas por acción.
    exitx=10 if mid==13 else 3 if mid==14 else 12
    z[0][h-1][exitx]=ID[floor]
    for x in [4,w-5]:
        put(x,1,'ventana_oficina' if mid==12 else 'ventana_nave',0)
        put(x,4,'lampara',2)
    if mid==12:
        # Estar a izquierda, investigación al fondo, dormitorio a derecha.
        for y in range(3,17):
            if y not in [7,8,14,15]:put(14,y,'pared_madera_baja',0)
        for x in range(1,14):
            if x not in [8,9,10]:put(x,10,'pared_madera_baja',0)
        for x in range(15,23):put(x,10,'pared_madera_baja',0)
        z[0][10][18]=ID[floor];z[0][10][19]=ID[floor]
        for x,y,t in [(3,4,'archivador_alto'),(3,5,'archivador_bajo'),(6,6,'escritorio_izq'),(7,6,'escritorio_der'),(5,14,'silla'),(8,14,'silla'),(20,14,'banco'),(20,15,'banco'),(22,12,'cajas'),(16,4,'fregadero'),(16,5,'cubo_despojos'),(4,16,'cajas')]:put(x,y,t)
        put(18,11,'lampara',2)
    elif mid==13:
        for x in range(3,11):put(x,8,'mesa_acero')
        # Un paso lateral comunica los dos lados del mostrador.
        for x in [3,6,9,12]:put(x,3,'rail_gancho',2)
        for x,y,t in [(3,5,'cubo_despojos'),(9,5,'fregadero'),(14,10,'cajas'),(15,10,'cajas'),(16,11,'cajas'),(4,11,'banco')]:put(x,y,t)
    elif mid==14:
        # Dos islas largas, circuitos de 2+ casillas de ancho para persecución.
        for x in [7,12]:
            for y in range(5,10):put(x,y,'mesa_acero')
            put(x,4,'rail_gancho',2)
        for x,y,t in [(2,4,'cajas'),(3,4,'cajas'),(17,10,'cubo_despojos'),(16,11,'mancha'),(4,8,'huellas'),(15,5,'huellas')]:put(x,y,t)
    elif mid==15:
        # Sala de espera, archivo de curas y pequeña sala de pacientes.
        for y in range(3,16):
            if y not in [9,10]:put(13,y,'pared_hormigon_baja',0)
        for x in range(1,13):
            if x not in [10,11]:put(x,10,'pared_hormigon_baja',0)
        for x,y,t in [(3,4,'archivador_alto'),(3,5,'archivador_bajo'),(10,5,'escritorio_izq'),(11,5,'escritorio_der'),(7,12,'banco'),(8,12,'banco'),(9,12,'banco'),(17,6,'mesa_acero'),(18,6,'mesa_acero'),(21,13,'cajas'),(21,14,'cajas')]:put(x,y,t)
        for x in [14,21]:put(x,11,'lampara',2)
    elif mid==16:
        # Biombos separan los tres puestos sin cerrar su corredor inferior.
        for x in [8,14]:
            for y in range(4,8):put(x,y,'pared_fria_baja',0)
        for x in [4,10,16]:
            put(x,5,'mesa_acero');put(x+1,5,'mesa_acero')
            put(x+1,4,'lampara',2)
        for x,y,t in [(3,10,'fregadero'),(3,11,'cubo_despojos'),(20,4,'archivador_alto'),(20,5,'archivador_bajo'),(20,14,'silla'),(6,15,'cajas'),(7,15,'cajas'),(15,10,'mancha')]:put(x,y,t)
    # Grupos de desgaste, sin obstruir aproximaciones ni destinos.
    for x,y in [(2,h-4),(w-3,h-5),(w-4,h-5)]:
        if not z[1][y][x]:put(x,y,'mancha')
    return [['set_map_tiles',dict(mapId=mid,layer=l,x=0,y=0,grid=z[l])] for l in range(3)]

def pintura():return [op for mid,_,w,h in MAPAS for op in tiles(mid,w,h)]

if __name__=='__main__':
    import sys
    ops=crear() if 'crear' in sys.argv else pintura()
    json.dump(ops,open('b_mapas3.json','w',encoding='utf-8'),ensure_ascii=False)
    print(len(ops),'operaciones')
